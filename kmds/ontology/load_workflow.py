from ontology.kmds_ontology import *
from owlready2.namespace import Ontology


def get_workflow(onto: Ontology) ->Workflow:
    """Given an ontology, return the workflow instance

    Args:
        onto (Ontology): The ontology from which the workflow instance must be loaded

    Returns:
        Workflow: The workflow in this ontology
    """

    ind_instances = onto.individuals()
    the_workflow_instance = None

    for inst in ind_instances:
        is_workflow_instance = isinstance(inst, KnowledgeApplicationWorkflow) | isinstance(inst, KnowledgeExtractionExperimentationWorkflow)
        if is_workflow_instance:
            the_workflow_instance = inst
            break

    
    return the_workflow_instance