from DMNVisionTool_backend.graphs.graph_requirements import Requirement, Association, InformationRequirement, KnowledgeRequirement, AuthorityRequirement
from DMNVisionTool_backend.graphs.graph_predictions import KeyPointPrediction
from DMNVisionTool_backend.commons.utils import generate_id
from typing import Type

class RequirementFactory:
    """Parent class for the factories used to create the DMN Requirements. """
    generated_ids = []

    def create_requirement(self, prediction: KeyPointPrediction):
        """Returns the corresponding requirement associated to the factory"""

class GenericRequirementFactory(RequirementFactory):
    """A generic factory for Requirement objects which creates a chosen Requirement by extracting box information,
    text and id.

    Parameters
    ----------
    requirement_class : type of Requirement
        The actual subclass of Requirement to create.
    """
    def __init__(self, requirement_class: Type[Requirement]):
        self.requirement_class = requirement_class

    def create_requirement(self, prediction: KeyPointPrediction) -> Requirement:
        while (True):
            id = generate_id(self.requirement_class.__name__)

            if id not in self.generated_ids:
                break

        self.generated_ids.append(id)

        return self.requirement_class(id, prediction)

# TO DO: Change keypoint categories numbers according to model
KEYPOINT_CATEGORIES = {
    1: "InformationRequirement",
    2: "AuthorityRequirement",
    3: "KnowledgeRequirement",
    4: "Association"
}

KEYPOINT_FACTORIES = {
    "InformationRequirement": GenericRequirementFactory(InformationRequirement),
    "KnowledgeRequirement": GenericRequirementFactory(KnowledgeRequirement),
    "AuthorityRequirement": GenericRequirementFactory(AuthorityRequirement),
    "Association": GenericRequirementFactory(Association)
}



def get_keypoint_factory(category_id: int) -> RequirementFactory:
    """Return the keypoint factory useful to create the requirement, None if the category is not available."""
    category = KEYPOINT_CATEGORIES.get(category_id)
    return KEYPOINT_FACTORIES.get(category)