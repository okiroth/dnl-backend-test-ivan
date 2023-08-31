FROM python:3.9

WORKDIR /code/scrapper

COPY requirements.txt ./
RUN pip install -r requirements.txt

ENV NUM_THREADS=40

COPY . .

CMD [ "scrapy", "runspider", "./main.py", "-O quotes.jsonl" ]