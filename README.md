[![Build Status](https://travis-ci.org/uhh-lt/cam.svg?branch=sqliteAspectSaving)](https://travis-ci.org/uhh-lt/cam)

# Overview

When comparing two objects, CAM not only generates the scores for both but also extracts up to ten aspects per object. These aspects are supposed to tell the user *why* the specific object is better than the other. To find out how CAM currently extracts aspects, have a look at `src/Backend/utils/pos_link_extracter.py`. To further improve on extracting aspects, a machine learning model should be generated that learns from well extracted aspects. To do this, a database containing sentences, their objects and extracted aspects as well as a rating for that aspect (whether it's an extracted aspect that makes sense or not) was needed. Creating this database is the goal of this branch.

Note that the name of the branch is sqliteAspectSaving. This is because at the beginning of the CAM aspect rating process, sqlite was used to create the database. This is not true any more. If you want, feel free to rename the branch.

# Deploy the branch to ltdocker

Currently this branch is deployed and running on ltdocker. For instructions on how to deploy it on a new system you can for example look at the readme of CAM's master branch and adjust it accordingly for this branch. These instructions assume you're working on ltdocker with Docker. You can access the system via [http://ltdemos.informatik.uni-hamburg.de/cam3/](http://ltdemos.informatik.uni-hamburg.de/cam3/). On ltdocker you'll find the branch installed on `srv/docker/pan-cam3/`.

# Updating existing installation to the newest version

To update the version running on ltdocker just run the following commands:

    cd srv/docker/pan-cam3/
    docker-compose down
    docker rmi cam-frontend3 cam-backend3
    git pull
    docker-compose up -d

Note that if you only made changes to the backend you don't need to remove the Docker image of the frontend so `docker rmi cam-backend3` will be enough then. The same is true the other way around if you only made changes to the frontend. Always removing both images by default doesn't hurt though, it just takes a little bit longer to restart the container.

# Docker volumes

On `srv/docker/pan-cam3/` you will not only find everything that's git-related but also two additional directories: `ratingresults/` and `camsqlvolume/`. **DO NOT DELETE THOSE DIRECTORIES** unless you wish to lose the whole rating database. Those two directories are where the sql database as well as the generated CSVs and CoNLL files are made persistent via Docker volumes. They won't be affected if you stop or restart the Docker container or do a git pull.

# Explanation of currently available features and how to work on them

Currently when you go to [http://ltdemos.informatik.uni-hamburg.de/cam3/](http://ltdemos.informatik.uni-hamburg.de/cam3/) you will find three different features.

## Rate aspects

The aspect rating feature is the foundation of everything this branch and the machine learning models that shall be created with its results are doing. When clicking on `Start!`, one of many predefined comparisons is randomly launched. Mark each aspect that you think makes sense (hit its `+good+` button) and leave out the rest, then hit `Submit`. For each marked aspect a database entry with a positive rating, for all other aspects a database entry with a negative rating will be saved.

### Working on this feature

If you want to add or remove predefined pairs you can do so in `src/Backend/db/preselected_pairs.py`. Please take care to only include pairs that are a) lower-case and b) sorted alphabetically. This shouldn't be necessary as all relevant occurences in the code should do a sort() and lower() themselves but just in case that there's an occurence where this has been forgotten you'll prevent an Error by taking care of this when adding the pairs.

If you want to change the front end you can do so in `src/Frontend/camFrontend/src/app/components/`, specifically in `user-interface/`, `result-presentation/` and `result-presentation/multiselect-chiplist/`. Note that changes regarding the data that's sent to the back end might require you to also change how the URL for communicating with the back end is generated in `src/Frontend/camFrontend/src/app/services/url-builder-service.ts`.

If you want to change how the ratings are saved you can do so in `src/Backend/db/mysql_connecter.py`.

If you want to change the volume that's used for making the database persistent you can do so in `docker-compose.yml`. Note that you could lose the whole database if you do this.

## Generate a CSV containing the ratings

The second button you'll find to the right is named `Export ratings to CSV` and that's exactly what it does. All ratings that have previously been inserted into the database are collected and then exported to a CSV that contains the following columns:

First Object, Second Object, Aspect, Object the aspect belongs to, most frequent rating, confidence, amount of positive ratings, amount of negative ratings, sentence examples 1-5.

You'll find the CSV at `srv/docker/pan-cam3/ratingresults/convertedratings.csv` on ltdocker.

### Working on this feature

If you want to change how the CSV is generated you can do so in `src/Backend/db/mysql_connecter.py`, specifically in the method `export_ratings()`.

If you want to change the volume that's used for making the CSV persistent you can do so in `docker-compose.yml`.

## Generate CoNLL files for training the machine learning model

The third button you'll find to the right is named `Create CoNLL files`. When hitting this button, three txt files are generated that are formatted as CoNLL files: For train, test, and dev. The way these files are formatted is specific for the [tagger](https://github.com/achernodub/targer) that's currently used to train the models so it might be necessary to change the formatting if you plan on using a different one.

You'll find the CoNLL files at `srv/docker/pan-cam3/ratingresults/` on ltdocker: `ratingsconlldev.txt`, `ratingsconlltest.txt`, and `ratingsconlltrain.txt`.

**IMPORTANT NOTE**: With the current implementation, the CoNLL file creation does **not** get its data directly from the database. Instead it takes the CSV as input. That means that before you can create the CoNLL files, you have to create the CSV!

### Working on this feature

If you want to change how the CoNLL files are generated you can do so in `src/Backend/db/conll_file_creator.py`.

If you want to change the volume that's used for making the CoNLL files persistent you can do so in `docker-compose.yml`.

## Create a database table containing sentence examples

This feature is currently not available via the front end because it shouldn't be necessary to use it again. It creates a table in the sql database that contains up to 20 sentence examples for each combination of pair of objects (taken from `src/Backend/db/preselected_pairs.py`) and extracted aspect. While doing so it lets CAM create an Elastic Search request for each pair and then looks for all sentences found for each object and for all aspects extracted for each object. Because of this the whole process takes some time to finish.

The resulting table is the foundation for all the other features: Up to five sentence examples are included in the CSV for each pair/aspect combination that will then be used for creating the CoNLL files. As the table already exists in the database you most likely won't need to run this creation process again. It may become necessary though when you decide to change the way these sentence examples are chosen, when you have to create a fresh database, or when CAM starts using a different Elastic Search database.

### Working on this feature

If you want to make this feature available via the front end again you can do so for example just by adding another button below the three existing buttons. You'd have to do this in `src/Frontend/camFrontend/src/app/components/user-interface/user-interface.component.html` and the button would have to have `(click)='createSentenceExamples()'`. All necessary methods for creating the table (communication between front and back end, requesting Elastic Search, creating the table) are still available and will be triggered just by hitting the button. Note that there currently is a known bug: When the table creation process is finished, the text shown on the front end will still say that it's being created and won't switch to saying that it has been created. You might have to check the docker logs of cam-backend3 to see when the process has actually finished.

Of course you could also call the `create_sentence_examples()` method of `src/Backend/db/mysql_connecter.py` directly to start creating the table. Note that you'd have to do this inside the docker container though. This method is also the place to go if you want to change how this table is being created.

Note that it should **not** be necessary to start the sentence examples table creation process just because you inserted new predefined pairs. After each rating, if there aren't any sentence examples for that specific pair/aspect combination, up to five sentence examples should automatically be added to the sentence examples table. Because of this you shouldn't run into any errors just because a new pair has been inserted.

# Training a machine learning model

Note that we're currently using [targer](https://github.com/achernodub/targer) for training the models. If you want to use a different tagger, these instructions may not be accurate for you.

When you want to train a model with targer, you have to do the following steps:

1. Clone targer to your system (make sure you are on a UNIX platform -- Windows doesn't seem to work)
2. Get word embeddings and store them inside `/embeddings`. There's a script inside the directory to download glove embeddings but that script didn't work when we tested it so we downloaded the embeddings manually via [http://nlp.stanford.edu/data/glove.6B.zip](http://nlp.stanford.edu/data/glove.6B.zip) and unzipped them inside `/embeddings`. Feel free to try different embeddings (found on [https://nlp.stanford.edu/projects/glove/](https://nlp.stanford.edu/projects/glove/) for example).
3. Run the `main.py` with your CoNLL files: `python3 main.py --test PATHTOYOURTESTFILE --train PATHTOYOURTRAINFILE --dev PATHTOYOURDEVFILE`. Note that it may be necessary to add `--gpu -1` if targer cannot operate using your graphics card to make it use the cpu instead. Feel free to try different commands specified on [targer's github page](https://github.com/achernodub/targer), for example to specify the machine learning model that should be used.