import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()

# OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')

# Create an instance of the OpenAI class
openai_instance = OpenAI()