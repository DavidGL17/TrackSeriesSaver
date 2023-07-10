# Dockerfile to launch the python app
FROM python:3.9
WORKDIR /app

# copy only the files needed to install dependencies
RUN pip install poetry
COPY pyproject.toml poetry.toml /app/
RUN poetry install

# copy the rest of the files
COPY . /app
# copy the settings file, and everything in the trackseriessaver folder
COPY settings.py /app/
COPY trackseriessaver /app/trackseriessaver

CMD ["poetry", "run", "trackseriessaver"]