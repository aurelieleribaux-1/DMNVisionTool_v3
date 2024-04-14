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
from DMNVisionTool_backend.graphs.PDF.elements_factories import DiagramFactory
from DMNVisionTool_backend.graphs.Sketches.elements_factories import DiagramFactorySketches
from DMNVisionTool_backend.commons.utils import sample_dmn, here
from DMNVisionTool_backend.tables.table_elements import TableElement, TableHeader, TableHitPolicy, TableInput, TableOutput, TableRule, InputEntry, OutputEntry
from DMNVisionTool_backend.tables.dmn_decisionLogic import Table
from DMNVisionTool_backend.graphs.graph_elements import Decision
from DMNVisionTool_backend.api.services import htr_service as htr 

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
    ocr_img_sketch_left, ocr_img_pdf_left, predict_img_left = pps.get_ocr_and_predict_images(path_left)
    ocr_img_sketch_right, ocr_img_pdf_right, predict_img_right = pps.get_ocr_and_predict_images(path_right)

    # Return predefined error if any of the image is none
    if ocr_img_sketch_left is None or predict_img_left is None or ocr_img_sketch_right is None or predict_img_right is None or ocr_img_pdf_left is None  or ocr_img_pdf_right is None:
        return PlainTextResponse(content=sample_dmn, status_code=200)

    # Classification
    for idx, (ocr_img_sketch, ocr_img_pdf, predict_img, path, sketch_field, graph_field, elements_field, ocr_field, flow_field, decisionLogic_field) in enumerate(
        [(ocr_img_sketch_left, ocr_img_pdf_left, predict_img_left, path_left, 'sketchLeft', 'graphLeft', 'elementsLeft', 'ocrLeft', 'flowsLeft','decisionLogicLeft'), 
         (ocr_img_sketch_right, ocr_img_pdf_right, predict_img_right, path_right, 'sketchRight', 'graphRight', 'elementsRight', 'ocrRight', 'flowsRight','decisionLogicRight')], 
         start=0):
        
    # SKETCH + GRAPH  
      if sketch_field in form and form[sketch_field] == 'true': 
        if graph_field in form and form[graph_field] == 'true':
            print(f"Converting image {idx} as a graph sketch...")
            #drd_elements = None
            if elements_field in form and form[elements_field] == 'true':
                obj_predictions = sps.SketchPredictObject(predict_img)
                drd_elements = scs.convert_object_predictions(obj_predictions)

                if flow_field in form and form[flow_field] == 'true':
                    kp_predictions = sps.SketchPredictKeypoint(predict_img)
                    requirements = scs.convert_keypoint_prediction(kp_predictions)
                    scs.connect_requirements(requirements, drd_elements)
                    scs.reference_requirements(requirements, drd_elements)
                     
                if ocr_field in form and form[ocr_field] == 'true':
                    text = os.get_text_from_img(ocr_img_sketch)
                    print('text:',text)
                    os.link_text(text, drd_elements)
        
    # SKETCH + TABLE            
        elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
            print(f"Converting image {idx} as a sketch table...")
            
            if elements_field  in form and form[elements_field] == 'true':
                    table_prediction = sps.SketchPredictTable(predict_img) 
                    converted_tables = scs.convert_table_predictions(table_prediction) 
                    table_element_predictions = sps.SketchPredictTableElement(predict_img)
                    table_elements = scs.convert_tableElement_predictions(table_element_predictions)
            
            if ocr_field in form and form[ocr_field] == 'true':
                # i get this error: File "/app/./DMNVisionTool_backend/api/services/htr_service.py", line 27, in get_text_from_element
                       # image = Image.open(image_path).convert("RGB")
                       #File "/usr/local/lib/python3.8/site-packages/PIL/Image.py", line 3283, in open
                       # fp = io.BytesIO(fp.read())
                    #AttributeError: 'numpy.ndarray' object has no attribute 'read'
                #htr.get_text_from_element(ocr_img, table_elements)

                #so for now i will still use this: 
                text = os.get_text_from_table_img(ocr_img_sketch)
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
            
                table_rules = scs.connect_entries2rule(table_rules, input_entries, output_entries)#
                table_connect = scs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)#
                tables.append(table_connect)
            
                elements_connect = scs.connect_graph2tables(drd_elements, tables)
     
                dmn_diagram = DiagramFactorySketches.create_element(elements_connect) 
                rendered_dmn_model = scs.render_diagram(dmn_diagram)
                print("XML representation of the DMN model:")
                print(rendered_dmn_model)
    

    # GRAPH + PDF
      else: 
        if graph_field in form and form[graph_field] == 'true':
            print(f"Converting image {idx} as a graph...")
            if elements_field in form and form[elements_field] == 'true':
                obj_predictions = ps.PredictObject(predict_img)
                drd_elements = cs.convert_object_predictions(obj_predictions)

                if flow_field in form and form[flow_field] == 'true':
                    kp_predictions = ps.PredictKeypoint(ocr_img_pdf)
                    requirements = cs.convert_keypoint_prediction(kp_predictions)
                    scs.connect_requirements(requirements, drd_elements)
                    scs.reference_requirements(requirements, drd_elements)
                    scs.connect_textAnnotations(requirements, drd_elements)
                    #drd_elements.extend(requirements)

                if ocr_field in form and form[ocr_field] == 'true':
                    text = os.get_text_from_img(ocr_img)
                    os.link_text(text, drd_elements)

                    

    # TABLE + PDF
        elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
            print(f"Converting image {idx} as a table...")
            if elements_field in form and form[elements_field] == 'true':
                table_predictions = ps.PredictTable(predict_img)
                converted_tables = cs.convert_table_predictions(table_predictions)
                ts_predictions = ps.PredictTableElement(predict_img)
                table_elements = cs.convert_tableElement_predictions(ts_predictions)

                
                if ocr_field in form and form[ocr_field] == 'true':
                    text = os.get_text_from_table_img(ocr_img_pdf)
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
                    
                    elements_connect = cs.connect_graph2tables(drd_elements, tables)
    
                    dmn_diagram = DiagramFactory.create_element(elements_connect) 
                    rendered_dmn_model = cs.render_diagram(dmn_diagram)
                    print("XML representation of the DMN model:")
                    print(rendered_dmn_model)
    # OTHER     
        #else:
        #    print('There is something wrong, image is neither a graph neither a table')
    
    
    return PlainTextResponse(content=rendered_dmn_model, status_code=200)
