import time
from DMNVisionTool_backend.api.services import preprocessing_service as ss
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from DMNVisionTool_backend.tables.table_factories import TableElementFactory 
from DMNVisionTool_backend.api.services import (
    predict_service as ps,
    ocr_service as os,
    convert_service as cs,
)
from DMNVisionTool_backend.graphs.elements_factories import DiagramFactory
from DMNVisionTool_backend.commons.utils import sample_dmn, here
from DMNVisionTool_backend.tables.table_elements import TableElement, TableHeader, TableHitPolicy, TableInput, TableOutput, TableRule, InputEntry, OutputEntry
from DMNVisionTool_backend.tables.dmn_decisionLogic import Table
from DMNVisionTool_backend.graphs.graph_elements import Decision

async def convert_images(request:Request):
    """Post method to manage the conversion of images to their corresponding
    dmn models
    There should be max one graph
    
    Returns
    -------
    str
        The converted dmn model
    """
    form = await request.form()
    image_left = form.get('imageLeft')
    image_right = form.get('imageRight')
    t = int(time.time_ns())
    path_left = here("../../temp_files/img_{}_{}".format(t, image_left.filename))
    path_right = here("../../temp_files/img_{}_{}".format(t, image_right.filename))
    
    with open(path_left, 'wb+') as disk_file_left, open(path_right, 'wb+') as disk_file_right:
        disk_file_left.write(await image_left.read())
        disk_file_right.write(await image_right.read())
        
    ocr_img_left, predict_img_left = ss.get_ocr_and_predict_images(path_left)
    ocr_img_right, predict_img_right = ss.get_ocr_and_predict_images(path_right)

    if ocr_img_left is None or predict_img_left is None or ocr_img_right is None or predict_img_right is None:
        return PlainTextResponse(content=sample_dmn, status_code=200)

    #drd_elements_left, drd_elements_right = None, None
    #tables_left, tables_right = [], []

    for idx, (ocr_img, predict_img, path, sketch_field, graph_field, elements_field, ocr_field, flow_field, decisionLogic_field) in enumerate(
        [(ocr_img_left, predict_img_left, path_left, 'sketchLeft', 'graphLeft', 'elementsLeft', 'ocrLeft', 'flowsLeft','decisionLogicLeft'), 
         (ocr_img_right, predict_img_right, path_right, 'sketchRight', 'graphRight', 'elementsRight', 'ocrRight', 'flowsRight','decisionLogicRight')], 
         start=1):
      if sketch_field in form and form[sketch_field] == 'true': 
        if graph_field in form and form[graph_field] == 'true':
            print(f"Converting image {idx} as a graph...")
            #drd_elements = None
            if elements_field in form and form[elements_field] == 'true':
                obj_predictions = ps.SketchPredictObject(predict_img)
                drd_elements = cs.convert_object_predictions(obj_predictions)

                if flow_field in form and form[flow_field] == 'true':
                    kp_predictions = ps.SketchPredictKeypoint(ocr_img)
                    requirements = cs.convert_keypoint_prediction(kp_predictions)
                    cs.connect_requirements(requirements, drd_elements)
                    cs.reference_requirements(requirements, drd_elements)
                    #drd_elements.extend(requirements)

                #if ocr_field in form and form[ocr_field] == 'true':
                #    text = os.get_text_from_img(ocr_img)
                #    os.link_text(text, drd_elements)

        #elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
        #    print(f"Converting image {idx} as a table...")
        #    if elements_field in form and form[elements_field] == 'true':
        #        table_predictions = ps.PredictTable(predict_img)
        #        converted_tables = cs.convert_table_predictions(table_predictions)
        #        ts_predictions = ps.PredictTableElement(predict_img)
        #        table_elements = cs.convert_tableElement_predictions(ts_predictions)

                
        #        if ocr_field in form and form[ocr_field] == 'true':
        #            text = os.get_text_from_table_img(ocr_img)
        #            os.link_text_table(text, table_elements) 

        #            tables = []
        #            table = Table 
        #            table_header = TableHeader
        #            table_hitPolicy = TableHitPolicy
        #            table_inputs = []
        #            table_outputs = []
        #            table_rules = []
        #            input_entries = []
        #            output_entries = []  

        #           for converted_table in converted_tables:
        #                if isinstance(converted_table, Table):
        #                   table = converted_table
        #            for table_element in table_elements:
        #                if isinstance(table_element, TableHeader):
        #                   table_header = table_element
        #                elif isinstance(table_element, TableHitPolicy):
        #                   table_hitPolicy = table_element
        #                elif isinstance(table_element, TableInput):
        #                   table_inputs.append(table_element)
        #                elif isinstance(table_element, TableOutput):
        #                   table_outputs.append(table_element)
        #                elif isinstance(table_element, TableRule):
        #                   table_rules.append(table_element)
        #                elif isinstance(table_element, InputEntry):
        #                   input_entries.append(table_element)
        #                elif isinstance(table_element, OutputEntry):
        #                   output_entries.append(table_element)
            
        #            table_rules = cs.connect_entries2rule(table_rules, input_entries, output_entries)               
        #            table_connect = cs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
        #            tables.append(table_connect) 
                
      else: 
        if graph_field in form and form[graph_field] == 'true':
            print(f"Converting image {idx} as a graph...")
            #drd_elements = None
            if elements_field in form and form[elements_field] == 'true':
                obj_predictions = ps.PredictObject(predict_img)
                drd_elements = cs.convert_object_predictions(obj_predictions)

                if flow_field in form and form[flow_field] == 'true':
                    kp_predictions = ps.PredictKeypoint(ocr_img)
                    requirements = cs.convert_keypoint_prediction(kp_predictions)
                    cs.connect_requirements(requirements, drd_elements)
                    cs.reference_requirements(requirements, drd_elements)
                    #drd_elements.extend(requirements)

                if ocr_field in form and form[ocr_field] == 'true':
                    text = os.get_text_from_img(ocr_img)
                    os.link_text(text, drd_elements)

            #if idx == 1:
            #    drd_elements_left = drd_elements
            #elif idx == 2:
            #    drd_elements_right = drd_elements

        elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
            print(f"Converting image {idx} as a table...")
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
    
                #if idx == 1:
                #    tables_left = tables 
                #elif idx == 2:
                #    tables_right = tables 
    elements_connect = cs.connect_graph2tables(drd_elements, tables)
    #if drd_elements_left is not None and tables_left is not None:
    #    elements_connect = cs.connect_graph2tables(drd_elements_left, tables_left)
    #    print('ok1')
    #elif drd_elements_left is not None and tables_right is not None:
    #    elements_connect = cs.connect_graph2tables(drd_elements_left, tables_right)
    #   print('ok2')
    #elif drd_elements_right is not None and tables_left is not None:
    #    elements_connect = cs.connect_graph2tables(drd_elements_right, tables_left)
    #    print('ok3')
    #elif drd_elements_right is not None and tables_right is not None:
    #    elements_connect = cs.connect_graph2tables(drd_elements_right, tables_right)
    #    print('ok4')

        
    dmn_diagram = DiagramFactory.create_element(elements_connect) 
    rendered_dmn_model = cs.render_diagram(dmn_diagram)
    print("XML representation of the DMN model:")
    print(rendered_dmn_model)
    
    return PlainTextResponse(content=rendered_dmn_model, status_code=200)
