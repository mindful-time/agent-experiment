import os 
from dotenv import load_dotenv
load_dotenv()

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient



class Setup:
    def __init__(self):
        self.credential=ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID") ,   
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )
        
    
    def initialize(self):
        self.secret_client = self.setup_env()
        if self.secret_client:
            print(self.setup_openai_key())
            print( self.setup_langchain_key())
            return {"status": "success", "message": "Environment variables setup successfully"}
        else:
            return {"status": "error", "message": "Failed to setup environment variables"}


    def setup_env(self):
    #environment variables and secret
        os.environ["AZURE_TENANT_ID"] = os.getenv("AZURE_TENANT_ID")
        os.environ["AZURE_CLIENT_ID"] = os.getenv("AZURE_CLIENT_ID")
        os.environ["AZURE_CLIENT_SECRET"] = os.getenv("AZURE_CLIENT_SECRET")
        AZURE_KEYVAULT_URL= os.getenv("AZURE_KEYVAULT_URL") 


        # getting the secret from key vault
        return SecretClient(vault_url=AZURE_KEYVAULT_URL, credential=self.credential)

    def setup_openai_key(self):
        # setting up the azure openai key
        secret = self.secret_client.get_secret("AZURE-OPENAI-KEY")
        AZURE_OPENAI_KEY = secret.value

        # setting up the openai key
        secret = self.secret_client.get_secret("OPENAI-API-KEY")
        os.environ["OPENAI_API_KEY"] = secret.value
        return {"status": "success", "message": "OpenAI key setup successfully"}

    def setup_langchain_key(self):
        #langchain setup
        secret = self.secret_client.get_secret("LANGCHAIN-API-KEY")
        os.environ["LANGCHAIN_API_KEY"] = secret.value
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = "tools-as-llm"
        
        return {"status": "success", "message": "Langchain key setup successfully"}
    

setup = Setup()
setup
