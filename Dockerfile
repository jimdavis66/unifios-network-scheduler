# syntax=docker/dockerfile:1
FROM python:3.9.19-slim-bullseye
RUN pip install requests python-dotenv schedule
COPY app .
CMD ["python", "-u", "app.py"]