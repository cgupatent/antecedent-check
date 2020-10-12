#
# Read and write files using the built-in Python file methods
#

import os
from os import path
import subprocess
import re
import time


def main():  

  os.chdir("H:/Connotation/apache-opennlp-1.9.3/bin")

  f = open("claim set 2.txt","r")
  if f.mode == 'r': # check to make sure that the file was opened
    fl1 = f.readlines() # readlines reads the individual lines into a list

  f = open("claim2clean.txt","w+")
    
  substr=list() # substr is the list of claim numbers, fl1 is the list of actual claim texts
  clnum=list() # clnum is the list of claim numbers in number form
  dpnum=list() # dpnum is the dependence 

  for i in range(len(fl1)):
    if re.match(r'^[0-9]{1,}.', fl1[i]) :
      substr.append( re.match(r'^[0-9]{1,}', fl1[i]).group(0) )
      clnum.append( int( re.match(r'^[0-9]{1,}', fl1[i]).group(0) ) )
      if re.search('claim [0-9]{1,}', fl1[i]):
        dpnum.append( int( re.sub('claim ', '', re.search('claim [0-9]{1,}', fl1[i]).group(0)) ) )
      else:
        dpnum.append(0)

      fl1[i]= re.sub('^' + substr[len(substr)-1] + r'.', 'Claim ' + substr[len(substr)-1] + r':', fl1[i])
      f.write(fl1[i])
    else:
      fl1[i]=''
  
  # close the file when done
  f.close()

  fl1 = list(filter(None, fl1))

  stream=os.popen('del clean2token.txt')
  while not(stream.close()==None):
    print(stream.close())

  stream=os.popen('opennlp TokenizerME en-token.bin < claim2clean.txt > clean2token.txt')

  while not(stream.close()==None):
    print(stream.close())

  f = open("clean2token.txt","r")

  if f.mode == 'r': # check to make sure that the file was opened
    tempfl = f.readlines() # tempfl list to read and parse tokenized claim text
  
  wordlist = [[] for i in range(len(substr))] # wordlist is the claim text parsed into words
  f = open("clean2token.txt","w+")
  for i in range(len(tempfl)):
    tempfl[i]=re.sub('\n', '', tempfl[i])
    wordlist[i]=tempfl[i].split(' ') # read original words into wordlist

    tempfl[i]=re.sub('comprising', 'having', tempfl[i]) #substituting sensitive words that throws off parsing

    f.write(tempfl[i] + '\n')
    
    
  f.close()


  stream=os.popen('del clean2parsed.txt')
  while not(stream.close()==None):
    print(stream.close())

  stream = os.popen('opennlp Parser en-parser-chunking.bin < clean2token.txt > clean2parsed.txt')

  while not(stream.close()==None):
    print(stream.close())

  f = open("clean2parsed.txt","r")

  if f.mode == 'r': # check to make sure that the file was opened
    fl2 = f.readlines() # fl2 is the list of compacted parsed claim texts

  f = open("clean2compact.txt","w+")
    
  for i in range(len(fl2)):
    fl2[i]=re.sub(' \(', '(', fl2[i])
    fl2[i]=re.sub('\(TOP\(NP', '', fl2[i])
    fl2[i]=re.sub('\)\)$', '', fl2[i])
    f.write(fl2[i])

  f.close()

  phraselayer=list() # phraselayer list is counting layers of phrases to be parsed for antecedent analysis
  # each claim will be parsed out by layers of phrases

  for i in range(len(fl2)):
    phraselayer.append(0)
    k=0
    for j in range(len(fl2[i])):
      if fl2[i][j] == '(' :
        k=k+1
        if k>phraselayer[i]:
          phraselayer[i]=k
      elif fl2[i][j] == ')' :
        k=k-1

  for i in range(len(fl2)):
    
    for x in range(phraselayer[i]):
      k=0
      wordcount=0
      wordstart = 0

      for j in range(len(fl2[i])):
        if fl2[i][j] == '(' :
          k=k+1
          if k==x+1 :
            phrasestart = j+1
            wordstart = wordcount

        elif fl2[i][j] == ')' :
          k=k-1
          if k==x :
            phraseend = j
            if re.search('\)', fl2[i][phrasestart:phraseend]):
              print(str(clnum[i]) + ' ' + str(dpnum[i]) + ' ' + str(wordstart) + ' ' + str(wordcount) + ' ' + re.match('[A-Z]{1,}', fl2[i][phrasestart:phraseend]).group(0) + ' ' + ' '.join(wordlist[i][wordstart:wordcount]))
        elif fl2[i][j]== ' ' :
          wordcount = wordcount + 1



if __name__ == "__main__":
  main()
