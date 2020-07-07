## a python wrapper for causalTree in R.
## use using the following import:
#### from ct_r import causal_tree_r

import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
import gc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

pandas2ri.activate()

class causal_tree_r(object):
    _counter = 0
    
    @staticmethod
    def value_encoder(val):
        if(isinstance(val, str)): return '"'+val+'"'
        if(isinstance(val, bool)): return 'T' if val else 'F'
        return str(val)
    
    def __init__(self):
        self.id = causal_tree_r._counter
        #print(self.id)
        #if(self.id==0): robjects.r('library(causalTree)')
        causalTree = importr('causalTree')
        causal_tree_r._counter += 1
    
    def tree_setup(self, df, features, outcome, treat, params):
        gc.collect()
        print("\n\n\n"+"*"*32)
        print("model_id = ", self.id)
        print("features = ", features)
        print("outcome = ", outcome)
        print("treat = ", treat)
        self.model_name = "ct_%d"%(self.id)
        eq = outcome + " ~ " + " + ".join(features)
        print("model_name = ", self.model_name)
        print(eq)
        
        ## construct params
        r_params = []
        r_params += ["data=df"]
        r_params += ["treat=%s"%("df$"+treat)]
        for p in params:
            r_params += ["%s=%s"%(p, causal_tree_r.value_encoder(params[p]))]
        
        #print(r_params)
        cmd = self.model_name + " <- " + "causalTree" + "(" + " , ".join([eq]+r_params) + ")"
        print(cmd)
        
        ## send data to r
        status = robjects.globalenv['df'] = df
        
        ## run cmd
        status = robjects.r(cmd)
    
    def predict(self, df_new):
    	## no R interface for predict found
    	#raise NotImplementedError("causal_tree_r.predict()")
    	#pass

        robjects.globalenv["df_new"] = df_new
        res = robjects.r('predict(%s, df_new)'%(self.model_name))
        return res

    
    def show_cp_table(self):
        gc.collect()
        cptable = robjects.r(self.model_name+"$cptable")
        #print(cptable[1])
        print("*** Complexity Parameter Table ***")
        print("    %12s nsplit %12s %12s %12s"%("CP", "rel error", "xerror", "xstd"))
        for i in range(len(cptable)):
            print("%3d %.6e %6d %.6e %.6e %.6e"%tuple([i]+list(cptable[i])) )
        print("**********************************")
        
        return {
            "CP":cptable[:,0],
            "nsplit":cptable[:,1],
            "rel_error":cptable[:,2],
            "xerror":cptable[:,3],
            "xstd":cptable[:,4],
        }
        
    def prune(self, c):
        gc.collect()
        if(c=="auto"):
            cmd = "%s$cptable[,1][which.min(%s$cptable[,4])]"%(self.model_name, self.model_name)
            #print(cmd)
            opcp = robjects.r(cmd)[0]
            #print(opcp)
        else:
            opcp = c
        cmd = "%s <- prune(%s, cp=%s)"%(self.model_name, self.model_name, causal_tree_r.value_encoder(opcp))
        #print(cmd)
        status = robjects.r(cmd)   
        return opcp
    
    def plot_tree(self, file="tree.png"):
        robjects.r("png('%s', res = 400, width = 4, height = 4, units = 'in')"%(file))
        robjects.r('rpart.plot(%s)'%self.model_name)
        robjects.r('dev.off()')
        img = mpimg.imread(file)
        plt.imshow(img)
        plt.axis('off')
        plt.show()
