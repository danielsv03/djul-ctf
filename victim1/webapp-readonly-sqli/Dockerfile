FROM python:3.11-slim

WORKDIR /app
COPY app.py /app/
# We'll COPY ctf_readonly.db into /data inside the image; later we ensure it's read-only
COPY ctf_readonly.db /data/ctf_readonly.db

RUN pip install --no-cache-dir flask

EXPOSE 8000
CMD ["python","app.py"]