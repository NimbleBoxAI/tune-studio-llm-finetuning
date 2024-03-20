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

# Set WandB project name
payload['job']['trainingConfig']['wandb_project'] = config.BENCHMARK_PREFIX

# Set the hub model id to upload the model to
payload['job']['trainingConfig']["hub_model_id"] = ""

# Set the base model id. You can read more at: https://nimbleboxai.github.io/devnbx-docs/3.-Misc/Supported-Models#finetuning
baseModel_to_test = ['phi-2']

# Hugging Face datasets to finetune on
dataset_to_test = [""]

# Hardware and training configurations
hw_to_test = ['nvidia-l4']
hw_count = ['1']

# Hyperparameters
ctx_length = 2048
no_epochs_to_test = [1]
gas_to_test = [4]
microbs_to_test = [2]

# Count the number of jobs created
count = 0
for baseModel in baseModel_to_test:
    for dataset_path in dataset_to_test:
        for no_epochs in no_epochs_to_test:
            for gpu in hw_to_test:
                for gpuCount in hw_count:
                    for gas in gas_to_test:
                        for mbs in microbs_to_test:
                            # Set the base model and dataset
                            payload['job']['baseModel'] = baseModel
                            payload['job']['datasets'][0]['path'] = dataset_path

                            # Set the hardware configurations
                            payload['job']['resource']['gpu'] = gpu
                            payload['job']['resource']['gpuCount'] = gpuCount

                            # Set the training configurations
                            payload['job']['trainingConfig']['num_epochs'] = no_epochs
                            payload['job']['trainingConfig']['micro_batch_size'] = mbs
                            payload['job']['trainingConfig']['gradient_accumulation_steps'] = gas
                            payload['job']['trainingConfig']['eval_batch_size'] = 8
                            payload['job']['trainingConfig']['sequence_len'] = ctx_length

                            # create a unique name for the job
                            dataset_name = payload['job']['datasets'][0]['path'].split('/')[-1]
                            name = f"{config.BENCHMARK_PREFIX}/{baseModel}/{dataset_name}/{gpuCount}x{gpu}/ctx-{ctx_length}/gas-{gas}/mbs-{mbs}/{timestamp}"
                            payload['job']['name'] = name

#                           # Set the wandb run id
                            payload['job']['trainingConfig']["wandb_run_id"] = name.replace('/', '_')

                            # Make the API call
                            print(f"Creating job with name: {name}")
                            response = requests.post(f"{config.BASE_STUDIO_URL}/CreateFinetuneJob", headers=headers, data=json.dumps(payload))

                            # Print the response status code
                            print(response.status_code)

                            if response.status_code == 200:
                                # Print the url of the job
                                count += 1
                                print(f"Job created [{name[:20]}...]:")
                                print(f"Link -> https://studio.tune.app/finetuning/{response.json()['id']}?org_id={config.ORGANIZATION}")
                            else:
                                print("Failed to create job")
                                print(response.text)
                                exit(1)

print("Total jobs created: ", count)