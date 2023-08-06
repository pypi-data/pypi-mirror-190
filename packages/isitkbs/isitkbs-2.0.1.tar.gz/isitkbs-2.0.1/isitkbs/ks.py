import pickle
import os
import matplotlib.pyplot as plt
import pandas as pd
import re
from scipy.sparse import hstack, csr_matrix
import numpy as np
import warnings
warnings.filterwarnings("ignore")
class isitkbs(object):

    def __init__(self, model='randomforest'):
        """Classe para detecção de keyboard smashing. 

        :param model: {'randomforest', 'naivebayes'} Modelo a ser utilizado para detecção de keyboard smashing. O randomforest tem a acurácia ligeiramente maior, contudo é mais lento que o naivebayes, default='randomforest'
        :type model: str, opcional
        """
        self.model = model

    def wordkbs(self, input_data):
        """Verifica se a string input_data apresenta algum keyboard smashing ou não. Se input_data for uma única palavra
        a função retorna se essa palavra é ou não keyboard smashing. Já no caso de input_data ser uma frase, a função retorna se essa frase
        apresenta algum keyboard smashing ou não. 

        :param input_data: Dado de entrada
        :type input_data: string
        :raises TypeError: Se a entrada não for uma string esse erro é lançado
        :return:  1 se input_data é um keyboard smashing, 0 caso contrário
        :rtype: int
        """
        
        if not isinstance(input_data, str):
            raise TypeError("input_data must be a string")
        
        if lex_extractor._is_kbs_manual(string=input_data):
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

        input_vowel_feature = csr_matrix(np.array(lex_extractor.type_ratio(input_data, 'v')).reshape(-1,1))
        input_consonant_feature = csr_matrix(np.array(lex_extractor.type_ratio(input_data, 'c')).reshape(-1,1))
        input_ttr_feature = csr_matrix(np.array(lex_extractor.ttr(input_data)).reshape(-1,1))

        input_lexical_features = hstack((input_vowel_feature, input_consonant_feature, input_ttr_feature))
        input_features = hstack((input_lexical_features, input_ngram_features))

        pred = trained_model.predict(input_features)
        return pred[0]

    def sentkbs(self, input_data):
        """Verifica se input_data apresenta algum keyboard smashing, e caso apresente, retorna a lista de mashings.

        :param input_data: Dado de entrada
        :type input_data: string ou lista
        :return: Uma lista com os keyboard smashings que foram identificados em input_data
        :rtype: lista
        """
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

    def freqkbs(self, input_data, graph=False):
        """Conta a frequência das letras que formam os keyboard smashings identificados em input_data e as retorna como um dicionário, caso graph=True também plota o gráfico correspondente.

        :param input_data: Dado de entrada
        :type input_data: string ou lista
        :param graph: Caso 'True' plota o gráfico de frequência, caso contrário não, default=False
        :type graph: bool, opcional
        :return: Um dicionário em que as chaves são as letras que formam os keyboard smashings presentes em input_data e os valores são a quantidade de vezes em que elas aparecem.
        :rtype: dicionário
        """
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
        """Função auxiliar para plotar o gráfico de frequência caso a função freqkbs seja chamada com o parâmetro 'graph=True'.

        :param cont_char: Dicionário com a frequência dos caracteres
        :type cont_char: dicionário
        """
        # Determina eixo x e eixo y
        x_axis = list(cont_char.keys())
        y_axis = list(cont_char.values())

        # Nomeia os eixos
        plt.xlabel('Caracteres')
        plt.ylabel('Freq')

        # Plota o gráfico
        plt.bar(x_axis, y_axis)

    def replacekbs(self, input_data, value=None, inplace=False, just_word=False):
        """Identifica os keyboard smashings em uma lista, string ou pd.DataFrame input_data e os substitui pelo valor de value, caso value seja vazio os keyboard smashings
        são deletados. Caso input_data seja um dataframe e just_word=False substitui toda a linha em que o keyboard smashing estiver presente

        :param input_data: Dados de entrada.
        :type input_data: string ou lista ou pd.DataFrame
        :param value: Valor pelo qual os keyboard smashings serão substituídos, caso vazio os mashings são apagados, default=None
        :type value: string, opcional
        :param inplace: Só faz efeito caso input_data seja um pd.DataFrame. Caso 'True' a substituição ocorre diretamente no dataframe, caso contrário é criada uma cópia dele, default=False
        :type inplace: bool, opcional
        :param just_word: Caso 'True' somente o keyboard smashing é substituído, caso contrário toda a linha do dataframe ou string da lista em que ele está inserido é substituída, default=False
        :type just_word: bool, opcional
        :return: Uma cópia de input_data com os keyboard smashings identificados substituídos pelo valor passado no parâmetro value. Caso input_data seja um pd.DataFrame e o parâmetro inplace=True o retorno é nulo, pois as substituições são feitas inplace.  
        :rtype: string ou lista ou pd.DataFrame
        """        
        
        value = value or "itskbs"

        # Se o tipo de entrada for um dataframe pandas, a função __dataframe é chamada para fazer o tratamento
        if isinstance(input_data, pd.DataFrame):
            df = input_data.copy(deep=False) if inplace else input_data.copy()
            return self.__dataframe(df, value, just_word)

        # Se o tipo de entrada for uma lista ou uma string de palavras, a função __listOrString é chamada
        if isinstance(input_data, str) or isinstance(input_data, list):
            return self.__listOrString(input_data, value, just_word)

    def __dataframe(self, df, value, just_word):
        """Função auxiliar para lidar com dataframes caso o input_data da replacekbs seja pd.DataFrame. Identifica os keyboard smashings em um dataframe 
           e os substitui pelo valor de value, caso value seja vazio os keyboard smashings são deletados. Caso just_word=False substitui toda a linha em que o keyboard smashing estiver presente.

        :param df: Dataframe do qual os keyboard smashings serão substituídos
        :type df: pd.DataFrame
        :param value: Valor pelo qual os keyboard smashings serão substituídos, caso vazio os mashings são apagados
        :type value: string
        :param just_word: Caso 'True' somente o keyboard smashing é substituído, caso contrário toda a linha do dataframe em que ele está inserido é substituída
        :type just_word: bool
        :return: Uma cópia de input_data com os keyboard smashings identificados substituídos pelo valor passado no parâmetro value.
        :rtype: pd.DataFrame
        """
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
        """_summary_

        :param input_data: String ou lista do qual os keyboard smashings serão substituídos
        :type input_data: lista ou string
        :param value: Valor pelo qual os keyboard smashings serão substituídos, caso vazio os mashings são apagados, defaults='itskbs'
        :type value: str, optional
        :param just_word: Caso 'True' somente o keyboard smashing é substituído, caso contrário toda a linha do dataframe ou string da lista em que ele está inserido é substituída, defaults=False
        :type just_word: bool, optional
        :return: Uma cópia de input_data com os keyboard smashings substituídos pelo valor passado no parâmetro value
        :rtype: lista ou string
        """
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
    


