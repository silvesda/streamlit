import openai
import streamlit as st

# Setze den Titel der App
st.title("Telenot Assistantv1")

# API-Schlüssel aus Streamlit Secrets abrufen
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Das Modell, das Sie verwenden möchten
model_id = "gpt-3.5-turbo"

# Initialisiere den Chatverlauf, falls noch nicht vorhanden
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vorherige Nachrichten anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Benutzer-Eingabe
if prompt := st.chat_input("Wie kann ich helfen?"):
    # Benutzerfrage zum Verlauf hinzufügen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant-Antwort anzeigen
    with st.chat_message("assistant"):
        # Anfrage an die OpenAI API senden
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=False
        )
        
        # Die Antwort des Assistant extrahieren
        assistant_response = response.choices[0].message["content"]
        st.markdown(assistant_response)
        
    # Antwort zum Chatverlauf hinzufügen
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
