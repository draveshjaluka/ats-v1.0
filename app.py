from dotenv import load_dotenv
load_dotenv()
import io
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up Streamlit
st.set_page_config(page_title="ATS v1.0")
st.header("ATS Powered by GEMINI")

# Caching API responses to avoid redundant requests
@st.cache_data
def get_response_cached(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Asynchronous function to improve API speed
async def get_response_async(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = await model.generate_content_async([input_text, pdf_content[0], prompt])
    return response.text

# Function to convert PDF to image
@st.cache_data
def pdf_convertor(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read(), first_page=0, last_page=0)  # Process only first page
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")

# User inputs
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF recommended)", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")

# Buttons
submit1 = st.button("Resume Summary")
submit2 = st.button("Percentage Match")

# Prompts
input_prompt1 = """You are an experienced tech recruiter with expertise in Data Science, Full Stack Web Development, Android Development, DevOps, and Data Analysis. 
Your task is to review the resume against the job description for these roles. Please provide a professional evaluation of the candidate’s strengths and weaknesses."""
input_prompt2 = """You are an advanced ATS (Applicant Tracking System) specializing in Data Science, Full Stack Web Development, Android Development, DevOps, and Data Analysis. 
Evaluate the resume against the provided job description. Output the percentage match, followed by matching and missing skills."""

# Processing Resume Summary
if submit1 and uploaded_file:
    with st.spinner("Analyzing resume... ⏳"):
        pdf_content = pdf_convertor(uploaded_file)
        response = get_response_cached(input_text, pdf_content, input_prompt1)
    st.subheader("Analysis Result:")
    st.write(response)

# Processing Percentage Match
elif submit2 and uploaded_file:
    with st.spinner("Calculating match percentage... ⏳"):
        pdf_content = pdf_convertor(uploaded_file)
        response = get_response_cached(input_text, pdf_content, input_prompt2)
    st.subheader("Match Percentage:")
    st.write(response)

elif (submit1 or submit2) and not uploaded_file:
    st.warning("⚠️ Please upload a resume first.")
