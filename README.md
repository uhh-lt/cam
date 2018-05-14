[![Build Status](https://travis-ci.org/uhh-lt/cam.svg?branch=master)](https://travis-ci.org/uhh-lt/cam)

# Overview

This implementation of the Comparative Argument Machine (CAM) was part of a three-week-project at the University of Hamburg. It was one of a few different language technology projects to be realized within this time. As a starting point for a bigger scientific project the goal was to make CAM be able to compare two objects via a large database. The main goal of the CAM project will be the comparison based on understanding of natural language and also to output natural language sentences as a result.

If you want to learn more about the project or help to develop it, feel free to contact us. A live demo is [available online](http://ltdemos.informatik.uni-hamburg.de/cam/).

# 1. Installing dependencies

## Backend

[Download Python 3](https://www.python.org/downloads)

In a shell, install requirements:

    pip install -r requirements.txt
    python -m nltk.downloader stopwords
    python -m nltk.downloader punkt
    python -m nltk.downloader averaged_perceptron_tagger

## Frontend

[Download nodejs with npm](https://nodejs.org/en/)

In a shell, install Angular:

    cd cam
    npm install
    npm start

# 2. Changing the default hostnames and search type

## Communication between frontend and backend

On default, the backend is running on a localhost. If you want to change this, maybe because you deployed the project to another server, change all HOSTNAME constants (like HOSTNAME_DEFAULT) in ./src/Frontend/camFrontend/src/app/url-builder/url-builder.component.ts.

## Communication between backend and search request server; search type

On default, the search request server is connected via SSH on port 9200. If you have a different server you want to do the search requests on, change ES_HOSTNAME in ./src/Backend/constants.py. The default search type is commoncrawl2 of Elastic Search. If you want to change this, change CRAWL_DATA_REPOS in the same file.

# 3. Launching the program

## Backend

In a shell within the Backend directory, start via:

    python main.py
    
if the ElasticSearch needs no credentials and via:

    python main.py username password
    
for an ElasticSearch instance with credentials.

(a local server is started that can be addressed via <http://127.0.0.1:5000>)

Directly receive search results from the backend (provided as a JSON object) via this URL:

    http://127.0.0.1:5000/cam?fs=FS&objectA=OBJA&objectB=OBJB&aspect1=ASP1&weight1=WEIGHT1

replace `FS` with false if you want to do the default search, or with true if you want to do a fast search.

replace `OBJA` and `OBJB` with the objects you want to compare, e. g. `OBJA` with dog and `OBJB` with cat. These are both mandatory.

replace `ASP1` and `WEIGHT1` with an aspect you want to include in the search requests and the weight you want to have it, e. g. `ASP1` with price and `WEIGHT1` with 5.
add as many aspects/weights as you want as long as you follow these rules:

* you always have to enter both an aspect and its weight. you can't enter one without the other.
* you always have to start with aspect1 and weight1, then aspect2 and weight2 and so forth. Don't skip a number as all numbers after that will not be read (order doesn't matter, as long as they exist somewhere in the URL).
* aspects/weights are optional and can be skipped completely if you just want to compare two objects without any aspects added.
* if you want the results to resemble those you'd get using the Frontend, use values from 1 to 5 for the weights as you can't enter other values in the frontend. The search will also work for other values though. Be careful with entering negative values or values close to an Integer overflow as they can produce unexpected results.

example for a good URL:

<http://127.0.0.1:5000/cam?fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1>

## Frontend

In a shell within the Frontend/cam-frontend directory, start via:

    ng serve -o

(the page will automatically be opened in your browser.)
