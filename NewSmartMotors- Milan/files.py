import sys
def savetofile(pointstosave): # the points to save should have format of [[light, pot],[light,pot]]
    import os
    if(os.listdir().count('data.py')):
        import data
        datapoints=[]
        del sys.modules["data"]
        import data
        try:
            datapoints=data.points
            datapoints.append(pointstosave)
        except:
            datapoints.append(pointstosave)
        del sys.modules["data"]
        #getting ready to reimporting data file
    else:
        datapoints=[]
        datapoints.append(pointstosave)
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
            display.showmessage("No data saved")
            return([])
    else:
        display.showmessage("No data saved")
        return([])
    
        #also make this go home

