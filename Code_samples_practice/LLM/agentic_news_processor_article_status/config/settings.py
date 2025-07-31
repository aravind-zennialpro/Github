import os


BASE_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "fd5dd9059e6c423ab6d91ea447f2e72d"
DEFAULT_QUERY = "bitcoin"
MAX_PAGES = 2
PAGE_SIZE = 5
LOG_DIR = "logs"
ARTICLE_STORE_BASE = "article_store"
QUEUE_DIR = os.path.join(ARTICLE_STORE_BASE, "queue")