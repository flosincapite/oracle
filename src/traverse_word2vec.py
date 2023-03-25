from .confused_predictive_model import textnorm
from nltk.corpus import stopwords
import numpy as np
import word2vec


def _normalize_phrase(phrase):
    return '_'.join(phrase.lower().strip().split())


def _denormalize_term(term):
    components = [s.strip() for s in term.split('_')]
    return ' '.join(component for component in components if component)


class OracularError(Exception):
    pass


class Oracle:

    def __init__(self, word2vec_model):
        self._model = word2vec_model

    @classmethod
    def from_binary(cls, binary_file):
        try:
            print(binary_file)
            word2vec_model = word2vec.load(binary_file)
        except Exception as e:
            print(e)
            raise OracularError('The oracle does not speak that language.')
        return Oracle(word2vec_model)

    def synonyms_for(self, phrase, n=10):
        term = _normalize_phrase(phrase)
        try:
            indices, metrics = self._model.similar(term)
        except KeyError:
            raise OracularError(f'The oracle does not know the word "{phrase}."')
        return [self._model.word(index) for index in indices]

    def closest_terms(self, vector, n=10):
        indices, metrics = self._model.closest(vector)
        return [_denormalize_term(self._model.word(index)) for index in indices]

    def _get_terms_and_delta(self, origin, destiny, n):
        first_term = _normalize_phrase(origin)
        try:
            source_vector = self._model.get_vector(first_term)
        except KeyError:
            raise OracularError(f'The oracle does not know the word "{origin}."')
        last_term = _normalize_phrase(destiny)
        try:
            destiny_vector = self._model.get_vector(last_term)
        except KeyError:
            raise OracularError(f'The oracle does not know the word "{destiny}."')
        # TODO: What if term isn't found?
        return (first_term, last_term, source_vector, destiny_vector)

    def traverse(self, origin, destiny, n=10):
        first_term, last_term, source_vector, destiny_vector = self._get_terms_and_delta(origin, destiny, n)
        delta = (destiny_vector - source_vector) / n

        terms = []
        term_set = set([first_term, last_term])

        def _add_term(term):
            term_set.add(term)
            terms.append(term)
        terms.append(first_term)
        for _ in range(n):
            source_vector += delta
            for term in self.closest_terms(source_vector):
                if term not in term_set:
                    _add_term(term)
                    break
            else:
                raise OracularError('how that happen?')
        terms.append(last_term)
        return [_denormalize_term(term) for term in terms]

    def traverse_text(self, origin, destiny, text, n=10):
        stop_words = set(stopwords.words('english') + ['from'])
        _, _, source_vector, destiny_vector = self._get_terms_and_delta(origin, destiny, n)
        delta = (destiny_vector - source_vector) / n
        whole_text = []
        for sentence in textnorm.generate_normalized_sentences(text):
            whole_text.extend(sentence.split())
        frozen_indices = set()
        vectors = []
        for i, word in enumerate(whole_text):
            frozen = False
            if word in stop_words:
                frozen = True
            else:
                try:
                    vector = self._model.get_vector(_normalize_phrase(word))
                    print('vector for', word, 'is', vector)
                except KeyError:
                    frozen = True
            if frozen:
                frozen_indices.add(i)
            else:
                vectors.append(vector)

        for _ in range(n):
            new_vectors = []
            for vector in vectors:
                new_vectors.append(vector + delta)
            vectors = new_vectors
            def v():
                for vector in vectors:
                    yield vector
            gen = v()
            sentence = []
            for i, word in enumerate(whole_text):
                if i in frozen_indices:
                    sentence.append(word)
                else:
                    vector = next(gen)
                    next_term = self.closest_terms(vector)[0]
                    sentence.append(next_term)
            yield ' '.join(sentence)
