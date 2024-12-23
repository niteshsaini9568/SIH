import streamlit as st
from PIL import Image
import google.generativeai as genai

# Set the page configuration at the top of the script
st.set_page_config(page_title="Image Recognition Chatbot", layout="wide")

# Configure the Google Generative AI with the provided API key
genai.configure(api_key="AIzaSyCTN7ONXDJRINqBZd-Oldp4CR0HFAPwxBs")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get the response from the generative model
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input_text:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

# Custom CSS for styling the app
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .chat-box {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 10px;
        }
        .chat-user {
            color: #007BFF;
            font-weight: bold;
        }
        .chat-bot {
            color: black;
            background-color: #d3d3d3;  /* Gray background */
            padding: 10px;
            border-radius: 10px;
            margin-top: 10px;
        }
        .uploaded-image {
            margin: 0 auto;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation and instructions
with st.sidebar:
    st.header("Navigation")
    st.write("Use the following options to interact with the chatbot:")
    st.markdown("- Upload an image.")
    st.markdown("- Ask a question about the uploaded image.")
    st.markdown("The chatbot will recognize objects in the image and provide relevant responses.")

# Main app title and instructions
st.title("Image Recognition Chatbot")
st.markdown("This chatbot recognizes objects in uploaded images and answers questions about them.")

# Display chat history in an expander to save space
with st.expander("Chat History", expanded=True):
    if st.session_state.chat_history:
        for message in st.session_state.chat_history:
            role_class = "chat-user" if message["role"] == "User" else "chat-bot"
            st.markdown(f"<div class='{role_class}'>{message['role']}: {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.write("No conversation history yet. Upload an image and start asking questions!")

# Input section
input_text = st.text_input("Ask a question about the image:", key="input")
uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"], key="upload")

image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True, output_format="auto")

# Button to submit the input and get the response
submit = st.button("Submit")

# If the submit button is clicked
if submit and image:
    response = get_gemini_response(input_text, image)
    
    # Add user input and bot response to chat history
    st.session_state.chat_history.append({"role": "User", "content": input_text})
    st.session_state.chat_history.append({"role": "Bot", "content": response})
    
    # Display the response
    st.subheader("The Response")
    st.markdown(f"<div class='chat-box chat-bot'>{response}</div>", unsafe_allow_html=True)
