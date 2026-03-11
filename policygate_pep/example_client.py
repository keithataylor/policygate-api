import policygate_pep.enforcer as enf

# Example input payload for customer defined endpoint. 
# This would normally be based on the actual data being processed by the service. 
payload = {
    "document_id": "123", 
    "env_name": "prod",
    "user_id": "456",
    "sensitivity": "restricted",
    "caller_trust": "low"
}

# Example URL (user defined) of the service endpoint that will handle the request and call the PEP enforcer.
# In this case, we assume the service is running locally on port 9000 and has an endpoint 
# for document summarisation at /summarise that accepts POST requests.
url = "http://localhost:9000/summarise"

# Use the post_json helper function from the enforcer module to send the request to the service endpoint.
response = enf.post_json(url=url, payload=payload, timeout=10)

print(F"Response: {response}")

