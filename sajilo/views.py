from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from fuzzywuzzy import fuzz
import numpy as np
import pandas as pd
import gensim
from scipy.spatial.distance import cosine, cityblock, jaccard, canberra, euclidean, minkowski, braycurtis




def index(request):
    return render(request,'sajilo/index.html')



def searchlist(request):
    question1 = str.lower(request.GET.get('q1'))
    question2= str.lower(request.GET.get('q2'))
    if question1 and question2:
        len_1 = len(question1)
        len_2 = len(question2)

        diff_len = len_1 - len_2

        len_char_q1 = len(''.join(set(str(question1).replace(' ', ''))))
        len_char_q2 = len(''.join(set(str(question2).replace(' ', ''))))
        len_word_q1 = len(str(question1).split())
        len_word_q2 = len(str(question2).split())

        common_words = len(set(str(question1).lower().split()).intersection(set(str(question2).lower().split())))

        fuzz_qratio = fuzz.QRatio(str(question1), str(question2))
        fuzz_WRatio = fuzz.WRatio(str(question1), str(question2))
        fuzz_partial_ratio = fuzz.partial_ratio(str(question1), str(question2))
        fuzz_partial_token_set_ratio = fuzz.partial_token_set_ratio(str(question1), str(question2))
        fuzz_partial_token_sort_ratio = fuzz.partial_token_sort_ratio(str(question1), str(question2))
        fuzz_token_set_ratio = fuzz.token_set_ratio(str(question1), str(question2))
        fuzz_token_sort_ratio = fuzz.token_sort_ratio(str(question1), str(question2))

        model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

        # sen2vec
        import scipy
        error_count = 0
        from nltk import word_tokenize
        from nltk.corpus import stopwords
        stop_words = stopwords.words('english')

        def sent2vec(s):
            words = str(s).lower()  # .decode('utf-8') ahile kaam lagdaina
            words = word_tokenize(words)
            words = [w for w in words if not w in stop_words]
            words = [w for w in words if w.isalpha()]
            M = []
            for w in words:
                try:
                    M.append(model[w])
                except:
                    continue
            M = np.array(M)
            v = M.sum(axis=0)
            return v / np.sqrt((v ** 2).sum())

        question1_vector = sent2vec(question1)
        question2_vector = sent2vec(question2)

        cosine_distance = cosine(question1_vector, question2_vector)
        cityblock_distance = cityblock(question1_vector, question2_vector)
        jaccard_distance = jaccard(question1_vector, question2_vector)
        canberra_distance = canberra(question1_vector, question2_vector)
        euclidean_distance = euclidean(question1_vector, question2_vector)
        minkowski_distance = minkowski(question1_vector, question2_vector, 3)
        braycurtis_distance = braycurtis(question1_vector, question2_vector)

        # prediction with classifier
        question = np.array([[diff_len, common_words, fuzz_qratio, fuzz_WRatio, fuzz_partial_ratio,
                              fuzz_partial_token_set_ratio, fuzz_partial_token_sort_ratio,
                              fuzz_token_set_ratio, fuzz_token_sort_ratio, cosine_distance, cityblock_distance,
                              canberra_distance, euclidean_distance, minkowski_distance,
                              braycurtis_distance]])

        from keras.models import load_model
        model = load_model('ANNmodel.h5')
        result = model.predict(question)


        context = {
            "question1": question1,
            "question2": question2,
            "len_1": len_1,
            "len_2": len_2,

            "diff_len": diff_len,

            "len_char_q1":len_char_q1,
            "len_char_q2": len_char_q2,
            "len_word_q1": len_word_q1,
            "len_word_q2": len_word_q2,

            "common_words": common_words,

            "fuzz_qratio": fuzz_qratio,
            "fuzz_WRatio": fuzz_WRatio,
            "fuzz_partial_ratio": fuzz_partial_ratio,
            "fuzz_partial_token_set_ratio": fuzz_partial_token_set_ratio,
            "fuzz_partial_token_sort_ratio": fuzz_partial_token_sort_ratio,
            "fuzz_token_set_ratio": fuzz_token_set_ratio,
            "fuzz_token_sort_ratio": fuzz_token_sort_ratio,

            "cosine_distance": cosine_distance,
            "cityblock_distance":cityblock_distance,
            "jaccard_distance":jaccard_distance,
            "canberra_distance":canberra_distance,
            "euclidean_distance":euclidean_distance,
            "minkowski_distance":minkowski_distance,
            "braycurtis_distance":braycurtis_distance,

            "result": result,



        }




        return render(request, 'sajilo/searchlist.html', context)





