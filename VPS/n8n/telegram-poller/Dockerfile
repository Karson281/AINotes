FROM python:3.11-slim
WORKDIR /app
COPY poller.py .
RUN pip install requests --quiet
CMD ["python", "-u", "poller.py"]
