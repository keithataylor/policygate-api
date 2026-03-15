from time import time

from fastapi import Response

import policygate_pep.enforcer as enforcer

# Example input payload for customer defined endpoint. 
# This would normally be based on the actual data being processed by the service. 
summarise_payload = {"document_id": "123"}

# Example URL (customer-defined) of the service endpoint that will call the PEP enforcer.
# In this case, we assume the customer service is running locally on port 9000, 
# with ML inference endpoint for document summarisation at /summarise.
client_endpoint_url = "http://127.0.0.1:9000/summarise"

# Use the post_json helper function from the enforcer module to send the request to the service endpoint.
response = enforcer.post_json(url=client_endpoint_url, payload=summarise_payload, timeout=10)

print(f"Status code: {response.status_code}, Reason: {response.reason}, Response: {response.json()}")   
