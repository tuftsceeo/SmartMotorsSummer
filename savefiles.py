import sys

# appends to the file 
def savetofile(pointtosave): # the points to save should have format of [light, mot]
    import os
    if(os.listdir().count('data.py')):
        import data
        datapoints=[]
        del sys.modules["data"]
        import data
        try:
            datapoints=data.points
            datapoints.append(pointtosave)
        except:
            datapoints.append(pointtosave)
        del sys.modules["data"]
        #getting ready to reimporting data file
    else:
        datapoints=[]
        datapoints.append(pointtosave)
        print("new file")
    #writing files to the data.py
    
    f=open("data.py","w")
    f.write("points="+str(datapoints)+"\r\n")
    f.close()

def replacefile(pointstosave):
    import os
    if(os.listdir().count('data.py')):
        f=open("data.py","w")
        f.write("points="+str(pointstosave)+"\r\n")
        f.close()
    else:
        return 0

    
def readfile():
    import os
    if(os.listdir().count('data.py')):
        import data
        if(data.points):
            return(data.points)
        else:
            #display.showmessage("No data saved")
            print("no points")
            return([])
    else:
        #display.showmessage("No data saved")
        print("data does not exist yet")
        return([])
    
        #also make this go home



