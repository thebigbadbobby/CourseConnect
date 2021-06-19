import sys
with open(sys.argv[1], 'r') as test_file:
    full_file=test_file.read()
    inputs= []
    for line in full_file:
        inputs.append(line)
    output=test(inputs, func)
    string = ""
    for result in output:
        string += result + "\n"
    saveµtoµfile("output.txt", string)
def saveµtoµfile(filename, text):
    outFile = open(filename,'w+')
    outFile.write(text)
