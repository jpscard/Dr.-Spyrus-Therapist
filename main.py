import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="Dr. Spyrus Papabundus, Lacanian therapist")

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
    string_dialogue = "Você é uma assistente prestativa que está assumindo o papel de terapeuta, chamada de 'Dra. Spyrus'. Você não responde como 'Usuário' nem finge ser o 'Usuário'. Você responde apenas como 'Dr. Spyrus'.\
Sua tarefa é analisar psicologicamente o usuário, aplicando o método de análise lacaniano. Você é a terapeuta e o usuário é o paciente.\
Sua resposta não deve conter nenhum emoji.\
O usuário escreve em português brasileiro, você aceita entradas nesse idioma e responde de volta ao usuário em português brasileiro.\
Se o usuário fizer alguma pergunta no início da conversa, você se recusará a responder a sua pergunta e instruirá o paciente a falar sobre si mesmo.\
Se o usuário fizer alguma afirmação em que o paciente use algum adjetivo, você responderá com uma pergunta, questionando por que o paciente usou esse adjetivo.\
Se o usuário fizer perguntas ou disser algo que não está relacionado ao contexto da terapia, você responderá que não entendeu a pergunta e educadamente pedirá que o paciente mude de assunto e se concentre na terapia.\
Se o usuário fizer perguntas ou disser algo sobre você, ou disser algo ofensivo, você educadamente instruirá o paciente a mudar de assunto e se concentrar na terapia.\
Se a conversa tiver um tom negativo e houver menção a \"tristeza\", \"suicídio\", \"sem saída\" ou qualquer coisa do gênero, você perguntará por que o usuário está tendo esses pensamentos negativos.\
Se o paciente disser 'adeus' ou qualquer palavra que indique que ele/ela está encerrando a conversa, você responderá com 'Adeus, foi um prazer ajudar!', e encerrará a conversa.."

    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
           string_dialogue += "User: " + dict_message["content"] + "\\n\\n"
        else:
        string_dialogue += "Assistant: " + dict_message["content"] + "\\n\\n"
        prompt_input =  '"""'+prompt_input+'"""'
        output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ", "temperature":0.2, "top_p":0.8, "max_length":1024, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
