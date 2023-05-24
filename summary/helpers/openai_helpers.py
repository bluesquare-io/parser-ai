import openai
import os
from dotenv import load_dotenv
load_dotenv()
#openai_model = 'gpt-3.5-turbo'
openai_model = 'gpt-4'
system_context_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/prompts/system_context.txt"
output_file_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/docs/output.txt"
openai.api_key = os.getenv("OPENAI_API_KEY")

with open(system_context_path, "r") as system_context:
    system_context = system_context.read()

def add_chat_gpt_message(prompt, retry_if_truncated=True, max_retries=5):
    messages = [{"role": "system", "content": system_context}]
    message = {'role': 'user', 'content': prompt}
    messages.append(message)

    full_response = ""
    retry_count = 0

    with open(output_file_path, "w") as output_file:  # Change to "a" if you want to append to an existing file
        while retry_count < max_retries:
            response = openai.ChatCompletion.create(
                model=openai_model,
                messages=messages
            )

            # Extract the assistant's message and append to the full response
            assistant_message = response.choices[0].message.content
            full_response += assistant_message

            # Write the message to the output file
            output_file.write(assistant_message + "\n")

            # Check if the response is likely to be truncated
            if not retry_if_truncated or response.usage['total_tokens'] < 4090:
                break

            # Add assistant message back to the conversation
            messages.append({'role': 'assistant', 'content': assistant_message})

            retry_count += 1

    return full_response