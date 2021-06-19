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
file = simpleµget("https://catalog.ucsc.edu/Current/General-Catalog/Academic-Units/Social-Sciences-Division/Environmental-Studies/Environmental-Studies-BA")
saveµtoµfile("EnvironmentalStudiesBA.txt",file)