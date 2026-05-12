from redis import Redis
from rq import Queue
from .config import REDIS_URL

redis_conn = Redis.from_url(REDIS_URL)
queue = Queue("pdf_to_pptx", connection=redis_conn)
