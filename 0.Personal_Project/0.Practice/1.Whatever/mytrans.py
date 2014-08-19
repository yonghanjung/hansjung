# Key idea
# goslate module can translate
# unicode or string to any language the user want
 
from bs4 import BeautifulSoup
import mechanize
import readability
from readability.readability import Document
import goslate
 
while True :
    url = raw_input('Put url to translate:\n')
    lang = raw_input('Korean? (ko), English? (en) :\n')
 
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent','Firefox')]
 
    htmltext = br.open(url).read()
    readable_title = Document(htmltext).short_title()
    readable_article = Document(htmltext).summary()
 
    soup = BeautifulSoup(readable_article)
    final = soup.text

     #=========== Extract the text from HTML document  ========
 
    gs = goslate.Goslate()
    print 'Direct Translating : ',gs.translate(readable_title,lang)
    print 'Japanese converting: ',gs.translate(gs.translate(readable_title,'ja'),lang)
    print '\n'
    print '[Direct Translating]\n',gs.translate(final,lang)
    print '\n =========================================================== \n'
    print '[Japanese converting]\n',gs.translate(gs.translate(final,'ja'),lang),'\n\n'