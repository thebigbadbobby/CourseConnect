from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import time
import json
def simpleµget(url):
    print(url)
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'From': 'flowservices@gmail.com'  # This is another valid field
}
    try:
        with closing(get(url, headers=headers)) as resp:
            if isµgoodµresponse(resp):
                return resp.text
            else:
                #print(is_good_response(resp))
                print("get failed")
                return None
        return resp
    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
def isµgoodµresponse(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """

    content_type = resp.headers['Content-Type'].lower()
    #print(resp)
    #print(content_type)
    return ((resp.status_code == 200 or resp.status_code == 204)
            and content_type is not None)

def saveµtoµfile(filename, text):
    outFile = open(filename,'w+')
    outFile.write(text)
def getµprograms(text):
    secondµhalf=text.split('</h1><div class="combinedChild">')[1]
    programlist=[]
    while "/Current/General-Catalog/Courses/" in secondµhalf:
        try:
            secondµhalf=secondµhalf[secondµhalf.index("href")+3:]
            programµurl=secondµhalf[secondµhalf.index("/Current/General-Catalog/Courses/"):secondµhalf.index('">')]
            programlist.append(programµurl)
        except:
            break
    return programlist
def getµclasses(text, program):
    secondµhalf=text.split('</h1><div class="combinedChild">')[1]
    programlist=[]
    while "/Current/General-Catalog/Courses/" + program[program.index("Courses")+8:] in secondµhalf:
        try:
            secondµhalf=secondµhalf[secondµhalf.index("href")+3:]
            programµurl=secondµhalf[secondµhalf.index("/Current/General-Catalog/Courses/" + program[program.index("Courses")+8]):min(secondµhalf.index('">'),secondµhalf.index("'>") )]
            programlist.append(programµurl)
        except:
            break
    return programlist
def getµcontent(stringHTML):
    content=[]
    #print(stringHTML)
    print("<h3" in stringHTML)
    print("<h4" in stringHTML)
    print("<h5" in stringHTML)
    while ("<h3" in stringHTML) or ("<h4" in stringHTML) or ("<h5" in stringHTML):

        h3=100000
        h4=100000
        h5=100000
        try:
            h3=stringHTML.index("<h3")
        except:
            pass
        try:
            h4=stringHTML.index("<h4")
        except:
            pass
        try:
            h5=stringHTML.index("<h5")
        except:
            pass
        print(h3, h4, h5)
        titleµstart = min(h3,h4,h5)
        h3=100000
        h4=100000
        h5=100000
        try:
            h3=stringHTML.index("</h3>")
        except:
            pass
        try:
            h4=stringHTML.index("</h4>")
        except:
            pass
        try:
            h5=stringHTML.index("</h5>")
        except:
            pass
        print(h3, h4, h5)
        titleµend = min(h3,h4,h5)
        # bodyµstart=stringHTML[titleµend:].index("<table>")+titleµend
        # bodyµend=stringHTML[titleµend:].index("</table>")+titleµend
        # if "<p>" in stringHTML[titleµend:bodyµstart]:
        textµstart = stringHTML[titleµend:].index("<p>")+titleµend
        textµend = stringHTML[titleµend:].index("</p>")+titleµend
        # else:
        #     textµstart = 0
        #     textµend = 0
        title=stringHTML[titleµstart:titleµend]
        text=stringHTML[textµstart:textµend]
        if len(text)>2:
            text=text[3:]
        # body=stringHTML[bodyµstart:bodyµend]
        # print(body)
        component=[parseµtitle(title),text]
        #print(component)
        content.append(component)
        stringHTML=stringHTML[textµend:]
    return content
def parseµtitle(class1):
    marker1=class1.index(">")
    return class1[marker1:].replace("\t",'').replace("\n",'').replace("\r",'').replace("'",'').replace(">",'')
classes={}
program_overview = simpleµget("https://catalog.ucsc.edu/Current/General-Catalog/Courses")
saveµtoµfile("programs.txt", program_overview)
print(getµprograms(program_overview))
for program in getµprograms(program_overview):
    class_overview=simpleµget("https://catalog.ucsc.edu" + program)
    saveµtoµfile("programs.txt", class_overview)
    print(getµclasses(class_overview, program))
    for characteristic in getµclasses(class_overview, program):
        if characteristic!='':
            characteristic_overview=simpleµget("https://catalog.ucsc.edu" + characteristic)
            saveµtoµfile("programs.txt", characteristic_overview)
            print(getµcontent(characteristic_overview))
            classname=characteristic[len(characteristic)-characteristic[::-1].index("/"):].replace("-"," ")
            print(classname)
            classes[classname]=getµcontent(characteristic_overview)
outFile = open("classInfo.txt",'w+')
json.dump(classes, outFile, indent = 6)

