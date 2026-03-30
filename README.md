cat << 'EOF' > README.md
# 🤖 Automated QA & DevOps Workspace (Multi-Agent System)

**Built for: Google Skills APAC Generative AI 2026 (Phase 1)**

## 📌 Project Overview
The Automated QA & DevOps Workspace is an API-based multi-agent system designed to act as a technical project manager and evaluator for software engineering teams. Instead of generic personal assistance, this system bridges the gap between raw deployment logs and actionable QA reporting. 

Powered by **Gemini 2.5 Flash** and **LangGraph**, the system intelligently routes natural language queries, queries structured databases for test logs, and synthesizes failure reports.

## 🏗️ Architecture & Core Requirements Met

This project fulfills all Phase 1 Core Requirements:

1. **Primary Agent & Sub-Agent Coordination:** Built using `langgraph.prebuilt.create_react_agent`. A primary coordinator understands the user's request and delegates tasks to specific tools/sub-functions.
2. **Store and Retrieve Structured Data:** Integrates a structured mock-database representing real-world CI/CD pipelines (Main, Staging, Dev environments).
3. **Integrate Multiple Tools:** Utilizes LangChain `@tool` decorators to give the AI access to external functions (e.g., `fetch_test_logs`).
4. **Handle Multi-Step Workflows:** The agent autonomously decides *how many times* to use a tool. If asked about multiple branches, it loops through its tools until it has all the necessary context before drafting the final report.
5. **Deploy as an API-Based System:** Fully containerized via Docker and deployed live on **Google Cloud Run** using FastAPI.

## 🚀 Live API Endpoint
The system is deployed and accessible globally at:
**`https://qa-devops-agent-617835725908.asia-southeast1.run.app`**

### Interactive Documentation (Swagger UI)
Visit the `/docs` route to interact with the agent via the browser:
[Live Swagger UI](https://qa-devops-agent-617835725908.asia-southeast1.run.app/docs)

## 💻 API Usage Example

You can trigger the multi-agent workflow using standard HTTP POST requests.

**cURL Request:**
```json
curl -X 'POST' \
  '[https://qa-devops-agent-617835725908.asia-southeast1.run.app/api/v1/analyze](https://qa-devops-agent-617835725908.asia-southeast1.run.app/api/v1/analyze)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "task_description": "Please check the test logs for the main branch and the staging branch. Give me a summary of both."
}'

Agentic Response:

JSON
{
  "status": "Success",
  "received_task": "Please check the test logs for the main branch and the staging branch...",
  "agent_response": "Here is a summary of the test logs:\n\n* **Main Branch:** FAILED. There are 3 UI tests that failed in `components/Dashboard.tsx` due to a 'Cannot read properties of undefined (reading map)' error.\n* **Staging Branch:** PASSED. All 142 tests passed with 0 warnings."
}
🛠️ Local Development Setup
Clone the repository.

Create a virtual environment: python3 -m venv venv && source venv/bin/activate

Install dependencies: pip install -r requirements.txt

Create a .env file with your GEMINI_API_KEY.

Run the server: uvicorn main:app --host 0.0.0.0 --port 8080
EOF
