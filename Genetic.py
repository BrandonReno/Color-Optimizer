from NeuralNetwork import Network as N
from Neurons import Neuron as NN
import matplotlib.pyplot as plt
import random

#Weights file to be read
WeightFile = "WeightsWrite.txt"
gen = {}


class Gene:
    MutationDecision = False
    MutationRate = .5
    MutationDecay = .5
    generations = 3

    def createDict(self, arrr):
        #dictionary that uses label as key and weights after that
        for arr in arrr:
            GeneAdd = Gene(arr[0:4], arr[4])
            if arr[5] in gen:
                gen[arr[5]].append(GeneAdd)
            else:
                gen[arr[5]] = [GeneAdd]
        return gen
    
    def __init__(self,weights,percent):
        self.weights = weights
        self.percent = percent

    def AdjustMutation(self):
        self.MutationRate = self.MutationRate * self.MutationDecay

    def setWeights(self, weights):
        self.weights = weights
    
    def setMutation(self,tof):
        self.MutationDecision = tof

    def setGenerations(self, Num):
        self.generations = Num

    def setPopSize(self,Size):
        NN.setPopSize(NN, Size)


    def getRandom(self,arrUse):
        randomNum = random.randint(0,len(arrUse) - 1)
        randomNumTwo = random.randint(0,len(arrUse) - 1)
        if (randomNum == randomNumTwo):
            self.getRandom(arrUse)
        return randomNum, randomNumTwo

    def Crossover(self):
        for key in gen:
            arrUse = [val for val in gen[key]]
            for i in range(int(NN.PopulationSize/2)):
                x,y = self.getRandom(arrUse)
                arr1 = arrUse[x]
                arr2 = arrUse[y]
                weightsArr1 = [w for w in arr1.weights]
                weightsArr2 = [w for w in arr2.weights]
                ChildWeights = self.CrossWeights(weightsArr1,weightsArr2)
                Child = Gene(ChildWeights, 20)
                gen[key].append(Child)
                

    def CrossWeights(self, arr1, arr2):
        ChildArr = []
        for i in range(len(arr1)):
            randomChoice = random.randint(0,1)
            if (randomChoice == 1):
                ChildArr.append(arr1[i])
            else:
                ChildArr.append(arr2[i])
        return ChildArr
            
 

    def Mutate(self):
        for key in gen:
            arrUse = [val for val in gen[key]]
            for i in range(int(NN.PopulationSize)):
                Number = random.random()
                arr1 = arrUse[i]
                NewWeights = []
                weightsArr1 = [w for w in arr1.weights]
                if(Number < self.MutationRate):
                    for i in range(len(weightsArr1)):
                        MutateNum = random.randint(0,1)
                        if (MutateNum == 1):
                            NewWeights.append(random.random())
                        else:
                            NewWeights.append(weightsArr1[i])
                    arr1.setWeights(NewWeights)
                else:
                    pass

                    

    def Elitist(self):
        for key in gen:
            arrUse = [val for val in gen[key]]
            arrUse.sort(key=lambda x: float(x.percent))
            for i in range(int(NN.PopulationSize/2)):
                del arrUse[i]
            gen[key] = arrUse

    def GetFitnessData(self):
        n = NN("Red")
        for key in gen:
            arrUse = [val for val in gen[key]]
            for i in range(int(NN.PopulationSize)):
                arr1 = arrUse[i]
                arr1.percent = n.CreateWeights(arr1.weights, key)

    def GenerationLoop(self,NumGens, dict, Mutation):
        for i in range(NumGens):
            self.Elitist()
            self.Crossover()
            if Mutation:
                self.Mutate()
            self.AdjustMutation()
            self.GetFitnessData()

    def run(self):
        self.GenerationLoop(self.generations,self.createDict(N.ReadFile(N,WeightFile)),self.MutationDecision)

    def plotData(self):
        self.run()
        x = [key for key in gen]
        y = []
        for key in gen:
            arrUse = [val for val in gen[key]]
            for i in range(1):
                arr1 = arrUse[NN.PopulationSize-1]
                y.append(arr1.percent)
        fig = plt.figure()
        plt.bar(x,y, color = [color.lower() for color in x])
        fig.suptitle("Generation {}".format(self.generations))
        plt.xlabel('Colors')
        plt.ylabel('Accuracy in Percent')
        plt.show()
        
                    

    def __str__(self):
        return("weights {0} and fitness {1}" .format(self.weights, self.percent))






