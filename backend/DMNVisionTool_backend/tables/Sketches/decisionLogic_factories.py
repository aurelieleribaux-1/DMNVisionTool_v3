from typing import Tuple, List, Union, Set, Type
from DMNVisionTool_backend.tables.Sketches.dmn_decisionLogic import Table, Decision_Logic
from DMNVisionTool_backend.tables.Sketches.table_predictions import TablePrediction
from DMNVisionTool_backend.commons.Sketch_utils import generate_id

class Factory:
    """Parent class for the factories used to create the DMN Tables. """
    generated_ids = []

    def create_table(self, prediction: TablePrediction):
        """Returns the corresponding table associated to the factory"""

class GenericFactory(Factory):
    """A generic factory for table objects which creates a chosen table by extracting box information,
    id.

    """

    def __init__(self, dl_class: Type[Decision_Logic]):
        self.dl_class = dl_class

    def create_table(self, prediction: TablePrediction) -> Decision_Logic:
        while (True):
            id = generate_id(self.dl_class.__name__)

            if id not in self.generated_ids:
                break

        self.generated_ids.append(id)

        # Instantiate an object of Decision_Logic
        return self.dl_class(id, prediction)

# TO DO: Change keypoint categories numbers according to model
TABLE_CATEGORIES = {
    7: "Table",
}

TABLE_FACTORIES = {
    "Table": GenericFactory(Table),
}

def get_table_factory(category_id: int) -> Factory:
    """Return the table factory useful to create the table, None if the category is not available."""
    category = TABLE_CATEGORIES.get(category_id)
    return TABLE_FACTORIES.get(category)