FROM python:3.9

WORKDIR /code/scrapper

COPY scrapper_packages.txt ./
RUN pip install -r scrapper_packages.txt

ENV NUM_THREADS=40

COPY . .

CMD [ "python", "./scrapper.py" ]