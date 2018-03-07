# 1. Installing dependencies:

## Backend:

### Download Python 3:

<https://www.python.org/downloads/>

### In a shell within the Backend directory, install requirements:

    pip install -r requirements.txt

### In a shell, download NLTK dependencies:

    python3
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')

## Frontend:

### Download nodejs with npm:

<https://nodejs.org/en/>

### In a shell, install Angular:

    npm install angular

# 2. Launching the program:

## Backend:

### In a shell within the Backend directory, start via:

    python main.py
(a local server is started that can be addressed via http://127.0.0.1:5000)

### Directly receive search results from the backend (provided as a JSON object) via this URL:

<http://127.0.0.1:5000/cam?objectA=*OBJA*&objectB=*OBJB*&aspect1=*ASP1*&weight1=*WEIGHT1*>

replace *OBJA* and *OBJB* with the objects you want to compare, e. g. *OBJA* with dog and *OBJB* with cat. These are both mandatory.

replace *ASP1* and *WEIGHT1* with an aspect you want to include in the search requests and the weight you want to have it, e. g. *ASP1* with price and *WEIGHT1* with 5.
add as many aspects/weights as you want as long as you follow these rules:
-   you always have to enter both an aspect and its weight. you can't enter one without the other.
-   you always have to start with aspect1 and weight1, then aspect2 and weight2 and so forth. Don't skip a number as all numbers after that will not be read (order doesn't matter, as long as they exist somewhere in the URL).
-   aspects/weights are optional and can be skipped completely if you just want to compare two objects without any aspects added.
-   if you want the results to resemble those you'd get using the Frontend, use values from 1 to 5 for the weights as you can't enter other values in the frontend. The search will also work for other values though. Be careful with entering negative values or values close to an Integer overflow as they can produce unexpected results.

example for a good URL:

<http://127.0.0.1:5000/cam?objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1>

## Frontend:

### In a shell within the Frontend/cam-frontend directory, start via:

    ng serve -o
(the page will automatically be opened in your browser.)