import re

import spacy
import spacy_spanish_lemmatizer
import stanza

from nltk.corpus import stopwords

class preprocessingClass:
    # Divide el texto en parrafos
    def divide_into_sentences(self, text, nlp):
        doc = nlp(text)

        sentences = []
        for sentence in doc.sentences:
            preprocessed_sentence = re.sub(" {2,}", " ", sentence.text)
            sentences.append(preprocessed_sentence)

        if len(sentences) == 0:
            sentences.append("00000")

        return sentences

    #Divide a un cuerpo/conjunto de documentos en sentencias
    def convert_into_sentences(self, corpus):
        doc_sents=[]
        doc_id = 0
        sent_id = 0

        nlp=stanza.Pipeline(lang="es", processors="tokenize")
        for text in corpus:
            sentences=self.divide_into_sentences(text, nlp)
            lista = []
            for sentence in sentences:
                lista.append((sent_id, sentence))
                sent_id += 1
            doc_sents.append((doc_id, lista))
            doc_id += 1
        return doc_sents

    # Metodo de preprocesamiento para una sentencia
    def spanish_preprocessor(self, sentence):
        tokenize=spacy.load('es_core_news_sm')
        # Separa el texto en palabras y lo lematiza
        tokenize.replace_pipe("lemmatizer", "spanish_lemmatizer")
        lematized_words=[word.lemma_ for word in tokenize(sentence)]

        # Remueve los signos de puntuación separados
        r=re.compile('[?¿¡!,.;:()"\'\s]+')
        list_of_words=[word for word in lematized_words if not r.match(word)]

        # Remueve las stopwords
        stop_words=set(stopwords.words('spanish'))
        tokenized_words=[word for word in list_of_words if word not in stop_words]

        return tokenized_words