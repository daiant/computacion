#! -*- encoding: utf8 -*-



## Nombres:

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import re
import sys


def sort_dic_by_values(d, asc=True):
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+') # no debería ser w minuscula?
        self.clean = re.compile('\w+')

    def diff(self, data, stops):
        s = set(stops)
        return [x for x in data if x not in s] ## Devuelve todas las x que están en data pero no en stops

    def create_dict(self, stat):
        return dict((x, stat.count(x)) for x in set(stat)) ## devuelve las veces que ha salido x palabra en lista stat

    def write_dict(self, full, dict, key, reverse):
        i=0
        res = ""
        for key in sorted(dict, key=key, reverse=reverse):
            if(not full and i>=20):
                break
            res += "\t" + key + ": " + str(dict[key]) +"\n"
            i+=1
        return res ## devuelve un to string del diccionario
    def calculate_args(self,lower, stopwords, bigram, full):
        res = ""
        if(lower):
            res+="l"
        if(stopwords):
            res+="s"
        if(bigram):
            res+="b"
        if(full):
            res+="f"
        return res

    def write_stats(self, filename, stats, use_stopwords, full):
        """
        Este método escribe en fichero las estadísticas de un texto


        :param
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas

        :return: None
        """

        with open(filename, 'w') as fh:
            fh.write("Lines: ")
            fh.write(str(stats["nlines"]) + "\n")
            fh.write("Number words (including stopwords): ")
            fh.write(str(stats["nwords"]) + "\n")
            if(use_stopwords):
                fh.write("Number words (without stopwords): ")
                fh.write(str(stats["nswords"]) + "\n")

            fh.write("Vocabulary size: ")
            fh.write(str(len(set(stats["word"]))) + "\n") # set devuelve únicas
            fh.write("Number of symbols: ")
            fh.write(str(len(stats["symbol"])) + "\n")
            fh.write("Number of different symbols: ")
            fh.write(str(len(set(stats["symbol"]))) + "\n") # set devuelve unicas

            dictionary = self.create_dict(stats["word"])
            fh.write("Words (alphabetical order): \n")
            fh.write(self.write_dict(full, dictionary, None, False))
            fh.write("Words (by frequency): \n")
            fh.write(self.write_dict(full, dictionary, dictionary.get, True))

            dict_symbol = self.create_dict(stats["symbol"])
            fh.write("Symbols (alphabetical order): \n")
            fh.write(self.write_dict(full, dict_symbol, None, False))
            fh.write("Symbols (by frequency): \n")
            fh.write(self.write_dict(full, dict_symbol, dict_symbol.get, True))
            fh.close()
            pass

    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadísticas de un fichero de texto


        :param
            filename: el nombre del fichero.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results

        sts = {

                'nwords':  0,
                'nswords': 0,
                'nlines':  0,
                'word':   {},
                'symbol': {}
                }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        # completar
        fh = open(filename, "r")
        data = fh.read()
        sts["nwords"] = len(data.split())
        fh.seek(0) # devolver el puntero a 0
        sts["nlines"] = sum(1 for line in fh)
        fh.close()

        data_clean = self.clean.findall(data) # eliminar no alfanuméricos
        data = self.diff(data_clean, stopwords) # eliminar stopwords
        sts['nswords'] = len(data)

        data_words = ' '.join(map(str, data)) ## creando un string para modificar (más rapido?) lo de las minúsculas
        data_sym = ''.join(map(str, data))

        if(lower):
            data_words = data_words.lower()
            data_sym = data_sym.lower()

        sts["word"] = list(data_words.split()) # devuelve una lista de palabros
        sts["symbol"] = list(data_sym)
        new_filename = filename.split(".")[0] + "_" + self.calculate_args(lower,True if len(stopwords)>0 else False, bigrams, full) + "_stats.txt" # cambiar
        self.write_stats(new_filename, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto


        :param
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower', action='store_true', default=False,
                    help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram', action='store_true', default=False,
                    help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full', action='store_true', default=False,
                    help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file, lower=args.lower, stopwordsfile=args.stopwords, bigrams=args.bigram, full=args.full)
