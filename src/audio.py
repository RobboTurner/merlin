from gtts import gTTS
from io import BytesIO
from random import shuffle
import streamlit as st

def read_list_aloud(list_to_read: list, shuffle_list = True) -> None:
    
    if shuffle_list:
        shuffle(list_to_read)
    
    sound_file = BytesIO()

    if len(list_to_read) == 0:
        speech = "No names submitted yet"
    else:
        speech = f"Prepare to hear your names. They are: {list_to_read}"

    gTTS(speech, lang='en', tld="co.uk").write_to_fp(sound_file)
    st.audio(sound_file, autoplay = True)