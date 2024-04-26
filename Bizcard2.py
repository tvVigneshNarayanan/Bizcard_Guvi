import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
from pymongo import MongoClient
import io

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bizcard"]
collection = db["business_cards"]

# SETTING PAGE CONFIGURATIONS
icon = Image.open("C:\\Users\\Vignesh T\\Downloads\\1.png")
st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR | By Vignesh T",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This project aims for extracting data from business card*!"""})
st.markdown("<h1 style='text-align: center; color: Green;'>BizCardX: Extracting Business Card Data with OCR</h1>",
            unsafe_allow_html=True)

# SETTING-UP BACKGROUND IMAGE
def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background:url("https://wallpapers.com/images/featured/plain-zoom-background-d3zz0xne0jlqiepg.jpg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)


setting_bg()

# CREATING OPTION MENU
selected = option_menu(None, ["Home", "Upload & Modify", "Delete"],
                       icons=["house", "cloud-upload", "pencil-square"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "35px", "text-align": "centre", "margin": "-3px",
                                            "--hover-color": "#545454"},
                               "icon": {"font-size": "35px"},
                               "container": {"max-width": "6000px"},
                               "nav-link-selected": {"background-color": "#ff5757"}})

# HOME MENU
if selected == "Home":
    col1, col2 = st.columns(2)
    with col1:
        st.image(Image.open("C:\\Users\\Vignesh T\\Downloads\\1.png"), width=500)
        st.markdown("## :green[**Technologies Used :**] Python,easy OCR, Streamlit, MongoDB, Pandas")
    with col2:
        st.write(
            "## :green[**About :**] Bizcard is a Python application designed to extract information from business cards.")
        st.write(
            '## The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')

# DELETE MENU
if selected == "Delete":
    # Implementation for delete operation in MongoDB
    pass

# extract the data
def extracted_text(picture):
    # Implementation for extracting data from the OCR result
    pass

if selected == "Upload & Modify":
    image = st.file_uploader(label="Upload the image", type=['png', 'jpg', 'jpeg'], label_visibility="hidden")

    @st.cache_data
    def load_image():
        reader = easyocr.Reader(['en'], model_storage_directory=".")
        return reader

    reader_1 = load_image()
    if image is not None:
        input_image = Image.open(image)
        # Setting Image size
        st.image(input_image, width=350, caption='Uploaded Image')
        st.markdown(
            f'<style>.css-1aumxhk img {{ max-width: 300px; }}</style>',
            unsafe_allow_html=True
        )

        result = reader_1.readtext(np.array(input_image), detail=0)

        # creating dataframe
        ext_text = extracted_text(result)
        df = pd.DataFrame(ext_text)
        st.dataframe(df)
        # Converting image into bytes
        image_bytes = io.BytesIO()
        input_image.save(image_bytes, format='PNG')
        image_data = image_bytes.getvalue()

        # Insert data into MongoDB
        data = {
            "Name": ext_text["Name"],
            "Designation": ext_text["Designation"],
            "Company name": ext_text["Company name"],
            "Contact": ext_text["Contact"],
            "Email": ext_text["Email"],
            "Website": ext_text["Website"],
            "Address": ext_text["Address"],
            "Pincode": ext_text["Pincode"],
            "Image": image_data
        }
        collection.insert_one(data)

        st.success('SUCCESSFULLY UPLOADED', icon="✅")
    else:
        st.write("Upload an image")
