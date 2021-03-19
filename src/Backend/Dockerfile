FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Install dependencies.
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Download machine learning files.
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger

# Copy the current directory contents into the container at /app
COPY . ./

EXPOSE 5000

# Run main.py when the container launches.
CMD python main.py reader reader
