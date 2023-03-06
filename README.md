# smith-waterman-affine-gap

This is a submission to CBB752 hw1 from Suchen Zheng

### sample command

```
python hw1.py -i sample-input1.txt -s blosum62.txt
```
This command would run file hw1.py with input from sample-input1.txt, using similarity matrix blosum62.txt. 

And the result would be saved to output.txt by default. 

Please notice, output.txt would be overwritten by the command everytime. 

```
python hw1.py -i sample-input1.txt -s blosum62.txt -o -2 -e -1 -f output.txt
```
This command define the follwoing:

"-o" : gap opening pendalty (default -2)

"-e" : gap extension pendalty (default -1)

"-f" : output file path (default ./output.txt)


### sample run

By running:
```
python hw1.py -i sample-input1.txt -s blosum62.txt
```
Which run the lcoal alignement for sample-input1.txt which containing two sequences:

```
MGLSDGEWQLVLNVWGKVEADIPGHGQEVLIRLFKGHPETLEKFDKFKHLKSEDEMKASEDLKKHGATVLTALGGILKKKGHHEAEIKPLAQSHATKHKIPVKYLEFISECIIQVLQSKHPGDFGADAQGAMNKALELFRKDMASNYKELGFQG
VLKCWGPMEADYATHGGLVLTRLFTEHPETLKLFPKFAGIAHGDLAGDAGVSAHGATVLNKLGDLLKARGAHAALLKPLSSSHATKHKIPIINFKLIAEVIGKVMEEKAG
```

The terminal output would be telling you the final alignment result, the alignment score, and the file containing the detailed results
```
MGLSDGEWQL(VLNVWGKVEADIPGHGQEVLIRLFKGHPETLEK-FDKF---KHLKSEDEMKASED--LKKHGATVLTALGGILKKKGHHEAEIKPLAQSHATKHKIPVKYLEF--ISECII-QVLQSKHPG)DFGADAQGAMNKALELFRKDMASNYKELGFQG
           ||  ||  |||   ||  || |||  ||||| | | ||    |    |   |  |     ||||||  ||  ||  | | |  |||  |||||||||     |  | |  |  |   |  |
          (VLKCWGPMEADYATHGGLVLTRLFTEHPETL-KLFPKFAGIAH--G-D-L-AG-DAGVSAHGATVLNKLGDLLKARGAHAALLKPLSSSHATKHKIPI--INFKLIAE-VIGKVMEEK-AG)
max score:  283.0
results saved to output.txt
```

The output.txt file would contain three sections (A sample "output.txt" has been included in this repo)

* Section 1) - Input sequences
```
-----------
|Sequences|
-----------
sequence1
MGLSDGEWQLVLNVWGKVEADIPGHGQEVLIRLFKGHPETLEKFDKFKHLKSEDEMKASEDLKKHGATVLTALGGILKKKGHHEAEIKPLAQSHATKHKIPVKYLEFISECIIQVLQSKHPGDFGADAQGAMNKALELFRKDMASNYKELGFQG
sequence2
VLKCWGPMEADYATHGGLVLTRLFTEHPETLKLFPKFAGIAHGDLAGDAGVSAHGATVLNKLGDLLKARGAHAALLKPLSSSHATKHKIPIINFKLIAEVIGKVMEEKAG
```

* Section 2) - Score matrix

* Section 3) - Best Local Alignment
```
----------------------
|Best Local Alignment|
----------------------
Alignment Score:283
Alignment Results:
MGLSDGEWQL(VLNVWGKVEADIPGHGQEVLIRLFKGHPETLEK-FDKF---KHLKSEDEMKASED--LKKHGATVLTALGGILKKKGHHEAEIKPLAQSHATKHKIPVKYLEF--ISECII-QVLQSKHPG)DFGADAQGAMNKALELFRKDMASNYKELGFQG
           ||  ||  |||   ||  || |||  ||||| | | ||    |    |   |  |     ||||||  ||  ||  | | |  |||  |||||||||     |  | |  |  |   |  |                                 
          (VLKCWGPMEADYATHGGLVLTRLFTEHPETL-KLFPKFAGIAH--G-D-L-AG-DAGVSAHGATVLNKLGDLLKARGAHAALLKPLSSSHATKHKIPI--INFKLIAE-VIGKVMEEK-AG)                       ```