# Extract-It

A Streamlit-based application for extracting text from images and PDFs while maintaining text formatting.

## Features

-   Upload images (PNG, JPG, JPEG, TIFF) or PDF files
-   Extract text with preserved formatting
-   View extracted text alongside the original document
-   Download extracted text as a text file
-   Support for multi-page PDF documents

## Installation

1. Ensure you have Python 3.7+ installed
2. Install Tesseract OCR:
    - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
    - macOS: `brew install tesseract`
    - Linux: `sudo apt-get install tesseract-ocr`
3. Install required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at http://localhost:8501

## How to Use

1. Upload an image or PDF file using the file uploader
2. The application will display the original document on the left
3. Extracted text will appear on the right side
4. You can download the extracted text using the "Download Extracted Text" button

## Note

For best results:

-   Use clear, high-resolution images
-   Ensure text in the image is readable and properly oriented
-   For PDF files, make sure they contain actual text or high-quality scans
