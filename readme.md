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