# LLM Module

## Setup

1.  Activate your virtual environment.

2.  Install required dependencies:

    ``` bash
    pip install torch transformers accelerate
    ```

3.  Create the folder:

        models/tiny-llama/

    *(See below for model installation instructions.)*

4.  Add the following to `.gitignore`:

        models/

5.  Ensure these files already exist in the project root:

    -   `search_results_jobs.json`
    -   `search_results_skills.json`

## Run the LLM Stage

From the project root:

``` bash
python -m llm.run
```

This will generate:

    final_results.json

The field `ai_summary` contains the generated explanation paragraph.

------------------------------------------------------------------------

## Install TinyLlama Model (Offline)

On a machine with internet access:

``` bash
git lfs install
git clone https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

After cloning completes:

1.  Copy the entire cloned folder into:

        career-intelligence/models/tinyllama/

2.  Verify that `model.safetensors` is large (\~2GB).

3.  The model will now run fully offline.
