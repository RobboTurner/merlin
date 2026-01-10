import streamlit as st

from src.db import GithubClient
from src.audio import read_list_aloud

st.set_page_config(page_title="Merlin Games", page_icon="🧙‍♂️")

# allows communication between different users
client = GithubClient()

with st.sidebar:
    username = st.text_input("What is your (real) name?")

    if st.button("New round (clears names)"):
        # clear our names out - TODO: make more flexible for multiple games
        client.write_github_json(dict())


empire, mafia = st.tabs(["Empire", "Mafia"])

with empire:
    st.title("Empire")
    
    with st.expander("Explain the rules"):
                st.write("""To play empire, each person must come up with a name that is known to everyone in the group. This could be a celebrity, fictional character or someone you *all* know personally.""")
                st.write("""To start, add your name to the below box. Once everyone has a name, choose someone to start the game on their phone. Make sure their volume is turned up!""")
    
    inpcol, buttcol = st.columns([4, 1])

    with inpcol:
        resp = st.text_input("Who are you playing?")

    with buttcol:
        # empty div for alignment :(
        st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
        if st.button("Submit name"):
            client.update_github_json({username: resp})
            st.text("Thanks for submitting your guess! To change your answer, send a different answer through. To let someone else without a phone submit their own name, make sure they change their name at the top!")

    
    if st.button("All names submitted"):
        # get final values
        final_list = [name for name in client.read_github_json().values()]
        
        # read aloud
        read_list_aloud(final_list, shuffle_list = True)    
        

with mafia:
    st.title("Mafia")
    st.write("Work in progress")