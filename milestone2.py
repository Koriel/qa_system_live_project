import pandas
import sklearn
import gensim
from gensim.models import Doc2Vec
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

questions = [
    'What fuel is used for the manufacturing of chlorine?',
    'What metric is used for evaluating emission?',
    'How can carbon emission of the processes of cement clinker be reduced?',
    'How is the Weighted Cogeneration Threshold calculated?',
    'What are carbon capture and sequestration?',
    'What stages does CCS consist of?',
    'What should be the average energy consumption of a water supply system?',
    'What are sludge treatments? -What is the process of anaerobic digestion?',
    'How is reforestation defined?',
    'What is the threshold of emission for inland passenger water transport?',
    'What are the requirements of reporting for electricity generation from natural gas where there might be fugitive emissions?',
]


# TfidfVectorizer
# linear_kernel


# gensim - Doc2vec alternate
# most_similar - gensim cosine distance
def read_corpus(text, tokens_only=False):
    for i, line in enumerate(text):
        tokens = gensim.utils.simple_preprocess(line)
        if tokens_only:
            yield tokens
        else:
            # For training data, add tags
            yield gensim.models.doc2vec.TaggedDocument(tokens, [i])


if __name__ == '__main__':
    paragraphs = pandas.read_csv('./eu_paragraphs.csv')

    stop_words = text.ENGLISH_STOP_WORDS
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    # for paragraph in paragraphs['paragraph'].tolist():
    #     X = vectorizer.fit_transform(paragraph)
    #     for question in questions:
    #         questions_vectorizer = TfidfVectorizer()
    #         question_vector = questions_vectorizer.fit_transform(question)
    #         distance = linear_kernel(question_vector[0], X[0])
    #         print( distance )
    X = vectorizer.fit_transform(paragraphs['paragraph'])
    # print(paragraphs)
    print(X)
    # print(X.shape)
    # linear_kernel(X, questions)

    # questions_vectors = vectorizer.transform(questions)
    # print(questions_vectors)
    # for question_vector in questions_vectors:
    #     distances = linear_kernel(question_vector, X).flatten()
    #     print(paragraphs["paragraph"][distances.argsort()[-1]])
    for question in questions:
        question_vector = vectorizer.transform([question])
        similarities = linear_kernel(question_vector, X).flatten()
        print(question)
        print(similarities.argsort()[-1])
        print(paragraphs["paragraph"][similarities.argsort()[-1]])

    # for question in questions:
    #     question_vectors = vectorizer.fit_transform(question)
    #     print(question_vectors)
    #     distance = linear_kernel(question_vectors, X)
    #     # print( distance )
    corpus = read_corpus(paragraphs["paragraph"])
    d2v = Doc2Vec()
    d2v.build_vocab(corpus)
    d2v.train(corpus, total_examples=d2v.corpus_count, epochs=d2v.epochs)
