import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import streamlit as st

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",  
    temperature=0.5,
    google_api_key=api_key
)

st.header("Recipe Bot")

user_input=st.text_input("Enter the Dish you want to eat in this textbox!!")

template = PromptTemplate(template = """You are a professional food expert. The user wants to make {user_input}.
    Prepare a recipe for him/her mentioning the ingredients , stemps , cooking time , difficulty level
    and nutritional facts about the dish.""" , 
    input_variables = ["user_input"])

prompt = template.invoke({
    'user_input': user_input
})
if st.button("Summarize"):
    result = model.invoke(prompt)
    st.write(result.content)

