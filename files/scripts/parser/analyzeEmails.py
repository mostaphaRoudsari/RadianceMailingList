from pprint import pprint
import json

class RADEmail(object):
    
    def __init__(self):
        self.subject = ""
        self.sender = ""
        self.email = ""
        self.refs = []
        self.id = ""
        self.replyTo = ""
        self.datetime = ""
        self.body = ""
        self.tags = []
        self.isquestion = True
        
    def setSubject(self, subject):
        self.subject = subject
    
    def setDatetime(self, datetime):
        self.datetime = datetime
    
    def setSender(self, sender):
        self.sender = sender
    
    def setEmail(self, email):
        self.email = email
    
    def setReference(self, ref):
        self.refs.append(ref)
    
    def setId(self, id):
        self.id = id
    
    def setReplyTo(self, replyTo):
        self.replyTo = replyTo
        self.isquestion = False # it's a reply
    
    def addMsg(self, msg):
        self.body += msg + "\n"
    
    def getDict(self):
        return {
            "subject" : self.subject,
            "sender" : self.sender,
            "email" : self.email,
            "refs": self.refs,
            "id": self.id,
            "replyTo": self.replyTo,
            "datetime" : self.datetime,
            "body": self.body,
            "tags": self.tags,
            "isquestion": self.isquestion
        }
    
    def writeToJson(self, path):
        with open(path, 'wb') as fp:
            json.dump(self.getDict(), fp)
    
    def __str__(self):
        return "subject:" + self.subject + \
               "\nsender: " + self.sender + \
               "\nemail: " + self.email + "\n"
    
def analyzeFile(f, year):
    
    # initiate a new email
    email = RADEmail()
    year = str(year)
    
    for line in f:
        
        line = line.strip()
        
        if line.startswith(">"):
            continue
            
        elif line.startswith("From ") and line.endswith(year):
            
            fp = "C:\\Users\\MSadeghipourroudsari\\Documents\\GitHub\\RadianceMailingList\\files\\json\\"
            
            sc.sticky["counter"]+= 1
            #print sc.sticky["counter"]
            
            email.writeToJson(fp + str(sc.sticky["counter"]) + ".json")
            
            
            #start of a new email
            analyzeFile(f, year)
        
        elif line.startswith("From: "):
            
            line = line.strip("From: ")
            
            spl = ["(", ")"]
            if line.find(spl[0])==-1: spl = ["[", "]"]
            if line.find(spl[0])==-1: spl = ["<", ">"]
            
            emailAddress = line.split(spl[0])[0].strip()
            email.setEmail(emailAddress)
            
            # in some cases sender name has (
            sender = line[line.find(spl[0])+1:line.find(spl[1])].split("mailto:")[-1]
            email.setSender(sender)
            
        elif line.startswith("Date: "):
            #print "date is" + line.strip("Date: ")
            email.setDatetime(line.strip("Date: "))
            
        elif line.startswith("Subject: "):
            
            subject = line.strip("Subject: ")
            
            nextLine = f.next()
            
            if nextLine.startswith("Message-ID: "):
                #print "ID is" + nextLine.strip("Message-ID: ")
                email.setId(nextLine.strip("Message-ID: ").strip())
                
            elif nextLine.startswith("In-Reply-To: "):
                email.setReplyTo(line.strip("In-Reply-To: "))
            else:
                subject += nextLine.strip()
            
            email.setSubject(subject)
            
        elif line.startswith("In-Reply-To: "):
            
            email.setReplyTo(line.strip("In-Reply-To: "))
            
        elif line.startswith("References: "):
            
            email.setReference(line.strip("References: "))
            
            # check next line not to be reference
            nextLine = f.next()
            while not nextLine.startswith("Message-ID: "):
                email.setReference(nextLine.strip())
                nextLine = f.next()
            
            email.setId(nextLine.strip("Message-ID: ").strip())
            
        else:
            email.addMsg(line)
    
    return counter


#with open(filepath, "rb") as f:
#    f.readline() #pass first line
#    analyzeFile(f)

import gzip
import shutil
import calendar
import scriptcontext as sc

sc.sticky["counter"] = 0

"""
for year in range(2000, 2016):

    for m in range(1, 13):
    
        month = calendar.month_name[m]
    
        #gzpath = r"C:\radianceMailList\%d-%s.txt.gz"%(year, month)
        filepath = r"C:\radianceMailList\%d-%s.txt"%(year, month)
        #print filepath
        #try:
        #    with gzip.open(gzpath, 'rb') as f_in, open(filepath, 'wb') as f_out:
        #        shutil.copyfileobj(f_in, f_out)
        #except:
        #    pass
        
        try:
            with open(filepath, "rb") as f:
                f.readline() #pass first line
                analyzeFile(f, year)
        except Exception, e:
            print `e`
            pass
"""