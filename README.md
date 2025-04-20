# Legal Document Assistant

A powerful web-based application designed to simplify legal document analysis using advanced AI technology. This tool helps legal professionals and users analyze documents, generate summaries, extract key information, and get AI-powered responses to legal queries.

## Features

- **Document Analysis**: Upload and analyze legal documents with AI-powered insights
- **Smart Classification**: Automatically categorizes documents into relevant legal categories
- **Key Phrase Extraction**: Identifies and extracts important legal terms and phrases
- **Document Summarization**: Generates concise summaries of legal documents
- **Interactive Chat**: Ask questions about your documents and receive AI-generated responses
- **Professional Drafting**: Generate professional response drafts based on legal context
- **Detailed Analysis**: Option for in-depth analysis with legal references

## Technology Stack

- Python Flask web framework
- WorqHat AI for language processing
- Modern web interface with responsive design

## Setup Instructions

1. Clone the repository
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your API key:
     ```
     WORQHAT_API_KEY=your_api_key_here
     ```

## Usage

1. Start the application:
   ```
   python app.py
   ```
2. Access the web interface through your browser
3. Upload a legal document
4. Use the various analysis tools and features:
   - Get document summaries
   - View key phrases
   - Ask questions about the document
   - Generate professional responses

## Security

- Secure API key handling through environment variables
- No document storage - all processing done in memory
- HTTPS support for secure data transmission