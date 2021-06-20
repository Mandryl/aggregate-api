FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 80

COPY ./ /app

WORKDIR /app

RUN pip install -U pip && \
    pip install --no-cache-dir pipenv && \
    pipenv install --system --ignore-pipfile --deploy && \
    pipenv --clear
