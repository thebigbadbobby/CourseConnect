from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import time
import json
import os
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
    while "/Current/General-Catalog/Academic-Units/" in secondµhalf:
        try:
            secondµhalf=secondµhalf[secondµhalf.index("href")+3:]
            programµurl=secondµhalf[secondµhalf.index("/Current/General-Catalog/Academic-Units/"):secondµhalf.index('">')]
            programlist.append(programµurl)
        except:
            break
    return programlist
def getµprogramµpages(programµlist):
    programµinfoµlist={}
    for filename in programµlist:
        programµinfo=simpleµget("https://catalog.ucsc.edu/"+program)
        
        title=programµinfo[programµinfo.index("g - ")+4:programµinfo.index("</title")-2]
        #print(programµinfo)
        saveµtoµfile("ProgramPages/"+title.replace(" ","").replace(".","").replace("/","")+".txt", programµinfo)
        programµinfoµlist[title]=getµcontent(programµinfo)
    return programµinfoµlist

def getµprogramµinfo():
    programµinfoµlist={}
    for (dirpath, dirnames, filenames) in os.walk("./ProgramPages"):
        for filename in filenames:
            with open("ProgramPages/" + filename, 'r') as test_file:
                programµinfo=test_file.read()
            
                title=programµinfo[programµinfo.index("g - ")+4:programµinfo.index("</title")-2]
                #print(programµinfo)
                # saveµtoµfile("ProgramPages/"+title.replace(" ","").replace(".","").replace("/","")+".txt", programµinfo)
                programµinfoµlist[title]=getµcontent(programµinfo)
    return programµinfoµlist
        # saveµtoµfile("AgroecologyBA.txt", programµinfo)
# def getµcategories(stringHTML):
#     categories={}
#     while "</h4>" in stringHTML:
#         titleµstart=stringHTML.index("<h4>")
#         titleµend=stringHTML.index("</h4>")
#         bodyµstart=stringHTML.index("</h4>")
#         bodyµend=stringHTML.index("<h4>", titleµstart+4)
#         categories[titleµstart:titleµend]=getµrequirements(stringHTML.index("</p>"))
#     return

# def getµrequirements(stringHTML):
#     requirements={}
#     while "</h5>" in stringHTML:
#         requirements[stringHTML.index("<h5>"):stringHTML.index("</h5>")]=getµclasses(stringHTML[stringHTML.index("</table>"):stringHTML.index("</table>")])
#     return requirements
def getµclasses(stringHTML):
    classes=[]
    count=0
    while "/en/Current/General-Catalog/Courses/" in stringHTML:
        count+=1
        short=stringHTML[stringHTML.index("/en/Current/General-Catalog/Courses/"):stringHTML.index("</a>")]
        # print("ekans", short)
        if short.isspace() or short=="":
            stringHTML=stringHTML[stringHTML.index('</a>')+3:]
            continue
        classes.append(parseµclass(short))
        # print(stringHTML)
        stringHTML=stringHTML[stringHTML.index('</a>')+3:]
    return classes
def parseµclass(class1):
    # print(class1)
    marker1=class1.index(">")
    #print(class1[marker1:])
    # marker2=class1[marker1:].index('"')+marker1
    return class1[marker1:].replace("'",'').replace(">",'')
def parseµtitle(class1):
    marker1=class1.index(">")
    return class1[marker1:].replace("\t",'').replace("\n",'').replace("\r",'').replace("'",'').replace(">",'')
def getµcontent(stringHTML):
    content={}
    key="Main Page"
    # content[key]={}
    #print(stringHTML)
    print("<h2" in stringHTML)
    print("<h3" in stringHTML)
    print("<h4" in stringHTML)
    print("<h5" in stringHTML)
    while ("<h2" in stringHTML) or ("<h3" in stringHTML) or ("<h4" in stringHTML) or ("<h5" in stringHTML):
        h2=100000
        h3=100000
        h4=100000
        h5=100000
        try:
            h2=stringHTML.index("<h2")
        except:
            pass
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
        print(h2, h3, h4, h5)
        titleµstart = min(h2,h3,h4,h5)
        h2=100000
        h3=100000
        h4=100000
        h5=100000
        

        try:
            h2=stringHTML.index("</h2>")
        except:
            pass
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
        print(h2, h3, h4, h5)

        titleµend = min(h2, h3,h4,h5)
        if min(h2, h3,h4,h5)==h2:
            echelon=2
        if min(h2, h3,h4,h5)==h3:
            echelon=3
        if min(h2, h3,h4,h5)==h4:
            echelon=4
        if min(h2, h3,h4,h5)==h5:
            echelon=5
        bodyµstart=stringHTML[titleµend:].index("<table>")+titleµend
        bodyµend=stringHTML[titleµend:].index("</table>")+titleµend
        if "<p>" in stringHTML[titleµend:bodyµstart]:
            textµstart = stringHTML[titleµend:].index("<p>")+titleµend
            textµend = stringHTML[titleµend:].index("</p>")+titleµend
        else:
            textµstart = 0
            textµend = 0
        title=stringHTML[titleµstart:titleµend]
        text=stringHTML[textµstart:textµend]
        if len(text)>2:
            text=text[3:]
        body=stringHTML[bodyµstart:bodyµend]
        # print(body)
        if echelon>2:
            component=[text,getµclasses(body),echelon]
        #print(component)
            content[key][parseµtitle(title)]=component
            stringHTML=stringHTML[bodyµend:]
        else:
            print("arbook", parseµtitle(title))
            key=parseµtitle(title)
            content[key]={}
            stringHTML=stringHTML[stringHTML.index("</h2>")+5:]
    # prevµechelon=2
    # prevµkey="Main Program"
    # content["Main Program"]={}
    # deletelist=[]
    # for key in content:
    #     # print(len(content[key]))
    #     # print(key,prevµkey, content[key],prevµechelon)
    #     if key=="Main Program":
    #         break
    #     if content[key][2]>prevµechelon:
    #         content[prevµkey][key]=content[key]
    #         deletelist.append(key)
    #     else:
    #         print(key,prevµkey, content[key][2],prevµechelon)
    #         prevkey=key
    # for key in deletelist:
    #     content.pop(key)
    
    return content
def updateµprogramµpages():
    program_overview = simpleµget("https://catalog.ucsc.edu/Current/General-Catalog/Academic-Programs/Bachelors-Degrees")
    saveµtoµfile("programs.txt",program_overview)
    programµlist=getµprograms(program_overview)
    programµinfo=getµprogramµpages(programµlist)

print("ekans")

programµinfo=getµprogramµinfo()
print(programµinfo)
outFile = open("majorInfo.txt",'w+')
json.dump(programµinfo, outFile, indent = 6)


