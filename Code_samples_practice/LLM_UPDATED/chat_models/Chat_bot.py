from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

# ✅ Load your Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY environment variable!")

# ✅ Initialize LLM (you can use "gemini-1.5-flash" if 2.5 not supported)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=GOOGLE_API_KEY
)

# ✅ Chat history
chat_history = [
    SystemMessage(content="You are a friendly AI assistant. Talk casually and help the user.")
]

print("🤖 Gemini Chat Started (type 'exit' to quit)\n")

while True:
    user_input = input("👤 You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("👋 Chat ended.")
        break

    # Add user message to history
    chat_history.append(HumanMessage(content=user_input))

    # Get model response
    response = llm.invoke(chat_history)

    # Add bot response to history
    chat_history.append(AIMessage(content=response.content))

    # Print bot reply
    print(f"🤖 Gemini: {response.content}\n")
