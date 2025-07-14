import os
import redis
from rq import Worker, Queue
from rq.worker import SimpleWorker

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
conn = redis.from_url(redis_url)

if __name__ == "__main__":
    queue = Queue(connection=conn)
    worker = SimpleWorker([queue], connection=conn)
    worker.work()  estava assim,   ficou assim : import os
import redis
from rq import Worker, Queue, Connection

redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
conn = redis.from_url(redis_url)

if __name__ == "__main__":
    with Connection(conn):
        queue = Queue()
        worker = Worker([queue])
        worker.work()