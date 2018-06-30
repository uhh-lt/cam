# Use an official Python runtime as a parent image
FROM python:3.6.1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader averaged_perceptron_tagger

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD python main.py reader reader
