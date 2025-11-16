from app import app, create_runtime
from waitress import serve
import signal
import sys

def shutdown_handler(sig, frame):
    print("[GDA] Signal caught, exiting...")
    sys.exit(0)

if __name__ == "__main__":
    print("[GDA] Early Startup")
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    create_runtime()
    serve(app, host="0.0.0.0", port=8080, threads=4)
