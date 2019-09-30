[![Build Status](https://travis-ci.org/uhh-lt/cam.svg?branch=master)](https://travis-ci.org/uhh-lt/cam)

# Overview

The Comparative Argument Machine (CAM) project is developed by the Language Technology Group, Department of Informatics, University of Hamburg. As a starting point for a bigger scientific project the current version compares two objects via a large database. The main goal of the CAM project will be the comparison based on understanding of natural language and also to output natural language sentences as a result.

If you want to learn more about the project or help to develop it, feel free to contact us. A live demo is [available online](http://ltdemos.informatik.uni-hamburg.de/cam/).

# Install CAM on a new machine

Currently there are two ways to deploy the CAM project to your own machine: With or without Docker. You will find instructions for both ways here.

## Deployment with Docker

### 1. Install Docker

Head to [the download page from Docker](https://docs.docker.com/install/) and find the right installation file for your system. Note that for some operating systems (for example, Windows 10 Home Edition) you can't install Docker itself and have to install [Docker Toolbox](https://docs.docker.com/toolbox/overview/) instead. Deploying with Docker Toolbox also works fine, but makes a difference you'll see later.

If you are on Linux, you have to [install Docker Compose](https://docs.docker.com/compose/install/) separately (installations for other systems already include Compose, the Toolbox also does).

After you've successfully installed Docker (and Compose), start a terminal and head over to the directory that shall contain the project, clone it from GitHub and start the Docker containers:

    git clone https://github.com/uhh-lt/cam.git
    cd cam
    docker-compose up -d

Attention: If you're on the Docker Toolbox, you will have to make changes to your files before using `docker-compose up` because Toolbox uses your docker machine ip instead of localhost. Head to `/src/Frontend/camFrontend/src/app/shared/url-builder.service.ts` and change the `HOSTNAME` constants, replacing `localhost` with your machine ip (you can get it via `docker-machine ip`).

After this, CAM is up and running and you can see its front end in your browser via `http://127.0.0.1:10101` or directly receive search results from the backend (provided as a JSON object) via this URL:

    http://127.0.0.1:5000/cam?model=default&fs=FS&objectA=OBJA&objectB=OBJB&aspect1=ASP1&weight1=WEIGHT1
http://127.0.0.1:10101
The parameters of this url are desribed in [API explained](https://github.com/uhh-lt/cam#API-explained)

An example for a good URL:

<http://127.0.0.1:5000/cam?model=default&fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1>

http://127.0.0.1:10101

### Elasticserach

Preferably, Elasticsearch should also get it's own Dockerfile or should be build from a Docker-image with docker-compose. In order for the suggestions-feature to be able to run, cross-origin resource sharing must be enabled all origins musst be allowed by adding 

    http.cors.enabled: true
    http.cors.allow-origin: "*"

to the `elasticsearch.yml`.
With elasticsearch setup, the suggestion-feature's index can be created by running `create_es-index_from_suggestions.py` from `/cam/src/Backend/create_suggestoins_index/` or by extracting `es-nodes.tar.gz` to elasticsearchs's default nodes location, which is `/var/lib/elasticsearch/`.

## Deployment without Docker

### 1. Installing dependencies

#### Backend

[Download Python 3](https://www.python.org/downloads)

In a terminal, install requirements:

    pip install -r requirements.txt
    python -m nltk.downloader stopwords
    python -m nltk.downloader punkt
    python -m nltk.downloader averaged_perceptron_tagger

To be able to use the machine learning approaches, it is necessary to download the following files and place them in ./src/Backend/data

- Download [Glove Embeddings](http://nlp.stanford.edu/data/glove.840B.300d.zip)
- Download [InferSent model](https://s3.amazonaws.com/senteval/infersent/infersent.allnli.pickle)

#### Frontend

[Download nodejs with npm](https://nodejs.org/en/)

In a terminal, install Angular:

    cd cam
    npm install
    npm start

### 2. Changing the default hostnames and search type

#### Communication between frontend and backend

On default, the backend is running on a localhost. If you want to change this, maybe because you deployed the project to another server, change all HOSTNAME constants (like HOSTNAME_DEFAULT) in ./src/Frontend/camFrontend/src/app/shared/url-builder.service.ts.

#### Communication between backend and search request server; search type

On default, the instance of Elastic Search used is running on <http://ltdemos.informatik.uni-hamburg.de/depcc-index/> as specified in ./src/Backend/constants.py. If you have a different server you want to do the search requests on, change ES_HOSTNAME in that file. The default search type is commoncrawl2 of Elastic Search. If you want to change this, change CRAWL_DATA_REPOS in the same file.

### 3. Launching the program

#### Backend

In a terminal within the Backend directory, start via:

    python main.py
    
if the ElasticSearch needs no credentials and via:

    python main.py username password
    
for an ElasticSearch instance with credentials.

(a local server is started that can be addressed via <http://127.0.0.1:5000>)

Directly receive search results from the backend (provided as a JSON object) via this URL:

    http://127.0.0.1:5000/cam?model=default&fs=FS&objectA=OBJA&objectB=OBJB&aspect1=ASP1&weight1=WEIGHT1

The parameters of this url are desribed in [API explained](https://github.com/uhh-lt/cam#API-explained)

example for a good URL:

<http://127.0.0.1:5000/cam?model=default&fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1>

#### Frontend

In a terminal within the Frontend/cam-frontend directory, start via:

    ng serve -o

(the page will automatically be opened in your browser.)

# API explained

To access the API URL parameters can be used, the structure is described underneath:

    BASE_ADDRESS/cam?model=MODEL&fs=FS&objectA=OBJA&objectB=OBJB&aspect1=ASP1&weight1=WEIGHT1
 _The base address is dependen from where the backend is deployed and accessed._

replace `MODEL` with either _default_, _bow_ or _infersent_, to select one of the actually given three models. If the parameter is left out, the default model is selected by default. \
replace `FS` with false if you want to do the default search, or with true if you want to do a fast search. \
replace `OBJA` and `OBJB` with the objects you want to compare, e. g. `OBJA` with dog and `OBJB` with cat. These are both mandatory. \
replace `ASP1` and `WEIGHT1` with an aspect you want to include in the search requests and the weight you want to have it, e. g. `ASP1` with price and `WEIGHT1` with 5.
add as many aspects/weights as you want as long as you follow these rules:

* you always have to enter both an aspect and its weight. you can't enter one without the other.
* you always have to start with aspect1 and weight1, then aspect2 and weight2 and so forth. Don't skip a number as all numbers after that will not be read (order doesn't matter, as long as they exist somewhere in the URL).
* aspects/weights are optional and can be skipped completely if you just want to compare two objects without any aspects added.
* if you want the results to resemble those you'd get using the Frontend, use values from 1 to 5 for the weights as you can't enter other values in the frontend. The search will also work for other values though. Be careful with entering negative values or values close to an Integer overflow as they can produce unexpected results.

example for a good URL:

<http://127.0.0.1:10100/cam?model=default&fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1>


# Updating existing installations to the newest version

Updating your currently deployed project to the newest version is different depending on if you've deployed it with or without Docker.

## Updating with Docker

    cd cam
    docker-compose down
    docker rmi cam-frontend cam-backend
    git pull
    docker-compose up -d

## Updating without Docker

    cd cam
    git pull

Then start the program exactly like described above.
