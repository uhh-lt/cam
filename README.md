[![Build Status](https://travis-ci.org/uhh-lt/cam-hci.svg?branch=master)](https://travis-ci.org/uhh-lt/cam-hci)
# Overview

# 1. Installing dependencies

## Backend

### Download Python 3:

<https://www.python.org/downloads/>

### In a shell, install requirements:

    pip install -r requirements.txt
    python -m nltk.downloader stopwords
    python -m nltk.downloader punkt
    python -m nltk.downloader averaged_perceptron_tagger

## Frontend

### Download nodejs with npm:

<https://nodejs.org/en/>

### In a shell, install Angular:

    npm install angular

# 2. Launching the program

## Backend

### In a shell within the Backend directory, start via:

    python main.py

(a local server is started that can be addressed via http://127.0.0.1:5000)

### Directly receive search results from the backend (provided as a JSON object) via this URL:

<http://127.0.0.1:5000/cam?objectA=*OBJA*&objectB=*OBJB*&aspect1=*ASP1*&weight1=*WEIGHT1*>

replace _OBJA_ and _OBJB_ with the objects you want to compare, e. g. _OBJA_ with dog and _OBJB_ with cat. These are both mandatory.

replace _ASP1_ and _WEIGHT1_ with an aspect you want to include in the search requests and the weight you want to have it, e. g. _ASP1_ with price and _WEIGHT1_ with 5.
add as many aspects/weights as you want as long as you follow these rules:

* you always have to enter both an aspect and its weight. you can't enter one without the other.
* you always have to start with aspect1 and weight1, then aspect2 and weight2 and so forth. Don't skip a number as all numbers after that will not be read (order doesn't matter, as long as they exist somewhere in the URL).
* aspects/weights are optional and can be skipped completely if you just want to compare two objects without any aspects added.
* if you want the results to resemble those you'd get using the Frontend, use values from 1 to 5 for the weights as you can't enter other values in the frontend. The search will also work for other values though. Be careful with entering negative values or values close to an Integer overflow as they can produce unexpected results.

example for a good URL:

<http://127.0.0.1:5000/cam?objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1>

## Frontend

### In a shell within the Frontend/cam-frontend directory, start via:

    ng serve -o

(the page will automatically be opened in your browser.)
