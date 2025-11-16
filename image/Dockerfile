FROM python:3.11-slim

RUN useradd -m flaskuser
WORKDIR /app
RUN chown flaskuser:flaskuser /app
USER flaskuser

COPY --chown=flaskuser:flaskuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

CMD ["python", "/app/src/run.py"]
