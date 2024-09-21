import os
import subprocess
import sys
import shlex

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_openai_tools_agent

from langgraph.graph import Graph, StateGraph, START, END

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser
from aider.coders import Coder
from aider.models import Model



# Example usage:
# result = run_aider_coder("make a script that prints hello world")
# print(result)
#
# result = run_aider_coder("make it say goodbye")
# print(result)
#
# result = run_aider_coder("/tokens")
# print(result)




from setup import setup

setup.initialize()

# cmd to run the aider
# aider --no-auto-commits

def run_aider_coder(instruction):
    """
    Run the aider coder with the given instruction.
    
    Args:
    instruction (str): The instruction to be executed by the coder.
    
    Returns:
    str: The result of the coder's execution.
    """
    # This is a list of files to add to the chat
    fnames = []
    # This is the model to use for the coder    
    # set AIDER_YES to --yes
    subprocess.run(["setx", "AIDER_YES", "--yes"])
    
    model = Model("gpt-4o-mini")

    # Create a coder object
    coder = Coder.create(main_model=model, fnames=fnames, )

    # Execute the instruction on those files and return the result
    result = coder.run(instruction)

    return result

def mkdir(directory):
    """
    Create a directory
    """
    os.makedirs(directory, exist_ok=True)
    print(f"Directory created: {directory}")


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
    Add dependencies to the project using poetry.
    
    Args:
    dependencies (list): A list of dependency names ex. ["streamlit", "pandas", "numpy", "sklearn"]
    """
    if isinstance(dependencies, str):
        # Convert space-separated string to list
        dependencies = shlex.split(dependencies)
    elif not isinstance(dependencies, list):
        raise ValueError("Dependencies must be a list")
    
    if not dependencies:
        print("No dependencies provided")
        return
    
    try:
        # Add all dependencies in a single poetry command
        subprocess.run([sys.executable, "-m", "poetry", "add"] + dependencies, check=True)
        print(f"Successfully added dependencies: {', '.join(dependencies)}")
    except subprocess.CalledProcessError as e:
        print(f"Error adding dependencies: {e}")
    except FileNotFoundError:
        print("Poetry not found. Make sure it's installed and in your PATH.")

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

def extract_data_from_pdf(pdf_file):
    """
    Extract data from pdf file, including tables, narratives, and important data points using an LLM.
    """        
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
            You are an AI tasked with extracting data from a PDF file.
            Your task is to think step by step and extract all relevant data from the PDF file,
            including tables, narratives, and important data points.
            Format the extracted data in the following JSON structure:
            ```json
            {{
                "tables": [
                    {{
                        "name": "table1",
                        "narrative": "Description of the table",
                        "data": ["data point 1", "data point 2", ...]
                    }},
                    ...
                ],
                "narratives": ["narrative1", "narrative2", ...],
                "important_data_points": ["data point 1", "data point 2", ...]
            }}
            ```
            The format should only be in JSON and nothin else. 
            """
        ),
        HumanMessagePromptTemplate.from_template(
        """
        Based on the following context, extract the data from the PDF file and format it as JSON:
        {context} and {metadata}
        """),
    ])
    
    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    # Create and run the extraction chain
    chain = prompt | llm | JsonOutputParser()
    
    # Load and split the PDF
    loader = PyPDFLoader(pdf_file)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks: {len(chunks)}")
    
    all_data = []
    
    try:
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1} of {len(chunks)}")
            data = chain.invoke({"context": chunk.page_content, "metadata": chunk.metadata})
            all_data.append(data)
    except Exception as e:
        print(f"Error processing split: {e}")

    # Combine all extracted data
    combined_data = {
        "tables": [],
        "narratives": [],
        "important_data_points": []
    }
    for data in all_data:
        if isinstance(data, dict):
            combined_data["tables"].extend(data.get("tables", []))
            combined_data["narratives"].extend(data.get("narratives", []))
            combined_data["important_data_points"].extend(data.get("important_data_points", []))
        else:
            print(f"Unexpected data format: {type(data)}")

    return combined_data

def create_aider_agent(llm):
    tools = [Tool(
        name="Aider",
        func=lambda prompt: (run_aider_coder(prompt)),
        description="Use aider to run the aider command line tool and prompt to generate code and test and make code"
    ),
    Tool(
        name="add_dependencies",
        func=lambda dependencies: add_dependencies(dependencies),
        description="Use this tool to add dependencies to the project make sure to add the dependencies full name like streamlit, pandas, numpy, sklearn, etc"
    ),
    Tool(
        name="extract_data_from_pdf",
        func=lambda context: extract_data_from_pdf(context),
        description="Use this tool to extract data from a PDF file and return it as a structured JSON object"
    ),
    Tool(
        name="mkdir",
        func=lambda directory: mkdir(directory),
        description="Use this tool to create a directory"
    )   
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
            You are an AI that uses Aider, which is a Aider to run codes. 
            Aider is AI pair programming in your terminal 
            which you can use to make all sorts of programme based on the users request.
            
            But before you start coding, you need to make the project structure based on the user request.
            Make sure to plan out the code you need to write before you start coding. 
            Make sure you think about the project structure, and make the folders and files structure needed first.
            Make sure to use the mkdir tool to create the directories needed.
            Make sure to use the add_dependencies tool to add the dependencies needed.
            Once you are done with the structure, start coding and make the functions and classes needed.
            Make sure to test the code and make sure there are no errors.
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

pdf_file =os.getenv("FILENAME")



# Use the agent
response = aider_agent.invoke({
    "input": f"Create a dashboard from pdf_file from the pdf:{pdf_file}"
})
print(response)