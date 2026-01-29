FROM python:3.13.5-slim
WORKDIR /app
EXPOSE 8000/tcp
SHELL ["/bin/sh", "-exc"]
RUN apt update && apt install bat -y

COPY --link --from=ghcr.io/astral-sh/uv:0.4 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync

RUN mkdir upload_files
COPY .env .env
COPY app.py config.py ./

COPY ./src ./src

# CMD uv run main.py
CMD uv run uvicorn app:app --host=0.0.0.0