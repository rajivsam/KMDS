import pytest

from kmds.ontology.kmds_ontology import get_ontology, set_ontology
from kmds.utils.path_utils import get_ontology_path


@pytest.fixture(autouse=True)
def reset_ontology_state():
    """Ensure each test starts from a clean ontology object.

    KMDS keeps ontology state in a module-level singleton, which can leak across
    tests unless explicitly reset.
    """
    fresh = get_ontology(get_ontology_path()).load()
    set_ontology(fresh)
    yield
    fresh = get_ontology(get_ontology_path()).load()
    set_ontology(fresh)
