
# extractor-pptx

Microservice for extracting and processing data from images and PPTX files, designed for Jet Rent a Car.

## Description
This service uses FastAPI to expose endpoints that allow:
- Extracting numeric tables from images using OCR (Tesseract).
- Classifying environmental labels by color in images.
- Processing PPTX files to extract texts and images, automatically classifying images by type (sticker, table, car).

## Main Structure
- `main.py`: FastAPI API with endpoints to process images and PPTX files.
- `extractor.py`: Logic for extracting numeric tables from images using OCR.
- `etiqueta.py`: Classification of environmental labels by color using OpenCV.
- `requirements.txt`: Required Python dependencies.
- `Dockerfile`: Production-ready Docker image, with Tesseract and system dependencies.

## Main Endpoints

### POST `/parse-table`
- **Description:** Extracts a numeric table from an image.
- **Parameters:**
  - `file`: Image (format supported by PIL).
  - `name`: Name of the image.
- **Response:** JSON with the extracted table.

### POST `/parse-etiqueta`
- **Description:** Classifies an environmental label by color.
- **Parameters:**
  - `file`: Label image.
  - `name`: Name of the image.
- **Response:** JSON with the detected label and color percentages.

### POST `/parse-pptx`
- **Description:** Processes a PPTX file, extracting texts and images from each slide.
- **Parameters:**
  - `file`: PPTX file.
- **Response:** JSON with texts and images classified by slide.

## Installation and Usage

### Docker
1. Build the image:
   ```sh
   docker build -t extractor-pptx .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 extractor-pptx
   ```

### Local (requirements: Python 3.11, Tesseract, poppler-utils, OpenCV, Pillow)
1. Install dependencies:
   ```sh
   pip install -r app/requirements.txt
   ```
2. Run the server:
   ```sh
   uvicorn app.main:app --reload
   ```

## Notes
- The OCR model uses the Spanish language (`spa.traineddata`).
- The `/parse-pptx` endpoint automatically classifies extracted images.

## Author
Alonso Gómez Jiménez

---

For questions or improvements, contact the development team.
