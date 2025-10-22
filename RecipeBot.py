import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
api_keyHug = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
api_keyGroq = os.getenv("GROQ_API_KEY")

class Recipe(BaseModel):
    ingredients: list[str] = Field(..., description="List of ingredients required")
    steps: list[str] = Field(..., description="Step-by-step cooking instructions")
    cooking_time: str = Field(..., description="Total cooking time")
    difficulty_level: str = Field(..., description="Difficulty level of the recipe")
    nutritional_facts: dict = Field(..., description="Nutritional information like calories, protein, etc.")

parser = JsonOutputParser(pydantic_object=Recipe)

st.header("🍳 Recipe Bot")

model_choice = st.selectbox("Choose your model:", [
    "Gemini (Google)",
    "LLaMA 3 (Groq)"
])

user_input = st.text_input("Enter the dish you want to eat:")

template = PromptTemplate(
    template="""You are a professional food expert. The user wants to make {user_input}.
Prepare a recipe in JSON format with the following fields:
{format_instructions}""",
    input_variables=["user_input"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

def get_model(choice):
    if choice == "Gemini (Google)":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.5,
            google_api_key=api_key
        )
    
    elif choice == "LLaMA 3 (Groq)":
        return ChatGroq(
            model_name="llama-3.1-8b-instant",  
            temperature=0.5,
            groq_api_key=api_keyGroq
        )

if st.button("Generate Recipe"):
    if user_input:
        model = get_model(model_choice)
        prompt = template.format(user_input=user_input)
        result = model.invoke(prompt)
        parsed = parser.parse(result.content)
        st.subheader("Structured Recipe Output:")
        st.json(parsed)
    else:
        st.warning("Please enter a dish name first.")