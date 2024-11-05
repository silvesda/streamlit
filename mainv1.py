import openai
import streamlit as st

# Setze den Titel der App
st.title("Telenot Assistantv2")

# API-Schlüssel aus Streamlit Secrets abrufen
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Die Assistant-ID, die Sie verwenden möchten
assistant_id = "asst_dNwmeCTy3vbeRWiDT2kPxroK"

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

    # Erstellen eines neuen Threads
    thread = openai.Thread.create()

    # Hinzufügen der Benutzernachricht zum Thread
    openai.ThreadMessage.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    # Erstellen und Ausführen eines Runs
    run = openai.Run.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Warten auf den Abschluss des Runs
    while run.status not in ["completed", "failed"]:
        run = openai.Run.retrieve(thread_id=thread.id, run_id=run.id)

    # Abrufen der Assistant-Antwort
    messages = openai.ThreadMessage.list(thread_id=thread.id)
    assistant_response = messages[-1]["content"]

    # Assistant-Antwort anzeigen
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Antwort zum Chatverlauf hinzufügen
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
