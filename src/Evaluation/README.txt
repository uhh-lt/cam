step1_unic_pairs.py
    Computes the unic pairs from the evaluation dataset to later on request all sentences corresponding to those pairs.
    Since the requests doesn't change based on extracted aspects, it is only necessary to request those 271 unic pairs
    and later on compute the scores based on the aspects and sentences.
    Takes less then a second.

step2_request_sentences.py
    Requests all the sentences for all unic pairs. The used query is the same, which is used in the backend to request the ES.
    The request is directly send to the ES, it is necessary to have a tunnel to the ltcpu1 to be able to access the ES directly.
    Takes about 10 minutes.

preprocessing_dataset.py
    Extracts aspects and outputs the preprocessed data to compute further or request the scores.

step3_calculate_scores.py
    Takes the in step 2 produces sentences to all unic pairs and the preprocessed_dataset with the aspects to calculate the scores.
    Takes about 1,5h.