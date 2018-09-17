#!/usr/bin/env python3
"""POS-tagging script

Usage: %(scriptName)s directory

This script allows the user to write part-of-speech tags to all files
in a directory.

It is assumed that the files have a `.txt' extension, are in plain text
format and contain English text. Output files are given a `.pos'
extension with the identical filename.

The script uses the default tagger and tagset currently specified by
the NLTK library, and requires that `nltk' be installed within the
Python environment in which the script is run.
"""

import sys                      # for dealing with arguments
import os                       # for file operations
# we do not import nltk at this time in case it's not needed, because
# it has a pretty steep loading time

if not len(sys.argv) == 2:
    print(__doc__ % {'scriptName' : sys.argv[0].split("/")[-1]})
    sys.exit(1)
elif not os.path.isdir(sys.argv[1]):
    print("Error: "+sys.argv[1]+" does not exist or is not a directory")
    sys.exit(1)
else:
    corpusdir = sys.argv[1]
    included_extensions = ('.txt')
    corpusfiles = [fn for fn in os.listdir(corpusdir) if fn.endswith(included_extensions)]
    print("Processing directory "+corpusdir)
    print(str(len(corpusfiles))+" files found")
    print("Loading NLTK")
    from nltk import pos_tag_sents
    from nltk.corpus.reader.plaintext import PlaintextCorpusReader
    counter = 0
    for fn in corpusfiles:
        counter += 1
        outputfn = fn + ".pos"
        print("Processing file "+str(counter)+" of "+str(len(corpusfiles))+": "+fn)
        if not os.path.isfile(fn):
            print("Warning: "+fn+" is not a regular file. Skipping")
        elif os.path.exists(os.path.join(corpusdir,outputfn)):
            print("Warning: "+outputfn+" already exists. Skipping")
        else:
            # read file into corpus object using the plain text reader
            corpus = PlaintextCorpusReader(corpusdir, fn)
            # POS-tag corpus object using the default NLTK tagger
            tagged = pos_tag_sents(corpus.sents())
            # write tagged corpus object
            outputpath=os.path.join(corpusdir,outputfn)
            try:
                with open(outputpath, 'w') as output:
                    for sent in tagged:
                        line = " ".join(word+"/"+tag for word, tag in sent)
                        output.write(line+'\n')
            except OSError:
                print("Error: could not write to file "+outputfn+". Skipping")
