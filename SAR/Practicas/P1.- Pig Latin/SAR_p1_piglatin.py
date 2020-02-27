#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin
# Carlos Sendra Gisbert (carsengi)
import sys
import re


class Translator():

    def __init__(self, punt=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            self.re = re.compile("(\w+)([.,;?!]*)")
        else:
            self.re = re.compile("(\w+)(["+punt+"]*)")

    def translate_word(self, word):
        """
        Este método recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """
        vocalic = ['a','e','i','o','u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y']
        firstCapital = False
        word1, s= self.re.match(word).groups()
        res = ""
        if(word1[0].isnumeric()):
            return word
        if(word1[0] in vocalic):
            yay = "YAY" if word1.isupper() else "yay"
            return word1+yay+s
        else:
            if(word1[0].isupper() and not word1.isupper()):
                word1 = word1[0].lower()+word1[1:]
                firstCapital = True
            while(len(word1)>0):
                if(word1[0] not in vocalic):
                    res += word1[0]
                    word1 = word1[1:]
                else:
                    ay = "AY" if word1.isupper() else "ay"
                    res += ay
                    res = word1+res
                    break
            if(firstCapital):
                res=res[0].upper()+res[1:]
        return res+s

    def translate_sentence(self, sentence):
        """
        Este método recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        # sustituir
        new_sentence = ""
        for word in sentence.split():
            new_sentence += self.translate_word(word) + " "

        return new_sentence

    def translate_file(self, filename):
        """
        Este método recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: True / False
        """

        # rellenar
        fp = open(filename, 'r')
        out = open(filename.split(".")[0] + "_latin.txt" , 'w')
        for line in fp:
            out.write(self.translate_sentence(line).strip()+'\n')
        out.close()
        fp.close()



if __name__ == "__main__":
    if len(sys.argv) > 2:
        print('Syntax: python %s [filename]' % sys.argv[0])
        exit
    else:
        t = Translator()
        if len(sys.argv) == 2:
            t.translate_file(sys.argv[1])
        else:
            while True:
                sentence = input("ENGLISH: ")
                if len(sentence) < 2:
                    break
                print("PIG LATIN:", t.translate_sentence(sentence))
