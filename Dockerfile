FROM python:3.11

COPY requirements.txt /workdir/
COPY app.py/ /workdir/app.py/
COPY backend.py/ /workdir/backend.py/
COPY vector_db/ /workdir/vector_db


WORKDIR /workdir
RUN pip install -r requirements.txt
#RUN pip install -U -e .

# Run the application
CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]