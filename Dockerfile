FROM python:3.9

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app

CMD ["poetry", "run", "start"]
