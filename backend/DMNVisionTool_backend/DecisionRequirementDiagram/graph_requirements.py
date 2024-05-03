from jinja2 import Environment, BaseLoader

from DMNVisionTool_backend.DecisionRequirementDiagram.graph_predictions import KeyPointPrediction

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
       # Adjust the tail and head coordinates to match the scaled elements
       scale_factor = 0.5  # Adjust this scale factor to match the one used for scaling the elements
       tail_x = self.prediction.tail[0] * scale_factor
       tail_y = self.prediction.tail[1] * scale_factor
       head_x = self.prediction.head[0] * scale_factor
       head_y = self.prediction.head[1] * scale_factor

       template = """<dmndi:DMNEdge dmnElementRef="{{ requirement.id }}" >
       <di:waypoint x="{{ tail_x }}" y="{{ tail_y }}" />
       <di:waypoint x="{{ head_x }}" y="{{ head_y }}" />
       </dmndi:DMNEdge>
       """
       rtemplate = self.jinja_environment.from_string(template)
       data = rtemplate.render(requirement=self, tail_x=tail_x, tail_y=tail_y, head_x=head_x, head_y=head_y)

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

        else: 
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
    
