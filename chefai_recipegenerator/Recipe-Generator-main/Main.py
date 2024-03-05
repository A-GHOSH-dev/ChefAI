import os
import streamlit as st
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain




# Initialize OpenAI API
llm = OpenAI(model="gpt-3.5-turbo-instruct", openai_api_key='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', temperature=0.9)

# Define prompt templates
prompt_template = PromptTemplate(
    template="Generate me a recipe of a meal that could be made using the following ingredients or the dish: {ingredients}",
    input_variables=['ingredients']
)

instruction_template = """With the ingredients generate the recipe for the dish:

Meals:
{meals}
"""
instruction_template_prompt = PromptTemplate(
    template=instruction_template,
    input_variables=['meals']
)

# Initialize LLMChain instances
meal_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    output_key="meals",
    verbose=True
)

instruction_chain = LLMChain(
    llm=llm,
    prompt=instruction_template_prompt,
    output_key="instruction_meals",
    verbose=True
)

# Initialize SequentialChain
overall_chain = SequentialChain(
    chains=[meal_chain, instruction_chain],
    input_variables=['ingredients'],
    output_variables=["meals", "instruction_meals"],
    verbose=True
)

# Set page background color
st.markdown(
    """
    <style>
        body {
            background-color: #f0f2f6;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Add GIF and title
st.image("https://media1.tenor.com/m/aeDvGql7fPMAAAAC/patrick-eat.gif", use_column_width=True)
st.markdown("<h1 style='color: #FF6347; text-align: center;'>🌟 Welcome to ChefAI! Enhance your cooking experience! 🍽️</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter your ingredients or dish below to generate a recipe!</p>", unsafe_allow_html=True)

# Input field and button
user_prompt = st.text_input("Enter the ingredients or dish 🥦🍗🥕")
if st.button("Generate") and user_prompt:
    with st.spinner("Generating ...."):
        # Generate and display recipe
        output = overall_chain({'ingredients': user_prompt})
        st.markdown("<h2>🍲 Generated Recipe:</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.write(output['meals'])
        col2.write(output['instruction_meals'])
