import requests
import os
import io
import base64
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image

# Load Together API key from environment
def call_together_ai_llm(messages):
    api_key = os.environ.get("TOGETHER_API_KEY")
    url = "https://api.together.xyz/v1/chat/completions"

    if not api_key:
        return "Error: TOGETHER_API_KEY not set in environment."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except KeyError:
            return f"Unexpected response format: {response.json()}"
    else:
        return f"Error: {response.text}"


def chat_with_agent(query, df=None, text="", image=None, file=None):
    if image:
        # OCR: Extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        if not extracted_text.strip():
            return "No text detected in the image."

        messages = [
            {"role": "system", "content": "You are a data analyst that can interpret text extracted from images."},
            {"role": "user", "content": f"{query}\n\nHere is the text extracted from the image:\n{extracted_text}"}
        ]
        return call_together_ai_llm(messages)

    elif file:
        try:
            pdf_reader = PdfReader(file)
            full_text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
            num_pages = len(pdf_reader.pages)
            word_count = len(full_text.split())

            messages = [
                {"role": "system", "content": "You are an expert document analyst."},
                {"role": "user", "content": f"{query}\n\nThis document has {num_pages} pages and about {word_count} words.\n\nHere's the content:\n{full_text[:4000]}"}  # Truncated to 4000 characters
            ]
            return call_together_ai_llm(messages)

        except Exception as e:
            return f"Failed to read PDF file: {str(e)}"

    elif df is not None:
        df_text = df.to_string()
        messages = [
            {"role": "system", "content": "You are a data analyst that understands tables and dataframes."},
            {"role": "user", "content": f"{query}\n\nHere is the data:\n{df_text}"}
        ]
        return call_together_ai_llm(messages)

    elif text:
        messages = [
            {"role": "system", "content": "You are an expert text analyst."},
            {"role": "user", "content": f"{query}\n\n{text}"}
        ]
        return call_together_ai_llm(messages)

    return "No data found to answer the query."
