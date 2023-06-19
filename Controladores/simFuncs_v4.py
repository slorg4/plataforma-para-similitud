from Controladores.preprocessing_functions import preprocessingClass

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.spatial import distance

from nltk.corpus import stopwords

from sentence_transformers import SentenceTransformer

import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

class similarities:
    preprocessor = preprocessingClass()
    model1 = SentenceTransformer('distiluse-base-multilingual-cased-v1')
    model2 = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    model3 = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

    tfidf_vectors = [] # Almacena los documentos vectorizados para el modelo de bolsa de palabras con TF-IDF
    tfidf_binary_vectors = [] # Almacena los documentos vectorizados para el modelo de bolsa de palabras con valores binarios
    model1_vectors = [] # Almacena los documentos vectorizados para el model1 basado en Sentence-Transformers
    model2_vectors = [] # Almacena los documentos vectorizados para el model2 basado en Sentence-Transformers
    model3_vectors = [] # Almacena los documentos vectorizados para el model3 basado en Sentence-Transformers
    doc2vec_vectors = [] # Almacena los documentos vectorizados para el modelo basado en Doc2Vec

    #Obtiene el promedio de los resultados de las comparaciones entre sentencias
    #Esta funcion se utiliza para obtener el resultado d2 vs d1 a partir de las comparaciones d1 vs d2,
    # evitando obtener nuevamente los resultados de las comparaciones entre sentencias
    def get_average_results_by_dict(self, comparation_results):
        average_result = 0.0
        single_results = 0.0
        for sentence in comparation_results.keys():
            single_results += max(comparation_results[sentence])
        average_result = single_results/ len(comparation_results)
        return average_result

    #Realiza la vectorización de los documentos basandose en el modelo de bolsa de palabras con TF-IDF
    def get_comp_vectors_by_tfidfvectorizer(self, docs_sentences):
        corpus = [sentence for doc_id, doc in docs_sentences for sent_id, sentence in doc]
        comp_vectors = []
        _stopwords=list(set(stopwords.words('spanish')))
        vectorizer=TfidfVectorizer(stop_words=_stopwords)
        vectors = vectorizer.fit_transform(corpus).toarray()
        for doc_id, doc in docs_sentences:
            vec = []
            for sent_id, sent in doc:
                vec.append((sent_id, vectors[sent_id]))
            comp_vectors.append((doc_id, vec))

        return comp_vectors

    # Realiza la vectorización de los documentos basandose en el modelo de bolsa de palabras con valores binarios
    def get_comp_vectors_by_binaryvectorizer(self, docs_sentences):
        corpus = [sentence for doc_id, doc in docs_sentences for sent_id, sentence in doc]
        comp_vectors = []
        _stopwords=list(set(stopwords.words('spanish')))
        vectorizer = CountVectorizer(binary=True, stop_words=_stopwords)
        vectors = vectorizer.fit_transform(corpus).toarray()
        for doc_id, doc in docs_sentences:
            vec = []
            for sent_id, sent in doc:
                vec.append((sent_id, vectors[sent_id]))
            comp_vectors.append((doc_id, vec))

        return comp_vectors

    # Realiza la vectorización de los documentos basandose en cualquier modelo basado en Sentence-Transformers
    def get_comp_vectors_by_stransformers(self, docs_sentences, model):
        comp_vectors = []
        for doc_id, doc in docs_sentences:
            lista = []
            for sent_id, sentence in doc:
                embedding = model.encode(sentence, convert_to_numpy=True)
                lista.append((sent_id, embedding))
            comp_vectors.append((doc_id, lista))

        return comp_vectors

    # Divide las sentencias de un documento en terminos
    # Funcion necesaria para la creacion del modelo de Doc2Vec
    def get_tokenized_sentences(self, docs_sents):
        tokenized_sentences = []
        for doc_id, doc in docs_sents:
            for sent_id, sentence in doc:
                tokenized_sentence = self.preprocessor.spanish_preprocessor(sentence)
                tokenized_sentences.append((sent_id, tokenized_sentence))

        return tokenized_sentences

    # Realiza la vectorización de los documentos basandose en el modelo basado en Doc2Vec
    def get_comp_vectors_by_doc2vec(self, docs_sents, model):
        comp_vectors=[]
        vectors=np.array(model.docvecs.vectors.data)
        for doc_id, doc in docs_sents:
            lista=[]
            for sent_id, sentence in doc:
                vector=vectors[sent_id]
                lista.append((sent_id, vector))
            comp_vectors.append((doc_id, lista))

        return comp_vectors

    # Obtiene los resultados de las comparaciones entre los documentos vectorizados
    # La medida de similitud utilizada se determina en base al parametro "sim_function"
    # Devuelve un arreglo de dimensiones nxn segun la cantidad de documentos
    def get_vectors_results(self, docs_vectors, sim_function):
        results = csr_matrix((len(docs_vectors), len(docs_vectors)), dtype=np.float64)
        list_of_comparations = []

        for doc_id1, vectors1 in docs_vectors:
            for doc_id2, vectors2 in docs_vectors:
                if (doc_id1, doc_id2) not in list_of_comparations:
                    if doc_id1 == doc_id2:
                        results[doc_id1, doc_id2] = 1.0
                        list_of_comparations.append((doc_id1, doc_id2))
                    else:
                        single_results = []
                        comparation_results = {}
                        provisional_matrix = []
                        for sent_id1, vector1 in vectors1:
                            highest_score = 0.0
                            for sent_id2, vector2 in vectors2:
                                if sent_id2 not in comparation_results.keys(): comparation_results[sent_id2] = []
                                score = sim_function(vector1, vector2) # Resultado de la comparacion entre un vector 1 y vector 2
                                comparation_results[sent_id2].append(score)
                                if score > highest_score: highest_score = score
                                if highest_score >= 0.9: break
                            single_results.append(highest_score)
                        average_result1=sum(single_results) / len(single_results)
                        average_result2=self.get_average_results_by_dict(comparation_results)
                        results[doc_id1, doc_id2] = average_result1
                        results[doc_id2, doc_id1] = average_result2
                        list_of_comparations.append((doc_id1, doc_id2))
                        list_of_comparations.append((doc_id2, doc_id1))

        return results.toarray()

    # Obtiene el coeficiente de jaccard entre dos vectores con valores binarios
    def jaccard_binary(self, x, y):
        vector1 = np.array(x)
        vector2 = np.array(y)
        intersection = np.logical_and(vector1, vector2)
        union = np.logical_or(vector1, vector2)
        try:
            similarity = float(intersection.sum()) / float(union.sum())
        except:
            similarity = 0.0
        return similarity

    # Obtiene el coeficiente de dice entre dos vectores con valores binarios
    def dice_binary(self, x, y):
        vector1 = np.array(x)
        vector2 = np.array(y)
        numerator = 2 * (np.logical_and(x, y).sum())
        denominator = vector1.sum() + vector2.sum()
        try:
            similarity = float(numerator) / float(denominator)
        except:
            similarity = 0.0
        return similarity

