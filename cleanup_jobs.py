import json
import requests
import config
from pprint import pprint


# Set up the API endpoint and authentication
headers = {"content-type": "application/json",}
list_jobs_payload = {"auth": {"organization": config.ORGANIZATION}}

headers.update(config.AUTH)

response = requests.post(
    f"{config.BASE_STUDIO_URL}/ListFinetuneJobs",
    headers=headers,
    data=json.dumps(list_jobs_payload),
)

all_benchmark_jobs = []

# Print the response status code
print(response.status_code)
for result in response.json()["jobs"]:
    if "name" in result.keys():
        if result["name"].split("/")[0] == config.BENCHMARK_PREFIX:
            print(f"Found a job to delete => {result['id']}, {result['name']}, {result['status']}")
            all_benchmark_jobs.append(result)

print(f"Are you sure you want to delete the above {len(all_benchmark_jobs)} jobs strating with '{config.BENCHMARK_PREFIX}'?")
print("Press 'y' to confirm or 'n' to cancel")

confirmation = input()

if confirmation == "y":
    for job in all_benchmark_jobs:
        print(f"Deleting job {job['name']}")
        delete_job_payload = {
            "auth": {"organization": config.ORGANIZATION},
            "id": job["id"],
        }
        response = requests.post(
            f"{config.BASE_STUDIO_URL}/DeleteFinetuneJob",
            headers=headers,
            data=json.dumps(delete_job_payload),
        )
        print("Status =>", response.status_code, response.text)
        print(f"Deleted job!")
else:
    print("Cancelled")
