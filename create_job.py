import json
import requests
import time
import config


# Get the current timestamp in seconds since the Unix epoch
timestamp = int(time.time())
headers = {'content-type': 'application/json'}
# Load the payload from the JSON file
with open('payload.json') as f:
    payload = json.load(f)

# Set up authentication
headers.update(config.AUTH)
payload['auth']['organization'] = config.ORGANIZATION
payload['job']['trainingConfig']['wandb_project'] = config.BENCHMARK_PREFIX

baseModel_to_test = ['llama2-13b-base']
dataset_to_test = ["chat-nbx/s0-1M"]

ctx_length = 2048

hw_to_test = ['nvidia-a100-80g']
hw_count = ['1']
no_epochs_to_test = [5]
gas_to_test = [4, 8, 16, 32] # , 2]
microbs_to_test = [8, 16, 32] # , 16, 8, 4]

count = 0

for baseModel in baseModel_to_test:
    for dataset_path in dataset_to_test:
        for no_epochs in no_epochs_to_test:
            for gpu in hw_to_test:
                for gpuCount in hw_count:
                    for gas in gas_to_test:
                        for mbs in microbs_to_test:
                            # Modify the payload to change the desired variables
                            payload['job']['baseModel'] = baseModel
                            payload['job']['datasets'][0]['path'] = dataset_path

                            payload['job']['resource']['gpu'] = gpu
                            payload['job']['resource']['gpuCount'] = gpuCount
                            payload['job']['trainingConfig']['num_epochs'] = no_epochs
                            payload['job']['trainingConfig']['micro_batch_size'] = mbs
                            payload['job']['trainingConfig']['gradient_accumulation_steps'] = gas
                            payload['job']['trainingConfig']['eval_batch_size'] = 8
                            payload['job']['trainingConfig']['sequence_len'] = ctx_length

                            dataset_name = payload['job']['datasets'][0]['path'].split('/')[-1]
                            name = f"{config.BENCHMARK_PREFIX}/{baseModel}/{dataset_name}/{gpuCount}x{gpu}/ctx-{ctx_length}/{no_epochs}ep/gas-{gas}/mbs-{mbs}/{timestamp}"

                            payload['job']['name'] = name
                            payload['job']['trainingConfig']["wandb_run_id"] = name.replace('/', '_')

                            print(f"Creating job with name: {name}")
                            # Make the API call
                            response = requests.post(f"{config.BASE_STUDIO_URL}/CreateFinetuneJob", headers=headers, data=json.dumps(payload))

                            # Print the response status code
                            print(response.status_code)
                            print(response.text)

                            count += 1
                            # exit()
print("Total jobs created: ", count)