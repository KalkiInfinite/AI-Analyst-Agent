import pandas as pd
import docx
import PyPDF2
import easyocr
from io import StringIO
from PIL import Image
import tempfile

reader = easyocr.Reader(['en'], gpu=False)

def parse_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == 'csv':
            return pd.read_csv(uploaded_file)

        elif file_type in ['xlsx', 'xls']:
            return pd.read_excel(uploaded_file)

        elif file_type == 'txt':
            return uploaded_file.read().decode('utf-8')

        elif file_type == 'docx':
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])

        elif file_type == 'pdf':
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
            return text.strip()

        elif file_type in ['png', 'jpg', 'jpeg']:
            # Save temporarily to feed into EasyOCR
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            result = reader.readtext(tmp_path, detail=0)
            return "\n".join(result)

        else:
            return "Unsupported file type."

    except Exception as e:
        return f"Error processing file: {str(e)}"