# Las siguientes funciones se encargan de llamar a las funciones de preprocesamiento, vectorizacion
#   y obtención de resultados de un conjunto de documentos
# El parametro "paths" indica el directorio de cada documento del conjunto
# El parametro "texts" indica el texto plano de cada documento del conjunto
# El parametro "vectors" puede utilizarse en caso de poseer los documentos ya vectorizados,
#   en caso contrario se envía una lista vacía
# El parametro "update_ui" es la funcion que emite el porcentaje del progreso de la funcion
# Toda funcion devuelve un id para los documentos vectorizados, los documentos vectorizados,
#   y los resultados de todas las comparaciones entre los documentos


#########################SIMILITUDES CON LA LIBREARIA SENTENCE-TRANSFORMERS 1####################
    def get_cossim_by_model1(self, paths, texts, vectors, update_ui):
        cossim_function = lambda doc1, doc2: cosine_similarity([doc1, doc2])[0][1]
        model_name, saved_vectors = vectors
        if model_name == "model1" and len(saved_vectors) > 0: self.model1_vectors = saved_vectors

        if len(self.model1_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model1)
            self.model1_vectors = docs_vectors
        else:
            docs_vectors = self.model1_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, cossim_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model1", docs_vectors), plagiarism_results

    def get_euclidean_by_model1(self, paths, texts, vectors, update_ui):
        euclid_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'euclidean')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "model1" and len(saved_vectors) > 0: self.model1_vectors = saved_vectors

        if len(self.model1_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model1)
            self.model1_vectors = docs_vectors
        else:
            docs_vectors = self.model1_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, euclid_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model1", docs_vectors), plagiarism_results

    def get_manhattan_by_model1(self, paths, texts, vectors, update_ui):
        manh_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'cityblock')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "model1" and len(saved_vectors) > 0: self.model1_vectors = saved_vectors

        if len(self.model1_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model1)
            self.model1_vectors = docs_vectors
        else:
            docs_vectors = self.model1_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, manh_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model1", docs_vectors), plagiarism_results

