import os
import subprocess
import sys

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_openai_tools_agent

from langgraph.graph import Graph, StateGraph, START, END
from langchain_community.document_loaders import PyPDFLoader

from setup import setup

setup.initialize()

# cmd to run the aider
# aider --no-auto-commits

def run_aider(llm_prompt):
    """
    Run the aider with the given prompt by the llm calling it as a tool
    """
    # Set the OPENAI_API_KEY environment variable
    subprocess.run(["setx", "OPENAI_API_KEY", os.environ["OPENAI_API_KEY"]])

    result = subprocess.run(
        [sys.executable, "-m", "aider", "--message", llm_prompt, "--yes"],
        capture_output=True,
        text=True
    )
    return result.stdout

def add_dependencies(dependencies):
    """
    Add dependencies to the project
    """
    for dependency in dependencies:
        subprocess.run(["poetry", "add", dependency])

def create_files(files):
    """
    Create files that is required to fullfill the user request
    """
    for file, content in files.items():
        if file.strip():  # Check if the filename is not empty or just whitespace
            with open(file.strip(), "w") as f:
                f.write(content)
        else:
            print(f"Skipping empty filename: '{file}'")

def create_aider_agent(llm):
    tools = [Tool(
        name="Aider",
        func=lambda prompt: run_aider(prompt),
        description="Use aider to run the aider command line tool and prompt to generate code and test and make code"
    ),
    Tool(
        name="add_dependencies",
        func=lambda dependencies: add_dependencies(dependencies),
        description="Use this tool to add dependencies to the project"
    )]
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
            You are an AI that uses Aider, which is a Aider to run codes. 
            Aider is AI pair programming in your terminal which you can use to make all sorts of programme based on the users request.
            """
        ),
        HumanMessagePromptTemplate.from_template(
        """
        {input}
        Remember to use the tools available to you when necessary.
        """),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

# Example usage:
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
aider_agent = create_aider_agent(llm)

pdf_file = r"C:\Users\akdahal\Downloads\GCCS_UNICEF_Country Office Guide_preview.pdf"

pdf = PyPDFLoader(pdf_file)
documents  = pdf.load()


# Use the agent
response = aider_agent.invoke({
    "input": f"Create a dashboard from {documents} in streamlit ,\
    make sure to analyze the pdf to get relevent information and data, these data should be shown in the dashboard\
    create a dashboard to show the data, make it interactive and user friendly"
})
print(response)