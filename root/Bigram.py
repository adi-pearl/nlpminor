# NaiveBayes

import sys
import getopt
import os
import math
import random
class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
          self.train = []
          self.test = []

class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
          self.klass = ''
          self.words = []
class NaiveBayes():
    trainDir="data/imdb1"
    singleTestDir="data"
    megaPos={}
    megaNeg={}
    vocabularySizePos=0
    vocabularySizeNeg=0
    totalVocabularySize=0
    punc=",. !:\t\n"
    numfolds=10

    def readFile(self, fileName):
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        result = self.segmentWords('\n'.join(contents))    
        return result
    def segmentWords(self,s):
        for ch in self.punc:
            s=s.replace(ch," ")
        return s.split()

    def buildSplits(self):
        posTrainFileNames = os.listdir('%s/pos/' % self.trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % self.trainDir)
        for fold in range(0,self.numfolds):
            print "[INFO]\tPerforming cross-validation fold: "+`fold`
            split = TrainSplit()
            for fileName in posTrainFileNames:
              example = Example()
              example.words = self.readFile('%s/pos/%s' % (self.trainDir, fileName))
              example.klass = 'pos'
              if fileName[2] == str(fold):
                split.test.append(example)
              else:
                split.train.append(example)
            for fileName in negTrainFileNames:
              example = Example()
              example.words = self.readFile('%s/neg/%s' % (self.trainDir, fileName))
              example.klass = 'neg'
              if fileName[2] == str(fold):
                split.test.append(example)
              else:
                split.train.append(example)
            ac=self.TrainAndTest(split)
            print 'accuracy: %.2f %s' % (ac,'%')
    #Training and Testing the data...
    def TrainAndTest(self,split):
        self.Train(split)
        return self.Test(split)
    def Train(self,split):
        self.megaPos={}
        self.megaNeg={}
        for ex in split.train:
            words=ex.words
            if ex.klass=='pos':
                for i in range(0,len(words)-1):
                    pair=(words[i],words[i+1])
                    if pair in self.megaPos:
                        self.megaPos[pair]+=1
                    else:
                        self.megaPos[pair]=1
            else:
                for i in range(0,len(words)-1):
                    pair=(words[i],words[i+1])
                    if pair in self.megaNeg:
                        self.megaNeg[pair]+=1
                    else:
                        self.megaNeg[pair]=1
        for key in self.megaPos:
            self.vocabularySizePos+=self.megaPos[key]
        for key in self.megaNeg:
            self.vocabularySizeNeg+=self.megaNeg[key]
        self.totalVocabularySize=self.vocabularySizePos+self.vocabularySizeNeg
    def Test(self,split):
        accuracy=0.0
        for ex in split.test:
            words=ex.words
            if self.classify(words)==ex.klass:
                accuracy+=1.0
        accuracy/=len(split.test)
        accuracy*=100.0
        return accuracy

    def TrainOnWholeCorpus(self):
        posTrainFileNames = os.listdir('%s/pos/' % self.trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % self.trainDir)
        split = TrainSplit()
        for fileName in posTrainFileNames:
            example = Example()
            example.words = self.readFile('%s/pos/%s' % (self.trainDir, fileName))
            example.klass = 'pos'
            split.train.append(example)
        for fileName in negTrainFileNames:
              example = Example()
              example.words = self.readFile('%s/neg/%s' % (self.trainDir, fileName))
              example.klass = 'neg'
              split.train.append(example)
        self.Train(split)
    
    #classifier based on Naive Bayes...
    def classify(self,words):
        #words=self.readFile("%s/test.txt" % (self.singleTestDir))
        posProb=math.log(0.5)
        for i in range(0,len(words)-1):
            pair=(words[i],words[i+1])
            if pair in self.megaPos:
                posProb+=math.log((self.megaPos[pair]+1.0)/(self.totalVocabularySize + self.vocabularySizePos));
            else:
                posProb+=math.log((1.0)/(self.totalVocabularySize + self.vocabularySizePos));
        negProb=math.log(0.5)
        for i in range(0,len(words)-1):
            pair=(words[i],words[i+1])
            if pair in self.megaNeg:
                negProb+=math.log((self.megaNeg[pair]+1.0)/(self.totalVocabularySize + self.vocabularySizeNeg));
            else:
                negProb+=math.log((1.0)/(self.totalVocabularySize + self.vocabularySizeNeg));
        if(posProb>=negProb):
            return "pos"
        else:
            return "neg"
    def __init__(self):
        self.buildSplits()

#print "hello"
nb=NaiveBayes()
nb.TrainOnWholeCorpus()
print nb.classify("bad");
print nb.classify("kartik");
print nb.classify("awesome");
print nb.classify("good");
print nb.classify("movie");
print nb.classify("was");
print nb.classify("movie was awesome");
print nb.classify("movie was horrible");
print nb.classify("movie was awesome but acting was bad");
print nb.classify("not impressive");
print nb.classify("not good");
print nb.classify("not bad");

_str=raw_input("");
while _str!="":
    print nb.classify(nb.segmentWords(_str));
    _str=raw_input("");
    
