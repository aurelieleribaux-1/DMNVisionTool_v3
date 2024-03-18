import requests

def deploy_dmn_model(xml_content):
    # Camunda REST API endpoint for deploying a DMN model
    camunda_api_url = "http://localhost:8080/engine-rest/deployment/create"

    # Headers specifying content type
    headers = {"Content-Type": "application/json"}

    # Body of the POST request containing the DMN model XML content
    payload = {
        "deployment-name": "My_DMN_Model_Deployment",
        "enable-duplicate-filtering": True,
        "deploy-changed-only": False,
        "deployment-source": "Local deployment",
        "files": {
            "dmn_model.dmn": {
                "content": xml_content
            }
        }
    }

    try:
        # Send POST request to Camunda REST API
        response = requests.post(camunda_api_url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("DMN model deployed successfully.")
        else:
            print(f"Failed to deploy DMN model. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error deploying DMN model: {e}")

# Assume 'rendered_dmn_model' contains the XML content of the DMN model
deploy_dmn_model(rendered_dmn_model)
