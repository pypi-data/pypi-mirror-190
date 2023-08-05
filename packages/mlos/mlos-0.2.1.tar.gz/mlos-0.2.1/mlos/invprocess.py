
import os
import pickle
import numpy as np
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing



class invproc:
    def __init__(self):
        self._noneed=""
    def tst(self,v):
        self.test="yes"
    def logtext(self,fn,msg,vb):
        # valx= str(msg).replace(config._wp,'')
        with open(fn, 'a') as f1:
            f1.write('\n')
            f1.write(str(msg))
        if vb:
            print(str(msg))
    def gettransfromed(self,fn,data):
        with open(fn, 'rb') as infile:  
            scaler = pickle.load(infile)
        return scaler.transform(data)
    def get_normalize_db(self,op,data,ntx):
        if (op=="scaling"): # Scaling 
            #mllib.mltext("MLP : " + op + ":scl:"  + ntx)
            scaler = preprocessing.MaxAbsScaler().fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif (op=="categorical_2_numeric"):
            scaler = preprocessing.LabelEncoder().fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif (op=="default_mlos_preprocessing"):
            #mllib.mltext("MLP : " + op + ":std:"  + ntx)
            scaler = preprocessing.StandardScaler().fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif (op=="standard_caling"):
            #mllib.mltext("MLP : " + op + ":std:"  + ntx)
            scaler = preprocessing.StandardScaler().fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif (op=="absolute_scaling"):
            #mllib.mltext("MLP : " + op + ":abs:"  + ntx)
            scaler = preprocessing.MaxAbsScaler().fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif(op=="zero2one_ormalization"):
            #mllib.mltext("MLP : " + op + ":mmn:"  + ntx)
            scaler = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif(op=="min_max_normalization"):
            #mllib.mltext("MLP : " + op + ":mmn:"  + ntx)
            scaler = preprocessing.MinMaxScaler().fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif(op=="quantile_ransformer"):
            #mllib.mltext("MLP : " + op + ":qt:"  + ntx)
            scaler = preprocessing.QuantileTransformer(random_state=0).fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif(op=="l1_normalization"):
            #mllib.mltext("MLP : " + op + ":l1:"  + ntx)
            scaler = preprocessing.Normalizer(norm='l1')
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif(op=="l2_normalization"):
            #mllib.mltext("MLP : " + op + ":l2:"  + ntx)
            scaler = preprocessing.Normalizer(norm='l2')
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        elif(op=="pca"):
            print("PCA does not support.")
            #mllib.mltext("MLP : " + op + ":pca:"  + ntx)
        else:
            #mllib.mltext("MLP : " + op + ":mlpd:"  + ntx)
            scaler = preprocessing.StandardScaler().fit(data)
            with open(ntx, 'wb') as outfile:  
                pickle.dump(scaler, outfile)
            return scaler.transform(data)
        return 0

    def visiontransform(self,fn,xTst):
        scaler =[]

        with open(fn, 'rb') as infile:  
            scaler = pickle.load(infile)
        return scaler.transform(xTst)

    def getinvtransfromed(self,fn,xTst):
        scaler =[]
        with open(fn, 'rb') as infile:  
            scaler = pickle.load(infile)
        return scaler.inverse_transform(xTst)

    def getinvtransfromed2(self,fn,data):
        scaler =[]
        with open(fn, 'rb') as infile:  
            scaler = pickle.load(infile)
        print("=====CLASSES==========")
        clslals=scaler.classes_
        
        # vvcv=  np.array(data)
        # print(vvcv)
        # nwclslals=[]
        # for cx in clslals:
        #     nwclslals.append(cx)
        # print(nwclslals)
        # inc_classes=scaler.transform(scaler.classes_)
        # print(inc_classes)
        # print("=====UNIQUE XTEST==========")
        # print(np.unique(data))
        # one_inval=scaler.transform(['_mlos__unseen_'])
        # print(one_inval)
        print(data)
        newxtst=[]
        for x in  data:
            v=x[0]
            # if(np.isnan(v)):
            #     newxtst.append('_mlos__unseen_')
            if v in clslals:
                newxtst.append(str(v))
            else:
                newxtst.append('_mlos__unseen_')
        print("=====UNIQUE NewList==========")
        
        trns=scaler.transform(newxtst)
        print(trns)
        return  trns
