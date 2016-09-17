from PIL import Image
import numpy
import scipy
import math
from scipy.misc import toimage
from scipy.misc import imsave
import cv2
import random

#reading image
i = Image.open('Image_Butterfly.jpg')

(width,height) = i.size

im = numpy.array(Image.open('Image_Butterfly.jpg'))

length=width*height


#creating rgb,xy array to save image metrics
p=numpy.zeros(shape=(length,5), dtype=int)
pixarray=numpy.array(p)


#creating another array for labelling
p=numpy.zeros(shape=(length,5), dtype=int)
prop=numpy.array(p)


#final array for conversion
resultArray=numpy.zeros(shape=(height,width,3), dtype=int)
#insering data into the image metrics array

z=0
for x in range (0,height-1):
    for y in range (0,width-1):
        b,g,r=im[x,y]
        pixarray[z,0]=x
        pixarray[z,1]=y
        pixarray[z,2]=r
        pixarray[z,3]=g
        pixarray[z,4]=b
        z=z+1

#thresholds
hs=120
hr=60
iterValue=10


#list for adding auxiliary data
auxlist =([])

#Mean Shift performaing function
def meanShift(meanArr):
    cmplist=([])
    naList = ([])
    global pixarray
    lengthPixArray = len(pixarray)
  
    #Initializing values 
    if(meanArr=="success"):
        index = random.randint(0,lengthPixArray-1)
        xinit = pixarray[index,0]
        yinit = pixarray[index,1]
        rinit = pixarray[index,2]
        ginit = pixarray[index,3]
        binit = pixarray[index,4]
    else:   
        xinit = meanArr[0]
        yinit = meanArr[1]
        rinit = meanArr[2]
        ginit = meanArr[3]
        binit = meanArr[4]
    
    count=0
    xsum=0
    ysum=0
    rsum=0
    gsum=0
    bsum=0

    #Calculating Euclidian distance and qualifying thresholded values
    for i in range(0, lengthPixArray-1):
        dists = math.sqrt(abs((xinit-pixarray[i,0])*(yinit-pixarray[i,0])+(yinit-pixarray[i,1])*(yinit-pixarray[i,1])))
        distr = math.sqrt(abs((rinit-pixarray[i,2])*(rinit-pixarray[i,2])+
            (ginit-pixarray[i,3])*(ginit-pixarray[i,3])+(binit-pixarray[i,4])*(binit-pixarray[i,4])))
        if(dists<hs and distr<hr):
            cmplist.append(pixarray[i])
            (xsum)=(xsum)+pixarray[i,0]
            (ysum)=(ysum)+pixarray[i,1]
            (rsum)=(rsum)+pixarray[i,2]
            (gsum)=(gsum)+pixarray[i,3]
            (bsum)=(bsum)+pixarray[i,4]
            count=count+1
        else:
            naList.append(i)
    if(count==0):
        return "success"
        
    #Calculating mean     
    xmean=float(xsum/count)
    ymean=float(ysum/count)
    rmean=float(rsum/count)
    gmean=float(gsum/count)
    bmean=float(bsum/count)
    
    meandistance = math.sqrt(abs((rmean-rinit)*(rmean-rinit)+(gmean-ginit)*(gmean-ginit)+(bmean-binit)*(bmean-binit)))
    
    #If new and original mean is less than iter
    if(meandistance<iterValue):
        for i in range(0,len(cmplist)-1):
            cmplist[i][2]=int(rmean)
            cmplist[i][3]=int(gmean)
            cmplist[i][4]=int(bmean)
            auxlist.append(cmplist[i])
        
        p=numpy.zeros(shape=(len(naList),6), dtype=int)
        tempArray=numpy.array(p)
        iterIndex=0
        for j in range(0,len(naList)-1):
            tempArray[iterIndex][0]=pixarray[naList[j]][0]
            tempArray[iterIndex][1]=pixarray[naList[j]][1]
            tempArray[iterIndex][2]=pixarray[naList[j]][2]
            tempArray[iterIndex][3]=pixarray[naList[j]][3]
            tempArray[iterIndex][4]=pixarray[naList[j]][4]
            iterIndex=iterIndex+1
        pixarray=tempArray
    
    #If new and original mean is less than iter          
    else:
        arr = numpy.array([xmean,ymean,rmean,gmean,bmean])
        return arr
        
    
    return "success"
    
# calling meanShift ()  function
result="success"
while(len(pixarray)>0):
    print(len(pixarray),"is length")
    result = meanShift(result)

resultArray=numpy.zeros(shape=(height,width,3), dtype=int)

#Displaying final reuslt
for a in range(0,len(auxlist)-1):
    resultArray[auxlist[a][0]][auxlist[a][1]] = auxlist[a][2],auxlist[a][3],auxlist[a][4] 
    
cv2.imwrite("Image_Butterfly_Output.jpg",resultArray)