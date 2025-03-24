## Task
Your task is to generate sample synthetic data, given the following Tools Config in <toolconfig> and </toolconfig> tags and the corresponding example tool config specified in <exampletoolconfig> and </exampletoolconfig> tags.

## Tools Config
<toolconfig>
"toolConfig": { #  all Optional
        "tools": [
                {
                    "toolSpec": {
                        "name": string # menaingful tool name (Max char: 64)
                        "description": string # meaningful description of the tool
                        "inputSchema": {
                            "json": { # The JSON schema for the tool. For more information, see JSON Schema Reference
                                "type": "object",
                                "properties": {
                                    <args>: { # arguments 
                                        "type": string, # argument data type
                                        "description": string # meaningful description
                                    }
                                },
                                "required": [
                                    string # args
                                ]
                            }
                        }
                    }
                }
            ],
   "toolChoice": "any" //Amazon Nova models support tool choice of "any", "auto" or "tool" with converse API
        }
    }
</toolconfig>

<exampletoolconfig> 
{
    "tools": [
        {
            "toolSpec": {
                "name": "top_song",
                "description": "Get the most popular song played on a radio station.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "sign": {
                                "type": "string",
                                "description": "The call sign for the radio station for which you want the most popular song. Example calls signs are WZPZ and WKRP."
                            }
                        },
                        "required": ["sign"]
                    }
                }
            }
        }
    ]
}
</exampletoolconfig> 

## Instructions
1. Review the Tools Config carefully to understand the data schema and requirements.
2. Use the provided example tool config as a reference:

### Example Tool Config
Example Tool Config column of resultant CSV must have more than one toolSpec. You can come up with example scenarios by being creative such as payment processing, sending email, triggering a workflow, calcuating the interest etc.,.


### Response style and format requirements:
- Generate sample data in CSV format for columns "User Query", "Tool Config Example" and "Selected Tool"expand your usecsaes beyond weather and songs. Be creative and generate more examples.'
- Generate synthetic data that adheres to the specified schema and constraints in the Tools Config.
- Ensure the generated data is realistic, consistent, and follows any provided rules or patterns.
- Present the synthetic data in a structured format, such as a table or a list of JSON objects.

Provide your response immediately without any preamble or additional information.