class lex_extractor():
    """Classe auxiliar da isitkbs para extração de features lexicais.
    """

    @classmethod
    def letter_counter(cls, string, type):
        """Conta a quantidade de cada vogal ou consoante em uma string de entrada.

        :param string: String da qual será feita a contagem das letras.
        :type string: string
        :param type: {'v', 'c'}, Se serão contadas as vogais ou consoantes
        :type type: string
        :return: Um dicionário em que as letras sãos as chaves e os valores são sua quantidade em string
        :rtype: dicionário
        """

        if (type == 'c'):
            return {letter: str(string).count(letter) for letter in 'bcdfghjklmnpqrstvwxyz'}
        elif (type == 'v'):
            return {letter: str(string).count(letter) for letter in 'aeiou'}  
        return {letter: str(string).count(letter) for letter in 'abcdefghijklmnopqrstuvwxyz'}

    @classmethod
    def type_counter(cls, string, type):
        """Conta a quantidade total de vogais ou consoantes em uma string de entrada.

        :param string: String da qual será feita a contagem das letras.
        :type string: string
        :param type: {'v', 'c'}, Se serão contadas as vogais ou consoantes
        :type type: string
        :return: A soma da quantidade total de vogais ou de consoantes da palavra
        :rtype: int
        """           
        return sum(cls.letter_counter(string, type).values())
    
    @classmethod
    def type_ratio(cls, string, type):
        """Cálcula a proporção de vogais ou consoantes em uma string de entrada.

        :param string: String da qual será feito o cálculo.
        :type string: string
        :param type: {'v', 'c'}, Se a propoção cálculada será de vogais ou consoantes
        :type type: string
        :return: Proporção de vogais ou consoantes na palavra
        :rtype: float
        """
        if (len(string) == 0):
            return 0
        return cls.type_counter(string, type)/len(string)

    @classmethod
    def bigram_counter(cls, lista):
        """Função auxiliar da bigrams que conta a quantidade de cada bigrama em uma lista e retorna um dicionário em que os bigramas são as chaves e sua quantidade na lista de entrada os valores

        :param lista: Lista com os bigramas.
        :type lista: lista
        :return: Dicionário em que os bigramas são as chaves e sua quantidade na lista de entrdada os valores
        :rtype: dicionário
        """

        dic = {}
        for i in lista:
            if i in dic:
                dic[i] += 1
            else:
                dic[i] = 1
        return dic

    @classmethod
    def bigrams(cls, string):
        """Dada uma string de entrada retorna um dicionário em que seus bigramas são as chaves e sua quantidade os valores

        :param string: String da qual os bigramas serão extraídos.
        :type string: string
        :return: Dicionário em que os bigramas são as chaves e sua quantidade na lista de entrdada os valores
        :rtype: dicionário
        """
        bigrams = []
        for i in range(len(string)-1):
            bigrams.append(string[i]+string[i+1])

        return cls.bigram_counter(bigrams)

    @classmethod
    def bigram_max_occurance(cls, string):
        """Dada uma string de entrada retorna qual a quantidade máxima de ocorrência de um mesmo bigrama

        :param string: String da qual os bigramas serão extraídos.
        :type string: string
        :return: Quantidade máxima de ocorrência de um mesmo bigrama
        :rtype: int
        """
        try:
            return (sorted(cls.bigrams(string).values(), reverse=True))[0]
        except:
            return 0
        
    @classmethod
    def ttr(cls, string):
        """Calcula o TypeTokenRatio (TTR) de uma string de entrada. O TTR é a quantidade de carácteres únicos divididade pelo tamanho total da string

        :param string: String da qual será realizado o cálculo do TTR.
        :type string: string
        :return: TypeTokenRatio (TTR) da string de entrada
        :rtype: float
        """

        if (len(string) == 0):
            return 0
        ttr = len(set(string)) / len(string)
        return ttr


    def __bigramas_proibidos(self, string):
        """Verifica se a string de entrada possui algum dos bigramas considerados 'proibidos' (Eles são raríssimos e palavras que não sejam keyboard smashing)

        :param string: String de entrada.
        :type string: string
        :return: 0 caso a string não possua nenhum dos bigramas na lista de proibidos, 1 caso contrário
        :rtype: int
        """
        proibidos = ['zx', 'xj', 'wx', 'vx', 'vq', 'vj', 'vf', 'sx', 'qz', 'qx', 'qk', 'qj', 'qc', 'jz', 'jx', 'jq', 'jf', 'hx', 'gx', 'fq', 'bx', 
                     'cv', 'cx', 'dx', 'fv', 'fx', 'fz', 'gv', 'jg', 'jk', 'jl', 'jm', 'jt', 'jv', 'jw', 'kq', 'kx', 'kz', 'pq', 'px', 'qd', 'qe', 
                     'qf', 'qg', 'qh', 'ql', 'qm', 'qn', 'qo', 'qp', 'qr', 'qs', 'qv', 'qw', 'qy', 'vb', 'vm', 'vp', 'vw', 'vz', 'xz', 'zj']

        bigramas = self.bigrams(string)

        for bigrama in bigramas:
            if bigrama in proibidos:
                return 1
        return 0   
    
    def __repeticao_de_bigramas(self, string, len):
        """Dada uma string de entrada verifica se o número máximo de repetição de seus bigramas passou do limite das palavras normais ou não

        :param string: String da qual será verificado o número máximo de repetição de bigramas
        :type string: string
        :param len: Tamanho da string de entrada
        :type len: int
        :return: 'True' se o número máximo de repetição de bigramas passou do limite das palavras normais, 'False' caso contrário
        :rtype: bool
        """

        max_o = self.bigram_max_occurance(string)
        if (max_o == 4 and len < 12) or max_o > 4:
            return True 
        return False

    @classmethod
    def _is_kbs_manual(cls, string):
        """Verifica se uma string é ou não keyboard smashing manualmente baseado na repetição máxima de seus bigramas e na presença de alguns bigramas proibidos

        :param string: String que será verificada se é keyboard smashing ou não
        :type string: string
        :return: 0 se a string não for considerada keyboard smashing, 1 caso contrário
        :rtype: int
        """
        try:    
            length = len(string)
            
            if cls.__repeticao_de_bigramas(cls, string, length): return 1
            if cls.__bigramas_proibidos(cls, string): return 1
        except:
            return 0
        