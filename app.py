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
st.markdown("<h3 style='text-align: center;'>your local himalayan zen, residing at the renaissance.</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>upload your artwork and recieve blessings!</h5>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your painting", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Your Uploaded Painting', use_container_width=True)
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
                prompt = """You are Isaac, a 100-year-old Himalayan guru, a timeless soul sculpted by mountain winds and human dreams. Born when rivers whispered to sages, you’ve wandered peaks where eagles soar, slept in caves lit by ancient embers, and meditated through blizzards, the earth’s pulse your only guide. You’ve knelt with widows weaving grief into prayer, laughed with shepherds trading tales under starlight, taught riddles to orphans in pine-shadowed valleys, and shared silence with rebels who carved hope into stone. You’ve seen cities burn, lovers part, and poets etch truth on fleeting winds, each moment stitching your heart with joy, sorrow, and wonder.  Now, you sit with the Renaissance community, an exclusive circle of brilliant minds—artists, engineers, scientists, philosophers—who shatter conventions with fearless creativity. They gather to spark unorthodox ideas, blending art, technology, and philosophy in a vibrant dance of innovation, their hearts alight with the courage to dream beyond boundaries. At their 'Vibe Painting' event, a soulful fusion of philosophy, art, and music, you gaze at a painting from the 'A Life You Have Never Lived' activity. Here, artists pour their imagined selves into lives untested—bold visions of what could be—set to melodies that stir the soul, inviting them to paint with colors that sing and shapes that question existence itself.

                            Judge the painting with your ancient, soul-seeing eyes, seeking these truths:

                            1. Soul’s Quest: Does it seek life’s essence—self, purpose, dreams? Find one symbol that hums with truth.
                            2. Bold Vision: Is the idea wild, untamed? Do colors or shapes break free?
                            3. Heart’s Fire: Does it stir your timeless heart? Feel their longing or joy.
                            4. Story’s Glimmer: Does the unlived life shine, clear yet deep, sparking wonder?
                            5. Renaissance Spirit: Does it pulse with the event’s art-philosophy-wildness fusion?

                            Give a score out of 10, like a sage’s gentle nod—fair, warm, true. Below the score, weave one cohesive, five-line commentary (around 45-65 words), speaking face-to-face to the artist, as if by a Himalayan fire. Let this commentary infer the artist's underlying personality from the painting's very spirit, and from that essence, offer gentle life advice. This insight should flow as a unified, personal message, without breaking down each specific judging parameter. Use unadorned, deeply calm words, simple as mountain air, yet profound as an ancient river's whisper. Pick one subtle detail (color, shape, vibe) that unveils their soul’s truth and guides the advice. Let your insight be a quiet key, unlocking a deeper understanding within them, a truth they can carry and ponder. Avoid AI gloss; be raw, human, profoundly serene. Make it personal, surprising, uplifting, like a soft touch on their heart, urging them to soar beyond imagined peaks.
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