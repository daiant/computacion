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
            fh.write("Number words: ")
            fh.write(str(stats["nwords"]) + "\n")
            fh.write("Vocabulary size: ")
            fh.write(str(len(set(stats["word"]))) + "\n")
            fh.write("Number of symbols: ")
            fh.write(str(len(stats["symbol"])) + "\n")
            fh.write("Number of different symbols: ")
            fh.write(str(len(set(stats["symbol"]))) + "\n")
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

                'nwords': 0,
                'nlines': 0,
                'word': {},
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
        #########################
        #### Para cada cosa un método o uno a parte???
        ##################
        data_clean = self.clean.findall(data)
        sts["word"] = list(data_clean) # devuelve una lista de palabros
        aux = ""
        for word in data_clean:
            aux+=word
        sts["symbol"] = list(aux)
        new_filename = filename.split(".")[0] + "__stats.txt" # cambiar
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

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                    help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram', action='store_true', default=False,
                    help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full', action='store_true', default=False,
                    help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file, lower=args.lower, stopwordsfile=args.stopwords, bigrams=args.bigram, full=args.full)
