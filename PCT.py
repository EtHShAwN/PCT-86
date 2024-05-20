#!/usr/bin/env python
# -*- coding: utf-8 -*-!
#2024/05/20 - 23:37

"""
        This is a script hot as f*ck for compiling C(more like dialect) source file to MASM Syntax real mode .ASM file

        !=============================！
        !                             !
        !   sorry dude I have ADHD    ！
        !                             !
        !=============================!
"""

import sys
import os


#initialization

def genObjFile():
        for i in range(0,len(src)-1):
                if src[i] == ".":
                        asmOutputFile = open(src[:i]+".asm","w")
                        return asmOutputFile
        print("[Warning] Source File's suffix is not determined, this may cause random error")
        
if len(sys.argv) != 1:
	for args in sys.argv[1:]:
		if args == "-h":
			print("pct86 - A tranlator for real mode C language\n\n[Usage]\n\tpct86 [file]")
			exit()
		else:
			src = args
			asmOutputFile = genObjFile()


try:
	src = open(src,"r")
except:
	print("[Error] File Error Occurs")
	exit()

#variables
headerFiles = []
index = 1
entryRet  = ""

#const set
data = {'int':'int','char':'char','double':'double','int*':'int pointer','char*':'char pointer','void':'void','void*':'void pointer'} #sorry float point not support yet

def noAuxillary(line):
        line = line.replace("\t","")
        line = line.replace("\r","")
        line = line.replace("\n","")
        line = line.replace(" ","")
        return line

def entry():
        asmOutputFile.write("assume cs:code\ncode segment\nmain:")
        if entryType == "void" or entryType == "void pointer":
                RetVal = ""
        else:
                RetVal = "ret"
                
        

for line in src:

	#process header file
        index+=1
        line = noAuxillary(line)
        if line[0:8] == "#include":
                header = line[8:]
                if header[0] == "<" and header[-1] == ">":
                        if sys.platform == "win32":
                                PATH = input("[Hint] Specify Standard Header File Path:")
                                header = {'Name':header[1:-1],'File':PATH+header[1:-1]}
                        else:
                                header = {'Name':header[1:-1],'File':"/usr/include/sys/"+header[1:-1]}
                elif header[0] == '"' and header[-1] == '"':
                        header = {'Name':header[1:-1],'File':"./"+header[1:-1]}
                else:
                        print("[Error] Invalid format of header file")
                        exit()
                headerFiles.append(header)
                print("[Info] header files:",headerFiles)

        #main process
        for i in range(0,len(line)-1):
                if line[i:i+6] == "main()" and line[i+6] == "{":
                        try:
                                data[line[:i]]
                        except:
                                print("[Error] Undefined type of Entry Point")
                                exit()
                        entryType = data[line[:i]]
                        print("[Info] Entry Point Type:",entryType)
                        print("[Proc] Write Entry Point to .ASM source file")
                        entry()
