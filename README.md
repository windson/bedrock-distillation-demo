# Amazon Bedrock Model Customisation: Distillation Job

This code sample demonstrates data preparation for Bedrock Model Distillation.

## Setup

1. Create a `.env` file in the root directory with the following content:
   ```
   S3_BUCKET_NAME=your-bucket-name-here
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

3. The program will generate `data/distillation_data.jsonl` with the converted data.