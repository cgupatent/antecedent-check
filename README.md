# antecedent-check
patent claim antecedent basis checking program, using Java based OpenNLP tool set and Python main program

** need to install latest Java and python
** need to download large model file:  http://opennlp.sourceforge.net/models-1.5/en-parser-chunking.bin, do not uncompress

need to have claim set 2.txt as input file with claim text

run antecedent.py

output:

claim2clean.txt # claim text with only the claims, all other texts are removed

clean2token.txt # claim text tokenized

clean2parsed.txt # claim text parsed

clean2compact.txt # claim text parsed with non-essential spaces removed.
