from time import time

import policygate_pep.enforcer as enforcer

# Example input payload for customer defined endpoint. 
# This would normally be based on the actual data being processed by the service. 
payload = {
    "document_id": "123", 
    "env_name": "development",
    "user_id": "789",
    "sensitivity": "public",
    "caller_trust": "low"
}

# Example URL (customer-defined) of the service endpoint that will call the PEP enforcer.
# In this case, we assume the customer service is running locally on port 9000, 
# with ML inference endpoint for document summarisation at /summarise.
client_endpoint_url = "http://127.0.0.1:9000/summarise"

start = time()
# Use the post_json helper function from the enforcer module to send the request to the service endpoint.
response = enforcer.post_json(url=client_endpoint_url, payload=payload, timeout=10)

end = time()
print(f"PEP client enforcer.post_json call to: {client_endpoint_url} took: {end - start:.2f}seconds")   
print(F"Response: {response}")

