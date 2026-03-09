from pydantic import BaseModel

from policygate.models import Decision
import requests

def decision_allow_handler():
    print("This is a placeholder for handling ALLOW decisions.")

def decision_block_handler():
    print("This is a placeholder for handling BLOCK decisions.")

def decision_require_review_handler():
    print("This is a placeholder for handling REQUIRE_REVIEW decisions.")

def decision_degrade_handler():
    print("This is a placeholder for handling DEGRADE decisions.")


# This is a simple demonstration of how a client application might interact with the PEP and PDP services.

class SummariseBody(BaseModel):
    document_id: str
    env_name: str
    user_id: str | None = None
    sensitivity: str
    caller_trust: str | None = None

summarise = SummariseBody(
    document_id="123",
    env_name="development",
    user_id="456",
    sensitivity="public",
    caller_trust="low"
)   

with requests.Session() as session: 
    summarise_response = session.post(url="http://localhost:9000/summarise", json=summarise.model_dump())  # Use model_dump() to convert Pydantic model to dict


print(f"Response status code: {summarise_response.status_code}, {summarise_response.reason}") 

decision = Decision(summarise_response.json()["decision"])

print(f"Response Decision: {decision}") 

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



