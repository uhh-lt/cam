[![GitHub Actions](https://img.shields.io/github/workflow/status/uhh-lt/cam/Docker%20build?style=flat-square)](https://github.com/uhh-lt/cam/actions?query=workflow%3A%22Docker+build%22)
[![Docker Hub frontend tags](https://img.shields.io/docker/v/webis/cam-frontend?style=flat-square&label=frontend+version)](https://hub.docker.com/repository/docker/webis/cam-frontend/tags)
[![Docker Hub frontend](https://img.shields.io/docker/pulls/webis/cam-frontend?style=flat-square&label=frontend+pulls)](https://hub.docker.com/repository/docker/webis/cam-frontend)
[![Docker Hub backend tags](https://img.shields.io/docker/v/webis/cam-backend?style=flat-square&label=backend+version)](https://hub.docker.com/repository/docker/webis/cam-backend/tags)
[![Docker Hub backend](https://img.shields.io/docker/pulls/webis/cam-backend?style=flat-square&label=backend+pulls)](https://hub.docker.com/repository/docker/webis/cam-backend)

# CAM: The Comparative Argument Machine

The Comparative Argument Machine (CAM) project is developed by the [Language Technology Group](https://www.inf.uni-hamburg.de/en/inst/ab/lt/home.html) at the University of Hamburg.
As a starting point for a bigger scientific project the current version compares two objects via a large database.
The main goal of the CAM project is the comparison based on understanding of natural language and to output natural language sentences as a result.

If you want to learn more about the project or help to develop it, feel free to [contact us](https://www.inf.uni-hamburg.de/en/inst/ab/lt/home/directions.html).
A live demo is [available online](http://ltdemos.informatik.uni-hamburg.de/cam/).

# Installation

Currently, there are two ways to deploy the CAM project to your own machine:
With or without Docker.
You will find instructions for both ways here.

## Deployment with Docker

### Web app

1. Install [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
1. Clone the CAM repository from GitHub:
      ```shell script
      git clone https://github.com/uhh-lt/cam.git
      cd cam
      ```
1. If you're using Docker Toolbox, you need to change the `HOSTNAME` constants in [`url-builder.service.ts`](/src/Frontend/camFrontend/src/app/services/url-builder.service.ts) to match your Docker machine IP (instead of `localhost`).
     You can check the Docker machine IP via `docker-machine ip`.
1. Start Docker containers:
    ```shell script
    docker-compose up -d
    ```

Now CAM is up and running.
You should be able to access the frontend app in your browser:  
http://localhost:10101  
Or directly receive search results from the backend (as JSON objects):  
http://localhost:10100/cam?model=default&fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1  
(The parameters of this URL are described [below](#API).)


### Elasticsearch

Preferably, Elasticsearch should also get its own Dockerfile or should be build from a Docker image with Docker Compose.
To use the suggestions feature, cross-origin resource sharing must be enabled for all origins in the `elasticsearch.yml` config:
```yaml
http.cors.enabled: true
http.cors.allow-origin: "*"
```

With Elasticsearch set up, the suggestions index can be created:
```shell script
cd cam/src/Backend/create_suggestoins_index/
python create_es-index_from_suggestions.py
```
Alternatively, extract [`es-nodes.tar.gz`](es-nodes.tar.gz) to Elasticsearchs' default nodes location (`/var/lib/elasticsearch/`).

## Deployment without Docker

1. Clone the CAM repository from GitHub:
    ```shell script
    git clone https://github.com/uhh-lt/cam.git
    cd cam
    ```

### Backend

1. Go to the backend folder:
    ```shell script
    cd src/Backend
    ```
1. Download [Python](https://www.python.org/downloads/release/python-361/) and install [Pipenv](https://pipenv.pypa.io/).
1. Install requirements:
    ```shell script
    pipenv install
    pipenv run python -m nltk.downloader stopwords
    pipenv run python -m nltk.downloader punkt
    pipenv run python -m nltk.downloader averaged_perceptron_tagger
    ```
1. Download the following files and place them in [`src/Backend/data`](src/Backend/data) (needed for the InferSent model):
    - [Glove Embeddings](https://nlp.stanford.edu/data/glove.840B.300d.zip)
    - [InferSent model](https://s3.amazonaws.com/senteval/infersent/infersent.allnli.pickle)
1. Change default hostnames and search type:
    - On default, Elasticsearch should be running on https://ltdemos.informatik.uni-hamburg.de/depcc-index/ as specified in [`config.json`](src/Backend/config.json).
        If you host the Index on a different cluster, change `elasticsearch.url` in that file.
    - The default search index is `depcc`.
        If you want to change this, change `elasticsearch.index` in [`config.json`](src/Backend/config.json).
1. Start the backend API:
    ```shell script
    pipenv run python main.py
    ```
   (If the Elasticsearch needs authentication, specify `ES_USERNAME` and `ES_PASSWORD` environment variables.)

Now the backend is up and running.
You should be able to receive search results from the backend (as JSON objects):  
http://localhost:5000/cam?model=default&fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1  
(The parameters of this URL are described [below](#API).)

#### Frontend

1. Download [Node.js](https://nodejs.org/en/download/current/)
1. Enter the frontend working directory:
    ```shell script
    cd src/Frontend/camFrontend
    ```
1. Install Angular dependencies:
    ```shell script
    npm install
    ```
1. Change default hostnames:  
    On default, the backend is running on `localhost`.
    If you want to change this, maybe because you deployed the project to another server, change all `HOSTNAME_` constants, e.g., `HOSTNAME_DEFAULT`, in [`url-builder.service.ts`](src/Frontend/camFrontend/src/app/services/url-builder.service.ts).
1. Start the frontend app:
    ```shell script
    ng serve -o
    ```

The frontend app will automatically open in your web browser.

# Updating

## Updating with Docker
```shell script
docker-compose down
docker rmi cam-frontend cam-backend
git pull
docker-compose up -d
```

## Updating without Docker
```shell script
git pull
```

Start the program like described [above](#installation).

# API

To access the API, URL parameters can be used.
The structure is described underneath:

```
BASE_ADDRESS/cam?model=MODEL&fs=FS&objectA=OBJA&objectB=OBJB&aspect1=ASP1&weight1=WEIGHT1
```

 _The base address depends on the backend deployment URL._

- Replace `MODEL` with either `default`, `bow` or `infersent`, to select one of the three included models.
    This parameter is optional.
- Replace `FS` with `false` if you want to do the default search, or with `true` to enable fast search.
- Replace `OBJA` and `OBJB` with the objects you want to compare, e.g., `dog` and `cat`.
    Both parameters are mandatory.
- Replace `ASP1` and `WEIGHT1` with an aspect you want to include and its weight, e. g. `price` and `5`.
- Add as many aspects/weights as you want, but follow these rules:
    - You must enter both aspect and weight.
    - Aspects and weight parameters must be numbered consecutively. That is, if you include `aspect2` and `weight2`, you have to include `aspect1` and `weight1` as well.
        Numbers start at `1`.
        The order of URL parameters does not matter.
    - Aspects/weights are optional. You can skip aspect/weight parameters to compare two objects without any aspects.
    - The frontend limits weights to integers from 1 to 5.
        If you need equivalent results as from the frontend, use weights from 1 to 5.
        However, arbitrary integer values may be used.
        Be careful with negative values or values close to an integer overflow.

Example URL:
http://localhost:5000/cam?model=default&fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1
