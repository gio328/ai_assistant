import gradio as gr
from tickets import tools, handle_tool_call
from config import openai_instance as openai
from talker import talker


model_use = 'gpt-4o-mini'
system_prompt = "You are a helpful assistant."

def message_gpt(message, history):
    messages = [{'role': 'system', 'content': system_prompt}] + history + [{'role': 'user', 'content': message}]

    # Log incoming message and history
    print(f"Message: {message}")
    print(f"History: {history}")

    response = openai.chat.completions.create(
        model=model_use,
        messages=messages,
        tools=tools
    )

    if response.choices[0].finish_reason=="tool_calls":
        print("Tool calls detected:")
        message = response.choices[0].message
        response = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=model_use, messages=messages)

    response_content = response.choices[0].message.content
    talker(response_content)
    return response_content

interface = gr.ChatInterface(
    fn=message_gpt, 
    title="Chatbot",
    type="messages",
    theme="default"
)

interface.launch()
