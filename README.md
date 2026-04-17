# AarogyaOne Support Chatbot

The project is structured into logical folders:
- **`bot/`**: Core engine and FastAPI logic.
- **`data/`**: JSON knowledge base files.
- **`tests/`**: Test and debug scripts.

## 🚀 How to Run

### 1. Local Run (FastAPI)
To run the API from the project root:
```bash
uvicorn bot.main:app --reload
```

### 2. Run Tests
To run the RAG or sub-category tests:
```bash
python -m tests.test_rag
python -m tests.test_subcategory
```

### 3. Docker Run
```bash
docker-compose up --build
```