from dotenv import load_dotenv
load_dotenv()
import io
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input,pc,prompt):
    model=genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    response=model.generate_content([input,pc[0],prompt])
    return response.text
def pdf_convertor(uploaded_file):
    if uploaded_file is not None:
        images=pdf2image.convert_from_bytes(uploaded_file.read(),dpi=70)
        first_page=images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts=[
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded ")
    
st.set_page_config(page_title="ATS v1.0")
st.header("ATS Powered by GEMINI")
input_text=st.text_area("Jod Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF recommended)",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploded sucessfully")

submit1 = st.button("Resume Summary")
submit2 = st.button("Percentage Match")


input_prompt1= """ You are an expreienced tech recruiter having experiecne in one of the following fields 
of Data Science, Full Stack Web Development, Full stack android development, Devops, Data analyst, your taks is to review
the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role
highlight the candidates strenght and weakness related to the specified requiements """

input_prompt2 = """ you are an skilled ATS(application tracking system) scanner with a deep understanding of Data Science, 
Full Stack Web Development, Full stack android development, Devops, Data analyst, and deep ATS functionality,
Evaluate the resume against the provided job description. give me the percentage if the resume matches.
Output format: Percentage then the skills which aling with the job description then the skills which are missing"""

if submit1:
    if uploaded_file is not None:
        pdf_content=pdf_convertor(uploaded_file)
        response=get_response(input_prompt1,pdf_content,input_text)
        st.subheader("the response is:")
        st.write(response)
    else:
        st.write("please upload a valid file")

elif submit2:
    if uploaded_file is not None:
        pdf_content=pdf_convertor(uploaded_file)
        response=get_response(input_prompt2,pdf_content,input_text)
        st.subheader("the response is:")
        st.write(response)
    else: 
        st.write("please upload a valid file")
