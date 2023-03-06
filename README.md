# smith-waterman-affine-gap

This is a submission to CBB572 hw1 from Suchen Zheng

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
