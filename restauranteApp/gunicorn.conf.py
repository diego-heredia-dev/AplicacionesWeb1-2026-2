import multiprocessing
import os

bind = "0.0.0.0:5000"

workers = int(os.environ.get("GUNICORN_WORKERS", 3))

worker_class = "sync"

threads = int(os.environ.get("GUNICORN_THREADS", 1))

timeout = int(os.environ.get("GUNICORN_TIMEOUT", 30))

graceful_timeout = 30

keepalive = 5

max_requests = 1000

max_requests_jitter = 100

accesslog = "-"

errorlog = "-"

forwarded_allow_ips = "127.0.0.1"