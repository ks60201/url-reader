import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import nltk
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import boto3
import json
import logging
from celery import Celery
import redis

# Configuration
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
BUCKET_NAME = os.getenv('BUCKET_NAME', 'url-chatbot-data')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Initialize Redis client
redis_client = redis.from_url(REDIS_URL)

# Initialize Celery
celery_app = Celery('chatbot', broker=REDIS_URL)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Download NLTK data (only needed once)
nltk.download('punkt')

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Async HTTP client session
async def get_http_session():
    return aiohttp.ClientSession()

# Upload data to S3
def upload_to_s3(data, key):
    try:
        if isinstance(data, dict):
            data = json.dumps(data)
        s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=data)
        logger.info(f"Uploaded to S3: {key}")
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")

# Download data from S3
def download_from_s3(key):
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        logger.error(f"Error downloading from S3: {e}")
    return None

# Extract text from URL
async def extract_text_from_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()

                # Store the extracted text in S3
                key = f"texts/{url.replace('/', '_')}.txt"
                upload_to_s3(text, key)

                return text
    except Exception as e:
        logger.error(f"Error extracting text from URL: {e}")
        return None

# Chunk text
def chunk_text(text, chunk_size=500):
    sentences = nltk.sent_tokenize(text)
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    return chunks

# Generate embeddings
def generate_embeddings(chunks):
    embeddings = model.encode(chunks)

    # Store embeddings in S3
    key = f"embeddings/{url.replace('/', '_')}.json"
    upload_to_s3({"embeddings": embeddings.tolist()}, key)

    return embeddings

# Get answer from DeepSeek API
async def get_deepseek_answer(question, context):
    try:
        api_url = "https://api.deepseek.com/v1/answer"
        payload = {
            "question": question,
            "context": context
        }
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers) as response:
                result = await response.json()
                return result['answer']
    except Exception as e:
        logger.error(f"Error calling DeepSeek API: {e}")
        return None

# Store QA pair in Redis and S3
def store_qa_pair(question, answer):
    qa_pair = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    }

    # Store QA pair in Redis
    redis_client.set(f"qa:{datetime.now().timestamp()}", json.dumps(qa_pair))

    # Store QA pair in S3
    key = f"qa_pairs/{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    upload_to_s3(qa_pair, key)

# Celery task for processing URLs
@celery_app.task
def process_url(url, question):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(ask_question(url, question))

# Main function to process a URL and answer a question
async def ask_question(url, question):
    # Step 1: Extract text from URL
    text = await extract_text_from_url(url)
    if not text:
        return "Error: Unable to extract text from the URL."

    # Step 2: Chunk the text
    chunks = chunk_text(text)

    # Step 3: Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Step 4: Generate embedding for the question
    question_embedding = model.encode([question])[0]

    # Step 5: Find the most relevant chunk
    similarities = cosine_similarity([question_embedding], embeddings)
    most_relevant_chunk_index = np.argmax(similarities)
    relevant_chunk = chunks[most_relevant_chunk_index]

    # Step 6: Get answer from DeepSeek API
    answer = await get_deepseek_answer(question, relevant_chunk)
    if not answer:
        return "Error: Unable to generate an answer."

    # Step 7: Store QA pair
    store_qa_pair(question, answer)

    return answer

# Example usage
if __name__ == '__main__':
    url = "https://example.com"  # Replace with your URL
    question = "What is the main topic of the article?"  # Replace with your question

    # Run the task asynchronously
    result = process_url.delay(url, question)
    print("Task ID:", result.id)
    print("Answer:", result.get(timeout=10))  # Wait for the result