import inspect
import math
import os
import random
import string
from typing import List

from DMNVisionTool_backend.DecisionRequirementDiagram.graph_elements import Element 
from DMNVisionTool_backend.DecisionTables.table_elements import TableElement, TableRule #tba 

def generate_id(prefix: str) -> str:
    """Utils that generate a random id given a string prefix

    Parameters
    ----------
    prefix: str
        The prefix of the id

    Returns
    -------
    str
        The random id with the given prefix
    """

    alphanumeric_str = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(7)
    )
    return f"{prefix}_{alphanumeric_str}"

def get_envelope_element(center: List[int], table_elements: List[TableElement]) -> TableElement:
    """Utils taht given oa list of Table elements and the desired center, return the element enveloping the element (of which the center is given)
    
    Parameters
    ----------
    center: List[int]
        A tuple with the coordinates of the desired center
    table_elements: List of tables elements to be considered for the nearest element
    
    Returns
    -------
    TableElement
        The table element enveloping the center
    """
    rules = []
    for element in table_elements:
        if isinstance (element, TableRule):
            rules.append(element)
    
    envelope = min(
        rules,
        key=lambda x: math.sqrt(
            pow(center[0] - x.prediction.center[0], 2)
            + pow(center[1] - x.prediction.center[1], 2)
        ),
    )
    
    return envelope


def get_nearest_element(
    center: List[int], elements: List[Element]) -> Element:
    """Utils that given a list of elements and the desired center, return the nearest element

    Parameters
    ----------
    center: List[int]
        A tuple with the coordinates of the desired center
    elements: List[Element]
        The list of objected to be considered for the nearest element

    Returns
    -------
    Element
        The nearest element to the given center
    """

    nearest = min(
        elements,
        key=lambda x: math.sqrt(
            pow(center[0] - x.prediction.center[0], 2)
            + pow(center[1] - x.prediction.center[1], 2)
        ),
    )

    return nearest

def here(resource: str):
    """Utils that given a relative path returns the corresponding absolute path, independently from the environment

    Parameters
    ----------
    resource: str
        The relative path of the given resource

    Returns
    -------
    str
        The absolute path of the give resource
    """
    stack = inspect.stack()
    caller_frame = stack[1][0]
    caller_module = inspect.getmodule(caller_frame)
    return os.path.abspath(
        os.path.join(os.path.dirname(caller_module.__file__), resource)
    )

# Verify specifications of the dmn sample table 
sample_dmn = '<?xml version="1.0" encoding="UTF-8"?> '\
             '<dmn:definitions xmlns:dmn="http://www.omg.org/spec/DMN/20151101/dmn.xsd" '\
             'xmlns:di="http://www.omg.org/spec/DMN/20151101/dmn-di.xsd" '\
             'xmlns:dc="http://www.omg.org/spec/DMN/20151101/dc.xsd" '\
             'xmlns:camunda="http://camunda.org/schema/1.0/dmn" id="sample-dmn" '\
             'name="Sample DMN Diagram" namespace="http://bpmn.io/schema/dmn"> '\
             '<dmn:decision id="Decision_1" name="SampleDecision"></dmn:decision><dmndi:DMNDiagram '\
             'id="DMNDiagram_1"><dmndi:DMNPlane id="DMNPlane_1" bpmnElement="Decision_1"><dmndi:DMNShape '\
             'id="_DMNShape_Decision_2" dmnElement="Decision_1"><dc:Bounds height="80.0" width="120.0" '\
             'x="100.0" y="100.0"/></dmndi:DMNShape></dmndi:DMNPlane></dmndi:DMNDiagram></dmn:definitions> '