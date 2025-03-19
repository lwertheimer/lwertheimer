import os
import streamlit as st
from openai import OpenAI

# Set up OpenAI client

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Configure Streamlit page
st.title("Text Summarizer")

# Create input form
with st.form("summarizer_form"):
    input_text = st.text_area(
        "Enter text to summarize:", 
        placeholder="Paste your text here...",
        height=200
    )
    submitted = st.form_submit_button("Summarize Text")

# Process form submission
if submitted:
    if not input_text.strip():
        st.error("Please enter some text to summarize.")
    else:
        with st.spinner("Generating summary..."):
            try:
                # Call OpenAI API
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Update with correct model name
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that provides concise summaries of text."
                        },
                        {
                            "role": "user", 
                            "content": f"Please summarize this text in 3-5 sentences. Finally, list the 3 most used words (excepting stop words) with their frequency in the original text in this format - The five most used words - and the 3 most used descriptive adjectives in the original text with their frequency in this format - The three most used descriptive adjectives - :\n\n{input_text}"
                        }
                    ],
                    temperature=0.5,
                    max_tokens=250
                )
                
                # Display summary
                summary = response.choices[0].message.content
                st.subheader("Text Summary")
                st.write(summary)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")