## News Aggregator System

### Introduction
This project aims to build a prototype news aggregator system that fetches news from the TSN RSS feed, identifies trending news using Google Trends data, calculates sentiment scores for matching news articles, and provides an API endpoint to access relevant news.

### Development Part

#### Technologies Used
- Python
- Django
- Celery
- RabbitMQ
- Google Trends API
- ChatGPT API

#### Setup
1. Clone this repository.
```bash
git clone https://github.com/YuliaHladyshkevych/news-aggregator.git
```
2. You can open project in IDE and configure .env file using .env.sample file 
as an example.
3. Build and run the Docker containers:
    ````bash
    docker-compose up --build
The API will be accessible at http://localhost:8000/.

#### Functionality
- Fetches news from TSN RSS feed.
- Identifies trending news using Google Trends data.
- Calculates sentiment scores for matching news articles using ChatGPT API.
- Provides an API endpoint to access relevant news.

#### API Endpoint
- `/api/trending-news`: Retrieves relevant news articles with headline, source link, publication date, sentiment score, and trending topic names. The news articles are sorted by sentiment score in descending order.
