

import os
import pandas as pd

class Selection():
    def __init__(self, DC, PC, SO): 
        self.DC = DC
        self.PC = PC
        self.SO = SO

        #data management
        self.optimizerName = "SELECTION"
        self.optimizerDir = None
        self.dataDir = None
        self.setOptimizerDirs()


        # class vars
        self.inputParams = pd.DataFrame({})



#######################################################
# Optimizer save funcs & directory management
#######################################################

    def setOptimizerDirs(self):
        #check for data and recursively create all dirs if not found
        baseDir = self.PC.getOptimizerDirectory()
        self.optimizerDir = os.path.join(baseDir, self.optimizerName)
        self.dataDir = os.path.join(self.optimizerDir, "data")
        if os.path.exists(self.dataDir) == False:
            os.makedirs(self.dataDir)

    def getOptimizerDir(self):
            #base optimizer dir
            return self.optimizerDir
    
    def getDataDir(self):
            #optimizer/data dir
            return self.dataDir


####################################################
# Setters and getters
####################################################

    def setParams(self, df):
        self.inputParams = df

    def setState(self, s):
        pass

    def getState(self):
        pass


####################################################
# Run, pause, stop
####################################################

    def run(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass



