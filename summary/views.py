from django.shortcuts import render
from django.http import HttpResponse
import os
import pdfminer
import openai
from pdfminer.high_level import extract_text
from dotenv import load_dotenv
from .helpers.text_helpers import *
from .helpers.openai_helpers import *

doc_to_analyze_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/docs/cdc.pdf"
prompts_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/prompts"
summary_file_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/docs/summary.txt"
analyze_file_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/docs/analyze.txt"

prompt_chunk_summary_text_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/prompts/summarize.txt"
with open(prompt_chunk_summary_text_path, "r") as prompt_chunk_summary_text:
    prompt_chunk_summary_text = prompt_chunk_summary_text.read()
summaries = []

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.schema import AgentFinish
from langchain.llms import OpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

doc_to_analyze_path = os.getenv("PROJECT_ABSOLUTE_PATH") + "/docs/analyze.txt"

callback_agent = ""
class MyCustomHandler(BaseCallbackHandler):
    def on_agent_finish(self, finish: AgentFinish, **kwargs: any) -> any:
        callback_agent = finish.return_values['output']

def analyze_interface(request):
    return render(request, 'index.html', {'analysis': ''})

def analyze(request):
    loader = TextLoader(analyze_file_path)
    index = VectorstoreIndexCreator().from_loaders([loader])
    query = request.POST.get('question', '')
    result = index.query(query)
    return render(request, 'index.html', {'analysis': result})

def index(request):
    # if not os.path.isfile(doc_to_analyze_path):
    #     return HttpResponse(f"File not found: {doc_to_analyze_path}")
    #
    # # Use PDFMiner to extract text from the PDF
    # text = extract_text(doc_to_analyze_path)
    # chunk_length = 2900 * 4
    # text_chunks = split_text_into_chunks(text, chunk_length)
    #
    # # Summarize each chunk using the OpenAI API and store the results in summary.txt
    # with open(summary_file_path, "a") as summary_file:
    #     for chunk in text_chunks:
    #         prompt = prompt_chunk_summary_text.format(chunk)
    #         summary = add_chat_gpt_message(prompt)
    #         summaries.append(summary)
    #         summary_file.write(summary + "\n"+"-----"+"\n")

    # Read the content of summary.txt
    with open(summary_file_path, "r") as summary_file:
        summary_content = summary_file.read()

    # Ask OpenAI to do a quotation base on the content of summary.txt
    contents = {}
    contents['#content'] = summary_content
    prompt = load_prompt("quotation.txt", contents)
    final_value = add_chat_gpt_message(prompt)
    return HttpResponse(final_value)