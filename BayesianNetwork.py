#!/usr/bin/env python
""" generated source for module BayesianNetwork """
from Assignment4 import *

import random



# 
#  * A bayesian network
#  * @author Panqu
#  
class BayesianNetwork(object):
    """ generated source for class BayesianNetwork """
    # 
    #     * Mapping of random variables to nodes in the network
    #     
    varMap = None

    # 
    #     * Edges in this network
    #     
    edges = None

    # 
    #     * Nodes in the network with no parents
    #     
    rootNodes = None

    # 
    #     * Default constructor initializes empty network
    #     
    def __init__(self):
        """ generated source for method __init__ """
        self.varMap = {}
        self.edges = []
        self.rootNodes = []

    # 
    #     * Add a random variable to this network
    #     * @param variable Variable to add
    #     
    def addVariable(self, variable):
        """ generated source for method addVariable """
        node = Node(variable)
        self.varMap[variable]=node
        self.rootNodes.append(node)

    # 
    #     * Add a new edge between two random variables already in this network
    #     * @param cause Parent/source node
    #     * @param effect Child/destination node
    #     
    def addEdge(self, cause, effect):
        """ generated source for method addEdge """
        source = self.varMap.get(cause)
        dest = self.varMap.get(effect)
        self.edges.append(Edge(source, dest))
        source.addChild(dest)
        dest.addParent(source)
        if dest in self.rootNodes:
            self.rootNodes.remove(dest)

    # 
    #     * Sets the CPT variable in the bayesian network (probability of
    #     * this variable given its parents)
    #     * @param variable Variable whose CPT we are setting
    #     * @param probabilities List of probabilities P(V=true|P1,P2...), that must be ordered as follows.
    #       Write out the cpt by hand, with each column representing one of the parents (in alphabetical order).
    #       Then assign these parent variables true/false based on the following order: ...tt, ...tf, ...ft, ...ff.
    #       The assignments in the right most column, P(V=true|P1,P2,...), will be the values you should pass in as probabilities here.
    #     
    def setProbabilities(self, variable, probabilities):
        """ generated source for method setProbabilities """
        
        probList = []
        for probability in probabilities:
            probList.append(probability)
        self.varMap.get(variable).setProbabilities(probList)

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using rejection sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of rejection samples to perform
    #     
    def performRejectionSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performRejectionSampling """


        listofS=[]
        validSample=0
        needC=False
        V=0
        TEMPQ=[]
        L=[]
        
        
        for element in self.rootNodes:
            TEMPQ.append(element)
            #L.append(elements)
            
        while(len(TEMPQ)>0):
            temp=TEMPQ[0]
            TEMPQ=TEMPQ[1:]
            if temp not in L:
               L.append(temp)
            
            for d in temp.children:
                if d in L:
                    continue
                
                TEMPQ.append(d)
            
        
        while(validSample<=numSamples):
            needC=False
            needB=False
            sample=Sample()

                
            for c in L:
                if(needB):
                    break

                randomN=random.random()
                #print randomN
                
                TP=c.getProbability(sample.assignments,True)
                sample.assignments[c.getVariable().getName()]= (randomN<TP)

                for element in givenVars:
                        
                       if(c.getVariable().getName()==element.getName() ):
                           #print randomN < TP
                           #print givenVars[element]
                           #print "end"
                           if((randomN < TP) != givenVars[element]):
                               #sample.assignments[element.getName()]= (random<TP)
                               #print element.getName()
                           #else:
                               needB=True
                               needC=True
                               break
                           
                       #else:
                        #   sample.assignments[element.getName()]= (random<TP)
                         #  print element.getName()
                           
            validSample=validSample+1
            #print "start"
            if(needC==True):
             #    print "continue"
                 continue
            else:
                 listofS.append(sample)
               
        i =0                       
        for s in listofS:
            i=i+1
            if  s.assignments[queryVar.getName()]==True:
                V=V+1
                
        return float(V)/float(len(listofS))
                
        
        


    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #     
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        listofS={}
        validSample=0
        TEMPQ=[]
        L=[]                
        for element in self.rootNodes:
            TEMPQ.append(element)            
        while(len(TEMPQ)>0):
            temp=TEMPQ[0]
            TEMPQ=TEMPQ[1:]
            if temp not in L:
               L.append(temp)            
            for d in temp.children:
                if d in L:
                    continue                
                TEMPQ.append(d)                    
        while(validSample<=numSamples):                        
            sample=Sample()
            sample.setWeight(1)                
            for c in L:
                randomN=random.random()
                TP=c.getProbability(sample.assignments,True)
                if c.getVariable() not in givenVars:
                  sample.assignments[c.getVariable().getName()]= (randomN<TP)
                else:
                    sample.assignments[c.getVariable().getName()]=givenVars[c.getVariable()]                    
                for element in givenVars:                        
                       if(c.getVariable().getName()==element.getName() ):
                           sample.setWeight(sample.getWeight()*TP)                                                      
            validSample=validSample+1
            listofS[sample]=sample.getWeight()
        total = 0
        valid=0        
        for cc in listofS:
            if  cc.assignments[queryVar.getName()]==True:
                valid=valid+listofS[cc]
            total=total+listofS[cc]                        
        return float(valid)/total       

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using Gibbs sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numTrials Number of Gibbs trials to perform, where a single trial consists of assignments to ALL
    #       non-evidence variables (ie. not a single state change, but a state change of all non-evidence variables)
    #     
    def performGibbsSampling(self, queryVar, givenVars, numTrials):
        """ generated source for method performGibbsSampling """
        #  TODO

        listOfS = []
        validSample = 0
        TempQ = []
        L = []
        for e in self.rootNodes:
            TempQ.append(e)
            
        while(len(TempQ) > 0):
            currE = TempQ[0]
            TempQ = TempQ[1:]
            if currE not in L:
                L.append(currE)
            for c in currE.children:
                if c not in L:
                    TempQ.append(c)
                #TempQ.append(currE)
        
              
        TempL = L
        L = []
        counter = 0
        counter1 = 0
        for e in TempL:
            if e.getVariable() not in givenVars:
                L.append(e)
        
        for e in L:
            if(e.getVariable().getName() == queryVar.getName()):
                L.remove(e)
                L.insert(len(L),e)
                break


        while(validSample < numTrials):
            validSample = validSample + 1
            sample = Sample()
            for e in givenVars:
                #sample.assignments[e] = givenVars[e]
                sample.setAssignment(e,givenVars[e])
            for element in L:
                randN = random.random()
                #sample.assignments[element.getVariable()] = randN < element.getProbability(sample.assignments,True)
                sample.setAssignment(element.getVariable(), randN < element.getProbability(sample.assignments, True))
            for e in L:
               HT = e.getProbability(sample.assignments, True)
               HF = e.getProbability(sample.assignments, False)
               
               H = 0
               
               if(sample.assignments[e.getVariable()] == True):
                   H = HT
               else:
                   H = HF
                 
               for c in e.children:
                   p = c.getProbability(sample.assignments,sample.assignments[c.getVariable()])
                   H = H * p
               #storeB = sample.assignments[e.getVariable()]
               #sample.assignments[e.getVariable()] = True  
               sample.setAssignment(e.getVariable(), not sample.assignments[e.getVariable()])
               #sample.assignments[e.getVariable()] = not sample.assignments[e.getVariable()]                 
               LR = e.getProbability(sample.assignments, sample.assignments[e.getVariable()])
               for c in e.children:
                   p = c.getProbability(sample.assignments,sample.assignments[c.getVariable()])
                   LR = LR * p
 
               #sample.assignments[e.getVariable()] = not sample.assignments[e.getVariable()]   
               sample.setAssignment(e.getVariable(),not sample.assignments[e.getVariable()])
               #LF = e.getProbability(sample.assignments, False)
               #for c in e.children:
                #   p = c.getProbability(sample.assignments,sample.assignments[c.getVariable()])
                 #  LF = LF * p   
                   
               LTotal = LR + H
               
               resultP = float(H)/LTotal
               #sample.assignments[e.getVariable()] = storeB
               
               if(not sample.assignments[e.getVariable()]):
                   resultP = float(LR)/LTotal
               else:
                   resultP = float(H)/LTotal
               randC = random.random()  
               if randC > resultP :
                   #sample.assignments[e.getVariable()] = False
                   sample.setAssignment(e.getVariable(),False)
               else:
                   #sample.assignments[e.getVariable()] = True
                   sample.setAssignment(e.getVariable(),True)

               #if(e.getVariable().getName() == queryVar.getName()):
               if(sample.assignments[queryVar]):
                   counter = counter + 1
               else:
                   counter1 = counter1 + 1
                      
               
        retVal = float(counter)/(counter + counter1)
       
           
                          
        
               
               
                
        
        
        
        return retVal








#    def performGibbsSampling(self,queryVar,givenVars,numTrials):
#        non_evidence = []
#        Normal = {}
#        Normal["True"] = 0
#        Normal["False"] = 0
#        sample = Sample()
#        for key in self.varMap.keys():
#            if key in givenVars:
#                sample.setAssignment(key,givenVars[key])
#            else:
#                non_evidence.append(key)
#                a = bool(random.getrandbits(1))
#                sample.setAssignment(key,a)
#        for i in range(numTrials):
#            for ne in non_evidence:
#                self.resample(sample,ne)
#                if sample.assignments[queryVar] == True:
#                    Normal["True"] = Normal["True"] + 1
#                else:
#                    Normal["False"] = Normal["False"] + 1
#        retVal = (float)(Normal["True"])/(float)(Normal["True"] + Normal["False"])
#        return retVal
#    
#    def resample(self,sample,var):
#        node = self.varMap[var]
#        p1 = node.getProbability(sample.assignments,True)
#        p2 = node.getProbability(sample.assignments,False)
#        p = 1.0
#        px = 1.0
#        
#        if sample.assignments[var] == True:
#            p = p1
#            px = p2
#        else:
#            p = p2
#            px = p1
#        for c in node.getChildren():
#            p3 = c.getProbability(sample.assignments,sample.assignments[c.getVariable()])
#            p = p * p3
#        sample.setAssignment(node.getVariable(), not sample.assignments[var])
#        for c in node.getChildren():
#            p4 = c.getProbability(sample.assignments,sample.assignments[c.getVariable()])
#            px = px * p4
#        sample.setAssignment(node.getVariable(),not sample.assignments[var])
#        if sample.assignments[var] == True:
#            p = (float)(p)/(float)(p + px)
#        else:
#            p = (float)(px)/(float)(p + px)
#        r = random.uniform(0,1)
#        if r < p:
#            sample.setAssignment(var,True)
#        else:
#            sample.setAssignment(var,False)