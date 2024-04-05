import jinja2
from typing import List, TYPE_CHECKING
from Levenshtein import distance

from DMNVisionTool_backend.graphs.graph_elements import Element, Diagram, Decision
from DMNVisionTool_backend.graphs.graph_requirements import Requirement, Association
from DMNVisionTool_backend.graphs.elements_factories import get_factory
from DMNVisionTool_backend.graphs.requirements_factories import get_keypoint_factory
from DMNVisionTool_backend.tables.table_elements import TableElement, TableHeader, TableHitPolicy, TableInput, TableOutput, TableRule, InputEntry, OutputEntry
from DMNVisionTool_backend.tables.dmn_decisionLogic import Table 
from DMNVisionTool_backend.commons.utils import get_nearest_element, here, get_envelope_element

from DMNVisionTool_backend.graphs import elements_factories as ef
from DMNVisionTool_backend.graphs import requirements_factories as rf
from DMNVisionTool_backend.tables import table_factories as tf
from DMNVisionTool_backend.tables import decisionLogic_factories as df

if TYPE_CHECKING:
    from graphs.graph_predictions import (
        ObjectPrediction,
        KeyPointPrediction,
    )

if TYPE_CHECKING:
    from tables.table_predictions import TableElementPrediction, TablePrediction

# TO DO: I added prints to check the working of the function but we can delete those later
def convert_object_predictions(predictions: List["ObjectPrediction"]):
    """Method that converts the prediction of the detected dmn object into Elements

    Parameters
    ----------
    predictions: List[ObjectPrediction]
        List of ObjectPrediction

    Returns
    -------
    List[Element]
        The list of converted DMN Element
    """

    elements = []
    for prediction in predictions:
        print("predictedLabel:", prediction.predicted_label)
        factory = ef.get_factory(prediction.predicted_label)
        print("Factory:" , factory)
        if factory is not None:
            print("factory is not none")
            dmn_element = factory.create_element(prediction)
            print("dmn element:", dmn_element)
            if dmn_element is not None:
                print("dmn element is not none")
                elements.append(dmn_element)

    return elements

# TO DO: I added prints to check the working of the function but we can delete those later
def convert_keypoint_prediction(predictions: List["KeyPointPrediction"]):
    """Method that converts the prediction of the keypoint into Requirement

    Parameters
    ----------
    predictions: List[KeyPointPrediction]
        List of KeyPointPrediction

    Returns
    -------
    List[Requirement]
        The list of converted dmn requirements
    """

    requirements = []
    for prediction in predictions:
        print("predictedLabel:", prediction.predicted_label)
        factory = rf.get_keypoint_factory(prediction.predicted_label)
        print("Factory:" , factory)
        if factory is not None:
            print("factory is not none")
            requirement = factory.create_requirement(prediction)
            if requirement is not None:
                print("requirement is not none")
                requirements.append(requirement)

    return requirements

def render_diagram(dmn_diagram: Diagram):
    """Method that renders a Diagram class into the final dmn string

    Parameters
    ----------
    dmn_diagram: Diagram
        id + definition id + List of ObjectPrediction

    Returns
    -------
    str
        The string representing the final dmn model
    """

    template_loader = jinja2.FileSystemLoader(
        searchpath=here("../../commons/templates/") 
    )
    template_env = jinja2.Environment(loader=template_loader)     
    template_file = "dmn_template.jinja"
    template = template_env.get_template(template_file)
    output_text = template.render({"diagram": dmn_diagram})

    return output_text

def connect_requirements(requirements: List[Requirement], elements: List[Element]):
    """Method that connects each Requirement to the Element it is pointing to.
    Adds the requirements to the element.requirements list of the Element
    
    Parameters
    ----------
    requirements: List[Requirement]
        List of detected Requirement
    elements: List[Element]
        List of Element 

    Returns
    -------
    elements: List[Element]
        The list of updated Elements 

    """
    for requirement in requirements:
        head = requirement.prediction.head
        
        near_head = get_nearest_element(head, elements)
        
        near_head.requirements.append(requirement)
    return elements

def reference_requirements(requirements: List[Requirement], elements: List[Element]):
    """Method that references each Requirement to the Element it is coming from.
    Adds that element to requirement.hRef
    
    Parameters
    ----------
    requirements: List[Requirement]
        List of detected Requirement
    elements: List[Element]
        List of Element 

    Returns
    -------
    requirements: List[Requirement]
        List of updated Requirement
    """
    for requirement in requirements:
        tail = requirement.prediction.tail
        
        near_tail = get_nearest_element(tail, elements)
        
        requirement.hRef = near_tail.id
        
    return requirements

