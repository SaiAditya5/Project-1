# 🤖 AI-Based API Test Automation Platform

An intelligent testing platform that automatically generates, executes, and analyzes API test cases using AI, Playwright, and k6.

---

## 🚀 Overview

This project automates the entire API testing pipeline:

- Parses API specifications (Swagger/OpenAPI)
- Generates test cases using AI
- Executes tests using Playwright
- Performs performance testing using k6
- Displays results in an interactive UI

---

## 🧠 How It Works

1. **Parser** extracts API endpoints from Swagger JSON  
2. **AI Engine** generates test scenarios  
3. **Test Builder** structures them into test cases  
4. **Playwright** executes API requests  
5. **k6** performs load testing  
6. **Streamlit UI** displays results  

---

## 🧩 Features

✅ AI-based test case generation  
✅ Structured test cases with unique IDs  
✅ API execution using Playwright  
✅ Performance testing using k6  
✅ Interactive dashboard (Streamlit)  
✅ Graph visualization of results  
✅ Downloadable test reports  
✅ Modular architecture  

---

## 🛠️ Tech Stack

- Python  
- Streamlit (UI)  
- Playwright (API Testing)  
- k6 (Performance Testing)  
- OpenAI (AI Test Generation)  
- Matplotlib (Visualization)  

---

## 📂 Project Structure

<pre>
ai-testing-project/
│
├── src/
│   ├── app.py
│   │
│   ├── core/
│   │   ├── parser.py
│   │   ├── ai_engine.py
│   │   ├── test_builder.py
│   │   ├── test_executor.py
│   │
│   ├── services/
│   │   └── orchestrator.py
│   │
│   ├── models/
│   │   └── schema.py
│   │
│   ├── performance/
│   │   └── k6_runner.py
│   │
│   └── utils/
│
├── data/
├── outputs/
│
├── test_execution.py
├── test_k6.py
│
├── requirements.txt
└── README.md
</pre>

---

## ▶️ How to Run

### 1. Create Virtual Environment

python -m venv .venv
.venv\Scripts\activate

### 2. Install Dependencies
```bash
-pip install -r requirements.txt
-pip install playwright matplotlib
-python -m playwright install
```
### 3. Run Application

python -m streamlit run src/app.py

---

## 🧪 Example Workflow
1. Upload Swagger JSON
2. Click Generate & Execute Tests
3. View:
      - Test cases
      - Execution results (PASS/FAIL)
      - Graph visualization
4. Run performance tests (k6)
5. Download reports

---

## 📊 Output

1. JSON report (test_results.json)
2. Text report (test_results.txt)
3. UI dashboard with metrics and charts

---

## 🔥 Performance Testing (k6)

1. Automatically generates load test scripts
2. Executes using k6
3. Displays performance metrics

---

## 🔮 Future Enhancements

1. YAML support for Swagger
2. Advanced response validation (schema-based)
3. CI/CD integration improvements
4. Better natural language reporting
5. Authentication support (JWT, OAuth)

---
