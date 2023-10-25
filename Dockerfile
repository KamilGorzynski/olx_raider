FROM python:3.10.0b3-slim

COPY chromedriver .
COPY headless-chromium .

COPY lambda_function.py .

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update

RUN apt-get install -y  libnss3
RUN apt-get install -y  libgtk-3-0
RUN apt-get install -y  libssl-dev

RUN chmod +x chromedriver

RUN chmod +x headless-chromium

CMD ["python", "lambda_function.py"]