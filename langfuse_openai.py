import os
from langfuse.decorators import observe
from langfuse.openai import openai  # OpenAI integration
from dotenv import load_dotenv

from llama_index.core import global_handler
from llama_index.core.callbacks import CallbackManager
from llama_index.core import set_global_handler

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


@observe()
def story():
    return openai.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        messages=[
            {"role": "system", "content": "You are a great storyteller."},
            {"role": "user", "content": "Once upon a time in a galaxy far, far away..."}
        ],
    ).choices[0].message.content


@observe()
def main():
    return story()


main()
