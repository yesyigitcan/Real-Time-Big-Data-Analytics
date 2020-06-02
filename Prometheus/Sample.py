from flask import Flask, Response, Request
from prometheus_client import start_http_server, Summary, generate_latest, Counter
import random
import time

app = Flask(__name__)
# Create a metric to track time spent and requests made.
COUNTER = Counter('my_basic_counter', 'A basic counter')

# Decorate function with metric.
@app.route("/metrics")
def process_request(t):
    """A dummy function that takes some time."""
    COUNTER.inc()
    time.sleep(1)
    return Response(generate_latest())

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    print(__name__)
    while True:
        process_request(random.random())