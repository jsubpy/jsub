import click
import os
import subprocess

from jsub import Jsub

from jsub.config  import load_config_file

JSUB_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#usage: jsub register <filelist>/<folder_name>
#	the command would run the dirac-register.sh script, which register the files to DFC; 
#	if the files are not under /cefs, would copy the files to /cefs/dirac/user/
#	the parameter can be the name of a folder

class RegisterToDFC(object):
	def __init__(self, jsubrc, input_list):
		self.__jsubrc = jsubrc
		self.__input_list = input_list

	def execute(self):
		j = Jsub(self.__jsubrc)

		if os.path.isfile(self.__input_list):	#get the list of files from a txt
			with open(self.__input_list) as f:
				files = [x for x in f.read().splitlines() if os.path.isfile(x)]
		if os.path.isdir(self.__input_list):	#all files in folder
			files = [os.path.join(os.path.realpath(self.__input_list),f) for f in os.listdir(self.__input_list) if os.path.isfile(os.path.join(os.path.realpath(self.__input_list),f))]

		for input_file in files:
			cmd_reg = [os.path.join(JSUB_COMMAND_DIR, 'scripts', 'dirac-register.sh')]
			cmd_reg.insert(999,input_file)
			reg_status=subprocess.call(cmd_reg)
	
			if reg_status!=0:
				click.echo("Error when registering file to DFC. (%s)" % input_file)

