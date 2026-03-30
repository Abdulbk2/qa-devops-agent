from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

app = FastAPI(title="QA & DevOps Agentic API")

class TaskRequest(BaseModel):
    task_description: str
    repo_url: str = None

# --- MOCK STRUCTURED DATABASE ---
MOCK_TEST_DB = {
    "main": "Status: FAILED. 3 UI tests failed in components/Dashboard.tsx. Error: 'Cannot read properties of undefined (reading map)'.",
    "staging": "Status: PASSED. 142 tests passed with 0 warnings.",
    "dev": "Status: FAILED. API timeout on /api/v1/users endpoint. Latency > 5000ms."
}

# --- DEFINE THE TOOL ---
@tool
def fetch_test_logs(branch_name: str) -> str:
    """Fetches the latest automated test logs from the database for a specific branch."""
    branch = branch_name.lower()
    if branch in MOCK_TEST_DB:
        return MOCK_TEST_DB[branch]
    return f"No test logs found for branch: {branch}"

tools = [fetch_test_logs]

# --- INITIALIZE AI & LANGGRAPH AGENT ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

# LangGraph automatically wires the LLM and tools together
agent_executor = create_react_agent(llm, tools)

@app.get("/")
def read_root():
    return {"status": "Active", "system": "Multi-Agent DevOps Workspace Online"}

@app.post("/api/v1/analyze")
def trigger_agent_workflow(request: TaskRequest):
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_api_key_here":
        return {"error": "GEMINI_API_KEY not configured in .env file"}
        
    # LangGraph expects a conversation history (messages array)
    system_prompt = "You are the Lead DevOps & QA Coordinator Agent. Answer this request using your tools: "
    full_prompt = system_prompt + request.task_description
    
    # Run the agent
    result = agent_executor.invoke({"messages": [("user", full_prompt)]})
    
    return {
        "status": "Success",
        "received_task": request.task_description,
        # Extract the final AI response from the message history
        "agent_response": result["messages"][-1].content
    }
