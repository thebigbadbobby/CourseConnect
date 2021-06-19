import sys
import json
import time
def saveµtoµfile(filename, text):
    outFile = open(filename,'w+')
    outFile.write(text)
def specific(info, args):
    # print(args[1])
    array=[]
    if len(args)==1:
        print(info)
        return info
    # print(info)
    if args[1] == "ALL":
        try:
            for key, value in info.items():
                array.append(value)
        except:
            for value in info:
                array.append(value) 
    else:
        try:
            array.append(info[args[1]])
        except:
            try: 
                array.append([info[int(args[1])]])
            except:
                array.append(["undefined on term " +args[1]])
    # print(array)
    array[:]=[specific(item, args[1:]) for item in array]
    final_array=[]
    # print(len(array))
    for item in array:
        final_array=final_array+item
    # time.sleep(1)
    return final_array
        
with open(sys.argv[1], 'r') as test_file:
    full_file=test_file.read()
    info=json.loads(full_file)
    objlist = json.dumps(specific(info, sys.argv[1:]))
    saveµtoµfile("input.txt", objlist)

