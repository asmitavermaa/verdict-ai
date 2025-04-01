import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WorqHat API configuration
WORQHAT_API_KEY = os.getenv('WORQHAT_API_KEY', 'wh_m8ysgq9rVBiKq103lz3Cbcr2wa0VOBElUMurlpz')

class WorqHatClient:
    """Client for interacting with WorqHat AI APIs"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or WORQHAT_API_KEY
        self.base_url = "https://api.worqhat.com/api/ai/content/v4"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt, context="", max_tokens=1000):
        """Generate text using WorqHat's AI models
        
        Args:
            prompt (str): The user's query or instruction
            context (str): Additional context for the AI to consider
            max_tokens (int): Maximum number of tokens to generate
            
        Returns:
            str: The generated text response
        """
        try:
            # Combine context and prompt if context is provided
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Prepare the request payload
            payload = {
                "question": full_prompt,
                "model": "aicon-v4-large-160824",  # Using the large model for better legal responses
                "randomness": 0.2,  # Lower randomness for more consistent legal responses
                "stream_data": False
            }
            
            # Make the API request to WorqHat's Content Generation API
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                return result.get('content', 'No content generated')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error generating text: {str(e)}"
    
    def summarize_text(self, text, max_tokens=500):
        """Summarize text using WorqHat's AI models
        
        Args:
            text (str): The text to summarize
            max_tokens (int): Maximum number of tokens in the summary
            
        Returns:
            str: The generated summary
        """
        try:
            # Prepare the request payload
            payload = {
                "question": f"Please summarize the following text:\n\n{text}",
                "model": "aicon-v4-large-160824",  # Using the large model for better summaries
                "randomness": 0.1,  # Lower randomness for more consistent summaries
                "stream_data": False
            }
            
            # Make the API request to WorqHat's Content Generation API
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                return result.get('content', 'No summary generated')
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def classify_document(self, text):
        """Classify a legal document using WorqHat's AI models
        
        Args:
            text (str): The document text to classify
            
        Returns:
            str: The document category
        """
        try:
            # Prepare the request payload with a prompt that asks for document classification
            payload = {
                "question": f"Classify the following legal document into one of these categories: Legal Notice, Ownership Documents, Contracts & Agreements, Financial Documents, Terms & Conditions / Privacy Policies, Intellectual Property Documents, Criminal Offense Documents, Regulatory Compliance Documents, Employment Documents, Court Judgments & Legal Precedents.\n\nDocument text:\n{text[:3000]}\n\nCategory:",
                "model": "aicon-v4-large-160824",  # Using the large model for better classification
                "randomness": 0.1,
                "stream_data": False
            }
            
            # Make the API request
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                category = result.get('content', '').strip()
                
                # Ensure the category is one of the predefined categories
                valid_categories = [
                    'Legal Notice', 'Ownership Documents', 'Contracts & Agreements',
                    'Financial Documents', 'Terms & Conditions / Privacy Policies',
                    'Intellectual Property Documents', 'Criminal Offense Documents',
                    'Regulatory Compliance Documents', 'Employment Documents',
                    'Court Judgments & Legal Precedents'
                ]
                
                # Return the category if valid, otherwise a default
                if any(valid_cat in category for valid_cat in valid_categories):
                    # Extract the matching category
                    for valid_cat in valid_categories:
                        if valid_cat in category:
                            return valid_cat
                    return category
                else:
                    return 'Contracts & Agreements'  # Default category
            else:
                return "Contracts & Agreements"  # Default category on error
                
        except Exception as e:
            return "Contracts & Agreements"  # Default category on exception
    
    def extract_key_phrases(self, text):
        """Extract key phrases from a legal document
        
        Args:
            text (str): The document text to analyze
            
        Returns:
            list: List of key phrases
        """
        try:
            # Prepare the request payload
            payload = {
                "question": f"Extract 5-10 key legal phrases or terms from the following document. Return them as a comma-separated list.\n\nDocument text:\n{text[:3000]}",
                "model": "aicon-v4-large-160824",  # Using the large model for better extraction
                "randomness": 0.1,
                "stream_data": False
            }
            
            # Make the API request
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                phrases_text = result.get('content', '')
                
                # Split the comma-separated list into individual phrases
                phrases = [phrase.strip() for phrase in phrases_text.split(',') if phrase.strip()]
                return phrases
            else:
                return ["Error extracting key phrases"]
                
        except Exception as e:
            return [f"Error: {str(e)}"]

# Create a global instance for use throughout the application
worqhat_client = WorqHatClient()

# Functions that mirror the existing multiagent interface

def respond_to_query(query, context=""):
    """Generate a response to a user query using WorqHat AI
    
    Args:
        query (str): The user's question
        context (str): Additional context for the AI
        
    Returns:
        str: The AI-generated response
    """
    return worqhat_client.generate_text(query, context)

def analyze_tone(text):
    """Analyze the tone of a legal document
    
    Args:
        text (str): The document text to analyze
        
    Returns:
        str: Tone analysis result
    """
    prompt = f"Analyze the tone of this legal document. Is it formal, aggressive, conciliatory, neutral, or mixed? Justify your analysis briefly.\n\n{text[:2000]}"
    return worqhat_client.generate_text(prompt)

def summarize_document(text):
    """Summarize a legal document
    
    Args:
        text (str): The document text to summarize
        
    Returns:
        str: Document summary
    """
    return worqhat_client.summarize_text(text)

# Create replacement functions for the existing NLP utilities

class DocumentClassifier:
    """Classifier for legal documents using WorqHat AI"""
    
    def classify(self, text):
        """Classify a legal document
        
        Args:
            text (str): The document text to classify
            
        Returns:
            str: The document category
        """
        return worqhat_client.classify_document(text)

class DocumentProcessor:
    """Processor for legal documents using WorqHat AI"""
    
    def get_summary(self, text):
        """Generate a summary of a legal document
        
        Args:
            text (str): The document text to summarize
            
        Returns:
            str: Document summary
        """
        return worqhat_client.summarize_text(text)
    
    def extract_key_phrases(self, text):
        """Extract key phrases from a legal document
        
        Args:
            text (str): The document text to analyze
            
        Returns:
            list: List of key phrases
        """
        return worqhat_client.extract_key_phrases(text)