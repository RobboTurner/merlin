import streamlit as st
from src.db import GithubClient
from src.audio import read_list_aloud

st.set_page_config(page_title="Empire")
with st.container(horizontal=True):
    st.title("Empire", width="stretch")
    game_id = st.number_input("Game ID", value = 1)
    

# allows communication between different users
client = GithubClient(game_id=game_id)

with st.expander("Explain the rules"):
            st.write("""To play empire, each person must come up with a name that is known to everyone in the group. This could be a celebrity, fictional character or someone you *all* know personally.""")
            st.write("""To start, add your name to the below box. Once everyone has a name, choose someone to start the game on their phone. Make sure their volume is turned up!""")

with st.form("empire"):
    yourname, character, buttcol = st.columns([3, 3, 1])

    with yourname:
        username = st.text_input("What is your (real) name?", placeholder=" real name (must be unique)")

    with character:
        resp = st.text_input("Who are you playing?", placeholder= "Scooby doo")

    with buttcol:
        # empty div for alignment :(
        st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)

       #only show button if form filled
        submit = st.form_submit_button("Submit name", type="primary")#not form_complete)
    
if submit:
    if not(bool(resp) and bool(username)):
        st.markdown(":red[Provide your name and character name!]")
    else:
        client.update_github_json({username: resp})
        st.text("Thanks for submitting your guess! To change your answer, send a different answer through. To let someone else without a phone submit their own name, make sure they change their name at the top!")

with st.container(horizontal=True):
    if st.button("All names submitted", type="primary", width = 150):
        # get final values
        final_list = [name for name in client.read_github_json().values()]

        # read aloud
        read_list_aloud(final_list, shuffle_list = True)

    if st.button("Delete all submitted names", type="primary", width = 150):
        # clear our names out - TODO: make more flexible for multiple games
        client.write_github_json(dict())