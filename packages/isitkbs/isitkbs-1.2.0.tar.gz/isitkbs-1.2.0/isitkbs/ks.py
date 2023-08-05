import pickle
import os
import matplotlib.pyplot as plt
import pandas as pd
import re
from scipy.sparse import hstack, csr_matrix
import numpy as np
class isitkbs(object):
    
    def __init__(self, model='randomforest'):
        self.model = model
    # Especifica qual modelo deve ser utilizado
    # Por padrão, usa-se o randomForest

    # Função para determinar se uma palavra é keyboardsmashing
    # A entrada deve ser uma palavra
    def wordkbs(self, input_data):
        if not isinstance(input_data, str):
            raise TypeError("input_data must be a string")
        
        if aux._is_kbs_manual(string=input_data):
            return 1

        modelpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'models/{self.model}.pkl')
        vectpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'models/{self.model}_count_vectorizer.pkl')
        selpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models/rf_selectkbest.pkl')

        trained_model = pickle.load(open(modelpath, 'rb'))
        vectorizer = pickle.load(open(vectpath, 'rb'))
        selector = pickle.load(open(selpath, 'rb'))

        if (len(input_data) == 1):
            return 0

        input_ngram_features = vectorizer.transform([input_data])
        if self.model == 'randomforest':
            input_ngram_features = selector.transform(input_ngram_features)
        # Extract lexical features for the new string
        input_vowel_feature = csr_matrix(np.array(aux.type_ratio(input_data, 'v')).reshape(-1,1))
        input_consonant_feature = csr_matrix(np.array(aux.type_ratio(input_data, 'c')).reshape(-1,1))
        input_ttr_feature = csr_matrix(np.array(aux.ttr(input_data)).reshape(-1,1))

        # Combine the N-gram and lexical features into a single feature matrix
        input_lexical_features = hstack((input_vowel_feature, input_consonant_feature, input_ttr_feature))
        input_features = hstack((input_lexical_features, input_ngram_features))

        # Make the prediction using the trained model
        pred = trained_model.predict(input_features)
        predprob = trained_model.predict_proba(input_features)
        #print(f"{pred}:{predprob}")
        return pred[0]

    # Função para determinar quais são os keyboard smashing em uma frase
    # A entrada deve ser uma string ou uma lista de palavras
    def sentkbs(self, input_data):
        mashs = []
        
        if isinstance(input_data, str):
            words = input_data.split()
        elif isinstance(input_data, list):
            words = input_data
        else:
            return mashs

        for word in words:
            if isinstance(word, str):
                if ' ' in word:
                    mashs_partial = self.sentkbs(word)
                    mashs.extend(mashs_partial)
                else:
                    res = self.wordkbs(word)
                    if res == 1:
                        mashs.append(word)
        
        return mashs

    # Função que mostra a frequência de caracteres em keyboard smashing
    # A entrada deve ser uma string ou uma lista de string
    def freqkbs(self, input_data, graph=False):
        char_counts = {}
        cleaned_data = ' '.join(self.sentkbs(input_data))
        if cleaned_data:
            cleaned_data = re.sub(r'[^\w\s]', '', cleaned_data)
            for char in set(cleaned_data):
                char_counts[char] = cleaned_data.count(char)
            char_counts = dict(sorted(char_counts.items()))
            char_counts.pop(' ', None)
            if graph:
                self.__freqgraph(char_counts)
        return char_counts

    def __freqgraph(self, cont_char):
        # Determina eixo x e eixo y
        x_axis = list(cont_char.keys())
        y_axis = list(cont_char.values())

        # Nomeia os eixos
        plt.xlabel('Caracteres')
        plt.ylabel('Freq')

        # Plota o gráfico
        plt.bar(x_axis, y_axis)

    def replacekbs(self, input_data, value=None, inplace=False, just_word=False):
        """ 
        Parâmetros:
        dataframe: dataframe pandas do qual os keyboard smashing vão ser substituidos.
        value: string que vai substituir os keyboard smashings, caso seja uma string vazia as linhas que apresentarem kbs serão removidas do dataframe
        inplace: se as substituições serão feitas no próprio dataframe dos parâmetros (True) ou será retornada uma cópia do df (False)
        just_word: se False, a posição toda do dataframe é substituído por value, se True somente o kbs presente na posição é substituido
        Ex: "This isdas test" -> "KBS" (just_word False)
                              -> "This KBS test" (just_word True)
        """
        value = value or "itskbs"
        
        """ 
        Se o tipo de entrada for um dataframe pandas, a função __dataframe é chamada para fazer o tratamento
        """
        if isinstance(input_data, pd.DataFrame):
            df = input_data.copy(deep=False) if inplace else input_data.copy()
            return self.__dataframe(df, value, just_word)

        """ 
        Se o tipo de entrada for uma lista ou uma string de palavras, a função __listOrString é chamada
        """
        if isinstance(input_data, str) or isinstance(input_data, list):
            return self.__listOrString(input_data, value, just_word)

    def __dataframe(self, df, value, just_word):
        wordskbs = []
        nRow = df.shape[0]
        nCol = df.shape[1]
        mashsIndex = []
        for row in range(nRow):
            for col in range(nCol):
                wordskbs = self.sentkbs(df.iloc[row, col])
                if (len(wordskbs) != 0):
                    if (just_word == False):
                        if(value == 'itskbs'):
                            mashsIndex.append(row)
                        else:
                            df.iloc[row, col] = value
                    else:
                        df.iloc[row, col] = self.replacekbs(
                            df.iloc[row, col], value)
        df.drop(mashsIndex, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def __listOrString(self, input_data, value='itskbs', just_word=False):
        is_list = True
        if type(input_data) == str:
            input_data = input_data.split()
            is_list = False
        
        wordskbs = self.sentkbs(input_data)
        output_data = []
        for i in input_data:
            if ' ' in i:
                sent = self.__listOrString(i, value, just_word)
                if just_word:
                    output_data.append(sent)
                    continue
                elif sent != i:
                    output_data.append(value)
                    continue
            if value == 'itskbs':
                if i not in wordskbs:
                    output_data.append(i)
            else:
                output_data.append(value if i in wordskbs else i)
        return ' '.join(output_data) if not is_list else output_data
    


class aux(object):

    # Funções auxiliares
    @classmethod
    def letter_counter(cls, string, type=None):
        if (type == 'c'):
            return {letter: str(string).count(letter) for letter in 'bcdfghjklmnpqrstvwxyz'}
        elif (type == 'v'):
            return {letter: str(string).count(letter) for letter in 'aeiou'}  
        return {letter: str(string).count(letter) for letter in 'abcdefghijklmnopqrstuvwxyz'}

    @classmethod
    def type_counter(cls, string, type=None):    
        return sum(cls.letter_counter(string, type).values())
    
    @classmethod
    def type_ratio(cls, string, type=None):
        if (len(string) == 0):
            return 0
        return cls.type_counter(string, type)/len(string)

    @classmethod
    def bigram_counter(cls, lista):
        dic = {}
        for i in lista:
            if i in dic:
                dic[i] +=1
            else:
                dic[i] =1
        return dic

    @classmethod
    def bigrams(cls, string):
        bigrams = []
        for i in range(len(string)-1):
            bigrams.append(string[i]+string[i+1])

        return cls.bigram_counter(bigrams)

    @classmethod
    def bigram_max_occurance(cls, string):
        try:
            return (sorted(cls.bigrams(string).values(), reverse=True))[0]
        except:
            return 0
        
    @classmethod
    def ttr(cls, string):
        if (len(string) == 0):
            return 0
        ttr = len(set(string)) / len(string)
        return ttr


    def __bigramas_proibidos(self, string):
        proibidos = ['zx', 'xj', 'wx', 'vx', 'vq', 'vj', 'vf', 'sx', 'qz', 'qx', 'qk', 'qj', 'qc', 'jz', 'jx', 'jq', 'jf', 'hx', 'gx', 'fq', 'bx', 
                     'cv', 'cx', 'dx', 'fv', 'fx', 'fz', 'gv', 'jg', 'jk', 'jl', 'jm', 'jt', 'jv', 'jw', 'kq', 'kx', 'kz', 'pq', 'px', 'qd', 'qe', 
                     'qf', 'qg', 'qh', 'ql', 'qm', 'qn', 'qo', 'qp', 'qr', 'qs', 'qv', 'qw', 'qy', 'vb', 'vm', 'vp', 'vw', 'vz', 'xz', 'zj']

        bigramas = self.bigrams(string)

        for bigrama in bigramas:
            if bigrama in proibidos:
                return 1
        return 0   
    
    def __repeticao_de_bigramas(self, string, len):
        max_o = self.bigram_max_occurance(string)
        if (max_o == 4 and len < 12) or max_o > 4:
            return True 
        return False

    
    # Resultado
    @classmethod
    def _is_kbs_manual(cls, string):
        try:    
            length = len(string)
            
            if cls.__repeticao_de_bigramas(cls, string, length): return 1
            if cls.__bigramas_proibidos(cls, string): return 1
        except:
            return 0
