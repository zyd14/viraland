# prepare executable programs
# author: yubing hou
# date: 2014/12/09

import os
import sys

class Compile:
	def __init__(self, vlhome):
		self.vlhome = str(vlhome)
		pass

	def compileinfo (self, fname):
		"""progress indicator function"""
		print ("Compiling source file: " + str(fname))
			
	def exe(self):
		"""Compile all source coming with viraland package"""
		currdir = os.getcwd()
		
		os.chdir(self.vlhome)
		#os.chdir("../")
		# create a folder for executable files, if not exist
		if not os.path.exists("bin/") or os.listdir("bin/") == "":
			os.makedirs ("bin/")
    	
    	# compile all source code into binary folders
		for file in os.listdir("src/src"):
		
		    # compile Java code
		    if file.endswith(".java"):
		        self.compileinfo(file)
		        os.system("javac src/src/" + file + " -d bin/")

		    # compile C++ source
		    if file.endswith(".cpp"):
		        self.compileinfo(file)
		        outfn = file[:-4]
		        os.system("g++ src/src/" + file + " -o bin/" + outfn)

		    # compile C source code
		    if file.endswith(".c"):
		        self.compileinfo(file)
		        outfn = file[:-2]
		        os.system("gcc src/src/" + file + " -o bin/" + outfn)
		os.chdir(currdir) # go back to the directory before