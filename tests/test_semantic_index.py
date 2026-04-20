"""Tests for the SemanticIndex feature."""

import pytest

from kmds.search import SemanticIndex
from kmds.utils.path_utils import get_kb_file_path


@pytest.fixture()
def app_kb_path():
    return get_kb_file_path("test_kb_app_workflow.xml")


@pytest.fixture()
def exp_kb_path():
    return get_kb_file_path("test_kb_exp_workflow.xml")


class TestSemanticIndexBuild:
    def test_build_from_kb_path(self, app_kb_path):
        idx = SemanticIndex()
        idx.build(app_kb_path)
        assert idx.count() > 0

    def test_build_is_idempotent(self, app_kb_path):
        idx = SemanticIndex()
        idx.build(app_kb_path)
        count_first = idx.count()
        # Building again should not duplicate documents (upsert semantics)
        idx.build(app_kb_path)
        assert idx.count() == count_first

    def test_build_raises_on_bad_path(self):
        idx = SemanticIndex()
        with pytest.raises(ValueError, match="Could not load"):
            idx.build("/nonexistent/path/kb.xml")

    def test_build_experimental_kb(self, exp_kb_path):
        idx = SemanticIndex()
        idx.build(exp_kb_path)
        assert idx.count() > 0


class TestSemanticIndexSearch:
    def test_search_returns_results(self, app_kb_path):
        idx = SemanticIndex()
        idx.build(app_kb_path)
        results = idx.search("data quality issues", n_results=3)
        assert isinstance(results, list)
        assert len(results) > 0

    def test_search_result_structure(self, app_kb_path):
        idx = SemanticIndex()
        idx.build(app_kb_path)
        results = idx.search("missing values", n_results=1)
        assert len(results) == 1
        r = results[0]
        assert "finding" in r
        assert "obs_type" in r
        assert "workflow_name" in r
        assert "distance" in r
        assert isinstance(r["distance"], float)

    def test_search_respects_n_results(self, app_kb_path):
        idx = SemanticIndex()
        idx.build(app_kb_path)
        results = idx.search("model performance", n_results=2)
        assert len(results) <= 2

    def test_search_empty_index_returns_empty_list(self):
        idx = SemanticIndex()
        results = idx.search("anything")
        assert results == []

    def test_search_ranks_by_relevance(self, app_kb_path):
        """The first result should be more relevant (lower distance) than the last."""
        idx = SemanticIndex()
        idx.build(app_kb_path)
        results = idx.search("feature engineering transformation", n_results=5)
        if len(results) >= 2:
            assert results[0]["distance"] <= results[-1]["distance"]


class TestSemanticIndexClear:
    def test_clear_empties_index(self, app_kb_path):
        idx = SemanticIndex()
        idx.build(app_kb_path)
        assert idx.count() > 0
        idx.clear()
        assert idx.count() == 0
