FROM python:3.13-slim
ENV POETRY_VIRTUALENSVS_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000

# docker build -t "fastapi_zero" .
# docker compose build
# docker run -it --name fastzeroapp -p 8000:8000 fastapi_zero
