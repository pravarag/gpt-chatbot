import openai
import gradio as gr
from openai.error import RateLimitError
import backoff

openai.api_key = ""

messages = [
    {"role": "chatbot", "content": "Youre helpful assistant."},
]



@backoff.on_exception(backoff.expo, RateLimitError)
def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

inputs = gr.inputs.Textbox(lines=7, label="Chat with bot")
outputs = gr.outputs.Textbox(label="Reply")

gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title="AI Chatbot",
             description="Please ask your question",
             theme="compact").launch(share=True)
