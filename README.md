# DocM - Intelligent Document Management

## Overview
DocM is a cutting-edge document management system designed to streamline document processing, extraction, and organization. By leveraging advanced AI capabilities, a robust backend infrastructure, and an intuitive user interface, DocM transforms unstructured information into structured, accessible data, ensuring seamless document management.

## Key Features
-  Optical Character Recognition (OCR): Extracts text from scanned documents and images with high accuracy.
-  Named Entity Recognition (NER): Identifies and categorizes key entities within documents, facilitating structured data extraction.
-  Metadata Extraction: Captures and indexes relevant metadata for efficient document retrieval.
-  Large Language Model (LLM) Integration: Enhances document comprehension and contextual analysis.
-  Django-Powered Backend: Provides a scalable, secure, and efficient backend architecture.
-  Intuitive UI/UX: Offers a seamless and user-friendly document handling experience.
- Optimized Frontend with Tailwind CSS: Ensures a visually appealing, responsive, and efficient user interface.

## Tech Stack
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Backend:** Django
- **AI & NLP:** Optical Character Recognition (OCR), Named Entity Recognition (NER), LLM APIs
- **Database:** Neon PostgreSQL
- **Version Control:** Git & GitHub

## Team members

- Mohit Madhu(Team Lead): AI, OCR and NER
- Kaustubh Kadam: Frontend and Backend
- Mayank: Frontend
- Shrinivas: UI/UX
- Sambhav: API, AI and LLMOPS

## Installation Steps
To set up and run DocM locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/KadamKaustubh147/ai_doc_manager
   ```

2. Set up a virtual environment and install dependencies:
   ```sh
   # On Linux/MacOS
   python3 -m venv .venv
   source .venv/bin/activate  
   # On Windows: 
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Navigate to the project directory:
   ```sh
   cd AiDocManager/
   ```


4. Start the development server:
   ```sh
   python manage.py runserver
   ```

5. Install tailwind css:
   ```sh
   python manage.py tailwind install
   ```


5. Access the application in your browser:
   ```
   http://127.0.0.1:8000/
   ```
