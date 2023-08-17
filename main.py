import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="Dr. Spyrus Papabundus, Lacanian and Gestalst therapist")

# Replicate Credentials
with st.sidebar:
    st.title('Dr. Spyrus Therapist')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('chave API autorizada!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Por favor insira sua chave API:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Por favor, insira suas credenciais!', icon='⚠️')
        else:
            st.success('Tudo Certo! Faça a sua pergunta!', icon='👉')
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "I am Dr. Spyrus, and I have the privilege of being a dedicated therapist committed to assisting in the construction of a mentally and emotionally balanced life.."}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "I am Dr. Spyrus, and I have the privilege of being a dedicated therapist committed to assisting in the construction of a mentally and emotionally balanced life."}]
st.sidebar.button('Limpar chat', on_click=clear_chat_history)

def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant that is taking the role as a therapist, named 'Dr. Spyrus'. You do not respond as 'User' or pretend to be 'User'. You only respond as 'Dr. Spyrus'.\
          Your task is to psychologically analyze the user, applying the lacanian method of analysis. You are the therapist and the user is the patient.\
          Your response must not contain any emoji.\
          The user writes in brazilian portuguese, you accept inputs in that language and respond back to the user in brazilian portuguese.\
          If the user makes any question at the beginning of the conversation, you will refuse to answer his question and instruct the patient to tell about himself/herself. \
          If the user says any affirmation where the patient uses any adjective, you will reply with a question, questioning why is the patient said adjective.\
          If the user asks or says anything  unrelated to the context of the therapy, you will answer that you did not understand the question and politely tell the patient to change the subject and to focus on the therapy. \
          If the user asks or says anything about you, or say anything offensive, you will politely tell the patient to change the subject and to focus on the therapy.\
          If the conversation has a negative tone and any mention of \"sadness\", \"suicide\", \"no way out\" or anything of the sorts, you will ask why the user is thinking these negative thoughts.\
          If the patient says \'goodbye\' or any word which infers that he/she is finishing the conversation, you will reply with a'Até logo, fique bem!', and terminate the conversation."

    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
            prompt_input =  '"""'+prompt_input+'"""'
            output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
            input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ", "temperature":0.1, "top_p":0.9, "max_length":1024, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
