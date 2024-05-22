import os
import sys

def parse(line,idx):
    global headFiles
    if line[0:8] == "#include":
        headFiles = preprocessor(line[8:],idx)
        print("[Info] Add head File "+headFiles[-1]+' to head file list')
        return  headFiles
    else:
        for types in dataType:
            if line[0:len(types)] == types:
                obj = {"DataType":dataType[types]}
                if types == "int":
                    obj = parseInt(line[len(types):],obj,idx)
                    synTree.append(obj)
                    return obj

def parseInt(line,obj,idx):
    if line[-1] == "{":
        for i in range(0,len(line)-1):
            if line[i] == "(":
                #parse argument
                obj["arg"] = parse(line[i:-2],idx)
                obj["val"] = "int func()"
                obj["var"] = line[0:i]

                return obj
                    
    elif line[-1] == ";":
        for i in range(0,len(line)-1):
            if line[i] == "=":
                obj["val"] = line[i+1:-1]
                obj["var"] = line[0:i]
        return obj

def parseVoid(line, obj, idx):
    if line[-1] == "{":
        for i in range(0, len(line) - 1):
            if line[i] == "(":
                obj["arg"] = parse(line[i:-2], idx)
                obj["val"] = "void func()"
                obj["var"] = line[0:i]
                return obj
    elif line[-1] == ";":
        for i in range(0, len(line) - 1):
            if line[i] == "=":
                obj["val"] = line[i+1:-1]
                obj["var"] = line[0:i]
        return obj

def parseChar(line, obj, idx):
    if line[-1] == "{":
        for i in range(0, len(line) - 1):
            if line[i] == "(":
                obj["arg"] = parse(line[i:-2], idx)
                obj["val"] = "char func()"
                obj["var"] = line[0:i]
                return obj
    elif line[-1] == ";":
        for i in range(0, len(line) - 1):
            if line[i] == "=":
                obj["val"] = line[i+1:-1]
                obj["var"] = line[0:i]
        return obj

def parsePointer(line, obj, idx):
    if line[-1] == "{":
        for i in range(0, len(line) - 1):
            if line[i] == "(":
                obj["arg"] = parse(line[i:-2], idx)
                if "int*" in line:
                    obj["val"] = "int pointer func()"
                elif "char*" in line:
                    obj["val"] = "char pointer func()"
                elif "void*" in line:
                    obj["val"] = "void pointer func()"
                obj["var"] = line[0:i]
                return obj
    elif line[-1] == ";":
        for i in range(0, len(line) - 1):
            if line[i] == "=":
                obj["val"] = line[i+1:-1]
                obj["var"] = line[0:i]
        return obj

def preprocessor(line,idx):
    global lastHeadIdx
    if idx - lastHeadIdx >= 2:
        exit()
    if line[0] == "<" and line[-1] == ">":
        headFile = line[1:-1]
        lastHeadIdx = idx
    elif line[0] == '"' and line[-1] == '"':
        headFile = line[1:-1]
        lastHeadIdx = idx
    headFiles.append(headFile)
    return headFiles

if __name__ == "__main__":

    #variable
    lastHeadIdx = 0
    headFiles = []
    synTree = []

    #constant
    dataType = {"int":"int","char":"char","void":"void","int*":"int ptr","char*":"char ptr","void*":"void ptr"}
    
    if len(sys.argv) != 1:
        args = sys.argv[1:]
        for arg in args:
            if arg == "-h":
                print("\nPCT.py a python script compile C to ASM\n[Usage]\n\tpct.py [file]")
            else:
                src = arg
    else:
        exit()
    
    try:
        source = []
        src = open(src,"r")
        for line in src:
            line = line.replace("\n","").replace("\t","")
            line = line.replace("\r","").replace(" ","")
            source.append(line)
        src = source
    except:
        print("[Error] File Error Occurs")
        exit()

    for i in range(0,len(src)-1):
        parse(src[i],i)

    print("syntax:",synTree,"\nheadfiles:",headFiles)
