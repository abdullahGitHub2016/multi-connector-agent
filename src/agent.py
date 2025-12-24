import os
import sys
from langchain_ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from src.tools_setup import tools

# Performance Tweaks
os.environ["LANGCHAIN_TRACING_V2"] = "false"
sys.dont_write_bytecode = True

# 1. Initialize Model with Stop Sequence
llm = ChatOllama(
    model="qwen2.5:0.5b-instruct", 
    temperature=0,
    stop=["Observation:"] 
)

# The template must have these EXACT variables
template = """Answer the following questions as best you can.
You have access to the following tools:

{tools}

Use the following format strictly:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the raw SQL query ONLY
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# 3. Create Agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=5
)

# 4. Interactive Loop
if __name__ == "__main__":
    print("\n" + "="*40)
    print("🚀 OMNIMIND AGENT READY FOR DEMO")
    print("="*40)
    
    while True:
        query = input("\nUser: ")
        if query.lower() in ['exit', 'quit']: break
        
        try:
            agent_executor.invoke({"input": query})
        except Exception as e:
            print(f"Agent Error: {e}")