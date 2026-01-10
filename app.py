import streamlit as st
import pandas as pd

st.set_page_config(page_title="Merlin Games", page_icon="🧙‍♂️")

empire, mafia = st.tabs(["Empire", "Mafia"])

with empire:
    st.title("Empire")
    
    with st.expander("Explain the rules"):
                st.write("""To play empire, each person must come up with a name that is known to everyone in the group. This could be a celebrity, fictional character or someone you *all* know personally.""")
                st.write("""To start, add your name to the below box. Once everyone has a name, choose someone to start the game on their phone. Make sure their volume is turned up!""")
with mafia:
    st.title("Mafia")
    st.write("Work in progress")