import requests, json
from time import sleep

api_key = "3dSjaKpyDOMNioQeCnWhzVTNPCRfyE5OiSOB1704zHcGJvNTeRJ1CpaJAl18cUoj"
post_url = "https://api.agent.ai/v1/agent/kh2fyfmqponb9vhm/webhook/7dbe8317/async"
get_url = "https://api.agent.ai/v1/agent/kh2fyfmqponb9vhm/webhook/7dbe8317/status"

def post_and_grab_id(url, big_idea, num_branches):
    the_input = {"big_idea" : big_idea, "num_small" : num_branches}
    # could also be data= for form data
    post_response = requests.post(url, json=the_input, headers={"x-api-key": api_key, "Content-Type": "application/json"})
    run_id = post_response.json().get("run_id")
    return run_id

def get_response_until_complete(url, run_id):
    get_response = requests.get(f"{url}/{run_id}",
                                headers={"x-api-key": api_key, "Content-Type": "application/json"})
    timeout = 0
    while (get_response.status_code == 204) | (timeout < 300):
        timeout += 1
        sleep(0.1)
    if get_response.status_code != 200:
        response = "Timeout reached. No response received."
    else:
        response = get_response.json().get("response")
    return response

while True:
    run_id = post_and_grab_id(post_url, "Create a mind map for learning Python programming", 5)
    final_response = get_response_until_complete(get_url, run_id)
    print(final_response)
    sleep(30)  # Pause for half a minute before the next iteration