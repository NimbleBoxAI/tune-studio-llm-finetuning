![TuneLogo](https://framerusercontent.com/images/P3ibw3xcMF3puvmNOGPVnc7wL18.png)
# Hyperparameter Search Scripts for TuneStudio


This repository contains scripts for performing hyperparameter searches on the TuneStudio platform for an LLMOps use case. The scripts require integration with Hugging Face and Weights & Biases (W&B) on the platform.

Prerequisites
-------------

* Access to a TuneStudio account
* Hugging Face and W&B integration on the platform
* Configuration file (`config.py`) with the following variables:
	+ `BASE_STUDIO_URL`: The base URL for the TuneStudio API
	+ `BENCHMARK_PREFIX`: A prefix for the names of the jobs created during the search
	+ `AUTH`: TuneStudio API key
	+ `ORGANIZATION`: The organization associated with the TuneStudio account

	 Sure, here's an example section for steps for using the repository:

Getting Started
---------------

1. **Create a `config.py` file:**

Create a new file named `config.py` in the root directory of the repository. This file should contain the required configuration variables for the scripts to run correctly. Here's an example configuration:

```python
BASE_STUDIO_URL = "https://studio.tune.app/tune.Studio"
BENCHMARK_PREFIX = "new-finetuning-search"
AUTH = {'x-tune-key': 'YOUR_TUNE_STUDIO_API_KEY'}
ORGANIZATION = "YOUR_TUNE_STUDIO_ORGANIZATION_ID"
```

Replace `YOUR_TUNE_STUDIO_API_KEY` with your TuneStudio API key and `YOUR_TUNE_STUDIO_ORGANIZATION_ID` with the name of your TuneStudio organization.

2. **Create finetuning jobs:**

Run the `create_job.py` script to create the finetuning jobs. This will search over the specified hyperparameters and create jobs on the TuneStudio platform.

```bash
python create_job.py
```

3. **Collect results:**

Once the finetuning jobs have completed, run the `collect_results.py` script to collect the results of the completed jobs.

```bash
python collect_results.py
```

This will parse the logs of the completed jobs and extract relevant training metrics.

You can also compare the results of the different hyperparameter combinations using the W&B dashboard.

4. **Clean up finetuning jobs:**

(Optional) To delete the finetuning jobs created by `create_job.py`, run the `cleanup_jobs.py` script.

```bash
python cleanup_jobs.py
```

This will filter jobs based on the `BENCHMARK_PREFIX` and allow you to confirm the deletion of the jobs before proceeding.

Note: Make sure to replace the placeholders in the code block for `config.py` with the actual values for your setup. Additionally, ensure that the `AUTH` variable is set correctly with your TuneStudio authentication credentials.

Scripts
-------

### `create_job.py`

This script creates finetuning jobs on TuneStudio with different hyperparameter combinations. The script searches over the following hyperparameters:

* Base model: `llama2-13b-base`
* Dataset: `chat-nbx/s0-1M`
* Number of epochs: `5`
* GPU: `nvidia-a100-80g`
* GPU count: `1`
* Gradient accumulation steps: `4, 8, 16, 32`
* Microbatch size: `8, 16, 32`

For more info, checkout the [Finetuning Docs](https://nimbleboxai.github.io/devnbx-docs/2.-Finetuning-LLMs/iii\)-Finetuning-with-APIs).

### `collect_results.py`

This script collects the results of the finetuning jobs created by `create_job.py`. The script filters jobs based on the `BENCHMARK_PREFIX` and only retrieves completed jobs.

The script then parses the logs of the completed jobs to extract relevant training metrics, such as:

* Training samples per second
* Training steps per second
* Global step
* Epoch
* Loss
* Learning rate

For more info, checkout the [API documentation](https://studio.tune.app/tune.Studio/docs/#post-/tune.Studio/ListFinetuneJobs.

### `cleanup_jobs.py`

This script deletes the finetuning jobs created by `create_job.py`. The script filters jobs based on the `BENCHMARK_PREFIX` and allows the user to confirm the deletion of the jobs before proceeding.

Usage
-----

1. Set up the required configuration in `config.py`.
2. Run `create_job.py` to create the finetuning jobs.
3. Wait for the jobs to complete.
4. Run `collect_results.py` to collect the results of the completed jobs.
5. (Optional) Run `cleanup_jobs.py` to delete the finetuning jobs.

For more info, checkout the [API documentation](https://studio.tune.app/tune.Studio/docs/#post-/tune.Studio/DeleteFinetuneJob).

License
-------

This project is licensed under the MIT License.

Acknowledgements
---------------

This project was created using the TuneStudio platform and requires integration with Hugging Face and W&B.

Note: Replace the placeholders (`<...>`) in the code block for `config.py` with the actual values for your setup. Additionally, ensure that the `AUTH` variable is set correctly with your TuneStudio API key.

Of course! Here's an example of how to include a link to the TuneStudio documentation and use Markdown headings: