import csv
import json
from s3_upload import upload_to_s3
    
def read_csv_data(csv_file):
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

## https://aws.amazon.com/blogs/machine-learning/a-guide-to-amazon-bedrock-model-distillation-preview/
## https://docs.aws.amazon.com/bedrock/latest/userguide/distillation-prepare-datasets.html

def create_jsonl_record_for_distillation(user_query, tool_config, selected_tool):
    record = {
        "schemaVersion": "bedrock-conversation-2024",
        "system": [
            {
                "text": "You are an AI assistant that helps users select appropriate tool for a given user query. "
                "The user query is present in <userquery> </usrequery> tags and the tools are present in <tools> </tools> tags. "
                "You respond with the chosen tool in and fill in the toolSpec based on the info available in the user query in the <result>  </result> tags. "
                "Your response must follow the schema of the toolspec. You respond without preamble."
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"<userquery>{user_query}</usrequery>\n<tools>{tool_config}</tools>"
                    }
                ]
            },
            # # keep this optional if you want to rely on teacher model's intelligence to predict the tool.
            # {
            #     "role": "assistant",
            #     "content": [
            #         {
            #             "text": ""
            #         }
            #     ]
            # }
        ]
    }
    return record

def convert_to_jsonl(csv_file, output_file):
    data = read_csv_data(csv_file)
    
    with open(output_file, 'w') as f:
        for row in data:
            try:
                record = create_jsonl_record_for_distillation(
                    row['User Query'],
                    row['Tool Config Example'],
                    row['Selected Tool']
                )
                # Validate that the record is valid JSON
                json.dumps(record)
                # Write the record as a single line
                f.write(json.dumps(record) + '\n')
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {str(e)}")
                continue
                


if __name__ == '__main__':
    output_file = 'data/distillation_data.jsonl'
    convert_to_jsonl('data/data.csv', output_file)
    # Upload the generated JSONL file to S3
    
    upload_to_s3(output_file)