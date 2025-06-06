# Smart Data Analyst Agent (SN Assignment)

A Streamlit-based web application that allows users to upload various document types (CSV, Excel, PDF, DOCX, TXT, images) and interact with their data using natural language queries. The app leverages AI to provide insights, answer questions, and generate visualizations from your data.

---

## Features

- **Multi-format File Upload:** Supports CSV, Excel, PDF, DOCX, TXT, PNG, JPG, JPEG.
- **Automatic Data Parsing:** Extracts tables or text from uploaded files.
- **Conversational AI:** Ask questions about your data in plain English.
- **Data Overview:** Displays key metrics and a preview of your data.
- **Visualization:** Generates charts automatically when you ask for them.
- **Session History:** Keeps track of your conversation for context.
- **Modern UI:** Stylish, responsive interface with custom themes.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SN-Assignment
```

### 2. Install Dependencies

Make sure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with your Together API key:

```env
TOGETHER_API_KEY=your_api_key_here
```

### 4. Run the Application

```bash
streamlit run app.py
```

---

## File Structure

```
SN Assignment/
│
├── app.py                  # Main Streamlit app
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Python dependencies
├── agent.ipynb             # (Currently empty, not used)
└── utils/
    ├── file_parser.py      # File parsing logic
    ├── chat_agent.py       # AI chat logic
    └── llama_api.py        # Llama API integration
```

> **Note:** The `agent.ipynb` file is currently empty and does not contain any code or logic.

---

## Usage

1. **Upload a file** using the sidebar uploader.
2. **Ask questions** about your data in the input box.
3. **View insights, answers, and visualizations** generated by the AI.
4. **Clear the conversation** at any time using the button provided.

---

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- pandas, matplotlib, and other dependencies (see `requirements.txt`)

---

## Notes

- The app uses the Together API for AI-powered responses. Make sure your API key is valid and has sufficient quota.
- For best results, use structured data (CSV, Excel) or clear text documents.

---

## License

This project is for educational purposes.

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Together API](https://www.together.ai/)
  
