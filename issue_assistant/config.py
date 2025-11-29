import os
from dotenv import load_dotenv
from groq import Groq
from github import Github, Auth

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
	raise RuntimeError("GITHUB_TOKEN environment variable is not set")
g = Github(auth=Auth.Token(token))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY environment variable is not set")
client = Groq(api_key=api_key)
