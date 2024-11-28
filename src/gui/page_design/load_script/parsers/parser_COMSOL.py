##--------------------------------------------------------------------\
#   Antenna Calculation and Autotuning Tool
#   '.src/gui/page_design/load_script/load_COMSOL.py'
#   Class for parsing COMSOL scripts for parameterized vars
#
#       should probably be in the sim_integrator, but theoretically
#       non-simulation based data should be able to be uploaded in the future
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   Last update: November 21, 2024
##--------------------------------------------------------------------\

import re

class ImportCOMSOLScript():
    def __init__(self, filepath):
        self.filepath = filepath
        self.script = [] #full file
        self.paramList = []
        self.paramValLst = []


    def importScript(self):
        self.readScript()
        self.populateDetectedKeywords()       
        return self.paramList, self.paramValLst, self.script


    def readScript(self):
        noErrors = False #returns False if there's an issue with the script
        try:
            with open(self.filepath) as f:
                for line in f.readlines(): 
                    self.script.append(line)
            noErrors = True
        except Exception as e:
            print(e)
        return noErrors    


    def populateDetectedKeywords(self):
        try:
            txt = self.script
            if txt == [] or txt == None:
                print("no parameters detected")
                pass
            else:
                keyLst, valLst = self.identifyKeywords(txt)
                self.paramList = keyLst
                self.paramValLst = self.cleanList(valLst) #get rid of newlines and some spacing
        except Exception as e:
            print(e)


    def identifyKeywords(self, txt):
        keyLst, valLst = self.extractKeywords(txt)
        #keyLst, valLst = uniqueKeywords(keyLst, valLst)
        return keyLst, valLst


    def extractKeywords(self,txt):
        #pulls out any parameters that start with '$'
        keyLst = []
        valLst = []
        ctr = 0
        for l in txt:
            pass

        print("This feature has not been integrated yet")
        return keyLst, valLst


    def uniqueKeywords(self, lst, valLst):
        #makes a list of unique keywords
        uniquelst = []
        lst2= []
        for x in lst:
            if x not in uniquelst:
                uniquelst.append(x)
        return uniquelst, lst2


    def cleanList(self, lst):
        #example lst input: [' "38.03628871563654 mm" \n', ' "29.442361217936117 mm" \n', ' "2*$length" \n', ' "1.6 mm" \n', ' "3.0589749829276442 mm" \n', ' "$length/4" \n', ' "1 mm" \n']
        txt = []
        for l in lst:
            l = re.sub("\n", "", l)
            l = re.sub("\"", "", l)
            l = l.strip() #get rid of leading and trailing whitespace
            txt.append(l)
        return txt
