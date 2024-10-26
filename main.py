import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Getting summary from LLM based on prompt
def generate_gemini_content(transcript_text,user_response):

    if user_response:
        prompt = f"""Human : Give response of the user question by only looking at the text provided in trasnscript within 200 words.
                    User question : {user_response}
                    Transcript:{transcript_text}"""
    else:
        prompt = f"You are a helpful assistant. Create a detailed summary of the following transcript within 200-500 words: {transcript_text}"
    model=genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

#Getting transscript from YT
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        trascript_text= YouTubeTranscriptApi.get_transcript(video_id)
         
        trascript =""
        for i in trascript_text:
            trascript+=" " + i["text"]
        
        return trascript
        
    except Exception as e:
        raise e

st.title("You tube video summariser")
yt_link =st.text_input("You Tube link:")
user_prompt = st.text_input("Any specific question")

if yt_link:
    video_id= yt_link.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcript_text=extract_transcript_details(yt_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,None)
        st.markdown("##Detailed Notes:")
        st.write(summary)

    

if st.button("Answer specific question"):
    #user_prompt = st.text_input("Any specific question:")
    if user_prompt:
        transcript_text=extract_transcript_details(yt_link)
        user_response= generate_gemini_content(transcript_text,user_prompt)
        st.markdown("##Response :")
        st.write(user_response)

