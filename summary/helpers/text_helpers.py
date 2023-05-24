import os
from dotenv import load_dotenv
load_dotenv()
prompts_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/prompts"
def split_text_into_chunks(text, chunk_length):
    chunks = []
    for i in range(0, len(text), chunk_length):
        chunk = text[i:i + chunk_length]
        chunks.append(chunk)
    return chunks

def load_prompt(name, contents):
    with open(prompts_path + "/" + name, "r") as prompt_file:
        prompt = prompt_file.read()

    prompt = prompt.replace('{', '{{').replace('}', '}}')
    prompt = prompt.format()

    for key, value in contents.items():
        prompt = prompt.replace(key, value)

    return prompt