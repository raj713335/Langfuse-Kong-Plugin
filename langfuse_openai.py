import os
from typing import List
from langfuse.openai import openai  # OpenAI integration
from dotenv import load_dotenv

from llama_index.core import set_global_handler
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

load_dotenv()

set_global_handler("langfuse")

# global_handler.start_trace(
#   session_id="first-session-01"
# )

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")


# completion = openai.chat.completions.create(
#     model=OPENAI_API_MODEL,
#     messages=[
#           {"role": "system", "content": "You are a very accurate calculator."},
#           {"role": "user", "content": "1 + 1 = "}],
# )
#
# print(completion.choices[0].message.content)

class message_schema(BaseModel):
    messages: List = []


@app.get("/llm_response")
def llm_response(message: message_schema):
    res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=100,
            messages=message.messages,
        ).choices[0].message.content

    return {'message': res}

# @observe()
# def story():
#     return openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         max_tokens=100,
#         messages=[
#             {"role": "system", "content": "You are a great storyteller."},
#             {"role": "user", "content": "Once upon a time in a galaxy far, far away..."}
#         ],
#     ).choices[0].message.content
#
#
# @observe()
# def main():
#     return story()


# main()

if __name__ == '__main__':
    uvicorn.run("langfuse_openai:app", host="localhost", port=5000, reload=True)
