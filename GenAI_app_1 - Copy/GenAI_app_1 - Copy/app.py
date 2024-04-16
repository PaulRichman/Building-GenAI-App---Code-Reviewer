from openai import OpenAI
import streamlit as st
import json

# Read the API key from file
with open("keys/.api_key.txt", "r") as f:
    api_key = f.read().strip()

# Set up OpenAI client
client = OpenAI(api_key=api_key)
# client = openai.OpenAI(api_key=api_key)

##################################
st.title("Python Code Review")
####################################

# take user's input
code = st.text_area("Enter Python code...")

# if the button is clicked, generate responses
if st.button("Generate"):

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                    You are a friendly AI Assistant. You take a python code as an input from the user.
                    Your job is to explain the bugs and generate the fixed code as an output.
                    Your output is a JSON with the following structure:
                    {"Bugs": "review_on_code", "Code": python fixed_code```}
                    """},
                {"role": "user", "content": f"Fix and explain the bugs in the following python code: {code}"}
            ],
            temperature=0.5
        )
        
        if response.choices[0].message:
            review = json.loads(response.choices[0].message.content)
            st.write(review)
            st.write(review["Bugs"])
            st.code(review["Code"])
        else:
            st.write("No response received from the API.")

    except Exception as e:
        st.error(f"Error: {e}")
