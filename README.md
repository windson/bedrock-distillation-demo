# Amazon Bedrock Model Customisation: Distillation Job

This code sample demonstrates data preparation for Bedrock Model Distillation.

## Setup

1. Create Synthetic data using prompts in prompts directory.
   - prompt1.md 
      - This sample prompt creates a csv of records with 3 columns (column names can be any names you wish) with the following details:
         - 1st column represents the incoming user query
         - 2nd column represents the tools or for your usecase, you can stuff in the reasoning or few shots (I used tool use example for Nova models)
         - 3rd column represents the result expected from Foundation Model.
      - Update the prompt according to your task and leverage on any LLM to generate synthetic data.
      - Copy the data to csv file. There is a scope for you to automate this.
      - NOTE: The Bedrock model distillation requires at least 100 records to initiate the distillation job.
   - prompt2.md
      - This sample prompt is to generate code to club the data in csv file to the format specified 
         - [here](https://docs.aws.amazon.com/bedrock/latest/userguide/distillation-data-prep-option-1.html) if you want to Provide your own prompts for data preparation (we are doing this as a part of this code sample) or
         - [here](https://docs.aws.amazon.com/bedrock/latest/userguide/distillation-data-prep-option-2.html) if you want to Use invocation logs for data preparation
      - I used on Amazon Q Developer `/dev` action in VS Code to do this step along with some self-taught coding skills.
   - promt3.md
      - This sample prompt is to upload the file to S3.
      - I used on Amazon Q Developer `/dev` action in VS Code to do this step along with some self-taught coding skills.



2. Create a `.env` file in the root directory with the following content:
   ```
   S3_BUCKET_NAME=YOUR_BUCKET_NAME
   S3_PREFIX=YOUR_CHOICE_OF_PREFIX
   AWS_REGION=us-west-2
   ```

## Usage

1. Ensure you have a `data/data.csv` file with the following columns:
   - User Query
   - Tool Config Example
   - Selected Tool

2. Run the tests:

   ```shell
   pytest test.py -v
   ```

3. Run the program:
   ```bash
   python main.py
   ```

3. The program will generate `data/distillation_data.jsonl` with the converted data and uploads it to S3. You can use this path when creating Distillation job and setting this path to "Distillation input dataset".

4. Though the dataset validation of jsonl is covered using tests `test_tool_config_json_structure` and `test_jsonl_output_structure`, you can validate the datset officially using the following steps:

```shell
git clone --depth 1 --filter=blob:none --sparse https://github.com/aws-samples/amazon-bedrock-samples.git
cd amazon-bedrock-samples
git sparse-checkout set custom-models/model_distillation/dataset-validation
cd custom-models/model_distillation/dataset-validation
python3 -m venv env
source env/bin/activate
pip install -U pip
pip install -r requirements.txt
python3 dataset_validator.py -p </PATH/TO/JSONL_FILE.jsonl>
```

Sample output of successful validation appears as follows:
```shell
(env) user@mac dataset-validation % python3 dataset_validator.py -p /Users/user/Documents/tech/distillation/data/distillation_data.jsonl
2025-03-24 23:41:24,581 - INFO - Validating file: /Users/user/Documents/tech/distillation/data/distillation_data.jsonl
2025-03-24 23:41:25,536 - INFO - 106 out of 106 prompts are valid for file: /Users/user/Documents/tech/distillation/data/distillation_data.jsonl
2025-03-24 23:41:25,640 - INFO - Validation complete.
```