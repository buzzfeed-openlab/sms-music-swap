from python:3.5

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "application.py"]
