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
    tables = [] 
    #for path, is_graph, is_table in zip(paths, graph, decisionLogic):
    #    i+=1
    #    print("Iteration:", i)
    if "graph" in form and form["graph"] == 'true':
            # Process the path as a graph
            #print(f"Converting {path} as a graph...")
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
            
    elif "decisionLogic" in form and form["decisionLogic"] == 'true':
            # Process the path as a table
            # print(f"Converting {path} as a table...")
            if "elements" in form and form["elements"] == 'true':
               table_predictions = ps.PredictTable(predict_img)
               #print("table_predictions:", table_predictions)
               ConvertedTables = cs.convert_table_predictions(table_predictions)
               ts_predictions = ps.PredictTableElement(predict_img)
               #print("ts_predictions:", ts_predictions)
               table_elements = cs.convert_tableElement_predictions(ts_predictions)
            
            if "ocr" in form and form["ocr"] == 'true':
               # OCR 
               text = os.get_text_from_table_img(ocr_img)
               os.link_text_table(text, table_elements)
               #print("table_elements after OCR:", table_elements)
            
            # Link table elements together
            # Assign empty variables
            #table = Table 
            #table_header = TableHeader
            #table_hitPolicy = TableHitPolicy
            #table_inputs = []
            #table_outputs = []
            #table_rules = []
            #input_entries = []
            #output_entries = []   
            # Assign table element predictions to the variables
            #for Convertedtable in ConvertedTables:
            #     if isinstance(Convertedtable, Table):
            #        table = Convertedtable
            #for table_element in table_elements:
            #    if isinstance(table_element, TableHeader):
            #        table_header = table_element
            #    elif isinstance(table_element, TableHitPolicy):
            #        table_hitPolicy = table_element
            #    elif isinstance(table_element, TableInput):
            #        table_inputs.append(table_element)
            #    elif isinstance(table_element, TableOutput):
            #        table_outputs.append(table_element)
            #    elif isinstance(table_element, TableRule):
            #        table_rules.append(table_element)
            #    elif isinstance(table_element, InputEntry):
            #       input_entries.append(table_element)
            #    elif isinstance(table_element, OutputEntry):
            #        output_entries.append(table_element)
                    
            # Prints for checking
            #print("table:", table)
            #print("table_header:", table_header)
            #print("table_hitPolicy:", table_hitPolicy)
            #print("table_inputs:", table_inputs)
            #print("table_outputs:", table_outputs)
            #print("table_rules:", table_rules)
            #print("input_entries:", input_entries)
            #print("output_entries:", output_entries)  
            
            #table_rules = cs.connect_entries2rule(table_rules, input_entries, output_entries)               
            #tableConnect = cs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
            #print("table after connecting:", tableConnect)
            #tables.append(tableConnect)
            
        #else:
            # Handle other cases, if necessary
            #print(f"No specific conversion for {path}")
            
    #elementsConnect = cs.connect_graph2tables(elements, tables)
    #for element in elementsConnect:
    #    element_name = element.get_name()
    #    print("Elements name:", element_name)
    #for table in tables:
    #    if isinstance(table, Table):
    #        if isinstance(table_header, TableHeader):
    #            header_label = table.header.get_label()
    #            print("Table's header:", header_label)
    
    dmn_diagram = DiagramFactory.create_element(element) ## elementsConnect
    rendered_dmn_model = cs.render_diagram(dmn_diagram)
    
    return rendered_dmn_model

# At the moment, convert_image takes a file_path as argument, 
# Later, we should add request handling in the function
# At the moment, convert_image takes a file_path as argument, 
# Later, we should add request handling in the function

