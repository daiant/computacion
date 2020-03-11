#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys

## Nombres:

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################



def sort_index(d):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')
        self.r2 = re.compile('\W+')


    def index_sentence(self, sentence, tri):
        sentence = self.r2.sub(" ", sentence)
        sentence = ("$ "+sentence+" $").lower()
        lista = sentence.split()
        dict = {}
        for w in range(len(lista)-1):
            if(lista[w] is not "$" or lista[w+1] is not "$"):
                self.index["bi"][lista[w]] = self.index["bi"].get(lista[w],{})
                self.index["bi"][lista[w]][lista[w+1]] = self.index["bi"][lista[w]].get(lista[w+1], 0)+1
        if(tri):
            for w in range(len(lista)-2):
                ref = "('"+lista[w]+"', '"+lista[w+1]+"')"
                self.index["tri"][ref] = self.index["tri"].get(ref,{})
                self.index["tri"][ref][lista[w+2]] = self.index["tri"][ref].get(lista[w+2], 0) +1


    def compute_index(self, filename, tri):
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        sentences = []
        with open(filename, "r") as fh:
            data = fh.read()
            data = data.replace("\n\n", ".")
            data = data.replace("\n", " ")
            sentences = self.r1.sub(".", data).split(".")
            pass
        for sentence in sentences:
            self.index_sentence(sentence, tri)
        sort_index(self.index['bi'])
        if tri:
            sort_index(self.index['tri'])


    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)


    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)


    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)

    def calculate_word(self, d, word):
        c = d.get(word)[0]
        lp = d.get(word)[1]
        c = random.randint(1,c)
        cont = 0
        for w in lp:
            cont+=w[0] # la length
            if(c<=cont):
                return w[1]

    def generate_sentences(self, n=10):
        # "('$', 'egg')"
        w1 = w2 = ""
        tri = self.index.get("tri") is not None
        for i in range(n):
            l = 1
            choice=0
            res="$ "
            current_word = "$"
            while l < 25:
                next_word = self.calculate_word(self.index['bi'], current_word)
                if tri:
                    w1 = current_word
                    w2 = next_word

                res += next_word + " "
                current_word = next_word
                next_word = ""
                l+=1

                if(current_word is "$" or l > 25):
                    break

                if tri:
                    ref = "('"+w1+"', '"+w2+"')"
                    if(self.index['tri'].get(ref) is None): # En el caso de que no hay combinación posibile
                        break

                    next_word = self.calculate_word(self.index["tri"], ref)
                    res += next_word + " "
                    current_word = next_word
                    next_word = ""
                    l+=1
                    if(current_word is "$" or l > 25):
                        break


            print(res)

if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")
