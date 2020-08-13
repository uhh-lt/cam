FROM python:3.6.1
RUN pip install --upgrade pip
RUN pip install pipenv

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install dependencies.
RUN pipenv install

# Download machine learning files.
RUN pipenv run python -m nltk.downloader stopwords
RUN pipenv run python -m nltk.downloader punkt
RUN pipenv run python -m nltk.downloader averaged_perceptron_tagger

# Run main.py when the container launches.
CMD pipenv run python main.py reader reader
