FROM python:3.4-alpine

WORKDIR . /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["flask", "run", "-h", "0.0.0.0"]
CMD [ "python", "app.py"]
EXPOSE 5000