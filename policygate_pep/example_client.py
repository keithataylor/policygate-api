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

# The response from the service endpoint detailing the PDP decision and information of PEP enforcement taken.
obligations = ""
if( response.get('obligations') and len(response['obligations'][0]) > 0):
    obligations = response['obligations'][0]

# Certain response fields such as obligations may be optional and not always returned by the PDP, 
# so we check for their presence before trying to access them.
if( obligations and len(obligations) > 0):
    obligations = response['obligations'][0].get('type')
    if( response['obligations'][0].get('params') and response['obligations'][0].get('params').get('max_tokens') ):
        obligations += "; MaxTokens: " + str(response['obligations'][0].get('params')['max_tokens'])
else:
    obligations = "None"

print(f"Decision handled for: {response['decision']},\nMessage: {response['message']},\nObligations: {obligations}")
