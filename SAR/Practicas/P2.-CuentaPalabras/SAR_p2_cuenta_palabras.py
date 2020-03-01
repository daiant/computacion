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
        self.clean_re = re.compile('\W+')

    def calculate_args(self, lower, stopwords, bigram, full):
        """
        Este método devuelve una cadena de texto con los argumentos elegidos
        para escribir en el filename de stats


        :param
            lower: boolean, si estará en minúsculas
            stopwords: boolean, si hay stopwords.
            bigram: boolean, si se contarán los bigramas
            full: boolean, si se deben mostrar las stats completas

        :return: string
        """
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

    def calculate_dict(self, data, stopwords):
        """
        Este método devuelve dos diccionarios, del vocabulario y de los símbolos (monogramas).


        :param
            data: una lista con las palabras del texto.
            stopwords: la lista de las palabras a no tener en cuenta (o vacío).

        :return: Dos diccionarios.
        """
        words = {}
        symbols = {}
        for word in data:
            if(word not in stopwords):
                words[word] = words.get(word, 0) + 1
                for char in word:
                    symbols[char] = symbols.get(char, 0) + 1
        return words, symbols

    def calculate_biwords(self, data, stopwords):
        """
        Este método devuelve un diccionario de los bigramas del texto.


        :param
            data: una lista con las palabras del texto, arregladas con $.
            stopwords: la lista de las palabras a no tener en cuenta (o vacío).

        :return: Un diccionario.
        """
        biwords = {}
        for i in range(len(data)-1):
            if(data[i] not in stopwords and data[i+1] not in stopwords):
                if data[i] is not "$" or data[i+1] is not "$":
                    biwords[data[i]+ " " +data[i+1]] = biwords.get(data[i]+" "+data[i+1], 0) + 1
        return biwords

    def calculate_bisymbols(self, data, stopwords):
        """
        Este método devuelve un diccionario con los pares de símbolos del texto.


        :param
            data: una lista con las palabras del texto.
            stopwords: la lista de las palabras a no tener en cuenta (o vacío).

        :return: Un diccionario.
        """

        bisymbols = {}
        for word in data:
            if word not in stopwords:
                for i in range(len(word)-1):
                    bisymbols[word[i]+word[i+1]] = bisymbols.get(word[i]+word[i+1], 0) + 1
        return bisymbols

    def write_dict(self, dict, full, values=False):
        """
        Este método devuelve una cadena con el diccionario parseado.


        :param
            dict: el diccionario
            full: boolen, si hay que escribir todas las entradas o 20.
            values: boolean, si hay que ordenar por valores o alfabéticamente (default False).

        :return: Una string.
        """
        i=0
        res = ""
        if values:
            aux = sort_dic_by_values(dict)
        else:
            aux = sorted(dict.items())
        for key in aux:
            if(not full and i>=20):
                break
            res += "\t" + key[0] + ": " + str(key[1]) +"\n"
            i+=1
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
            fh.write(str(stats.get("nlines")) + "\n")

            fh.write("Number words (including stopwords): ")
            fh.write(str(stats.get("nwords")) + "\n")
            if(use_stopwords):
                fh.write("Number words (without stopwords): ")
                fh.write(str(stats.get("nwords_s"))+"\n")

            fh.write("Vocabulary size: ")
            fh.write(str(len(stats.get("word"))) + "\n")
            fh.write("Number of symbols: ")
            fh.write(str(stats.get("nsymbols")) + "\n")
            fh.write("Number of different symbols: ")
            fh.write(str(len(stats.get("symbol"))) + "\n")

            fh.write("Words (alphabetical order):\n")
            fh.write(self.write_dict(stats.get("word"), full))
            fh.write("Words (by frequency):\n")
            fh.write(self.write_dict(stats.get("word"), full, True))

            fh.write("Symbols (alphabetical order):\n")
            fh.write(self.write_dict(stats.get("symbol"), full))
            fh.write("Symbols (by frequency):\n")
            fh.write(self.write_dict(stats.get("symbol"), full, True))

            if(stats.get("biword") is not None):
                fh.write("Word pairs (alphabetical order):\n")
                fh.write(self.write_dict(stats.get("biword"), full))
                fh.write("Word pairs (by frequency):\n")
                fh.write(self.write_dict(stats.get("biword"), full, True))

                fh.write("Symbol pairs (alphabetical order):\n")
                fh.write(self.write_dict(stats.get("bisymbol"), full))
                fh.write("Symbol pairs (by frequency):\n")
                fh.write(self.write_dict(stats.get("bisymbol"), full, True))

            pass


    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadÃ­sticas de un fichero de texto


        :param
            filename: el nombre del fichero.
            lower: booleano, se debe pasar todo a minÃºsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadÃ­sticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results

        stats = {
                'nwords': 0,
                'nwords_s': 0,
                'nlines': 0,
                'nsymbols': 0,
                'word': {},
                'symbol': {}
                }

        if bigrams:
            stats['biword'] = {}
            stats['bisymbol'] = {}
        # Abre documento
        fh = open(filename, "r")

        data = ""
        data_bi = ""
        # trata los datos y cuenta líneas y demás.
        for line in fh:
            if lower:
                line = line.lower()
            data += line
            stats["nlines"] += 1
            if bigrams:
                l = self.clean_re.sub(" ", line)
                data_bi += "$ " + l + "$ "


        data = self.clean_re.sub(" ", data) # devuelve string alfánumerico + espacios.
        #Stats de conteo
        stats["nwords"] = len(data.split())

        if(len(stopwords)>0):
            stats["nwords_s"] = sum(1 for x in data.split() if x not in stopwords)

        stats["nsymbols"] = sum(1 for x in data.split() for l in x if x not in stopwords)

        # Diccionarios
        stats["word"], stats["symbol"] = self.calculate_dict(data.split(), stopwords)
        if bigrams:
            stats["biword"] = self.calculate_biwords(data_bi.split(), stopwords)
            stats["bisymbol"] = self.calculate_bisymbols(data.split(), stopwords)

        # Escribiendo los datos
        argumentos = self.calculate_args(lower, True if len(stopwords)>0 else False, bigrams, full)
        new_filename = filename.split(".")[0] + "_" + argumentos + "_stats." + filename.split(".")[1]
        self.write_stats(new_filename, stats, stopwordsfile is not None, full)


    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadÃ­sticas de una lista de ficheros de texto


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
