import time
from DMNVisionTool_backend.api.services import preprocessing_service as pps
from DMNVisionTool_backend.api.services import sketch_preprocessing_service as spps
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from DMNVisionTool_backend.api.services import (
    predict_service as ps,
    sketch_predict_service as sps,
    ocr_service as os,
    sketch_ocr_service as sos,
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
        
        # Classification
        for idx, (path, sketch_field, digital_field, graph_field,  decisionLogic_field) in enumerate(
                [(path_left, 'sketchLeft', 'DigitalLeft', 'graphLeft', 'decisionLogicLeft'), 
                 (path_right, 'sketchRight', 'DigitalRight', 'graphRight', 'decisionLogicRight')], 
                start=0):
                print("Processsing image idx:", idx)
                
                # HANDWRITTEN 
                if sketch_field in form and form[sketch_field] == 'true':
                        print('Processing image as a sketch')
                        # HANDWRITTEN DRD
                        if graph_field in form and form[graph_field] == 'true':
                                ocr_img_sketch, predict_img_sketch = spps.get_ocr_and_predict_images(path)
                                
                                print(f"Converting image {idx} as a graph sketch...")
                                obj_predictions = sps.SketchPredictObject(predict_img_sketch)
                                drd_elements = scs.convert_object_predictions(obj_predictions)
                        
                                kp_predictions = sps.SketchPredictKeypoint(predict_img_sketch)
                                requirements = scs.convert_keypoint_prediction(kp_predictions)
                                scs.connect_requirements(requirements, drd_elements)
                                scs.reference_requirements(requirements, drd_elements)
                     
                                text = sos.get_text_from_img(ocr_img_sketch,obj_predictions)
                                sos.link_text(text, drd_elements)
                                # drd_elements= sos.get_text_from_img(ocr_img_sketch,drd_elements)

                        # HANDWRITTEN + DECISION TABLE
                        elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
                                ocr_img_sketch, predict_img_sketch = spps.get_ocr_and_predict_images(path)
                                
                                print(f"Converting image {idx} as a sketch table...")
                        
                                table_element_predictions = sps.SketchPredictTable(predict_img_sketch)
                                table_elements = scs.convert_table_object_predictions(table_element_predictions)
                                
                                text = sos.get_text_from_table_img_sketch(ocr_img_sketch,table_element_predictions)
                                sos.link_text_table(text, table_elements)
            
                                tables = []
                                table = Table 
                                table_header = TableHeader
                                table_hitPolicy = TableHitPolicy
                                table_inputs = []
                                table_outputs = []
                                table_rules = []
                                input_entries = []
                                output_entries = []
                                
                                # OR add here empty elements if there is none? 
                                for table_element in table_elements:
                                        if isinstance(table_element, Table):
                                                table = table_element
                                                print("CR - There is a table")
                                        elif isinstance(table_element, TableHeader):
                                                table_header = table_element
                                                print("CR - There is a header")
                                        elif isinstance(table_element, TableHitPolicy):
                                                table_hitPolicy = table_element
                                                print("CR - There is a hitpolicy")
                                        elif isinstance(table_element, TableInput):
                                                table_inputs.append(table_element)
                                                print("CR - There is a input")
                                        elif isinstance(table_element, TableOutput):
                                                table_outputs.append(table_element)
                                                print("CR - There is a output")
                                        elif isinstance(table_element, TableRule):
                                                table_rules.append(table_element)
                                                print("CR - There is a rule")
                                        elif isinstance(table_element, InputEntry):
                                                input_entries.append(table_element)
                                                print("CR - There is a input entry")
                                        elif isinstance(table_element, OutputEntry):
                                                output_entries.append(table_element)
                                                print("CR - There is a output entry")
                                                
                                scs.create_extra_table_elements(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules, input_entries, output_entries)
            
                                table_rules = scs.connect_entries2rule(table_rules, input_entries, output_entries)
                                table_connect = scs.connect_components2table(table, table_header, table_hitPolicy, table_inputs, table_outputs, table_rules)
                                tables.append(table_connect)
            
                                elements_connect = scs.connect_graph2tables(drd_elements, tables)
     
                                dmn_diagram = DiagramFactorySketches.create_element(elements_connect) 
                                rendered_dmn_model = scs.render_diagram(dmn_diagram)
                                print("XML representation of the DMN model:")
                                print(rendered_dmn_model)
                        
                # DIGITAL  
                elif digital_field in form and form[digital_field] == 'true':
                        # DIGITAL + DRD
                        if graph_field in form and form[graph_field] == 'true':
                                ocr_img_pdf, predict_img_pdf = pps.get_ocr_and_predict_images(path)
                        
                                print(f"Converting image {idx} as a digital graph...")
                                obj_predictions = ps.PredictObject(predict_img_pdf)
                                drd_elements = cs.convert_object_predictions(obj_predictions)

                                kp_predictions = ps.PredictKeypoint(predict_img_pdf)
                                requirements = cs.convert_keypoint_prediction(kp_predictions)
                                scs.connect_requirements(requirements, drd_elements)
                                scs.reference_requirements(requirements, drd_elements)

                                text = os.get_text_from_img(ocr_img_pdf,obj_predictions)
                                os.link_text(text, drd_elements)

                        # DIGITAL + TABLE
                        elif decisionLogic_field in form and form[decisionLogic_field] == 'true':
                                ocr_img_pdf, predict_img_pdf = pps.get_ocr_and_predict_images(path)
                        
                                print(f"Converting image {idx} as a digital decision table...")
                        
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

        return PlainTextResponse(content=rendered_dmn_model, status_code=200)