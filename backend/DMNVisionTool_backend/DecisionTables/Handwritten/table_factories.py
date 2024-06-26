from typing import Tuple
from typing import Type

from DMNVisionTool_backend.DecisionTables.table_elements import (
    TableElement,
    TableHeader,
    TableHitPolicy,
    TableInput,
    TableOutput,
    TableRule,
    InputEntry,
    OutputEntry,
    Table,
)

from DMNVisionTool_backend.DecisionTables.table_predictions import TablePrediction
from DMNVisionTool_backend.commons.Sketch_utils import generate_id

def calculate_width_height(
    x_start: float, y_start: float, x_end: float, y_end: float
) -> Tuple[float, float]:
    """Returns the width and the height of a box given the initial and the ending x and y coordinates."""
    return abs(x_end - x_start), abs(y_end - y_start)

class TableElementFactory:
    """Parent class for the factories used to create the Table Elements. """
    generated_ids = []

    def create_element(self, prediction: TablePrediction):
        """Returns the corresponding element associated to the factory"""

class GenericTableElementFactory(TableElementFactory):
    """A generic factory for Table Elements which creates a chosen table element by extracting box information,
    text and id.

    Parameters
    ----------
    element_class : type of table Element
        The actual class of table Element to create.
    """
    generated_ids = []

    def __init__(self, element_class: Type[TableElement]):
        self.element_class = element_class

    def create_element(self, prediction: TablePrediction) -> TableElement:
        """Returns the chosen DMN Element created by the factory"""
        while(True):
            id = generate_id(self.element_class.__name__)

            if id not in self.generated_ids:
                break

        self.generated_ids.append(id)

        return self.element_class(id, prediction)

# TO DO: Change categories in the model to have 0-1-2-3-4
CATEGORIES = {
    0: "OutputEntry",
    1: "InputEntry",
    2: "TableOutput",
    3: "TableInput",
    4: "TableHeader",
    5: "TableRule",
    6: "TableHitPolicy",
    7: "Table"
}

FACTORIES = {
    "TableHeader": GenericTableElementFactory(TableHeader),
    "TableHitPolicy": GenericTableElementFactory(TableHitPolicy),
    "TableInput": GenericTableElementFactory(TableInput), 
    "TableOutput": GenericTableElementFactory(TableOutput),
    "TableRule": GenericTableElementFactory(TableRule),
    "InputEntry": GenericTableElementFactory(InputEntry),
    "OutputEntry": GenericTableElementFactory(OutputEntry),
    "Table": GenericTableElementFactory(Table)
    }

def get_table_factory(category_id: int) -> TableElementFactory:
    """Return the factory useful to create the element, None if the category is not available."""
    category = CATEGORIES.get(category_id)
    return FACTORIES.get(category)