#########################SIMILITUDES CON LA LIBREARIA SENTENCE-TRANSFORMERS 2####################
    def get_cossim_by_model2(self, paths, texts, vectors, update_ui):
        cossim_function = lambda doc1, doc2: cosine_similarity([doc1, doc2])[0][1]
        model_name, saved_vectors = vectors
        if model_name == "model2" and len(saved_vectors) > 0: self.model2_vectors = saved_vectors

        if len(self.model2_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model2)
            self.model2_vectors = docs_vectors
        else:
            docs_vectors = self.model2_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, cossim_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model2", docs_vectors), plagiarism_results

    def get_euclidean_by_model2(self, paths, texts, vectors, update_ui):
        euclid_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'euclidean')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "model2" and len(saved_vectors) > 0: self.model2_vectors = saved_vectors

        if len(self.model2_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model2)
            self.model2_vectors = docs_vectors
        else:
            docs_vectors = self.model2_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, euclid_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model2", docs_vectors), plagiarism_results

    def get_manhattan_by_model2(self, paths, texts, vectors, update_ui):
        manh_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'cityblock')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "model2" and len(saved_vectors) > 0: self.model2_vectors = saved_vectors

        if len(self.model2_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model2)
            self.model2_vectors = docs_vectors
        else:
            docs_vectors = self.model2_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, manh_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model2", docs_vectors), plagiarism_results

