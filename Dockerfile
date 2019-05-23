FROM python:3.7-alpine

RUN apk add --no-cache tzdata
ENV TZ America/Los_Angeles

WORKDIR . /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["flask", "run", "-h", "0.0.0.0"]
CMD [ "python", "app.py"]
EXPOSE 5000

#http://0.0.0.0:5000/