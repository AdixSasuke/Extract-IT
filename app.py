import streamlit as st
import pytesseract
from PIL import Image
import tempfile
import os
from pdf2image import convert_from_path, convert_from_bytes
from bs4 import BeautifulSoup

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set page config
st.set_page_config(
    page_title="Extract-It: HOCR Text Extraction Tool",
    page_icon="📝",
    layout="wide"
)

def extract_text_from_hocr(hocr_bytes):
    """Extract text from HOCR format with better formatting preservation"""
    soup = BeautifulSoup(hocr_bytes, 'html.parser')
    
    # Find all text elements in the HOCR (ocr_line elements contain line information)
    lines = soup.find_all('span', class_='ocr_line')
    
    formatted_text = []
    for line in lines:
        # Extract all words from this line
        words = line.find_all('span', class_='ocrx_word')
        line_text = ' '.join([word.get_text().strip() for word in words])
        if line_text.strip():
            formatted_text.append(line_text)
    
    return '\n'.join(formatted_text)

@st.cache_data
def extract_text_from_image(_image):
    """Extract text from an image using Tesseract OCR with HOCR format"""
    # Use HOCR format for better formatting preservation
    hocr_bytes = pytesseract.image_to_pdf_or_hocr(_image, extension='hocr')
    return extract_text_from_hocr(hocr_bytes)

def process_pdf(pdf_file):
    """Convert PDF to images and extract text"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        temp_pdf.write(pdf_file.read())
        pdf_path = temp_pdf.name
    
    try:
        # Convert PDF pages to images
        images = convert_from_bytes(open(pdf_path, 'rb').read())
        
        all_text = []
        for i, img in enumerate(images):
            st.subheader(f"Page {i+1}")
            st.image(img, width=600)
            
            # Extract text from the image using HOCR
            text = extract_text_from_image(img)
            all_text.append(text)
            
        return all_text
    finally:
        # Clean up temporary file
        os.unlink(pdf_path)

def main():
    st.title("Extract-It: HOCR Text Extraction Tool")
    st.write("Upload an image or PDF file to extract text while preserving formatting") 
    uploaded_file = st.file_uploader("Choose an image or PDF file", type=['png', 'jpg', 'jpeg', 'tiff', 'pdf'])
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Document")
            
            if uploaded_file.name.lower().endswith('.pdf'):
                # Process PDF
                extracted_texts = process_pdf(uploaded_file)
                
                # Display all extracted text
                with col2:
                    st.subheader("Extracted Text (HOCR)")
                    for i, text in enumerate(extracted_texts):
                        st.subheader(f"Text from Page {i+1}")
                        st.text_area(f"Extracted text from page {i+1}", text, height=300, key=f"text_{i}")
                        
                        # Add download button for each page
                        st.download_button(
                            label=f"Download Text from Page {i+1}",
                            data=text,
                            file_name=f"extracted_text_page_{i+1}.txt",
                            mime="text/plain",
                            key=f"download_{i}"
                        )
            else:
                # Process image
                image = Image.open(uploaded_file)
                st.image(image, width=600)
                
                with col2:
                    st.subheader("Extracted Text (HOCR)")
                    
                    # Extract text using HOCR
                    with st.spinner("Extracting text using HOCR..."):
                        extracted_text = extract_text_from_image(image)
                    
                    # Display extracted text
                    st.text_area("Extracted text", extracted_text, height=400)
                    
                    # Add download button
                    st.download_button(
                        label="Download Extracted Text",
                        data=extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )

if __name__ == "__main__":
    main()