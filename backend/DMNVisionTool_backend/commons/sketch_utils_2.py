from DMNVisionTool_backend.DecisionTables.Handwritten import table_factories as tf
from DMNVisionTool_backend.DecisionTables.table_predictions import TablePrediction
from typing import List 

import math

from typing import List

from DMNVisionTool_backend.DecisionTables.table_elements import TableElement, TableRule #tba 

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
    
    # If the list of rules is not empty
    if rules:
        print("Rules where found in the predictions")
        envelope = min(
        rules,
        key=lambda x: math.sqrt(
            pow(center[0] - x.prediction.center[0], 2)
            + pow(center[1] - x.prediction.center[1], 2)
        ),
    )
    # If the list of rules is empty
    else:
        print("No rules where recognized by the model, so a rule is created")
        size = 4
        top_left_x = center[0] - size / 2
        top_left_y = center[1] + size / 2
        bottom_right_x = center[0] + size / 2
        bottom_right_y = center[1] - size / 2

        prediction = TablePrediction(5, top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        factory = tf.get_table_factory(prediction.predicted_label)
        envelope = factory.create_element(prediction)

    return envelope