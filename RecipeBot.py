import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

class Recipe(BaseModel):
    ingredients: list[str] = Field(..., description="List of ingredients required")
    steps: list[str] = Field(..., description="Step-by-step cooking instructions")
    cooking_time: str = Field(..., description="Total cooking time")
    difficulty_level: str = Field(..., description="Difficulty level of the recipe")
    nutritional_facts: dict = Field(..., description="Nutritional information like calories, protein, etc.")

parser = JsonOutputParser(pydantic_object=Recipe)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.5,
    google_api_key=api_key
)

st.header("Recipe Bot")
user_input = st.text_input("Enter the dish you want to eat:")

template = PromptTemplate(
    template="""You are a professional food expert. The user wants to make {user_input}.
Prepare a recipe in JSON format with the following fields:
{format_instructions}""",
    input_variables=["user_input"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

if st.button("Generate Recipe"):
    if user_input:
        prompt = template.format(user_input = user_input)
        result = model.invoke(prompt)
        parsed = parser.parse(result.content)
        st.subheader("Structured Recipe Output:")
        st.json(parsed)
    else:
        st.warning("Please enter a dish name first.")