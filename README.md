# **AI-Powered URL Information Chatbot**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AWS](https://img.shields.io/badge/AWS-S3-orange)
![Redis](https://img.shields.io/badge/Redis-Caching-red)
![Celery](https://img.shields.io/badge/Celery-Task%20Queue-green)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-yellow)

This project is an **AI-powered chatbot** that extracts information from a given URL, processes the data, generates answers using DeepSeek's API, and stores the question-answer pairs in **Amazon S3** and **Redis**. The system is designed to be **scalable** and **production-ready**, with features like asynchronous processing, task queues, and caching.

---

## **Features**

- **URL Text Extraction**: Extracts text from a given URL using `BeautifulSoup`.
- **Text Chunking**: Splits the extracted text into smaller chunks for efficient processing.
- **Embedding Generation**: Generates embeddings for text chunks using the `SentenceTransformer` model.
- **DeepSeek API Integration**: Uses DeepSeek's API to generate answers to user queries.
- **Data Storage**: Stores extracted text, embeddings, and question-answer pairs in **Amazon S3** and caches QA pairs in **Redis**.
- **Scalability**: Uses **Celery** for task queue management and **aiohttp** for asynchronous HTTP requests.
- **Error Handling and Logging**: Comprehensive error handling and logging for reliability and debugging.

---

## **Prerequisites**

1. **Python 3.8+**: Install Python from [python.org](https://www.python.org/).
2. **AWS Account**: Create an S3 bucket and generate AWS credentials.
3. **DeepSeek API Key**: Sign up for DeepSeek's API and get your API key.
4. **Redis**: Install and run Redis locally or use a cloud service.
5. **Celery**: Install Celery for task queue management.



