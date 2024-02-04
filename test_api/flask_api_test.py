import requests
import json

# API endpoint URL
url = "https://hackviolet-api-5cbt6nlbxq-uk.a.run.app/match"
# url = "https://hackviolet-api-5cbt6nlbxq-uk.a.run.app/book"

# Request headers
headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "X-Request-Id": "123456789"
}

# Request payload
payload = {
    'username': 'jdoe',
    'hours': '8 am to 11 am'
    # 'provider_id': 'awhite',
    # 'date': 'today',
    # 'start_time': '9 AM',
    # 'end_time': '11 AM'
}

json_payload = json.dumps(payload)


print("sending post")
# Send POST request
response = requests.request("POST", url, headers=headers, data=json_payload)

# Check response status code
if response.status_code == 200:
    # Request successful
    print(response.json())
else:
    # Request failed
    print("Request failed with status code:", response)


# """
# curl -X POST "https://kbase-api-esp-pohgsp7pwa-uk.a.run.app/v1/services/kbase_opensai_search" \
#   -H "Content-Type: application/json" \
#   -H "X-Request-Id: 123456789" \
#   -H "Authorization: Bearer eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJSUzI1NiIsICJraWQiOiAiM2JmMzNmY2Y3ZjgzODZkMzZlZGFmMDUxMzA0N2RhYWJhZWM1NTgzMCJ9.eyJpYXQiOiAxNjg3MzY0NDkxLCAiZXhwIjogMTcxODkwMDQ5MSwgImlzcyI6ICJzYS1qd3RAaG5zLW1sLXZvaWNlLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwgImF1ZCI6ICJodHRwczovL2tiYXNlLWFwaS1lc3AtcG9oZ3NwN3B3YS11ay5hLnJ1bi5hcHAiLCAic3ViIjogInNhLWp3dEBobnMtbWwtdm9pY2UuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAiZW1haWwiOiAic2Etand0QGhucy1tbC12b2ljZS5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSJ9.kqkD-JbaEPMsKngfarlVhURLnKMXAd7m4fy3XxJJWdg1WgHk2VU98YwfZX-kQmN-l1oCJNemF_m4KWqjJRcdC3QXZiVV6IGLWn8bl_-jd7IHWOvjdHbnf_WZLbSiXOJjBb9SFBuedPQTbKAN-uc-FMsaB75ac1lxkmJ0p2bv6KfnnzTluhg6gVrK4sfhUTLkcPmZj7pq-2NAxWt2B9GWO-tZYg--nGiwqk1f5cqd6jmEQadwlsp2MlYjy5Q4aPH6DNoTsTxLcJMv5A2ST1T4AIHDG6DaAAoS7ZE_QJc9PFBjpH4FWd0WK92T94iakbbwwty5G48dx0JINUvmpko7eQ" \
#   -d '{
#     "requestData": {
#         "query": "How to install a trimast on a wooden roof?",
#         "application": "IP_FIELD_SERVICES",
#         "version": "1",
#         "env": "dev",
#         "alpha": "0.5"
#     }
# }'


# curl -X POST "https://compute.googleapis.com/compute/v1/projects/hns-ml-voice/zones/us-east1-c/instances/tmp2-casenotes-history-job-vm/stop"
# """


# url = "https://compute.googleapis.com/compute/v1/projects/hns-ml-voice/zones/us-east1-c/instances/tmp2-casenotes-history-job-vm/stop"

# response = requests.request("POST", url)