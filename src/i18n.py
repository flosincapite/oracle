_I18N_MAPPING = {
    "LANGUAGE_GARBAGE_ORACLE_TITLE": {
        "en": "LANGUAGE GARBAGE ORACLE",
        "es": "EL ORÁCULO DE BASURA LINGÜÍSTICA"
    },
    "ORACLE_PERSONA_NAME": {
        "en": "THE ORACLE",
        "es": "EL ORÁCULO"
    },
    "CONSULT_ORACLE_AGAIN": {
        "en": "Consult the Oracle Again",
        "es": "Consultar al Oráculo otra vez"
    },
    "ORIGIN_WORD_SUGGESTION": {
        "en": "e.g. Beginning",
        "es": "p.ej. Inicio"
    },
    "DESTINY_WORD_SUGGESTION": {
        "en": "e.g. End",
        "es": "p.ej. Final"
    },
    "ORACLE_WALKED_WORDS": {
        "en": "the oracle has walked in words",
        "es": "el oráculo ha seguido el camino de palabras"
    },
    "ORACLE_LOITERS": {
        "en": "the oracle loiters on the word",
        "es": "el oráculo se para con la palabra"
    },
    "ORACLE_SMELLS": {
        "en": "still smelling the Delphic vapors",
        "es": "todavía huele los vapores Délfos"
    },
    "CONFUSED_POET_TITLE": {
        "en": "CONFUSED POET",
        "es": "POETA CONFUNDIDE"
    },
    "CONFUSED_POET_PERSONA_NAME": {
        "en": "THE CONFUSED POET",
        "es": "POETA CONFUNDIDE"
    },
    "CONFUSED_POET_CORPUS_SUGGESTION": {
        "en": "a great deal of text, e.g. from Wikipedia",
        "es": "un montón de texto, p.ej. de Wikipedia"
    },
    "CONFUSED_POET_SYNONYM_SUGGESTION": {
        "en": "lists of synonyms, e.g. beast,animal;arrow,dart",
        "es": "lista de sinónimos, p.ej. animal,bestia;flecha,dardo"
    },
    "CONSULT_POET_AGAIN": {
        "en": "Consult the Poet Again",
        "es": "Consultar al/a la poeta otra vez"
    },
    "GET_AN": {
        "en": "get an",
        "es": "ver su"
    }
}


def internationalize(i18n_code, label):
    return _I18N_MAPPING.get(label, {}).get(i18n_code)
