#!/usr/bin/python
__author__ = "FirstName LastName"
__email__ = "first.last@yale.edu"
__copyright__ = "Copyright 2021"
__license__ = "GPL"
__version__ = "1.0.0"

### Usage: python hw1.py -i <input file> -s <score file>
### Example: python hw1.py -i input.txt -s blosum62.txt
### Note: Smith-Waterman Algorithm

import argparse
import numpy as np
import pandas as pd

### This is one way to read in arguments in Python. 
parser = argparse.ArgumentParser(description='Smith-Waterman Algorithm')
parser.add_argument('-i', '--input', help='input file', required=True)
parser.add_argument('-s', '--score', help='score file', required=True)
parser.add_argument('-o', '--opengap', help='open gap', required=False, default=-2)
parser.add_argument('-e', '--extgap', help='extension gap', required=False, default=-1)
args = parser.parse_args()

### Implement your Smith-Waterman Algorithm
def runSW(inputFile, scoreFile, openGap, extGap):
	### load input file

	# read the input file
	in_f = open(inputFile, "r")

	#read all lines in from the file
	input_lines = in_f.readlines()

	#remove spaces in lines if there is any
	input_lines = [line.strip() for line in input_lines]
	print(input_lines)
	col_seq = input_lines[0]
	row_seq = input_lines[1]
	# read score matrix
	score_df = pd.read_fwf(scoreFile,sep='\t',index_col=0)
	
	score_mtx = np.zeros((len(row_seq)+1,len(col_seq)+1))
	gap_mtx = np.zeros((len(row_seq)+1,len(col_seq)+1))

	# filled_flag matrix is to record if the cell is filled or not 0-not filled, other-filled
	# 1-filled with 0, 2-filled from diagnoal cell, 3-filled from top cell, 4-filled from left cell
	filled_flag = np.zeros((len(row_seq)+1,len(col_seq)+1)) 

	global_max_score = 0
	global_max_i = 0
	global_max_j = 0

	D = np.zeros((len(row_seq)+1,len(col_seq)+1))
	U = np.zeros((len(row_seq)+1,len(col_seq)+1))
	L = np.zeros((len(row_seq)+1,len(col_seq)+1))
	M = np.zeros((len(row_seq)+1,len(col_seq)+1))

	# traceback matrix, 0-stop, 1-match, 2-up, 3-left
	T = np.zeros((len(row_seq)+1,len(col_seq)+1)) 



	for i in range(len(row_seq)):
		i = i+1
		for j in range(len(col_seq)):

			
			match_score = score_df[row_seq[i-1]][col_seq[j]]
			j = j+1
			D[i][j] = max(
				D[i-1][j-1]+match_score,
				U[i-1][j-1]+match_score,
				L[i-1][j-1]+match_score
				)

			U[i][j] = max(
				D[i-1][j]+openGap,
				U[i-1][j]+extGap
				)
			L[i][j] = max(
				D[i][j-1]+openGap,
				L[i][j-1]+extGap
				)

			max_score = max(D[i][j],U[i][j],L[i][j],0)
			M[i][j] = max_score

			# update our max score recorder
			if max_score>global_max_score:
				global_max_score = max_score
				global_max_i = i
				global_max_j = j

			# update trace back matrix
			if max_score == 0:
				T[i][j] = 0
			elif max_score == D[i][j]:
				T[i][j] = 1
			elif max_score == U[i][j]:
				T[i][j] = 2
			elif max_score == L[i][j]:
				T[i][j] = 3

	## traceback

	print(global_max_score)
	## three result line holders
	line1 = ""
	line2 = ""
	line3 = ""

	# before start the traceback, filling the holder with unmatched end of sequence

	row_seq_end = row_seq[global_max_i:]
	col_seq_end = col_seq[global_max_j:]

	max_end_length = max(len(row_seq_end),len(col_seq_end))
	row_seq_end = row_seq_end + " "*(max_end_length-len(row_seq_end))
	col_seq_end = col_seq_end + " "*(max_end_length-len(col_seq_end))

	line1 = ")"+row_seq_end
	line2 = " "*len(line1)
	line3 = ")"+col_seq_end

	print(line1)
	print(line2)
	print(line3)

	## start traceback
	current_i = global_max_i
	current_j = global_max_j

	while (current_i > 0) and (current_j>0):
		if T[current_i][current_j] == 0:
			break

		if T[current_i][current_j] == 1:
			line1 = row_seq[current_i-1]+line1
			line3 = col_seq[current_j-1]+line3
			if row_seq[current_i-1] == col_seq[current_j-1]:
				line2 = "|"+line2
			else:
				line2 = " "+line2
			current_i = current_i -1
			current_j = current_j -1
		elif T[current_i][current_j] == 2:
			line1 = row_seq[current_i-1]+line1
			line2 = " "+line2
			line3 = "-"+line3
			current_i = current_i -1
		elif T[current_i][current_j] == 3:
			line1 = "-"+line1
			line2 = " "+line2
			line3 = col_seq[current_j-1]+line3
			current_j = current_j -1

		

	row_seq_prefix = row_seq[0:current_i]
	col_seq_prefix = col_seq[0:current_j]

	max_prefix_length = max(len(row_seq_prefix),len(col_seq_prefix))
	row_seq_prefix = " "*(max_prefix_length-len(row_seq_prefix))+row_seq_prefix+"("
	col_seq_prefix = " "*(max_prefix_length-len(col_seq_prefix))+col_seq_prefix+"("

	line1 = row_seq_prefix+line1
	line2 = " "*len(row_seq_prefix)+line2
	line3 = col_seq_prefix+line3
	print(line3)
	print(line2)
	print(line1)

	### write output
	out_f = open("output.txt","w+")
	# out_f.writelines(["-----------\n", "|Sequences|\n", "-----------\n"])
	for l in ["-----------\n", "|Sequences|\n", "-----------\n","sequence1\n",col_seq , "\nsequence2\n",row_seq,\
	"\n--------------\n","|Score Matrix|\n","--------------\n"]:
		out_f.write(l) 
	out_f.close()

	M = M.astype(int)


	score_df = pd.DataFrame(M,columns =[""]+[*col_seq])

	# print(score_df.shape)
	score_df.insert (0,"  ",[""]+[*row_seq])
	print(score_df)
	# dfAsString = score_df.to_string(index=False)
	# out_f.write(dfAsString)

	score_df.to_csv('output.txt', sep ='\t',mode='a',index =False)

	out_f = open("output.txt","a")
	for l in ["----------------------\n", "|Best Local Alignment|\n", "----------------------\n",\
	"Alignment Score:{}\n".format(int(global_max_score)),
	"Alignment Results:\n",
	line3,"\n",line2,"\n",line1,"\n"]:
		out_f.write(l) 




	

### Run your Smith-Waterman Algorithm
runSW(args.input, args.score, args.opengap, args.extgap)