import time
from DMNVisionTool_backend.api.services import preprocessing_service as pps
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from DMNVisionTool_backend.api.services import (
    predict_service as ps,
    sketch_predict_service as sps,
    ocr_service as os,
    convert_service as cs,
    sketch_convert_service as scs,
)
from DMNVisionTool_backend.DecisionRequirementDiagram.Digital.elements_factories import DiagramFactory
from DMNVisionTool_backend.DecisionRequirementDiagram.Handwritten.elements_factories import DiagramFactorySketches
from DMNVisionTool_backend.commons.utils import sample_dmn, here
from DMNVisionTool_backend.DecisionTables.table_elements import Table, TableElement, TableHeader, TableHitPolicy, TableInput, TableOutput, TableRule, InputEntry, OutputEntry
from DMNVisionTool_backend.DecisionRequirementDiagram.graph_elements import Decision

async def convert_images(request:Request):
    """Post method to manage the conversion of images to their corresponding
    dmn models
    There should be max one graph
    
    Returns
    -------
    str
        The converted dmn model
    """
    # Await and handle request
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
    ocr_img_pdf_left, ocr_img_sketch_left, predict_img_pdf_left, predict_img_sketch_left = pps.get_ocr_and_predict_images(path_left)
    ocr_img_pdf_right, ocr_img_sketch_right, predict_img_pdf_right, predict_img_sketch_right = pps.get_ocr_and_predict_images(path_right)

    # Return predefined error if any of the image is none
    if ocr_img_sketch_left is None or predict_img_pdf_left is None or ocr_img_sketch_right is None or predict_img_pdf_right is None or ocr_img_pdf_left is None or ocr_img_pdf_right is None or predict_img_sketch_left is None or predict_img_sketch_right is None:
        return PlainTextResponse(content=sample_dmn, status_code=200)

    # Classification
    for idx, (ocr_img_pdf, ocr_img_sketch, predict_img_pdf, predict_img_sketch, path, sketch_field, digital_field, graph_field,  decisionLogic_field) in enumerate(
        [(ocr_img_pdf_left, ocr_img_sketch_left, predict_img_pdf_left, predict_img_sketch_left, path_left, 'sketchLeft', 'DigitalLeft', 'graphLeft', 'decisionLogicLeft'), 
         (ocr_img_pdf_right, ocr_img_sketch_right, predict_img_pdf_right, predict_img_sketch_right, path_right, 'sketchRight', 'DigitalRight', 'graphRight', 'decisionLogicRight')], 
         start=0):
        
    # HANDWRITTEN + DRD  
      if sketch_field in form and form[sketch_field] == 'true': 
        if graph_field in form and form[graph_field] == 'true':
            print(f"Converting image {idx} as a graph sketch...")
            #drd_elements = None
            obj_predictions = sps.SketchPredictObject(predict_img_sketch)
            drd_elements = scs.convert_object_predictions(obj_predictions)

                
            kp_predictions = sps.SketchPredictKeypoint(predict_img_sketch)
            requirements = scs.convert_keypoint_prediction(kp_predictions)
            scs.connect_requirements(requirements, drd_elements)
            scs.reference_requirements(requirements, drd_elements)
                     
            text = os.get_text_from_img(ocr_img_sketch,obj_predictions)
            print('text:',text)
            os.link_text(text, drd_elements)
        
    # HANDWRITTEN + DECISION TABLE            
        elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
            print(f"Converting image {idx} as a sketch table...")
            
            table_element_predictions = sps.SketchPredictTable(predict_img_sketch)
            table_elements = scs.convert_table_object_predictions(table_element_predictions)
            
    
            text = os.get_text_from_table_img_sketch(ocr_img_sketch,table_element_predictions)
            print('text', text)
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

            for table_element in table_elements:
                if isinstance(table_element, Table):
                        table = table_element
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
            
            table_rules = scs.connect_entries2rule(table_rules, input_entries, output_entries)
            table_connect = scs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
            tables.append(table_connect)
            
            elements_connect = scs.connect_graph2tables(drd_elements, tables)
     
            dmn_diagram = DiagramFactorySketches.create_element(elements_connect) 
            rendered_dmn_model = scs.render_diagram(dmn_diagram)
            print("XML representation of the DMN model:")
            print(rendered_dmn_model)
    

    # DRD + DIGITAL
      elif digital_field in form and form[digital_field] == 'true': 
        if graph_field in form and form[graph_field] == 'true':
            print(f"Converting image {idx} as a graph...")
            obj_predictions = ps.PredictObject(predict_img_pdf)
            drd_elements = cs.convert_object_predictions(obj_predictions)

            kp_predictions = ps.PredictKeypoint(predict_img_pdf)
            requirements = cs.convert_keypoint_prediction(kp_predictions)
            scs.connect_requirements(requirements, drd_elements)
            scs.reference_requirements(requirements, drd_elements)
            #drd_elements.extend(requirements)

            text = os.get_text_from_img(ocr_img_pdf,obj_predictions)
            os.link_text(text, drd_elements)

                    

    # DECISION TABLE + DIGITAL
        elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
            print(f"Converting image {idx} as a table...")
            ts_predictions = ps.PredictTable(predict_img_pdf)
            table_elements = cs.convert_table_object_predictions(ts_predictions)

            text = os.get_text_from_table_img_pdf(ocr_img_pdf,ts_predictions)
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

            for table_element in table_elements:
                    if isinstance(table_element, Table):
                           table = table_element
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
                    
            elements_connect = cs.connect_graph2tables(drd_elements, tables)
    
            dmn_diagram = DiagramFactory.create_element(elements_connect) 
            rendered_dmn_model = cs.render_diagram(dmn_diagram)
            print("XML representation of the DMN model:")
            print(rendered_dmn_model)
    # OTHER     
        #else:
        #    print('There is something wrong, image is neither a graph neither a table')
    
    
    return PlainTextResponse(content=rendered_dmn_model, status_code=200)
