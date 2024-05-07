from dataclasses import dataclass, field
from typing import List

from jinja2 import Environment, BaseLoader

from DMNVisionTool_backend.DecisionTables.table_predictions import TablePrediction, Text

class Table:
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
        self.header = None
        self.hitPolicy = None
        self.inputs = []
        self.outputs = []
        self.rules = []
        self.label = []
        self.jinja_environment = Environment(loader=BaseLoader())

class TableElement:
    """Parent class for all the elements that can be put within a DMN Table.
    (Header, output entry, input entry, hit policy, output, input, rule or table)

    Parameters
    ----------
    id : str
        Unique identifier of the DMN Element.
    prediction : ObjectPrediction
        The prediction given by the object detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.requirements = []
        self.label = []
        self.jinja_environment = Environment(loader=BaseLoader())
        
    
class TableHeader(TableElement):
    """Class for a table

    Parameters
    ----------
    id : str
        Unique identifier of the DMN Table.
    prediction : TableElementPrediction
        The prediction given by the table detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):        
        self.id = id
        self.prediction = prediction
        self.label = []
        self.jinja_environment = Environment(loader=BaseLoader())

    def get_label(self):
        """Returns the text of the table header as a string"""
        return " ".join([text.text for text in self.label])

class TableHitPolicy(TableElement):
    """Class for a table

    Parameters
    ----------
    id : str
        Unique identifier of the DMN Table.
    prediction : TableElementPrediction
        The prediction given by the table detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):        
        self.id = id
        self.label = []
        self.prediction = prediction
        self.jinja_environment = Environment(loader=BaseLoader())

    def get_label(self):
        """Returns the text of the table hit policy as a string"""
        return " ".join([text.text for text in self.label])

class TableInput(TableElement): 
    """Class for the input of a Table. 
    An input is the column header of all the input entries
    
    Parameters
    ----------
    id : str
        Unique identifier of the input
    prediction : CellPrediction
        The prediction given by the cells detection predictor.
         
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.label = []
        self.expression = []
        self.typeRef = []
        self.jinja_environment = Environment(loader=BaseLoader())
        
    def get_label(self):
        """Returns the text of the input label as a string """
        if not self.label:
            return "NaN"
        else:
            return " ".join([text.text for text in self.label])
    
    def render_input(self):      
        self.typeRef.append("string")
        template = """
        <input id="{{ input.id }}" label="{{ input.get_label() }}">
            <inputExpression id="{{ input.id }}_{{ input.id }}" typeRef="{{ input.typeRef }}">
            </inputExpression>
        </input>
        """
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(input=self)

        return data


        
class TableOutput(TableElement): 
    """Class for the output of a Table. 
    An output is the column header of all the output entries
    
    Parameters
    ----------
    id : str
        Unique identifier of the input
    prediction : CellPrediction
        The prediction given by the cells detection predictor.
         
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.label = []
        self.typeRef = []
        self.jinja_environment = Environment(loader=BaseLoader())
        
    def get_label(self):
        """Returns the text of the output label as a string """
        if not self.label:
            return "NaN"
        else:
            return " ".join([text.text for text in self.label])
    
    def render_output(self):      
        self.typeRef.append("string")
        template = """<output id="{{ output.id }}" label="{{ output.get_label() }}" typeRef="{{ output.typeRef}}"/> """
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(output=self)

        return data


class TableRule(TableElement): 
    """Class for the rule of a Table. 
    A rule is defined by multiple input entries and an output entry
    
    Parameters
    ----------
    id : str
        Unique identifier of the input
    prediction : CellPrediction
        The prediction given by the cells detection predictor.
         
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.label = []
        self.inputEntries = []
        self.outputEntries = []
        self.jinja_environment = Environment(loader=BaseLoader())

class InputEntry(TableElement): 
    """Class for the input entry of a Table. 
    
    Parameters
    ----------
    id : str
        Unique identifier of the input entry
    prediction : CellPrediction
        The prediction given by the cells detection predictor.
         
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.label = []
        self.jinja_environment = Environment(loader=BaseLoader())
        
    def get_label(self):
        """Returns the text of the input label as a string """
        if not self.label:
            return "NaN"
        else:
            return " ".join([text.text for text in self.label])
    
    def render_inputEntry(self):        
        template = """<inputEntry id="{{ input_entry.id }}"> 
                        <text>{{ input_entry.get_label() }}</text>
                    </inputEntry>"""
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(input_entry=self)

        return data

class OutputEntry(TableElement): 
    """Class for the output entry of a Table. 
    
    Parameters
    ----------
    id : str
        Unique identifier of the input entry
    prediction : CellPrediction
        The prediction given by the cells detection predictor.
         
    """
    def __init__(
        self,
        id: str,
        prediction: TablePrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.label = []
        self.jinja_environment = Environment(loader=BaseLoader())
        
    def get_label(self):
        """Returns the text of the input label as a string """
        if not self.label:
            return "NaN"
        else:
            return " ".join([text.text for text in self.label])
    
    def render_outputEntry(self):        
        template = """<outputEntry id="{{ output_entry.id }}"> 
                        <text>{{ output_entry.get_label() }}</text>
                    </outputEntry>"""
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(output_entry=self)

        return data
