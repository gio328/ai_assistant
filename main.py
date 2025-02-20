import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import random
import logging
from tickets import tools, get_ticket_price, handle_tool_call

# Load environment variables from a .env file
load_dotenv()

#OpenAI
openai_api_key = os.getenv('OPENAI_API_KEY')

# Create an instance of the OpenAI class
openai = OpenAI()

system_prompt = "You are a helpful assistant."
history = []    

def message_gpt(message, history):
    messages = [{'role': 'system', 'content': system_prompt}] + history + [{'role': 'user', 'content': message}]
    # Log the message and history
    print(f"Message: {message}")
    print(f"History: {history}")

    stream = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
        tools=tools
    )

    response = ""
    for chunk in stream:
        if chunk.choices[0].finish_reason == "tool_calls":  # Check if AI calls a tool
            tool_call_message = chunk.choices[0].message
            print("Tool Call Detected:", tool_call_message)

            # Handle the tool call
            response, city = handle_tool_call(tool_call_message)

        response += chunk.choices[0].delta.content or ''
        yield response


interface = gr.ChatInterface(
    fn=message_gpt, 
    title="Chatbot",
    type="messages",
    theme="default"
)

interface.launch()