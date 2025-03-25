import os
from groq import Groq

'''
Groq API client

Before starting, make sure to execute the following command

    export GROQ_API_KEY=<your-api-key-here>

It sets an env variabile with your groq api key.

'''

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def call_to_llm(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
        model="llama3-70b-8192",
    )

    return chat_completion.choices[0].message.content



