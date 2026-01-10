import streamlit as st
from random import shuffle
from src.db import GithubClient

st.set_page_config(page_title="Merlin Games", page_icon="🧙‍♂️")
username = st.text_input("what is your (real) name?")

empire, mafia = st.tabs(["Empire", "Mafia"])

client = GithubClient()

with empire:
    st.title("Empire")
    
    with st.expander("Explain the rules"):
                st.write("""To play empire, each person must come up with a name that is known to everyone in the group. This could be a celebrity, fictional character or someone you *all* know personally.""")
                st.write("""To start, add your name to the below box. Once everyone has a name, choose someone to start the game on their phone. Make sure their volume is turned up!""")
    resp = st.text_input("test")
    

    if st.button("Send"):
        client.update_github_json({username: resp})
        st.text("Thanks for submitting your guess! To change your answer, send a different answer through. To let someone else without a phone submit their own name, make sure they change their name at the top!")

    if st.button("All names submitted"):
        final_list = [name for name in client.read_github_json().values()]
        shuffle(final_list)   
        st.write(final_list)
            

with mafia:
    st.title("Mafia")
    st.write("Work in progress")