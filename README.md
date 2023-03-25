# oracle
the oracle: a Flask backend for various writing toys that use computational linguistics.

## Installation
git clone <this repo>
cd src
git clone <confused-predictive-model>
mv confused-predictive-model confused\_predictive\_model
cd ..
pip install -r requirements.txt
pip install -r src/confused\_predictive\_model/requirements.txt
<replace np.float with float in word2vec/wordvectors.py>
<python; import nltk; nltk.download('stopwords')>

## TODO
i18n
caching/saving models for reuse
