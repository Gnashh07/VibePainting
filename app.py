import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv

# Load environment variables (like your API key)
load_dotenv()

# Configure the Gemini API
# Make sure to set your GOOGLE_API_KEY in a .env file or environment variables
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    st.error("Google API Key not found. Please set GOOGLE_API_KEY in your .env file or environment variables.")
    st.stop() # Stop the app if key is missing


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Or whichever Gemini model you prefer for vision tasks

st.set_page_config(
    page_title="isaac.",
    page_icon="images/icon.ico",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; font-size: 130px;'>isaac.</h1>", unsafe_allow_html=True)    
st.markdown("<h3 style='text-align: center;'>your friendly neighbourhood vibe-checker</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>upload your masterpiece and let isaac rate your vibe!</h5>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your painting", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Your Uploaded Painting', use_column_width=True)
    st.write("") # Add a little space

    if st.button("Analyze Painting"):
        with st.spinner("AI is analyzing your masterpiece..."):
            try:
                # Prepare the image for Gemini API
                # Gemini Pro Vision can directly take PIL Image objects or bytes
                img_data = io.BytesIO()
                image.save(img_data, format=image.format if image.format else 'PNG') # Save with original format or default to PNG
                img_data.seek(0) # Rewind the buffer

                # You can also resize if needed, but Gemini usually handles various sizes
                # For very large images, consider resizing to something like max 1024x1024
                # if max(image.size) > 1024:
                #    image.thumbnail((1024, 1024))

                # Craft the prompt for Gemini
                # This is crucial! Experiment with different prompts.
                prompt = """Analyze this painting. Consider the use of colors, shapes, lines, composition,
                            and overall emotional tone. Based purely on these visual elements,
                            what kind of personality traits might the artist possess?
                            Be descriptive and provide a few distinct characteristics.
                            Avoid making definitive or diagnostic statements, and present it as an interpretation.
                            """

                # Send image and prompt to Gemini
                response = model.generate_content([prompt, image]) # Pass PIL Image object directly

                # Display the AI's personality inference
                st.subheader("AI's Personality Interpretation:")
                st.info(response.text) # Access the generated text

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
                st.warning("Please try uploading another image or check your API key/network connection.")

st.markdown("---")