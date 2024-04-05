from jinja2 import Environment, BaseLoader

from DMNVisionTool_backend.graphs.graph_predictions import KeyPointPrediction

class Requirement:
    """Parent class for all the requirements that can be put within a DMN Diagram.
    (Every flow/arrow in a DRD represents a requirement)
    (Exception: Association btw TextAnnotation & Element)

    Parameters
    ----------
    id : str
        Unique identifier of the Requirement.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.jinja_environment = Environment(loader=BaseLoader())
        self.hRef = None 

    def render_requirement(self):
        """Returns the xml string associated to this kind of requirement"""

    def render_shape(self):
        """Returns the xml string containing the shape information of this kind of requirement"""
        template = """<dmndi:DMNEdge dmnElementRef="{{ requirement.id }}" >
        <di:waypoint x="{{ requirement.prediction.tail[0] }}" y="{{ requirement.prediction.tail[1] }}" />
        <di:waypoint x="{{ requirement.prediction.head[0] }}" y="{{ requirement.prediction.head[1] }}" />
      </dmndi:DMNEdge>
        """
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(requirement=self)

        return data
    
class InformationRequirement(Requirement):
    """Represents a DMN Information Requirement

    Parameters
    ----------
    id : str
        Unique identifier of the Requirement.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        super(InformationRequirement, self).__init__(id, prediction)

    def render_requirement(self):
        """Returns the xml string associated to a InformationRequirement"""
        
        if self.hRef is not None and "Decision" in self.hRef:
            template = """<informationRequirement id="{{ requirement.id }}"> <requiredDecision href="#{{ requirement.hRef }}" /> </informationRequirement>"""

        elif self.hRef is not None and "Input" in self.hRef: 
            template = """<informationRequirement id="{{ requirement.id }}"> <requiredInput href="#{{ requirement.hRef }}" /> </informationRequirement>"""

        render_template = self.jinja_environment.from_string(template)
        data = render_template.render(requirement=self)

        return data
    
class KnowledgeRequirement(Requirement):
    """Represents a DMN Knowledge Requirement.

    Parameters
    ----------
    id : str
        Unique identifier of the Requirement.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        super(KnowledgeRequirement, self).__init__(id, prediction)

    def render_requirement(self):
        """Returns the xml string associated to a KnowledgeFlow"""

        template = """<knowledgeRequirement id="{{ requirement.id }}"> <requiredKnowledge href="#{{ requirement.hRef }}" /> </knowledgeRequirement>"""
        render_template = self.jinja_environment.from_string(template)
        data = render_template.render(requirement=self)

        return data
    
class AuthorityRequirement(Requirement):
    """Represents a DMN Authority Requirement.

    Parameters
    ----------
    id : str
        Unique identifier of the Requirement.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        super(AuthorityRequirement, self).__init__(id, prediction)

    def render_requirement(self):
        """Returns the xml string associated to a AuthorityRequirement"""

        template = """<authorityRequirement id="{{ requirement.id }}"> <requiredAuthority href="#{{ requirement.hRef }}" /> </authorityRequirement>"""
        render_template = self.jinja_environment.from_string(template)
        data = render_template.render(requirement=self)

        return data
    
class Association(Requirement):
    """Class for the associations (between textAnnotation and DMN Elements) that can be put within a DMN Diagram.

    Parameters
    ----------
    id : str
        Unique identifier of the Association.
    prediction : KeyPointPrediction
        The prediction given by the keypoint detection predictor.
    """
    def __init__(
        self,
        id: str,
        prediction: KeyPointPrediction,
    ):
        self.id = id
        self.prediction = prediction
        self.jinja_environment = Environment(loader=BaseLoader())
        self.sourceRef = None
        self.targetRef = None

    def render_association(self):
        """Returns the xml string associated to this Association"""

        template = """<association id="{{ association.id }}" >
        <sourceRef href="#{{ association.sourceRef}}" /> <targetRef href="#{{association.targetRef}}" /> 
        </association>
         
           requiredKnowledge href="#{{ flow.Ref }}" /> <knowledgeRequirement>" """
        render_template = self.jinja_environment.from_string(template)
        data = render_template.render(association=self)
        
        return data
    def render_shape(self):
        """Returns the xml string containing the shape information of this kind of flow"""
        template = """<dmndi:DMNEdge id="{{ association.id }}_di" dmnElementRef="{{ association.sourceRef }}" >
        <di:waypoint x="{{ association.prediction.tail[0] }}" y="{{ association.prediction.tail[1] }}" />
        <di:waypoint x="{{ association.prediction.head[0] }}" y="{{ association.prediction.head[1] }}" />
      </bpmndi:BPMNEdge>
        """
        rtemplate = self.jinja_environment.from_string(template)
        data = rtemplate.render(association=self)

        return data