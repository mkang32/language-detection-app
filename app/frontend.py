import streamlit as st
import json
import requests
from PIL import Image


st.title("Language Detection App")


image = Image.open('images/front_image.jpg')
st.image(image)
expander = st.expander("Check supported languages")
expander.write("""
Arabic, Danish, Dutch, English, French, German,
Greek, Hindi, Italian, Kannada, Malayalam, Portugeese,
Russian, Spanish, Sweedish, Tamil, Turkish


Check out more about the project from [this Github repository](https://github.com/mkang32/language-detection-app)
""")

st.write()

# get input text
text = st.text_input("Write your text input:")

# make prediction on click
if st.button("Predict :sunglasses:"):
    res = requests.post(url="http://127.0.0.1:8000/predict", data=json.dumps({"text": text}))
    res = res.json()
    st.subheader(f"**{res.get('language')}** with the probability of **{res.get('probability')}**")


