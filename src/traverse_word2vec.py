import word2vec


def _normalize_phrase(phrase):
    return '_'.join(phrase.lower().strip().split())


def _denormalize_term(term):
    components = [s.strip() for s in term.split()]
    return '_'.join(component for component in components if component)


class OracularError(Exception):
    pass


class Oracle:

    def __init__(self, word2vec_model):
        self._model = word2vec_model

    @classmethod
    def from_binary(cls, binary_file):
        word2vec_model = word2vec.load(binary_file)
        return Oracle(word2vec_model)

    def synonyms_for(self, phrase, n=10):
        term = _normalize_phrase(phrase)
        indices, metrics = self._model.similar(term)
        return [self._model.word(index) for index in indices]

    def closest_terms(self, vector, n=10):
        indices, metrics = self._model.closest(vector)
        return [_denormalize_term(self._model.word(index)) for index in indices]

    def traverse(self, origin, destiny, n=10):
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
