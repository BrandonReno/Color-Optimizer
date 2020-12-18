from NeuralNetwork import Network
import math
import random
import numpy as np


class Neuron:
    
    """
    Here you can adjust the values for Learning Rate:LR
    Threshhold Value:Thresh
    Epochs = number of epochs
    You can also enter the files for the program to read in for training and testing data
    """

    TrainingFile = "training.txt"
    TestingFile = "TestReal.txt"
    WeightOutput = "WeightsWrite.txt"
    PopulationSize = 30
    Thresh = 0
    LR = .2
    Epochs = 300
    percenteee = 0

    """ neurons is a list that hold all the neurons in it with there color labels and weights, Error is a list used in testing that 
    gets added to everytime something is not correct and correct is a list that gets added to everytime something coes out correct
    output == correct output, multiple is a list of 1s that is appended to everytime an example makes more than one color fire
    zeroes is a list that is appended a 1 everytime an example doesnt fire for any color
    """
    neurons = []
    error = 0
    correct = 0
 
    def __init__(self,Label):
        #Constant weights to start,every color starts the same
        #Fired: increments based on how many times the neuron fires
        #NoFire: increments based on how many times the neuron does not fire
        #Last weight in Weights is the bias weight
        self.Weights = [.2,.3,.1,.5]
        self.label = Label
        self.Fired = 0
        self.WrongFire = 0
        #FiredCorrectly: List of the examples that cause the neuron to fire correctly
        #FiredShouldntHave: List of examples that cause the neuron to fire when it shouldnt have
        #ShouldHaveDidnt: List of examples that causes the neuron to not fire when it should have
        self.FiredCorrectly = 0

    def resetLists(self):
        self.FiredCorrectly = 0
        self.WrongFire = 0
        self.Fired = 0
 
    def setPopSize(self,size):
        self.PopulationSize = size

    def CreateNPArr(self,FileName):
        #puts into a np array three inputs and then the color output
        Net = Network()
        Inputs = np.array(Net.ReadFile(FileName))
        return Inputs
        

    def GetTargetColor(self,Arr):
        #returns the target color associated with the array
        return Arr[len(Arr)-1]

    def ConvertToIntArr(self,Arr):
        #converts the int numbers from 255 number bases to num between 0 and 1
        val = [int(n)/255 for n in Arr[0:3]]
        #Adding the bias input at the end
        val.append(1)
        return val

    def UpdateWeights(self,Arr, Correct, Actual):
        #updates the weights based on the results of the correct output vs the actual output
        for i in range(len(self.Weights)):
            self.Weights[i] = self.Weights[i] + (self.LR*((Correct - Actual) * Arr[i]))

        
    def MakeNeurons(self):
        #makes all the color neurons and puths them into a list
        n1 = Neuron("Red")
        n2 = Neuron("Blue")
        n3 = Neuron("Green")
        n4 = Neuron("Orange")
        n5 = Neuron("Yellow")
        n6 = Neuron("Purple")
        n7 = Neuron("Pink")
        n8 = Neuron("Brown")
        n9 = Neuron("Gray")
        self.neurons = [n1,n2,n3,n4,n5,n6,n7,n8,n9]

    def GetPrediction(self,Arr):
        #based on the sum of the weights and inputs together it makes a prediction 0 or 1 if the neuron should fire
        total = 0
        for inp,wei in zip(Arr,self.Weights):
            total += inp*wei
        return 1.0 if total >= self.Thresh else 0.0

    def GetCorrectOutput(self,str1, str2):
        #returns 1 if the colors are the same, target and what the neuron is, and 0 if they are different
        return 1.0 if (str1 == str2) else 0.0

    def GetError(self,arr):
        #returns the error percentage
        return ((self.error/(len(arr) * len(self.neurons))) * 100)

    def PrintWeights(self, Filename):
         #Goes through each neuron and prints out the weights that were most successful in a file
        Weights = open(Filename, "a")
        for ne in self.neurons:
            for i in range(len(ne.Weights)):
                Weights.write(str(ne.Weights[i]))
                Weights.write(" ")
            Weights.write(str((ne.FiredCorrectly/ne.Fired)*100))
            Weights.write(" ")
            Weights.write(ne.label)
            Weights.write("\n")
        

    def Train(self,Arr,epoch):
        #goes through each example on each color neuron and trains the weights to be used in testing
        for i in range(epoch):
            #loop through epoch number of times
            for ne in self.neurons:
                #take one of the colors
                for i in range(len(Arr)):
                    #compare it to all the example data
                    RGBArr = Arr[i]
                    RGBVal = self.ConvertToIntArr(RGBArr)
                    CorrectOutput = self.GetCorrectOutput(ne.label, self.GetTargetColor(RGBArr))
                    Output = ne.GetPrediction(RGBVal)
                    ne.UpdateWeights(RGBVal,CorrectOutput, Output)
            random.shuffle(Arr)

    def IncrementFinalPercent(self,Output, CorrectOutput):
        #adds to whichever list if the output is the correct output or if it isnt
        if(Output == CorrectOutput):
            self.correct += 1
        else:
            self.error += 1

        
    def TestTheNN(self,Arr):
        #testing function that prints percent error at the end of it
        #Same function really as train except it does not update weights
            for i in range(len(Arr)):
                for ne in self.neurons:
                    RGBArr = Arr[i]
                    RGBVal = self.ConvertToIntArr(RGBArr)
                    CorrectOutput = self.GetCorrectOutput(ne.label, self.GetTargetColor(RGBArr))
                    Output = ne.GetPrediction(RGBVal)
                    ne.IncrementFires(Output,CorrectOutput)
                    self.IncrementFinalPercent(Output, CorrectOutput)
            Percent = self.GetError(Arr)
            print("ERROR PERCENT: {:.2f}%\n ".format(Percent))

    def TestSpecificColor(self,Arr,WeightsArr, label):
        self.MakeNeurons()
        for ne in self.neurons:
            if (ne.label == label):
                ne.Weights = WeightsArr
                for i in range(len(Arr)):
                        RGBArr = Arr[i]
                        RGBVal = self.ConvertToIntArr(RGBArr)
                        CorrectOutput = self.GetCorrectOutput(ne.label, self.GetTargetColor(RGBArr))
                        Output = ne.GetPrediction(RGBVal)
                        ne.IncrementFires(Output,CorrectOutput)
                return (((ne.FiredCorrectly/ne.Fired)*100))



        

    def PrintStatistics(self):
        #Goes through each neuron and prints out the statistics associated with it
        print("***INDIVIDUAL COLOR STATISTICS***")
        for ne in self.neurons:
            print("{} --- Fired Accurately:{:.2f}%".format(ne.label,(ne.FiredCorrectly/ne.Fired)*100))

    
    def IncrementFires(self,Output, CorrectOutput):
        #function to keep track of if a color fires or not
            if (CorrectOutput == 1):
                if (Output == CorrectOutput):
                    self.FiredCorrectly += 1
                self.Fired += 1



    def TrainTestPrint(self,numIterations):
        for i in range(numIterations):
            n.Train(n.CreateNPArr(n.TrainingFile),n.Epochs,)
            n.TestTheNN(n.CreateNPArr(n.TestingFile))
            n.PrintWeights(n.WeightOutput)
            n.PrintStatistics()
            for neu in self.neurons:
                neu.resetLists()
            self.error = 0

    def CreateWeights(self,arr, label):
        self.MakeNeurons()
        arrint = [float(i) for i in arr]
        for neu in self.neurons:
            if (neu.label == label):
                return neu.TestSpecificColor(neu.CreateNPArr(neu.TestingFile),arrint,label)
            


            
                    
if __name__ == "__main__":
    n = Neuron("Red")
    n.MakeNeurons()
    n.TrainTestPrint(n.PopulationSize)


   
    
    
    
    