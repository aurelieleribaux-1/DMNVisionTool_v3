import jinja2
from typing import List, TYPE_CHECKING
from Levenshtein import distance
import random

from DMNVisionTool_backend.DecisionRequirementDiagram.graph_elements import Element, Diagram, Decision
from DMNVisionTool_backend.DecisionRequirementDiagram.graph_requirements import Requirement
from DMNVisionTool_backend.DecisionRequirementDiagram.Handwritten.elements_factories import get_factory
from DMNVisionTool_backend.DecisionRequirementDiagram.Handwritten.requirements_factories import get_keypoint_factory
from DMNVisionTool_backend.DecisionTables.table_elements import Table, TableElement, TableHeader, TableHitPolicy, TableInput, TableOutput, TableRule, InputEntry, OutputEntry 
from DMNVisionTool_backend.commons.Sketch_utils import get_nearest_element, here, get_envelope_element

from DMNVisionTool_backend.DecisionRequirementDiagram.Handwritten import elements_factories as ef
from DMNVisionTool_backend.DecisionRequirementDiagram.Handwritten import requirements_factories as rf
from DMNVisionTool_backend.DecisionTables.Handwritten import table_factories as tf 

from DMNVisionTool_backend.DecisionTables.table_predictions import TablePrediction 

if TYPE_CHECKING:
    from DecisionRequirementDiagram.graph_predictions import (
        ObjectPrediction,
        KeyPointPrediction,
    )

#if TYPE_CHECKING:
#    from DecisionTables.table_predictions import TableElementPrediction, TablePrediction 

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
    print("Number of predictions:", len(predictions))  # Debug message
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
    print("Number of predictions:", len(predictions))  # Debug message
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


def convert_table_object_predictions(predictions: List["TablePrediction"]):
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
        factory = tf.get_table_factory(prediction.predicted_label)
        print("Factory:" , factory)
        if factory is not None:
            print("factory is not none")
            dmn_table = factory.create_element(prediction)
            print("dmn table:", dmn_table)
            if dmn_table is not None:
                print("dmn table is not none")
                converted_tables.append(dmn_table)

    return converted_tables

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
            
    for decision_table in tables:
        if isinstance(decision_table, Table):
            print("Table recognised is an instance of a table")
            if isinstance(decision_table.header, TableHeader):
                print("There is a decision table header of the class TableHeader")
                header_label = decision_table.header.get_label()
                print("Header label:", header_label)
                label = header_label # Header label will be used for the matching
            
            elif isinstance(decision_table.outputs, TableOutput):
                output_label = decision_table.outputs.get_label()
                print("There is a decision table output of the class TableOutput")
                print("Output label:", output_label)
                label = output_label # Output label will be used for the matching
                
            else: 
                print("Neither header nor output label was recongized in the table so table will be assigned to a random decision")
                label = None
                
            # Case 1: There is either a header or output recognized
            if label is not None:
            # Check in all decisions in the graph, which one is the closest (Levenstein) to the label used for the matching
            # Initialize distance
                dist=0
                old_distance = 10000
                for decision in decisions:
                    decision_name = decision.get_name()
                    print("Decision name:", decision_name)
                    dist = distance(decision_table.header.get_label(), decision_name)
                    if dist < old_distance:
                        old_distance = dist
                        decision_matched = decision
                    
                decision_matched.table.append(decision_table)
                    
            # Case 2: Neither header nor output was recognized, label is None
            else: 
                # Assign table to random decision
                for decision in decisions:
                    random_decision = random.choice(decisions)
                    random_decision.table.append(decision_table)
                
        else:
            print("Table is not an instance of Table class, something went wrong")
            label = None
                
    return elements

def create_extra_table_elements(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules, input_entries, output_entries):
    """Method that creates extra table elements in case of missing ones
    
    Parameters
    ----------
    table = Table 
    table_header = TableHeader
    table_hitPolicy = TableHitPolicy
    table_inputs = []
    table_outputs = []
    table_rules = []
    input_entries = []
    output_entries = []
    
    Returns
    -------
    table = Table 
    table_header = TableHeader
    table_hitPolicy = TableHitPolicy
    table_inputs = []
    table_outputs = []
    table_rules = []
    input_entries = []
    output_entries = []
    """
    # Set a random bbox prediction
    # To do: Retrieve bbox from one prediction that is well predicted?
    top_left_x = 1
    top_left_y = 1
    bottom_right_x = 10
    bottom_right_y = 10
    
    if not isinstance(table, Table):
        print("No table was predicted, so one is added")
        prediction = TablePrediction(7, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        factory = tf.get_table_factory(prediction.predicted_label)
        table = factory.create_element(prediction)
    if not isinstance(table_header, TableHeader):
        print("No table header was predicted, so one is added")
        prediction = TablePrediction(4, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        factory = tf.get_table_factory(prediction.predicted_label)
        table_header = factory.create_element(prediction)
    if not isinstance(table_hitPolicy, TableHitPolicy):
        print("No table header was predicted, so one is added")
        prediction = TablePrediction(6, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        factory = tf.get_table_factory(prediction.predicted_label)
        table_hitPolicy = factory.create_element(prediction)
    if table_inputs == []:
        print("No table_inputs was predicted, so one is added")
        prediction = TablePrediction(3, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        factory = tf.get_table_factory(prediction.predicted_label)
        extra_input = factory.create_element(prediction)
        table_inputs.append(extra_input)
    if table_outputs == []:
        print("No table_outputs was predicted, so one is added")
        prediction = TablePrediction(2, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        factory = tf.get_table_factory(prediction.predicted_label)
        extra_output = factory.create_element(prediction)
        table_outputs.append(extra_output)
    if table_rules == []:
        print("No table_rules was predicted, so one is added")
        prediction = TablePrediction(5, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        factory = tf.get_table_factory(prediction.predicted_label)
        extra_rule = factory.create_element(prediction)
        table_rules.append(extra_rule)
        
    return table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules, input_entries, output_entries