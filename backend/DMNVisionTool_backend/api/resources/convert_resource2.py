# Convert resource 2 to be sure not to remove anything that we would need when modifying the code

# Imports 
import time
from DMNVisionTool_backend.api.services import preprocessing_service as ss
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from DMNVisionTool_backend.tables.table_factories import TableElementFactory 
from DMNVisionTool_backend.api.services import (
    predict_service as ps,
    sketch_predict_service as sps,
    ocr_service as os,
    convert_service as cs,
    sketch_convert_service as scs,
)
from DMNVisionTool_backend.graphs.elements_factories import DiagramFactory
from DMNVisionTool_backend.graphs.Sketches.elements_factories import DiagramFactorySketches
from DMNVisionTool_backend.commons.utils import sample_dmn, here
from DMNVisionTool_backend.tables.table_elements import TableElement, TableHeader, TableHitPolicy, TableInput, TableOutput, TableRule, InputEntry, OutputEntry
from DMNVisionTool_backend.tables.dmn_decisionLogic import Table
from DMNVisionTool_backend.graphs.graph_elements import Decision
from DMNVisionTool_backend.api.services import htr_service as htr

# Convert Resource
async def convert_images(request:Request):
    """Post method to manage the conversion of images to their corresponding
    dmn models
    There should be max one graph
    
    Returns
    -------
    str
        The converted dmn model
    """
    # Await & handle request
    form = await request.form()
    image_left = form.get('imageLeft')
    image_right = form.get('imageRight')
    
    # Generate unique path names for both files
    t = int(time.time_ns())
    path_left = here("../../temp_files/img_{}_{}".format(t, image_left.filename))
    path_right = here("../../temp_files/img_{}_{}".format(t, image_right.filename))
    
    # Write the uploaded images to the disk
    with open(path_left, 'wb+') as disk_file_left, open(path_right, 'wb+') as disk_file_right:
        disk_file_left.write(await image_left.read())
        disk_file_right.write(await image_right.read())
        
    # Perform preprocessing on both images
    ocr_img_left, predict_img_left = ss.get_ocr_and_predict_images(path_left)
    ocr_img_right, predict_img_right = ss.get_ocr_and_predict_images(path_right)
    
    # Return predefined error response if any of the images is none !!to do: Add an error message
    if ocr_img_left is None or predict_img_left is None or ocr_img_right is None or predict_img_right is None:
        return PlainTextResponse(content=sample_dmn, status_code=200)
    
    # Classification
    for idx, (ocr_img, predict_img, sketch_field, graph_field, elements_field, ocr_field, flow_field, decisionLogic_field) in enumerate(
        [(ocr_img_left, predict_img_left, 'sketchLeft', 'graphLeft', 'elementsLeft', 'ocrLeft', 'flowsLeft','decisionLogicLeft'), 
         (ocr_img_right, predict_img_right, 'sketchRight', 'graphRight', 'elementsRight', 'ocrRight', 'flowsRight','decisionLogicRight')], 
         start=1):
        
        # PDF + GRAPH
        if sketch_field not in form and form[sketch_field] == 'false' and graph_field in form and form[graph_field]== 'true':
            print(f"Converting image {idx} as a PDF GRAPH...")
            
            if elements_field in form and form[elements_field] == 'true':
                obj_predictions = ps.PredictObject(predict_img)
                drd_elements = cs.convert_object_predictions(obj_predictions)

            if flow_field in form and form[flow_field] == 'true':
                kp_predictions = ps.PredictKeypoint(ocr_img)
                requirements = cs.convert_keypoint_prediction(kp_predictions)
                cs.connect_requirements(requirements, drd_elements)
                cs.reference_requirements(requirements, drd_elements)
            
            if ocr_field in form and form[ocr_field] == 'true':
                text = os.get_text_from_img(ocr_img)
                os.link_text(text, drd_elements)
        
        # PDF + TABLE
        elif sketch_field not in form and form[sketch_field] == 'false' and decisionLogic_field in form and form[decisionLogic_field]== 'true':
            print(f"Converting image {idx} as a PDF TABLE...")
            
            if elements_field in form and form[elements_field] == 'true':
                table_predictions = ps.PredictTable(predict_img)
                converted_tables = cs.convert_table_predictions(table_predictions)
                ts_predictions = ps.PredictTableElement(predict_img)
                table_elements = cs.convert_tableElement_predictions(ts_predictions)

            if ocr_field in form and form[ocr_field] == 'true':
                text = os.get_text_from_table_img(ocr_img)
                os.link_text_table(text, table_elements) 

            tables = []
            table = Table 
            table_header = TableHeader
            table_hitPolicy = TableHitPolicy
            table_inputs = []
            table_outputs = []
            table_rules = []
            input_entries = []
            output_entries = []  

            for converted_table in converted_tables:
                if isinstance(converted_table, Table):
                    table = converted_table
            for table_element in table_elements:
                if isinstance(table_element, TableHeader):
                    table_header = table_element
                elif isinstance(table_element, TableHitPolicy):
                    table_hitPolicy = table_element
                elif isinstance(table_element, TableInput):
                    table_inputs.append(table_element)
                elif isinstance(table_element, TableOutput):
                    table_outputs.append(table_element)
                elif isinstance(table_element, TableRule):
                    table_rules.append(table_element)
                elif isinstance(table_element, InputEntry):
                    input_entries.append(table_element)
                elif isinstance(table_element, OutputEntry):
                    output_entries.append(table_element)
            
                table_rules = cs.connect_entries2rule(table_rules, input_entries, output_entries)               
                table_connect = cs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
                tables.append(table_connect)
        
        # SKETCH + GRAPH
        elif sketch_field in form and form[sketch_field] == 'true' and graph_field in form and form[graph_field]== 'true':
            print(f"Converting image {idx} as a SKETCH GRAPH...")
            
            if elements_field in form and form[elements_field] == 'true':
                obj_predictions = sps.SketchPredictObject(predict_img)
                drd_elements = scs.convert_object_predictions(obj_predictions)
            
            if flow_field in form and form[flow_field] == 'true':
                kp_predictions = sps.SketchPredictKeypoint(predict_img)
                requirements = scs.convert_keypoint_prediction(kp_predictions)
                scs.connect_requirements(requirements, drd_elements) 
                scs.reference_requirements(requirements, drd_elements)
            
            if ocr_field in form and form[ocr_field] == 'true':
                htr.get_text_from_element(drd_elements, ocr_img)
        
        # SKETCH + TABLE
        elif sketch_field in form and form[sketch_field] == 'true' and decisionLogic_field in form and form[decisionLogic_field]== 'true':
            print(f"Converting image {idx} as a SKETCH TABLE...")
            
            if elements_field in form and form[elements_field] == 'true':
                table_prediction = sps.PredictTable(predict_img) 
                converted_tables = cs.convert_table_predictions(table_prediction) 
                table_element_predictions = sps.PredictTableElement(predict_img)
                table_elements = cs.convert_tableElement_predictions(table_element_predictions)
            
            if ocr_field in form and form[ocr_field] == 'true':
                htr.get_text_from_element(table_elements, ocr_img)
            
            # to do: Move this somewhere else to have a cleaner code here??
            tables = []
            table = Table 
            table_header = TableHeader
            table_hitPolicy = TableHitPolicy
            table_inputs = []
            table_outputs = []
            table_rules = []
            input_entries = []
            output_entries = []  

            for converted_table in converted_tables:
                if isinstance(converted_table, Table):
                    table = converted_table
            for table_element in table_elements:
                if isinstance(table_element, TableHeader):
                    table_header = table_element
                elif isinstance(table_element, TableHitPolicy):
                    table_hitPolicy = table_element
                elif isinstance(table_element, TableInput):
                    table_inputs.append(table_element)
                elif isinstance(table_element, TableOutput):
                    table_outputs.append(table_element)
                elif isinstance(table_element, TableRule):
                   table_rules.append(table_element)
                elif isinstance(table_element, InputEntry):
                   input_entries.append(table_element)
                elif isinstance(table_element, OutputEntry):
                    output_entries.append(table_element)
            
            table_rules = cs.connect_entries2rule(table_rules, input_entries, output_entries)
            table_connect = cs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
            tables.append(table_connect) 
            
        # OTHER
        else:
            print(f"Something went wrong when trying to convert {idx}...")
            

        # Connect Graph to Table(s)
                     
        elements_connect = cs.connect_graph2tables(drd_elements, tables)
        
        dmn_diagram = DiagramFactory.create_element(elements_connect) 
        rendered_dmn_model = cs.render_diagram(dmn_diagram)
        print("XML representation of the DMN model:")
        print(rendered_dmn_model)
        
        return PlainTextResponse(content=rendered_dmn_model, status_code=200)