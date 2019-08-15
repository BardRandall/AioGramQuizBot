FROM python:3.7

WORKDIR /app

COPY requirements.txt data.json /app/

RUN pip3 install -r requirements.txt

COPY core/ /app/core/

CMD ["python3", "-m", "core"]
