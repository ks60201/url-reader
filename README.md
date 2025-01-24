This project is an AI-powered chatbot that extracts information from a given URL, processes the data, generates answers using DeepSeek's API, and stores the question-answer pairs in Amazon S3 and Redis. The system is designed to be scalable and production-ready, with features like asynchronous processing, task queues, and caching.

Features
URL Text Extraction:

Extracts text from a given URL using BeautifulSoup.

Text Chunking:

Splits the extracted text into smaller chunks for efficient processing.

Embedding Generation:

Generates embeddings for text chunks using the SentenceTransformer model.

DeepSeek API Integration:

Uses DeepSeek's API to generate answers to user queries.

Data Storage:

Stores extracted text, embeddings, and question-answer pairs in Amazon S3.

Caches question-answer pairs in Redis for faster retrieval.

Scalability:

Uses Celery for task queue management and aiohttp for asynchronous HTTP requests.

Error Handling and Logging:

Comprehensive error handling and logging for reliability and debugging.

Prerequisites
Python 3.8+:

Install Python from python.org.

AWS Account:

Create an S3 bucket and generate AWS credentials.

DeepSeek API Key:

Sign up for DeepSeek's API and get your API key.

Redis:

Install and run Redis locally or use a cloud service.

Celery:

Install Celery for task queue management.

Installation
Clone the Repository:

bash
Copy
git clone https://github.com/your-username/url-chatbot.git
cd url-chatbot
Install Dependencies:

bash
Copy
pip install -r requirements.txt
Set Environment Variables:
Create a .env file in the root directory and add the following:

plaintext
Copy
AWS_ACCESS_KEY=your-aws-access-key
AWS_SECRET_KEY=your-aws-secret-key
AWS_REGION=us-east-1
BUCKET_NAME=url-chatbot-data
DEEPSEEK_API_KEY=your-deepseek-api-key
REDIS_URL=redis://localhost:6379/0
Download NLTK Data:

bash
Copy
python -c "import nltk; nltk.download('punkt')"
Running the Project
Start Redis:

bash
Copy
redis-server
Start Celery Worker:

bash
Copy
celery -A chatbot worker --loglevel=info
Run the Main Script:

bash
Copy
python chatbot.py
Sample Output
Input
python
Copy
url = "https://example.com"
question = "What is the main topic of the article?"
Output
plaintext
Copy
Task ID: 550e8400-e29b-41d4-a716-446655440000
Answer: The main topic of the article is the importance of scalable AI systems in modern technology.
Logs
plaintext
Copy
INFO:root:Uploaded to S3: texts/https_example.com.txt
INFO:root:Uploaded to S3: embeddings/https_example.com.json
INFO:root:Uploaded to S3: qa_pairs/20231010120000.json
S3 Bucket Contents
texts/https_example.com.txt: Extracted text from the URL.

embeddings/https_example.com.json: Embeddings for the text chunks.

qa_pairs/20231010120000.json: Question-answer pair stored in JSON format.

Redis Cache
Key: qa:1696944000.123456

Value:

json
Copy
{
  "question": "What is the main topic of the article?",
  "answer": "The main topic of the article is the importance of scalable AI systems in modern technology.",
  "timestamp": "2023-10-10T12:00:00.123456"
}
API Documentation
Endpoints
POST /ask:

Request Body:

json
Copy
{
  "url": "https://example.com",
  "question": "What is the main topic of the article?"
}
Response:

json
Copy
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success"
}
GET /result/{task_id}:

Response:

json
Copy
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "answer": "The main topic of the article is the importance of scalable AI systems in modern technology."
}
Contributing
Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature-branch).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
