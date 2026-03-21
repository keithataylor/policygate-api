from time import perf_counter, time

from policygate.models import Decision
import requests
from typing import Any, Callable
from policygate.models import EvaluateResponseV1, Decision


def post_json(url: str, payload: dict, timeout: int = 10) -> requests.Response:
    '''
    Helper function to send a POST request with JSON payload and return the response as a dictionary.
    Args:
        url (str): The URL to send the POST request to.
        payload (dict): The JSON payload to include in the POST request.
        timeout (int): The timeout for the request in seconds. Default is 10 seconds. 
        Returns: dict: The JSON response from the server as a dictionary.
        Raises: requests.exceptions.RequestException: If an error occurs while making the request.
    '''
    try:
        with requests.Session() as session:
            start = perf_counter()
            summarise_response = session.post(url=url, json=payload, timeout=timeout)
            end = perf_counter()
            print(f"session.post in post_json to {url} took {end - start:.2f} seconds")
            summarise_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request to the PEP: {e}")
        raise SystemExit(1)

    return summarise_response



# Enforcer function to call the PDP and route to the correct handler based on the decision.
def enforce(
    *,
    evaluate_request: dict[str, Any],
    pdp_url: str,
    on_allow: Callable[[EvaluateResponseV1], Any],
    on_degrade: Callable[[EvaluateResponseV1], Any],
    on_block: Callable[[EvaluateResponseV1], Any],
    on_require_review: Callable[[EvaluateResponseV1], Any],
    timeout_seconds: float = 5.0,
) -> Any:
    """
    Call the PDP /evaluate endpoint, validate the response, and route to the
    correct handler based on the returned decision.

    The handlers are supplied by the calling PEP/service code.

    Parameters
    ----------
    evaluate_request:
        Plain dict payload to POST to the PDP /evaluate endpoint.
    pdp_url:
        Full PDP evaluate endpoint URL, e.g. 'http://localhost:8000/evaluate'.
    on_allow:
        Handler for Decision.ALLOW.
    on_degrade:
        Handler for Decision.DEGRADE.
    on_block:
        Handler for Decision.BLOCK.
    on_require_review:
        Handler for Decision.REQUIRE_REVIEW.
    timeout_seconds:
        Requests timeout for the PDP call.

    Returns
    -------
    Any
        Whatever the selected handler returns.

    Raises
    ------
    requests.exceptions.RequestException
        If the HTTP request to the PDP fails.
    ValueError
        If the PDP response is invalid or contains an unknown decision.
    """

    try:
        with requests.Session() as session:
            start = perf_counter()
            response = session.post(
                url=pdp_url,
                json=evaluate_request,
                timeout=timeout_seconds,
            )
            end = perf_counter()
            print(f"Timer: session.post in enforce to {pdp_url} took {end - start:.2f} seconds")
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"Failed to call PDP at '{pdp_url}': {e}"
        ) from e

    try:
        response_json = response.json()
    except ValueError as e:
        raise ValueError(
            f"PDP returned a non-JSON response from '{pdp_url}'."
        ) from e

    try:
        decision_response = EvaluateResponseV1.model_validate(response_json)
    except Exception as e:
        raise ValueError(
            f"PDP response failed schema validation: {e}"
        ) from e

    if decision_response.decision == Decision.ALLOW:
        return on_allow(decision_response)

    if decision_response.decision == Decision.DEGRADE:
        return on_degrade(decision_response)

    if decision_response.decision == Decision.BLOCK:
        return on_block(decision_response)

    if decision_response.decision == Decision.REQUIRE_REVIEW:
        return on_require_review(decision_response)

    raise ValueError(
        f"Unsupported decision returned by PDP: {decision_response.decision}"
    )

