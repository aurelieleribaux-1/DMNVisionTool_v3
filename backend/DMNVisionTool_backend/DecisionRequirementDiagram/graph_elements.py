from dataclasses import dataclass, field
from typing import List

from jinja2 import Environment, BaseLoader

from DMNVisionTool_backend.DecisionRequirementDiagram.graph_predictions import ObjectPrediction, Text

class Element:
    """Parent class for all the elements that can be put within a DMN Model.
    (Decision, Input Data, Business Knowledge, Knowledge Source & Text Annotation)

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
        prediction: ObjectPrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.requirements = []
        self.name = []
        self.jinja_environment = Environment(loader=BaseLoader())

    def render_element(self):
        """Returns the xml string associated to this kind of element"""

    def get_name(self):
        """Returns the text of the element as a string"""
        return " ".join([text.text for text in self.name])

    def render_shape(self):
       """Returns the xml string containing the shape information of this kind of element"""
       # Adjust the height, width, top left x, and top left y to make the element smaller
       scale_factor = 0.5  # Adjust this scale factor as needed
       height = self.prediction.height * scale_factor
       width = self.prediction.width * scale_factor
       top_left_x = self.prediction.top_left_x * scale_factor
       top_left_y = self.prediction.top_left_y * scale_factor

       template = """<dmndi:DMNShape dmnElementRef="{{ element.id }}" >
       <dc:Bounds height="{{ height }}" width="{{ width }}" x="{{ top_left_x }}" y="{{ top_left_y }}" />
       </dmndi:DMNShape>
       """
       rtemplate = self.jinja_environment.from_string(template)
       data = rtemplate.render(element=self, height=height, width=width, top_left_x=top_left_x, top_left_y=top_left_y)

       return data

    
class Decision(Element):
    """Represents a DMN Decision element.

    Parameters
    ----------
    id : str
        Unique identifier of the DMN Element.
    prediction : ObjectPrediction
        The prediction given by the object detection predictor.
    table : Table
        The decision table associated with this decision element
    """
    def __init__(
        self,
        id: str,
        prediction: ObjectPrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.requirements = []
        self.name = []
        self.jinja_environment = Environment(loader=BaseLoader())
        self.table = []

    def render_element(self):
        template = """<decision id="{{ decision.id }}" name="{{ decision.get_name() }}" />"""
        
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(decision=self)

        return data 

class InputData(Element):
    """Represents a DMN Input Data element.

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
        prediction: ObjectPrediction,
    ):
        super(InputData, self).__init__(id, prediction)

    def render_element(self):
        template = """<inputData id="{{ input_data.id }}" name="{{ input_data.get_name() }}" />"""

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(input_data=self)

        return data
    
class BusinessKnowledge(Element):
    """Represents a DMN Business Knowledge element.

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
        prediction: ObjectPrediction,
    ):
        super(BusinessKnowledge, self).__init__(id, prediction)

    def render_element(self):
        template = """<businessKnowledgeModel id="{{ business_knowledge.id }}" name="{{ business_knowledge.get_name() }}" />"""

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(business_knowledge=self)

        return data
    
class KnowledgeSource(Element):
    """Represents a DMN Knowledge Source element.

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
        prediction: ObjectPrediction,
    ):
        super(KnowledgeSource, self).__init__(id, prediction)

    def render_element(self):
        template = """<knowledgeSource id="{{ knowledge_source.id }}" name="{{ knowledge_source.get_name() }}" />"""

        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(knowledge_source=self)

        return data



@dataclass()
class Diagram:
    """Represents a DMN Diagram which contains all the information used to write the xml file.

    Parameters
    ----------
    id : str
        Unique identifier of the DMN Element.
    definition_id : str
        Unique identifier of the BPMN Definition tag.
    elements_list : list of elements
        The list of elements to include in the xml file.
    """
    id: str
    definition_id: str
    elements_list: List[Element]