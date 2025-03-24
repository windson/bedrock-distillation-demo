/dev Write a program that creates a jsonline file in the following structure of jsonline format.

```jsonl
{
    "schemaVersion": "bedrock-conversation-2024",
    "system": [
        {
            "text": string
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": string
                }
            ]
        },
        {
            "role": "assistant"
            "content": [
               {
                   "text": string
               }
            ]
        }
    ]
}
```
Specifically, each record has a mandatory field, schemaVersion, that must have the value bedrock-conversation-2024 at this launch. The record can optionally include a system prompt that indicates the role assigned to the model.

In the messages field, the user role is required. The input prompt provided to the model must read the columns "User Query","Tool Config Example" from data.csv file and put them to the following format
"User Query: {userquery} \n Tool Config: {toolconfig}".
While the assistant role, must contain the desired response which will be populated from the "Selected Tool" column of data.csv file

