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
    file = form.get('image')
    t = int(time.time_ns())
    path = here("../../temp_files/img_{}_{}".format(t, file.filename))
    with open(path, 'wb+') as disk_file:
        disk_file.write(await file.read())
    ocr_img, predict_img = ss.get_ocr_and_predict_images(path)

    if ocr_img is None or predict_img is None:
            return PlainTextResponse(content=sample_dmn, status_code=200)
    #i = 0 
    #for path, is_graph, is_table in zip(paths, graph, decisionLogic):
    #    i+=1
    #    print("Iteration:", i)
    if "graph" in form and form["graph"] == 'true':
            # Process the path as a graph
            print(f"Converting as a graph...")
            if "elements" in form and form["elements"] == 'true':
                # Process the path as a graph
                #print(f"Converting {path} as a graph...")
                obj_predictions = ps.PredictObject(predict_img)
                #print("obj_predictions:", obj_predictions)
                elements = cs.convert_object_predictions(obj_predictions)
                #print("elements:", elements)
            
                if "flows" in form and form["flows"] == 'true':
                   # Keypoints predictions
                   kp_predictions = ps.PredictKeypoint(ocr_img)
                   #print("kp_predictions:", kp_predictions)
                   requirements = cs.convert_keypoint_prediction(kp_predictions)
                   #print("requirements:", requirements)
                   cs.connect_requirements(requirements, elements)
                   cs.reference_requirements(requirements, elements)
                   elements.extend(requirements)

                if "ocr" in form and form["ocr"] == 'true':
                   # OCR
                   text = os.get_text_from_img(ocr_img)
                   os.link_text(text, elements)
                
                dmn_diagram = DiagramFactory.create_element(elements) ## elementsConnect
                rendered_dmn_model = cs.render_diagram(dmn_diagram)
                
            else:
                rendered_dmn_model = sample_dmn

    elif "decisionLogic" in form and form["decisionLogic"] == 'true':
            # Process the path as a table
            print(f"Converting as a table...")
            if "elements" in form and form["elements"] == 'true':
                table_predictions = ps.PredictTable(predict_img)
                #print("table_predictions:", table_predictions)
                ConvertedTables = cs.convert_table_predictions(table_predictions)
                ts_predictions = ps.PredictTableElement(predict_img)
                #print("ts_predictions:", ts_predictions)
                table_elements = cs.convert_tableElement_predictions(ts_predictions)
               
                # Link table elements together
                # Assign empty variables
                tables = []
                table = Table 
                table_header = TableHeader
                table_hitPolicy = TableHitPolicy
                table_inputs = []
                table_outputs = []
                table_rules = []
                input_entries = []
                output_entries = []   
                # Assign table element predictions to the variables
                for Convertedtable in ConvertedTables:
                    if isinstance(Convertedtable, Table):
                       table = Convertedtable
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
                    
                # Prints for checking
                #print("table:", table)
                #print("table_header:", table_header)
                #print("table_hitPolicy:", table_hitPolicy)
                #print("table_inputs:", table_inputs)
                #print("table_outputs:", table_outputs)
                #print("table_rules:", table_rules)
                #print("input_entries:", input_entries)
                #print("output_entries:", output_entries)  
            
                table_rules = cs.connect_entries2rule(table_rules, input_entries, output_entries)               
                tableConnect = cs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
                #print("table after connecting:", tableConnect)
                tables.append(tableConnect)
            
            
                if "ocr" in form and form["ocr"] == 'true':
                  # OCR 
                  text = os.get_text_from_table_img(ocr_img)
                  os.link_text_table(text, table_elements)
                  #print("table_elements after OCR:", table_elements)
            
                dmn_diagram = DiagramFactory.create_element(tables) ## elementsConnect
                rendered_dmn_model = cs.render_diagram(dmn_diagram)
            
            else:
                 rendered_dmn_model = sample_dmn
            
    #elementsConnect = cs.connect_graph2tables(elements, tables)
    #for element in elementsConnect:
    #    element_name = element.get_name()
    #    print("Elements name:", element_name)
    #for table in tables:
    #    if isinstance(table, Table):
    #        if isinstance(table_header, TableHeader):
    #            header_label = table.header.get_label()
    #            print("Table's header:", header_label)
    
    #dmn_diagram = DiagramFactory.create_element(elementsConnect) 
    #rendered_dmn_model = cs.render_diagram(dmn_diagram)
    
    return PlainTextResponse(content=rendered_dmn_model, status_code=200)

# At the moment, convert_image takes a file_path as argument, 
# Later, we should add request handling in the function
# At the moment, convert_image takes a file_path as argument, 
# Later, we should add request handling in the function

