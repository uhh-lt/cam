import urllib

from utils.es_requester import (extract_sentences, request_context_sentences,
                                request_document_by_id)


def get_sentence_context(document_id, sentence_id, context_size):
    document_id = urllib.parse.quote(document_id)
    if context_size is None and sentence_id is None:
        context = request_document_by_id(document_id)
    else:
        context = request_context_sentences(
            document_id, int(sentence_id), int(context_size))
    context_sentences = extract_sentences(context, False)
    context_sentences.sort(key=lambda elem: next(iter(elem.id_pair.values())))
    return [context_sentence.__dict__ for context_sentence in context_sentences]
