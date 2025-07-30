import streamlit as st
from PIL import Image
import requests
import base64
import io
import re

def format_name(name):
    formatted_name = name
    
    formatted_name = formatted_name.replace("\\", " ")
    formatted_name = formatted_name.replace("/", " ")
    formatted_name = formatted_name.replace("105_classes_pins_dataset", " ")
    formatted_name = formatted_name.replace("bollywood_celeb_faces", " ")
    formatted_name = formatted_name.replace(".jpg", " ")
    formatted_name = formatted_name.replace(".png", " ")
    formatted_name = formatted_name.replace(".jpeg", " ")
    
    # remove underscores
    formatted_name = formatted_name.replace("_", " ")
    # remove numbers
    formatted_name = re.sub(r'\d', '', formatted_name)
    formatted_name = formatted_name.replace("\\", " ")
    # remove extra spaces
    formatted_name = re.sub(r'\s+', ' ', formatted_name)
    
    if "pins" in formatted_name:
        formatted_name = formatted_name.replace("pins", " ")
        # substring first half
        formatted_name = formatted_name[:int(len(formatted_name) / 2) + 1]
    
    # trim
    formatted_name = formatted_name.strip()
    # capitalize
    formatted_name = formatted_name.capitalize()
    
    return formatted_name

# Function to convert image to base64
def convert_to_base64(uploaded_file):
    # Read the file as bytes
    image_bytes = uploaded_file.read()

    # Encode the bytes to base64
    base64_bytes = base64.b64encode(image_bytes)

    # Convert bytes to string
    base64_string = base64_bytes.decode('utf-8')

    return base64_string

# Function to send image to API and get processed image
def process_image(image_base64):
    api_endpoint = "https://manavsarkar07-trial.hf.space/predict-actor/"  # Replace this with your API endpoint
    payload = {"base64_data": image_base64}
    response = requests.post(api_endpoint, json=payload)
    response_data = response.json()
    return response_data

# Streamlit app
def main():
    st.set_page_config(page_title="Celebrity Prediction App", page_icon=":guardsman:", layout="wide")
    st.title("Celebrity Prediction App")
    st.subheader("Check if your face matches with your favorite celebrity!")

    
    # image = st.camera_input("Click a selfie")

    # upload_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])    
    
    tab1, tab2 = st.tabs(["Camera", "Image Upload"])

    with tab1:
        image = st.camera_input("Click a selfie")

    with tab2:
        upload_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if upload_file is not None:
        image = upload_file
    
    # If image is uploaded via camera or file uploader
    if image is not None:
        # Display image
        # st.image(image, caption="Uploaded Image", use_column_width=True)
        base64_string = convert_to_base64(image)
        base64_string = "data:image/jpeg;base64," + base64_string
        # confirm button
        if st.button("Check Now!"):
            # loading bar
            with st.spinner("Searching for celebrity..."):

                response_data = process_image(base64_string)
                
                # Get processed image
                processed_image_base64 = response_data["celeb_image"]
                
                celebrity_name = response_data["celeb"]

                predicted_age = response_data["res"]["age"]
                predicted_gender = response_data["res"]["gender"]
                # Display processed image
                image = Image.open(io.BytesIO(base64.b64decode(processed_image_base64)))
                st.image(image, caption=format_name(celebrity_name), use_container_width=True)
                st.write(f"You look like {format_name(celebrity_name)}")
                st.write(f"Predicted Age: {predicted_age}")
                st.write(f"Predicted Gender: {predicted_gender}")


           
if __name__ == "__main__":
    main()
