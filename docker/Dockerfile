FROM python:alpine3.18

RUN apk update &&  \
    apk --no-cache add \
    gcc \
    musl-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    libffi-dev \
    shared-mime-info

WORKDIR /app

COPY ./app .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
