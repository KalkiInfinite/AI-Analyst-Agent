import os
from dotenv import load_dotenv
from together import Together

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def ask_llm_chat(message_list):
    """
    message_list: A list of dicts like:
    [{"role": "system", "content": "You are a data analyst."},
     {"role": "user", "content": "Analyze the dataset."}]
    """
    response = client.chat.completions.create(
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=message_list,
    )
    return response.choices[0].message.content.strip()
