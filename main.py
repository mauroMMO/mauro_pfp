from controller import Controller
from view import View
import os
from dotenv import load_dotenv
## human made evidence briefings path ##
directory_path = "briefings"
## embedding model ##
embedding_model = "all-MiniLM-L6-v2"
## openai model name ##
openai_model_name = "gpt-4o-mini"
load_dotenv(dotenv_path='env.env')
openai_api_key = os.getenv("openai_api_key")
topics = [
    "Intro",
    "Main Findings",
    "Who is this briefing for",
    "Where the findings come from",
    "What is included in this briefing",
    "What is not included in this briefing"
]
topics_chunk_size = [
    300,    
    4000,   
    200,    
    300,    
    300,    
    300     
]

controller = Controller(directory_path, embedding_model, openai_model_name, openai_api_key, topics, topics_chunk_size)
view = View(controller)

if __name__ == "__main__":
    view.run()