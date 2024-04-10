from dataclasses import dataclass, field
from typing import List

from jinja2 import Environment, BaseLoader

from DMNVisionTool_backend.tables.Sketches.table_predictions import TablePrediction  #,Text
from DMNVisionTool_backend.tables.Sketches.table_elements import TableHeader, TableHitPolicy


class Decision_Logic:
    """Parent class for the Decision Logic that can be put within a DMN Model."""
    def __init__(self, id: str, prediction: TablePrediction):
        self.id = id
        self.prediction = prediction
        self.name = []
        self.jinja_environment = Environment(loader=BaseLoader())

    def render_element(self):
        """Returns the xml string associated to this kind of element"""

    def get_name(self):
        """Returns the text of the element as a string"""
        return " ".join([text.text for text in self.name])

    def render_shape(self):
        """Returns the xml string containing the shape information of this kind of element"""
        template = """<dmndi:DMNShape dmnElementRef="{{ element.id }}" >
        <dc:Bounds height="{{ element.prediction.height }}" width="{{ element.prediction.width }}" x="{{ element.prediction.top_left_x }}" y="{{ element.prediction.top_left_y }}" />
      </dmndi:DMNShape>
        """
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(element=self)

        return data

class Table(Decision_Logic):
    """Class for a table

    Parameters
    ----------
    id : str
        Unique identifier of the DMN Table.
    prediction : TablePrediction
        The prediction given by the table detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.header = TableHeader
        self.hitPolicy = TableHitPolicy
        self.inputs = []
        self.outputs = []
        self.rules = []
        self.label = []
        self.jinja_environment = Environment(loader=BaseLoader())
