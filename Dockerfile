FROM python:3.10-alpine as exporter

WORKDIR /app
RUN pip install --no-cache-dir --upgrade poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -vv --no-ansi --without-hashes --no-interaction --format requirements.txt --output requirements.txt


FROM python:3.10-alpine as builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=exporter /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.10-alpine

RUN apk update &&  \
    apk --no-cache add \
    gcc \
    musl-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    libffi-dev \
    shared-mime-info \
    fontconfig \
    ttf-dejavu \
    ttf-droid \
    ttf-freefont \
    ttf-liberation \
    ttf-opensans \
    ttf-inconsolata \
    curl \
    git

RUN git config --system --add safe.directory '*'

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /usr/app
CMD ["python", "/usr/app/src/main.py"]

COPY --from=builder /opt/venv /opt/venv
COPY . .