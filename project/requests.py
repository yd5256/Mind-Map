import requests, json

api_key = #
agent_url = #
run_id = requests.post(agent_url)


get_response = requests.get(f"{agent_url}/{run_id.text}", headers={"x-api-key": api_key})


if (get_response.status_code == 200): 
        response = get_response.response

elif (get_response.status_code == 204):
        response = get_response.message


