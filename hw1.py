#!/usr/bin/python
__author__ = "Suchen Zheng"
__email__ = "suchen.zheng@yale.edu"
__copyright__ = "Copyright 2023"
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
parser.add_argument('-f', '--out_f_name', help='output file name', required=False, default="output.txt")
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
	print("input_lines: ",input_lines)
	col_seq = input_lines[0]
	row_seq = input_lines[1]
	
	# read score matrix
	score_df = pd.read_fwf(scoreFile,sep='\t',index_col=0)

	# place holder for maximun score and location of maximun score
	global_max_score = 0
	global_max_i = 0
	global_max_j = 0

	# initialize score matrix
	# D - score from diagnal cells
	# U - score from up cells
	# L - score from left cells
	# M - maxmimun score among all cases
	D = np.zeros((len(row_seq)+1,len(col_seq)+1))
	U = np.zeros((len(row_seq)+1,len(col_seq)+1))
	L = np.zeros((len(row_seq)+1,len(col_seq)+1))
	M = np.zeros((len(row_seq)+1,len(col_seq)+1))

	# traceback matrix, 0-stop, 1-diagnal, 2-up, 3-left
	T = np.zeros((len(row_seq)+1,len(col_seq)+1)) 


	# start alignment
	for i,char_i in enumerate(row_seq):
		i = i+1
		for j,char_j in enumerate(col_seq):
			j = j+1

			# look up the match score from simnilarity matrix
			match_score = score_df[char_i][char_j]

			# possible score if it is a match - score from disganl cells 
			D[i][j] = max(
				M[i-1][j-1]+match_score,
				U[i-1][j-1]+match_score,
				L[i-1][j-1]+match_score,
				0
				)
			# possible score if it is a gap on the column sequence - score from up cells 
			U[i][j] = max(
				M[i-1][j]+openGap,
				U[i-1][j]+extGap,
				0
				)

			# possible score if it is a gap on the row sequence - score from left cells 
			L[i][j] = max(
				M[i][j-1]+openGap,
				L[i][j-1]+extGap,
				0
				)

			# maximum score among above cases
			max_score = max(D[i][j],U[i][j],L[i][j],0)
			M[i][j] = max_score

			#--------------------------------------------------------
			# Debug block: check intermediate step and look at all calculated values
			# if i == 78 and j == 63:
			# 	print(char_i,char_j)
			# 	print(D[i][j],M[i-1][j-1]+match_score,U[i-1][j-1]+match_score,L[i-1][j-1]+match_score)
			# 	print(U[i][j],M[i-1][j]+openGap, U[i-1][j]+extGap)
			# 	print(L[i][j],M[i][j-1]+openGap,L[i][j-1]+extGap)
			# 	print(max_score)

			# 	print(L[0:4,32:34])
			#--------------------------------------------------------

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
	
	## start traceback
	current_i = global_max_i
	current_j = global_max_j


	# the traceback stop when one sequence end or a stop sign "0" met 
	while (current_i > 0) and (current_j>0):
		if T[current_i][current_j] == 0:
			break

		elif int(T[current_i][current_j]) == 1:
			line1 = row_seq[current_i-1]+line1
			line3 = col_seq[current_j-1]+line3
			if row_seq[current_i-1] == col_seq[current_j-1]:
				line2 = "|"+line2
			else:
				line2 = " "+line2
			current_i = current_i -1
			current_j = current_j -1
		elif int(T[current_i][current_j]) == 2:
			line1 = row_seq[current_i-1]+line1
			line2 = " "+line2
			line3 = "-"+line3
			current_i = current_i -1
		elif int(T[current_i][current_j]) == 3:
			line1 = "-"+line1
			line2 = " "+line2
			line3 = col_seq[current_j-1]+line3
			current_j = current_j -1

	# construct the prefix
	row_seq_prefix = row_seq[0:current_i]
	col_seq_prefix = col_seq[0:current_j]

	max_prefix_length = max(len(row_seq_prefix),len(col_seq_prefix))
	row_seq_prefix = " "*(max_prefix_length-len(row_seq_prefix))+row_seq_prefix+"("
	col_seq_prefix = " "*(max_prefix_length-len(col_seq_prefix))+col_seq_prefix+"("

	line1 = row_seq_prefix+line1
	line2 = " "*len(row_seq_prefix)+line2
	line3 = col_seq_prefix+line3

 	# print out for immediate information
	print(line3)
	print(line2)
	print(line1)
	print("max score: ",global_max_score)


	### write output

	# first section of output, sequnce information and score matrix title
	out_f = open(args.out_f_name,"w+")
	# out_f.writelines(["-----------\n", "|Sequences|\n", "-----------\n"])
	for l in ["-----------\n", "|Sequences|\n", "-----------\n","sequence1\n",col_seq , "\nsequence2\n",row_seq,\
	"\n--------------\n","|Score Matrix|\n","--------------\n"]:
		out_f.write(l) 
	out_f.close()

	# save the score matrix to csv first and then 
	M = M.astype(int)
	score_df = pd.DataFrame(M,columns =[""]+[*col_seq])
	# print(score_df.shape)
	score_df.insert (0,"  ",[""]+[*row_seq])
	score_df.to_csv(args.out_f_name, sep ='\t',mode='a',index =False)



	#--------------------------------------------------------
	# debug block - uncomment following block if need to save and look at each matrix
	#--------------------------------------------------------
	
	# U_df = pd.DataFrame(U,columns =[""]+[*col_seq])
	# U_df.insert (0,"  ",[""]+[*row_seq])
	# U_df.to_csv("my_U_{}".format(args.input), sep ='\t',mode='a',index =False)

	# M_df = pd.DataFrame(M,columns =[""]+[*col_seq])
	# M_df.insert (0,"  ",[""]+[*row_seq])
	# M_df.to_csv("my_M_{}".format(args.input), sep ='\t',mode='a',index =False)

	# L_df = pd.DataFrame(L,columns =[""]+[*col_seq])
	# L_df.insert (0,"  ",[""]+[*row_seq])
	# L_df.to_csv("my_L_{}".format(args.input), sep ='\t',mode='a',index =False)

	# T_df = pd.DataFrame(T,columns =[""]+[*col_seq])
	# T_df.insert (0,"  ",[""]+[*row_seq])
	# T_df.to_csv("my_T_{}".format(args.input), sep ='\t',mode='a',index =False)

	#--------------------------------------------------------


	
	# save the final part of the result, the alignment
	out_f = open(args.out_f_name,"a")
	for l in ["----------------------\n", "|Best Local Alignment|\n", "----------------------\n",\
	"Alignment Score:{}\n".format(int(global_max_score)),
	"Alignment Results:\n",
	line3,"\n",line2,"\n",line1,"\n"]:
		out_f.write(l)

	# message to user about the file saving information
	print("results saved to {}".format(args.out_f_name))




### Run your Smith-Waterman Algorithm
runSW(args.input, args.score, args.opengap, args.extgap)