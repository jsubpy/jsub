#!/usr/bin/env python

import os
import sys, getopt

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	for o,a in opts:
		if o == "--input_file":
			input_file=a
	try:
		print(input_file)
	except:
		print("failed to print input file")
	file_to_cp='../'+os.path.basename(input_file)
	dest_filename=file_to_cp+'.cp'
	print('cp %s %s'% (file_to_cp,dest_filename))
	os.system('cp %s %s'% (file_to_cp,dest_filename))
	print("sed -i '1,3 p' %s"%dest_filename)	
	os.system("sed -i '1,3 p' %s"%dest_filename)	

if __name__ == '__main__':
	sys.exit(main())
