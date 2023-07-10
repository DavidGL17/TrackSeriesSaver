# Dockerfile to launch the python app
FROM python:3.9
WORKDIR /app

# copy only the files needed to install dependencies
RUN pip install poetry
COPY pyproject.toml poetry.toml /app/
RUN poetry install

# copy the settings file, and everything in the trackseriessaver folder
COPY settings.yml /app/settings.yml
COPY trackseriessaver /app/trackseriessaver

CMD ["poetry", "run", "trackseriessaver"]