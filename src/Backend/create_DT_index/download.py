import urllib.request
import io
import gzip


# Download the file from `url` and save it locally under `file_name`:

BASE_URL = 'http://ltdata1.informatik.uni-hamburg.de/depcc/distributional-models/dependency_lemz-true_cooc-false_mxln-110_semf-true_sign-LMI_wpf-1000_fpw-1000_minw-5_minf-5_minwf-2_minsign-0.0_nnn-200/SimPruned/part-'

for i in range(0,1,1):
    index = ''
    for j in range(0,5-len(str(i)),1):
        index += '0'
    index += str(i)
    print(index)

    response = urllib.request.urlopen(BASE_URL + index + '.gz')
    compressed_file = io.BytesIO(response.read())
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)

    with open('../data/part-{}.txt'.format(index), 'wb') as outfile:
        outfile.write(decompressed_file.read())