#########################SIMILITUDES CON LA LIBREARIA SENTENCE-TRANSFORMERS 3####################
    def get_cossim_by_model3(self, paths, texts, vectors, update_ui):
        cossim_function = lambda doc1, doc2: cosine_similarity([doc1, doc2])[0][1]
        model_name, saved_vectors = vectors
        if model_name == "model3" and len(saved_vectors) > 0: self.model3_vectors = saved_vectors

        if len(self.model3_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model3)
            self.model3_vectors = docs_vectors
        else:
            docs_vectors = self.model3_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, cossim_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model3", docs_vectors), plagiarism_results

    def get_euclidean_by_model3(self, paths, texts, vectors, update_ui):
        euclid_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'euclidean')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "model3" and len(saved_vectors) > 0: self.model3_vectors = saved_vectors

        if len(self.model3_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model3)
            self.model3_vectors = docs_vectors
        else:
            docs_vectors = self.model3_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, euclid_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model3", docs_vectors), plagiarism_results

    def get_manhattan_by_model3(self, paths, texts, vectors, update_ui):
        manh_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'cityblock')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "model3" and len(saved_vectors) > 0: self.model3_vectors = saved_vectors

        if len(self.model3_vectors) == 0:
            doc_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_stransformers(doc_sents, self.model3)
            self.model3_vectors = docs_vectors
        else:
            docs_vectors = self.model3_vectors
        update_ui(percent=50)

        sim_results = self.get_vectors_results(docs_vectors, manh_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("model3", docs_vectors), plagiarism_results

#########################SIMILITUDES UTILIZANDO DOC2VEC#######################################
    def get_cossim_by_doc2vec(self, paths, texts, vectors, update_ui):
        cossim_function = lambda doc1, doc2: cosine_similarity([doc1, doc2])[0][1]
        model_name, saved_vectors = vectors
        if model_name == "doc2vec" and len(saved_vectors) > 0: self.doc2vec_vectors = saved_vectors

        if len(self.doc2vec_vectors) == 0:
            docs_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=10)
            # Formateando los documentos para entrenar el modelo
            data = self.get_tokenized_sentences(docs_sents)
            tagged_data = [TaggedDocument(words=_d, tags=[str(id)]) for id, _d in data]
            # Inicializando doc2vec
            model=gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=1, epochs=2000)
            # Creando vocabulario
            model.build_vocab(tagged_data)
            update_ui(percent=25)
            # Entrenando doc2vec
            model.train(tagged_data, total_examples=model.corpus_count, epochs=2000)
            # Vectorizando las sentencias

            docs_vectors = self.get_comp_vectors_by_doc2vec(docs_sents, model)
            self.doc2vec_vectors = docs_vectors
        else:
            docs_vectors = self.doc2vec_vectors
        update_ui(percent=50)

        
        sim_results=self.get_vectors_results(docs_vectors, cossim_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("doc2vec", docs_vectors), plagiarism_results

    def get_euclidean_by_doc2vec(self, paths, texts, vectors, update_ui):
        euclid_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'euclidean')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "doc2vec" and len(saved_vectors) > 0: self.doc2vec_vectors = saved_vectors

        if len(self.doc2vec_vectors) == 0:
            docs_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=10)
            # Formateando los documentos para entrenar el modelo
            data = self.get_tokenized_sentences(docs_sents)
            tagged_data = [TaggedDocument(words=_d, tags=[str(id)]) for id, _d in data]
            # Inicializando doc2vec
            model=gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=1, epochs=2000)
            # Creando vocabulario
            model.build_vocab(tagged_data)
            update_ui(percent=25)
            # Entrenando doc2vec
            model.train(tagged_data, total_examples=model.corpus_count, epochs=2000)

            # Vectorizando las sentencias
            docs_vectors = self.get_comp_vectors_by_doc2vec(docs_sents, model)
            self.doc2vec_vectors = docs_vectors
        else:
            docs_vectors = self.doc2vec_vectors
        update_ui(percent=50)

        sim_results=self.get_vectors_results(docs_vectors, euclid_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("doc2vec", docs_vectors), plagiarism_results

    def get_manhattan_by_doc2vec(self, paths, texts, vectors, update_ui):
        manh_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'cityblock')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "doc2vec" and len(saved_vectors) > 0: self.doc2vec_vectors = saved_vectors

        if len(self.doc2vec_vectors) == 0:
            docs_sents = self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=10)
            # Formateando los documentos para entrenar el modelo
            data = self.get_tokenized_sentences(docs_sents)
            tagged_data = [TaggedDocument(words=_d, tags=[str(id)]) for id, _d in data]
            # Inicializando doc2vec
            model=gensim.models.doc2vec.Doc2Vec(vector_size=300, min_count=1, epochs=2000)
            # Creando vocabulario
            model.build_vocab(tagged_data)
            update_ui(percent=25)
            # Entrenando doc2vec
            model.train(tagged_data, total_examples=model.corpus_count, epochs=2000)
            # Vectorizando las sentencias
            docs_vectors = self.get_comp_vectors_by_doc2vec(docs_sents, model)
            self.doc2vec_vectors = docs_vectors
        else:
            docs_vectors = self.doc2vec_vectors
        update_ui(percent=50)

        sim_results=self.get_vectors_results(docs_vectors, manh_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("doc2vec", docs_vectors), plagiarism_results

###################SIMILITUDES UTILIZANDO EL MODELO BASADO EN BOLSA DE PALABRAS##################
# Hace uso de las clases TfidfVectorizer y CountVectorizer de la biblioteca scikit-learn
    def get_cossim_by_tfidf(self, paths, texts, vectors, update_ui):
        cossim_function=lambda doc1, doc2: cosine_similarity([doc1, doc2])[0][1]
        model_name, saved_vectors = vectors
        if model_name == "tfidf" and len(saved_vectors) > 0: self.tfidf_vectors = saved_vectors

        if len(self.tfidf_vectors) == 0:
            # Comienza el tiempo del preprocesamiento de los documentos
            doc_sents=self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_tfidfvectorizer(doc_sents)
            self.tfidf_vectors = docs_vectors
        else:
            docs_vectors = self.tfidf_vectors
        update_ui(percent=50)

        sim_results=self.get_vectors_results(docs_vectors, cossim_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        counter = 1
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)
            update_ui(percent=counter)
            counter+=1


        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("tfidf", docs_vectors), plagiarism_results

    def get_euclidean_by_tfidf(self, paths, texts, vectors, update_ui):
        euclid_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'euclidean')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "tfidf" and len(saved_vectors) > 0: self.tfidf_vectors = saved_vectors

        if len(self.tfidf_vectors) == 0:
            # Comienza el tiempo del preprocesamiento de los documentos
            doc_sents=self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_tfidfvectorizer(doc_sents)
            self.tfidf_vectors = docs_vectors
        else:
            docs_vectors = self.tfidf_vectors
        update_ui(percent=50)

        sim_results=self.get_vectors_results(docs_vectors, euclid_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("tfidf", docs_vectors), plagiarism_results

    def get_manhattan_by_tfidf(self, paths, texts, vectors, update_ui):
        manh_function = lambda doc1, doc2: 1/(1 + distance.cdist([doc1], [doc2], 'cityblock')[0][0])
        model_name, saved_vectors = vectors
        if model_name == "tfidf" and len(saved_vectors) > 0: self.tfidf_vectors = saved_vectors

        if len(self.tfidf_vectors) == 0:
            # Comienza el tiempo del preprocesamiento de los documentos
            doc_sents=self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_tfidfvectorizer(doc_sents)
            self.tfidf_vectors = docs_vectors
        else:
            docs_vectors = self.tfidf_vectors
        update_ui(percent=50)

        sim_results=self.get_vectors_results(docs_vectors, manh_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("tfidf", docs_vectors), plagiarism_results

    def get_jaccard_by_tfidf(self, paths, texts, vectors, update_ui):
        jacc_function = lambda doc1, doc2: self.jaccard_binary(doc1, doc2)
        model_name, saved_vectors = vectors
        if model_name == "binary" and len(saved_vectors) > 0: self.tfidf_binary_vectors = saved_vectors

        if len(self.tfidf_binary_vectors) == 0:
            # Comienza el tiempo del preprocesamiento de los documentos
            doc_sents=self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_binaryvectorizer(doc_sents)
            self.tfidf_binary_vectors = docs_vectors
        else:
            docs_vectors = self.tfidf_binary_vectors
        update_ui(percent=50)

        sim_results=self.get_vectors_results(docs_vectors, jacc_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("binary", docs_vectors), plagiarism_results

    def get_dice_by_tfidf(self, paths, texts, vectors, update_ui):
        dice_function = lambda doc1, doc2: self.dice_binary(doc1, doc2)
        model_name, saved_vectors = vectors
        if model_name == "binary" and len(saved_vectors) > 0: self.tfidf_binary_vectors = saved_vectors

        if len(self.tfidf_binary_vectors) == 0:
            doc_sents=self.preprocessor.convert_into_sentences(texts)
            update_ui(percent=25)

            docs_vectors = self.get_comp_vectors_by_binaryvectorizer(doc_sents)
            self.tfidf_binary_vectors = docs_vectors
        else:
            docs_vectors = self.tfidf_binary_vectors
        update_ui(percent=50)

        sim_results=self.get_vectors_results(docs_vectors, dice_function)
        update_ui(percent=80)

        # Obtiene los resultados de plagio en formato adecuado
        plagiarism_results=[]
        for n in range(len(paths)):
            for m in range(len(paths)):
                document_pair=(paths[n], paths[m])
                score=(document_pair[0], document_pair[1], sim_results[n][m])
                plagiarism_results.append(score)

        plagiarism_results=sorted(plagiarism_results)
        update_ui(percent=99)
        return ("binary", docs_vectors), plagiarism_results
