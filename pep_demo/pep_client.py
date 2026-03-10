####################################################################################################################
#   pep_client.py 
#   Simple demonstration to show how a client application might interact with the PEP and PDP services. 
#   The input is hardcoded for demonstration purposes, but in a real application, inputs would likely come 
#   from the application's context, user input, or other sources.
#   Here we assume a user is trying to summarise a document, and we want to evaluate the policy for that action.
#   The client sends a request to the PEP, which forwards it to the PDP for evaluation. The PDP returns a decision,
#   and the client handles that decision accordingly.
#######################################################################################################################
from pydantic import BaseModel
from policygate.models import Decision
import requests

# Simple Pydantic model to represent the request body for the summarise endpoint. 
# In a real application, this would likely be more complex and include additional fields as needed.
class SummariseBody(BaseModel):
    document_id: str
    env_name: str
    user_id: str | None = None
    sensitivity: str
    caller_trust: str | None = None

# For demonstration purposes, we will hardcode the input values.
summarise = SummariseBody(
    document_id="123",
    env_name="development",
    user_id="456",
    sensitivity="public",
    caller_trust="low"
)   

# Call the PEP's summarise endpoint with the input data. The PEP will forward this to the PDP for evaluation.
# http://localhost:9000/summarise simulates the PEP's endpoint for handling summarisation requests. 
# In a real application, this would be the actual URL of the PEP service.
try:
    with requests.Session() as session:
        summarise_response = session.post(
            "http://localhost:9000/summarise",
            json=summarise.model_dump(),
            timeout=10,
        )
        summarise_response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request to the PEP: {e}")
    raise SystemExit(1)



print(f"Response status code: {summarise_response.status_code}, {summarise_response.reason}") 

decision = Decision(summarise_response.json()["decision"])

print(f"Response Decision: {decision}") 


def decision_allow_handler():
    print("This is a placeholder for handling ALLOW decisions.")

def decision_block_handler():
    print("This is a placeholder for handling BLOCK decisions.")

def decision_require_review_handler():
    print("This is a placeholder for handling REQUIRE_REVIEW decisions.")

def decision_degrade_handler():
    print("This is a placeholder for handling DEGRADE decisions.")


match decision:
    case Decision.ALLOW:
        decision_allow_handler()
    case Decision.BLOCK:   
        decision_block_handler()
    case Decision.REQUIRE_REVIEW:
        decision_require_review_handler()  
    case Decision.DEGRADE:
        decision_degrade_handler()
    case _:
        print("Received unknown decision from policy evaluation. This should NOT be possible if the API is working correctly.")



