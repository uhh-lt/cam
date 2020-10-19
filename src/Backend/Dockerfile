FROM python:3.6.1
RUN pip install --upgrade pip
RUN pip install "pipenv>=2020.8.13"

# Set the working directory to /app
WORKDIR /app

# Install dependencies.
ADD Pipfile /app/Pipfile
ADD Pipfile.lock /app/Pipfile.lock
RUN pipenv install

# Download machine learning files.
RUN pipenv run python -m nltk.downloader stopwords
RUN pipenv run python -m nltk.downloader punkt
RUN pipenv run python -m nltk.downloader averaged_perceptron_tagger

# Copy the current directory contents into the container at /app
ADD . /app

# Run main.py when the container launches.
CMD pipenv run python main.py reader reader
