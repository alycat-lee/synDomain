#-*- coding: utf8 -*-
import HTMLParser
import re
class LocalIP(HTMLParser.HTMLParser):   
    def __init__(self):   
        HTMLParser.HTMLParser.__init__(self)   
          
    def handle_data(self, data):   
        reg = re.compile(r'\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]')
        temp = re.findall(reg,data)
        if(len(temp) > 0):
	        self.content = temp[0]
