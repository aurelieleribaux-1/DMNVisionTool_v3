from typing import Tuple, List, Union, Set, Type

from DMNVisionTool_backend.graphs.Sketches.graph_elements import (
    Element,
    InputData,
    Decision,
    BusinessKnowledge,
    KnowledgeSource,
    TextAnnotation,
    Diagram,
)

from DMNVisionTool_backend.graphs.Sketches.graph_predictions import ObjectPrediction
from DMNVisionTool_backend.commons.Sketch_utils import generate_id

def calculate_width_height(
    x_start: float, y_start: float, x_end: float, y_end: float
) -> Tuple[float, float]:
    """Returns the width and the height of a box given the initial and the ending x and y coordinates."""
    return abs(x_end - x_start), abs(y_end - y_start)

class DiagramFactorySketches:
    """Factory class used to create a Diagram given a set of elements
    """
    @staticmethod
    def create_element(elements: List[Element]) -> Diagram:
        """Factory method that creates a Diagram from a set of elements"""
                
        diagram_id = generate_id("DMNDiagram")
        definition_id = generate_id("Definitions")
        
        return (
            Diagram(
                diagram_id,
                definition_id,
                elements,
            )
        )

class ElementFactory:
    """Parent class for the factories used to create the DMN Elements. """
    generated_ids = []

    def create_element(self, prediction: ObjectPrediction):
        """Returns the corresponding element associated to the factory"""

class GenericElementFactory(ElementFactory):
    """A generic factory for Element objects which creates a chosen Element by extracting box information,
    text and id.

    Parameters
    ----------
    element_class : type of Element
        The actual class of Element to create.
    """
    generated_ids = []

    def __init__(self, element_class: Type[Element]):
        self.element_class = element_class

    def create_element(self, prediction: ObjectPrediction) -> Element:
        """Returns the chosen DMN Element created by the factory"""
        while(True):
            id = generate_id(self.element_class.__name__)

            if id not in self.generated_ids:
                break

        self.generated_ids.append(id)

        return self.element_class(id, prediction)

# TO DO: Change categories in the model to have 0-1-2-3-4
CATEGORIES = {
    1: "KnowledgeSource",
    2: "BusinessKnowledge",
    3: "Decision",
    4: "InputData",
    5: "TextAnnotation"
    }

#FACTORIES = {
#    "Decision": GenericElementFactory(Decision, "DecisionDefinition"),
#    "InputData": GenericElementFactory(InputData, "InputDataDefinition"),
#    "BusinessKnowledge": GenericElementFactory(BusinessKnowledge, "BusinessKnowledgeDefinition"),
#    "KnowledgeSource": GenericElementFactory(KnowledgeSource, "KnowledgeSourceDefinition"), 
#    "TextAnnotation": GenericElementFactory(TextAnnotation, "TextAnnotationDefinition")
#    }

FACTORIES = {
    "KnowledgeSource": GenericElementFactory(KnowledgeSource), 
    "BusinessKnowledge": GenericElementFactory(BusinessKnowledge),
    "Decision": GenericElementFactory(Decision),
    "InputData": GenericElementFactory(InputData),
    "TextAnnotation": GenericElementFactory(TextAnnotation)
    }

def get_factory(category_id: int) -> ElementFactory:
    """Return the factory useful to create the element, None if the category is not available."""
    category = CATEGORIES.get(category_id)
    return FACTORIES.get(category)