#
    """Post method to manage the conversion of images to their corresponding
    dmn models
    There should be max one graph
    
    Parameters
    ----------
    paths: List
        List of path to the images to be converted
    graph: List
        List of flags indicating whether the image is a graph or not
    decisionLogic: List
        List of flags indicating whether the image is a graph or not
    
    Returns
    -------
    str
        The converted dmn model
    """
    i = 0
    tables = [] 
    for path, is_graph, is_table in zip(paths, graph, decisionLogic):
        i+=1
        print("Iteration:", i)
        if is_graph:
            # Process the path as a graph
            print(f"Converting {path} as a graph...")
            
            ocr_img, predict_img = ss.get_ocr_and_predict_images(path)
            print("ocr_img:",ocr_img)
            print("predict_img:", predict_img)
            
            if ocr_img is None or predict_img is None:
                print("ocr_img or predict_img is None")
                return sample_dmn
            
            # Elements predictions
            obj_predictions = ps.PredictObject(predict_img)
            print("obj_predictions:", obj_predictions)
            elements = cs.convert_object_predictions(obj_predictions)
            print("elements:", elements)
            
            # Keypoints predictions
            kp_predictions = ps.PredictKeypoint(ocr_img)
            print("kp_predictions:", kp_predictions)
            requirements = cs.convert_keypoint_prediction(kp_predictions)
            print("requirements:", requirements)
            cs.connect_requirements(requirements, elements)
            cs.reference_requirements(requirements, elements)

            # OCR
            text = os.get_text_from_img(ocr_img)
            os.link_text(text, elements)
            
        elif is_table:
            # Process the path as a table
            print(f"Converting {path} as a table...")
            
            ocr_img, predict_img = ss.get_ocr_and_predict_images(path)
            print("ocr_img:",ocr_img)
            print("predict_img:", predict_img)
            
            if ocr_img is None or predict_img is None:
                print("ocr_img or predict_img is None")
                return sample_dmn

            table_predictions = ps.PredictTable(predict_img)
            print("table_predictions:", table_predictions)
            ConvertedTables = cs.convert_table_predictions(table_predictions)
            ts_predictions = ps.PredictTableElement(predict_img)
            print("ts_predictions:", ts_predictions)
            table_elements = cs.convert_tableElement_predictions(ts_predictions)
            
            # OCR 
            text = os.get_text_from_table_img(ocr_img)
            os.link_text_table(text, table_elements)
            print("table_elements after OCR:", table_elements)
            
            # Link table elements together
            # Assign empty variables
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
            print("table:", table)
            print("table_header:", table_header)
            print("table_hitPolicy:", table_hitPolicy)
            print("table_inputs:", table_inputs)
            print("table_outputs:", table_outputs)
            print("table_rules:", table_rules)
            print("input_entries:", input_entries)
            print("output_entries:", output_entries)  
            
            table_rules = cs.connect_entries2rule(table_rules, input_entries, output_entries)               
            tableConnect = cs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
            print("table after connecting:", tableConnect)
            tables.append(tableConnect)
            
        else:
            # Handle other cases, if necessary
            print(f"No specific conversion for {path}")
            
    elementsConnect = cs.connect_graph2tables(elements, tables)
    for element in elementsConnect:
        element_name = element.get_name()
        print("Elements name:", element_name)
    for table in tables:
        if isinstance(table, Table):
            if isinstance(table_header, TableHeader):
                header_label = table.header.get_label()
                print("Table's header:", header_label)
    
    dmn_diagram = DiagramFactory.create_element(elementsConnect)
    rendered_dmn_model = cs.render_diagram(dmn_diagram)
    
    return rendered_dmn_model


"""
def convert_image(path, elements=True, requirements=True, ocr=True, tables=True):
    Post method to manage the conversion of an image to its corresponding
    dmn model. The request should contains form fields that tells whether
    elements detection, flow detection and OCR should be performed on the images

    Returns
    -------
    str
        The converted bpmn model
            
    ocr_img, predict_img = ss.get_ocr_and_predict_images(path)
    print("ocr_img:",ocr_img)
    print("predict_img:", predict_img)

    if ocr_img is None or predict_img is None:
        print ("ocr_img or predict_img is None")
        return sample_dmn

    if elements is True:
        obj_predictions = ps.PredictObject(predict_img)
        print("obj_predictions:", obj_predictions)
        elements = cs.convert_object_predictions(obj_predictions)
        print("elements:", elements)

        if requirements is True:
            kp_predictions = ps.PredictKeypoint(ocr_img)
            print("kp_predictions:", kp_predictions)
            requirements = cs.convert_keypoint_prediction(kp_predictions)
            print("requirements:", requirements)
            cs.connect_requirements(requirements, elements)
            cs.reference_requirements(requirements, elements)
            # cs.connect_textAnnotations -> To add later

        if ocr is True:
            text = os.get_text_from_img(ocr_img)
            os.link_text(text, elements)
            
    else:
        rendered_dmn_model = sample_dmn
        print("elements is not True")
            
    if tables is True:
        ts_predictions = ps.PredictTableElement(predict_img)
        print("tabel_predictions:", ts_predictions)
        table_elements = cs.convert_tableElement_predictions(ts_predictions)
        print("table_elements 1:", table_elements)
        table_elements = cs.connect_components2table(ts_predictions)
        print("table_elements 2:", table_elements)
        table_elements = cs.connect_entries2rule(ts_predictions)
        print("table_elements 3:", table_elements)
            
        if ocr is True:
            text = os.get_text_from_img(ocr_img)
            os.link_text(text, elements)
            
        cs.connect_graph2table(elements, table_elements)
            
    else:
        rendered_dmn_model = sample_dmn
            

    dmn_diagram = DiagramFactory.create_element(elements)
    rendered_dmn_model = cs.render_diagram2(dmn_diagram)
    
    return rendered_dmn_model"""
