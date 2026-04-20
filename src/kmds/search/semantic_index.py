"""Semantic index for KMDS knowledge bases.

Embeds observation findings from an RDF knowledge graph into a vector
database so that natural language queries can retrieve relevant findings.

Technology choices
------------------
- **sentence-transformers** (``all-MiniLM-L6-v2`` by default): fast,
  open-source embedding model with a large community footprint.
- **ChromaDB**: open-source, Python-native vector database that supports
  both in-memory (ephemeral) and on-disk (persistent) operation.

Example usage
-------------
::

    from kmds.search import SemanticIndex

    # Build and persist an index from a KB file
    idx = SemanticIndex(persist_dir="./my_index")
    idx.build("path/to/kb.xml")

    # Query the index
    results = idx.search("missing values in intake data", n_results=5)
    for r in results:
        print(r["obs_type"], r["finding"])

    # Load a previously persisted index and search without rebuilding
    idx2 = SemanticIndex(persist_dir="./my_index")
    results = idx2.search("imputation strategy")
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from kmds.utils.load_utils import get_workflow, load_kb, load_observations

logger = logging.getLogger(__name__)

_COLLECTION_NAME = "kmds_observations"


class SemanticIndex:
    """Semantic vector index over a KMDS knowledge base.

    Parameters
    ----------
    persist_dir:
        Directory on disk where ChromaDB will persist the index.  If
        ``None`` the index lives in memory only and is lost when the
        object is garbage collected.
    model_name:
        HuggingFace sentence-transformers model used for embedding.
        Defaults to ``"all-MiniLM-L6-v2"``, a fast, lightweight model
        with good semantic retrieval quality.
    """

    DEFAULT_MODEL: str = "all-MiniLM-L6-v2"

    def __init__(
        self,
        persist_dir: str | None = None,
        model_name: str = DEFAULT_MODEL,
    ) -> None:
        self._model_name = model_name
        self._ef = SentenceTransformerEmbeddingFunction(model_name=model_name)

        if persist_dir is not None:
            self._client = chromadb.PersistentClient(path=persist_dir)
            # Persistent indexes reuse a fixed collection name so the index
            # survives across process restarts.
            collection_name = _COLLECTION_NAME
        else:
            self._client = chromadb.EphemeralClient()
            # Ephemeral clients share an in-process store, so use a unique
            # collection name to keep instances isolated from each other.
            collection_name = f"{_COLLECTION_NAME}_{uuid.uuid4().hex}"

        self._collection_name = collection_name
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._ef,
            metadata={"hnsw:space": "cosine"},
        )

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def build(self, kb_path: str) -> None:
        """Load a KMDS knowledge-base file and index all observations.

        Parameters
        ----------
        kb_path:
            Path (or URL) to an RDF/OWL knowledge-base file produced by
            KMDS (``*.xml``).
        """
        onto = load_kb(kb_path)
        if onto is None:
            raise ValueError(f"Could not load knowledge base from '{kb_path}'")
        self.build_from_onto(onto)

    def build_from_onto(self, onto: Any) -> None:
        """Index all observations from an already-loaded ontology.

        Parameters
        ----------
        onto:
            An owlready2 ``Ontology`` object previously loaded with
            :func:`kmds.utils.load_utils.load_kb`.
        """
        workflow = get_workflow(onto)
        if workflow is None:
            raise ValueError("No workflow instance found in the knowledge base")

        workflow_name: str = str(getattr(workflow, "name", "workflow"))
        workflow_description: str = getattr(workflow, "description", "") or ""

        obs_df = load_observations(onto)

        documents: list[str] = []
        metadatas: list[dict] = []
        ids: list[str] = []

        # Index the workflow-level description as a searchable document.
        if workflow_description.strip():
            documents.append(workflow_description)
            metadatas.append(
                {
                    "obs_type": "workflow_description",
                    "workflow_name": workflow_name,
                    "finding_seq": -1,
                }
            )
            ids.append("workflow_description_0")

        # Index every individual observation finding.
        for idx, row in obs_df.iterrows():
            finding = row.get("finding")
            if not finding:
                continue

            meta: dict[str, Any] = {
                "obs_type": str(row.get("obs_type") or ""),
                "finding_seq": int(row.get("finding_seq") or 0),
                "workflow_name": workflow_name,
            }
            intent = row.get("intent")
            if intent is not None:
                meta["intent"] = str(intent)

            documents.append(str(finding))
            metadatas.append(meta)
            ids.append(f"obs_{idx}")

        if not documents:
            logger.warning("No text content found in the knowledge base; index is empty.")
            return

        # ChromaDB deduplicates by id; upsert so re-indexing is idempotent.
        self._collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
        logger.info("Indexed %d document(s) from workflow '%s'.", len(documents), workflow_name)

    # ------------------------------------------------------------------
    # Querying the index
    # ------------------------------------------------------------------

    def search(self, query: str, n_results: int = 5) -> list[dict]:
        """Retrieve the most semantically similar observations for *query*.

        Parameters
        ----------
        query:
            Natural language search string.
        n_results:
            Maximum number of results to return.

        Returns
        -------
        list[dict]
            Each dict contains:

            ``finding``
                The original observation text.
            ``obs_type``
                Observation category (e.g. ``"Data Quality Observation"``).
            ``workflow_name``
                Name of the workflow the observation belongs to.
            ``finding_seq``
                Original sequence number of the finding (``-1`` for the
                workflow description entry).
            ``distance``
                Cosine distance from the query vector (lower = more similar).
            ``intent`` *(optional)*
                Intent tag when present on the observation.
        """
        count = self._collection.count()
        if count == 0:
            logger.warning("Index is empty. Call build() or build_from_onto() first.")
            return []

        effective_n = min(n_results, count)
        raw = self._collection.query(
            query_texts=[query],
            n_results=effective_n,
        )

        results: list[dict] = []
        if raw and raw.get("documents"):
            for doc, meta, dist in zip(
                raw["documents"][0],
                raw["metadatas"][0],
                raw["distances"][0],
            ):
                entry = {"finding": doc, "distance": dist, **meta}
                results.append(entry)

        return results

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def count(self) -> int:
        """Return the number of documents currently in the index."""
        return self._collection.count()

    def clear(self) -> None:
        """Remove all documents from the index."""
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            embedding_function=self._ef,
            metadata={"hnsw:space": "cosine"},
        )
