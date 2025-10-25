import requests, json

api_key = "3dSjaKpyDOMNioQeCnWhzVTNPCRfyE5OiSOB1704zHcGJvNTeRJ1CpaJAl18cUoj"

post_url = "https://api.agent.ai/v1/agent/kh2fyfmqponb9vhm/webhook/7dbe8317/async"
post_response = requests.post(post_url, headers={"x-api-key": api_key, "Content-Type": "application/json"})
run_id = post_response.json().get("run_id")

get_url = "https://api.agent.ai/v1/agent/kh2fyfmqponb9vhm/webhook/7dbe8317/status"
get_response = requests.get(f"{get_url}/{run_id}", headers={"x-api-key": api_key, "Content-Type": "application/json"})


if get_response.status_code == 200:
        response = get_response.json().get("response")

elif get_response.status_code == 204:
        response = get_response.json().get("message")


