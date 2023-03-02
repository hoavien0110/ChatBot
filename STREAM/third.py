import openai
import streamlit as st
from streamlit_chat import message

def open_file(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as infile:
        return infile.read()

openai.api_key = open_file('api_key.txt')

def generate_response(prompt, engine = "text-davinci-003", temp = 0.7, top_p = 1.0, tokens = 1024, freq_pen = 0.0, pres_pen = 0.0, ):
    prompt = prompt.encode(encoding = 'utf-8', errors = 'ignore').decode()
    response = openai.Completion.create(
        engine = engine,
        prompt = prompt,
        temperature = temp,
        max_tokens = tokens,
        # top_p = top_p,
        frequency_penalty = freq_pen,
        presence_penalty = pres_pen,
        stop = None)
    text = response.choices[0].text
    # message = completions.choices[0].text
    return text

st.title("ChatBot")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "Hello, how are you", key = "input")
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    #store the output
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key = str(i))
        message(st.session_state['past'][i], is_user = True, key = str(i) + '_user')

