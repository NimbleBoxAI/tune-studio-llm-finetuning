import json
import requests
import datetime
from pprint import pprint
import config

# Set up the API endpoint and authentication
headers = {"content-type": "application/json"}
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
            if result["status"] == "COMPLETED":
                ### Get results
                print(
                    "Found the job =>",
                    result["id"],
                    result["name"],
                    result["status"],
                    result["createdAt"],
                    result["updatedAt"],
                    result["meta"]["metadata"]["training_config"]["wandb_run_id"],
                    result["meta"]["metadata"]['training_config']['micro_batch_size'],
                    result["meta"]["metadata"]['training_config']['gradient_accumulation_steps'],
                )

                logs = []
                next_page_token = None
                count = 0

                while True:
                    get_logs_payload = {
                        "auth": {"organization": config.ORGANIZATION},
                        "resourceId": result["id"],
                        "type": "LOG_TYPE_JOB",
                        "page": {"limit": 70},
                    }

                    if next_page_token is not None:
                        get_logs_payload["page"]["prevPageToken"] = next_page_token

                    # print("get_logs_payload", get_logs_payload)

                    logs_response = requests.post(
                        f"{config.BASE_STUDIO_URL}/GetLog",
                        headers=headers,
                        data=json.dumps(get_logs_payload),
                    )

                    if logs_response.status_code !=200 or "log" not in logs_response.json():
                        print("Error in fetching logs", logs_response.status_code, logs_response.text)
                        break

                    # print("next_page_token", logs_response.json()["page"])
                    logs.extend(logs_response.json()["log"])
                    # print("next_page_token", next_page_token)

                    next_page_token = logs_response.json()["page"]["prevPageToken"]
                    count += 1

                print("====== total_logs", len(logs))
                print("====== Total pages", count)
                logs = sorted(logs, key=lambda x: x["timestamp"])

                ### Parse results
                data = {
                    # config
                    "config/id": result["id"],
                    "config/name": result["name"],
                    "config/base_model_id": result["meta"]["metadata"]["base_model_id"],
                    "config/gpu": result["resource"]["gpu"],
                    "config/gpuCount": result["resource"]["gpuCount"],
                    "config/dataset": result["meta"]["metadata"]["training_config"]["datasets"][0]["path"],
                    "config/wandb_runid": result["meta"]["metadata"]["training_config"]["wandb_run_id"],
                    "config/micro_batch_size": result["meta"]["metadata"]["training_config"]["micro_batch_size"],
                    "config/gradient_accumulation_steps": result["meta"]["metadata"]["training_config"]["gradient_accumulation_steps"],
                    # train data
                    "train/epoch": None,  # number of epochs
                    "train/global_step": None,  # number of steps
                    "train/train_samples_per_second": None,
                    "train/train_steps_per_second": None,
                    # eval data
                    # "eval/eval_samples_per_second": None,
                    # "eval/eval_steps_per_second": None,
                    # all time related
                    "infra/createdAt": datetime.datetime.strptime(result["createdAt"].split(".")[0].replace('Z',''), "%Y-%m-%dT%H:%M:%S"),  # when job scheduled
                    "infra/startedAt": datetime.datetime.strptime(result["startedAt"].split(".")[0].replace('Z',''), "%Y-%m-%dT%H:%M:%S"),  # when pod started; in format '2024-02-09T10:52:26.941420545Z'
                    "job_log/start_time": None,  # init-container start time
                    "job_log/first_loss_time": None,  # timestamp for first {'loss'... log
                    "job_log/last_loss_time": None,  # timestamp for train_runtime
                    # "upload/startedAt": None,  # when upload started
                    # "upload/finishedAt": None,  # when upload finished
                    "job_log/end_time": None,  # termination helper
                    "infra/finishedAt": datetime.datetime.strptime(result["finishedAt"].split(".")[0], "%Y-%m-%dT%H:%M:%S"),  # story ends; in format '2024-02-09T10:52:26.941420545Z'
                }

                # parse name to find the parameters

                # parse job start and end time
                data["job_log/start_time"] = datetime.datetime.strptime(logs[0]["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")  # in format '2024-02-09T10:51:12.674849Z'
                data["job_log/end_time"] = datetime.datetime.strptime(logs[-1]["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")  # in format '2024-02-09T10:51:12.674849Z'

                # parse wandb logs
                # remove everything from logs before the message "wandb: Run summary:"
                wandb_logs = logs[
                    logs.index(
                        next(
                            log
                            for log in logs
                            if "message" in log.keys()
                            and "wandb: Run summary:" in log["message"]
                        )
                    ) :
                ]

                for log in wandb_logs:
                    if "message" in log.keys():
                        if "wandb" in log["message"] and "train/" in log["message"]:
                            temp = list(filter(None, log["message"].split(" ")))[1:]
                            key = temp[0]
                            value = temp[1]

                            if key in data:
                                data[key] = value

                found_loss = False
                for log in logs:
                    if "message" in log.keys():
                        # print(log["message"])
                        if not found_loss and "{'loss':" in log["message"]:
                            print(log["message"])
                            data["job_log/first_loss_time"] = datetime.datetime.strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
                            found_loss = True
                        if "{'train_runtime':" in log["message"]:
                            print(log["message"])
                            data["job_log/last_loss_time"] = datetime.datetime.strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")

                pprint(data)
                all_benchmark_jobs.append(data)
                # exit()

# Save the results to a csv file
import csv
import time

timestamp = int(time.time())

with open(f"results-{timestamp}.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(all_benchmark_jobs[0].keys())

    for job in all_benchmark_jobs:
        writer.writerow(job.values())
