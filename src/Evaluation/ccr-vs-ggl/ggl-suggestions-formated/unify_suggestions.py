import os
import json
import csv
import pprint
from random import randint

pp = pprint.PrettyPrinter(indent=4)

CANDIDATES_CSV_PATH = os.path.abspath("/home/hauke/Git/cam/src/Evaluation/ccr-vs-ggl/ggl-suggestions-formated/comparison-objects_and_suggestions_vocab.csv")
CANDIDATES_CSV_PATH_SHORT = os.path.abspath("/home/hauke/Git/cam/src/Evaluation/ccr-vs-ggl/ggl-suggestions-formated/comparison-objects_and_suggestions_short_vocab.csv")

# vocab:
#camSuggestionsFile = './cam-suggestions-all_vocab.json'
# english words:
camSuggestionsFile = './cam-suggestions-all_vocab.json'
gglSuggestionsFile = './ggl-suggestions-all_vocab.json'


unifiedArray = []
unifiedArraySmall = []

barChartArray = [0,0,0,0,0,0,0,0]

meanCamSuggestions = 0
meanCamSuccessfulSuggestions = 0
meanGglSuggestions = 0
meanGglSuccessfulSuggestions = 0

meanTP = 0
meanFN = 0
meanFP = 0
meanPrecision = 0
meanRecall = 0
meanF1Score = 0

atLeastOneCamSuggestion = 0
atLeastOneGglSuggestion = 0

with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
    writer = csv.writer(f)
    writer.writerows([['comparison object'] + ['CAM suggestions'] + ['Google suggestions']])

with open(CANDIDATES_CSV_PATH_SHORT, 'a', newline='', encoding="UTF-8") as short:
    writer = csv.writer(short)
    writer.writerows([['comparison object'] + ['CAM suggestions'] + ['Google suggestions']])

with open(camSuggestionsFile) as cam_json_file:
    camSuggestions = json.load(cam_json_file)

    with open(gglSuggestionsFile) as ggl_json_file:
        gglSuggestions = json.load(ggl_json_file)

        # vocab: 190, english words: 369759
        for i in range(0,190,1):
            
            camSuggestionList = camSuggestions[i]["suggestions"]
            meanCamSuggestions += len(camSuggestionList)
            if len(camSuggestionList) > 0:
                atLeastOneCamSuggestion += 1
                meanCamSuccessfulSuggestions += 1
            
            gglSuggestionList = gglSuggestions[i]["suggestions"]
            meanGglSuggestions += len(gglSuggestionList)
            if len(gglSuggestionList) > 0:
                atLeastOneGglSuggestion += 1
                meanGglSuccessfulSuggestions += 1

            intersection = list(set(camSuggestionList) & set(gglSuggestionList))
            true_positives = len(intersection)
            false_negatives = len(gglSuggestionList) - true_positives
            false_positives = len(camSuggestionList) - true_positives
            if len(camSuggestionList) == 0:
                precision = 0
            else:
                precision = true_positives / len(camSuggestionList)
            
            if len(gglSuggestionList) == 0:
                recall = 0
            else:
                recall = true_positives / len(gglSuggestionList)

            if precision == 0 or recall == 0:
                f1score = 0
            else:
                f1score = 1 / ((1 / recall) + (1 / precision)) / 2

            unifiedObj = {}
            unifiedObj["__comparison_object"] = camSuggestions[i]["comparison_object"]
            unifiedObj["_cam_suggestions"] = camSuggestionList
            unifiedObj["_ggl_suggestions"] = gglSuggestionList

            unifiedObj["true_positives"] = true_positives
            meanTP += true_positives

            unifiedObj["false_negatives"] = false_negatives
            meanFN += false_negatives

            unifiedObj["precision"] = precision
            meanPrecision += precision

            unifiedObj["recall"] = recall
            meanRecall += recall

            unifiedObj["f1score"] = f1score
            meanF1Score += f1score

            barChartArray[len(camSuggestionList)] += 1

            if len(camSuggestionList) > 0 and len(gglSuggestionList) > 0:
                unifiedArraySmall.append(unifiedObj)

            unifiedArray.append(unifiedObj)

            camSuggestionsStringList = ", ".join(camSuggestionList)
            gglSuggestionsStringList = ", ".join(gglSuggestionList)

            with open(CANDIDATES_CSV_PATH, 'a', newline='', encoding="UTF-8") as f:
                writer = csv.writer(f)
                writer.writerows([[camSuggestions[i]["comparison_object"]] + [camSuggestionsStringList] + [gglSuggestionsStringList]])
                
            if len(camSuggestionList) > 0:
                with open(CANDIDATES_CSV_PATH_SHORT, 'a', newline='', encoding="UTF-8") as short:
                    writer = csv.writer(short)
                    writer.writerows([[camSuggestions[i]["comparison_object"]] + [camSuggestionsStringList] + [gglSuggestionsStringList]])



meanCamSuccessfulSuggestions = meanCamSuggestions / atLeastOneCamSuggestion
meanCamSuggestions /= len(unifiedArray)
meanGglSuccessfulSuggestions = meanGglSuggestions / atLeastOneGglSuggestion
meanGglSuggestions /= len(unifiedArray)

meanTP /= len(unifiedArray)
meanFN /= len(unifiedArray)
meanPrecision /= len(unifiedArray)
meanRecall /= len(unifiedArray)
meanF1Score /= len(unifiedArray)

print("atLeastOneCamSuggestion: ", atLeastOneCamSuggestion)
print("atLeastOneGglSuggestion: ", atLeastOneGglSuggestion)

print("meanCamSuggestions: ", meanCamSuggestions)
print("meanCamSuccessfulSuggestions: ", meanCamSuccessfulSuggestions)
print("meanGglSuggestions: ", meanGglSuggestions)
print("meanGglSuccessfulSuggestions: ", meanGglSuccessfulSuggestions)

print("meanTP:        ", meanTP)
print("meanFN:        ", meanFN)
print("meanPrecision: ", meanPrecision)
print("meanRecall:    ", meanRecall)
print("meanF1Score:   ", meanF1Score)

#pp.pprint(unifiedArraySmall[23])

print("small:  ", len(unifiedArraySmall))
print("normal: ", len(unifiedArray))


#print(randint(0,369759))

#for i in range(0,10,1):
#    pp.pprint(unifiedArray[randint(0,369759)])


outfilename = './unified_vocab.json'
with open(outfilename, 'w') as outfile:
    json.dump(unifiedArray, outfile, indent=4)

outfilename = './unified_vocab-small.json'
with open(outfilename, 'w') as outfile:
    json.dump(unifiedArraySmall, outfile, indent=4)

print(barChartArray)