# Text Annotations are a subclass of Element
# Association are not a subclass of Requirement
# Consider changing this for more clarity in the code
def connect_textAnnotations(associations: List[Association], elements:List[Element]):
    """Method that connects each text Annotation to the Element it is associated with.
    Adds a Text Annotation element to sourceRef 
    & Element to targetRef
    
    Parameters
    ----------
    assocations: List[Association]
        List of detected Associations
    elements: List[Element]
        List of Element 

    Returns
    -------
    assocations: List[Association]
        List of detected Associations
    """
    for association in associations:
        tail = association.prediction.tail
        head = association.prediction.head
        
        near_tail = get_nearest_element(tail, elements)
        near_head = get_nearest_element(head, elements)
        
        association.sourceRef = near_tail
        association.targetRef = near_head
        
    return associations

# TO DO: I added prints to check the working of the function but we can delete those later
def convert_table_predictions(predictions: List["TablePrediction"]):
    """Method that converts the prediction of the detected table into a Table Element

    Parameters
    ----------
    predictions: List[TablePrediction]
        List of TablePrediction

    Returns
    -------
    List[Element]
        The list of converted DMN Element
    """

    converted_tables = []
    for prediction in predictions:
        print("predictedLabel:", prediction.predicted_label)
        factory = df.get_table_factory(prediction.predicted_label)
        print("Factory:" , factory)
        if factory is not None:
            print("factory is not none")
            dmn_table = factory.create_table(prediction)
            print("dmn table:", dmn_table)
            if dmn_table is not None:
                print("dmn table is not none")
                converted_tables.append(dmn_table)

    return converted_tables

def convert_tableElement_predictions(predictions: List["TableElementPrediction"]):
    """Method that converts the prediction of the detected table element into TableElements

    Parameters
    ----------
    predictions: List[TableElementPrediction]
        List of TableElementPrediction

    Returns
    -------
    List[TableElement]
        The list of converted Table Element
    """
    tableElements = []
    for prediction in predictions:
        print("predictedLabel:", prediction.predicted_label)
        factory = tf.get_factory(prediction.predicted_label)
        print("Factory:" , factory)
        if factory is not None:
            print("factory is not none")
            table_element = factory.create_element(prediction)
            print("table element:", table_element)
            if table_element is not None:
                print("dmn element is not none")
                tableElements.append(table_element)

    return tableElements

# Assumption: We only predict one table at a time, not multiple tables on the same picture
def connect_components2table(table: Table, header: TableHeader, hitPolicy: TableHitPolicy, inputs:List[TableInput]=[], outputs: List[TableOutput]=[], rules: List[TableRule]=[]):
    """Method that connects every component of the table to the table

    Parameters
    ----------
    table: Table
        The table element.
    header: TableHeader
        Table header. 
    hitPolicy: TableHitPolicy
        Table hit policy
    inputs: List[TableInput]
        Table inputs
    outputs: List[TableOutput]
        Table's outputs
    rules: List[TableRule]
        Table's rules    
    """
    if not isinstance(table, Table):
        print("Table is not an instance of a Table")
        
    else: 
        print ("Table is an instance of a Table")
        if header is not None:
            table.header = header
        if hitPolicy is not None:
            table.hitPolicy = hitPolicy
        for input in inputs: 
            table.inputs.append(input)
        for output in outputs: 
            table.outputs.append(output)
        for rule in rules: 
            table.rules.append(rule)

    return table
    
def connect_entries2rule(rules: List[TableRule]=[], inputEntries: List[InputEntry]=[], outputEntries: List[OutputEntry]=[]):
    """Method that connects the input and output entries to the rule they are in
    
    Parameters
    ----------
    rules: List[TableRule]
        List of the rules detected in the table
    inputEntries: List[inputEntry]
        List of input entries detected in the table
    outputEntries: List[outputEntry]
        List of output entries detected in the table
    """
    for inputEntry in inputEntries:
        center = inputEntry.prediction.center
        envelope = get_envelope_element(center, rules) 
        envelope.inputEntries.append(inputEntry)
        
    for outputEntry in outputEntries:
        center = outputEntry.prediction.center
        envelope = get_envelope_element(center, rules) 
        envelope.outputEntries.append(outputEntry)
        
    return rules

def connect_graph2tables(elements: List[Element], tables: List[Table]):
    """Method that connects table to the right decision element based on its header
    
    Parameters
    ----------
    elements: List[Element]
        List of the decision elements
    tables: List[Table]
        List of the tables
    """
    decisions = []
    for element in elements: 
        if isinstance(element, Decision):
            decisions.append(element)

    for decision in decisions:
        decision_name = decision.get_name()
        print("Decision name:", decision_name)
        for decision_table in tables:
            if isinstance(decision_table, Table):
                print("table recognised is an instance of a table")
                if isinstance(decision_table.header, TableHeader):
                    print("There is a decision table header of the class TableHeader")
                    header_lable = decision_table.header.get_label()
                    print("Header label:", header_lable)
                    
                    if distance(decision_table.header.get_label(), decision_name) <= 6:
                    #if decision_table.header.get_label() == :
                        decision.table.append(decision_table)
                        print("Decision table added to the decision")
                    
                else: 
                    print("There is no decision table's header or it is not of the class TableHeader")
                
            else: 
                print("No table has been recognised")
                
    return elements
