
class Network:
    def ReadFile(self,FileName):
            #function used to read the input file and return an array of arrays of the rgb inputs and then the color output
            Map = open(FileName, "r")
            Temp = []
            #Seperate out the information in the file
            with open(FileName) as f:
                for l in Map:
                        Temp.append((l.strip().split(" ")))
            return Temp
