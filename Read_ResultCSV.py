
# coding: utf-8

# Implrt the required components

# In[21]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from  tkinter import *
from tkinter import filedialog


# Define some global value

# In[22]:


startMeasuredData = "Creation Time"
#startMeasuredDefectData = 


# Define the fuction which will give the line idexes

# In[23]:


def check(strToFind):
    with open(csvPath) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    #content = [x.strip() for x in content] # to ignor the \n
    indx=0
    a=np.array([])
    for line in content:
        indx+=1
        if line.split(';').count(strToFind)==1:
            a=np.append(a,indx)
            #print(a)
    return np.uint16(a) 


# Define the Path of the CSV file

# In[24]:


def openFileDia():
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "D:/NeruralNetworks/Jupyter/learn/TestData",title = "choose your file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    print (root.filename)
    root.withdraw()
    return root.filename
csvPath = openFileDia()
#csvPath="d:\\NeruralNetworks\\Jupyter\\learn\\TestData\\PLS.csv"


# In[ ]:





# Load the required data

# In[25]:


indx = check(startMeasuredData)
df = pd.read_csv(csvPath,';',skiprows=indx[1]-1,nrows=(indx[2]-indx[1]-2),low_memory=False)


# In[26]:


tt=df['Creation Time']


# Display Data

# In[27]:


LP=df['Laser Power Mean']
plt.plot(LP)
#plt.xticks
plt.ylabel('some numbers')
plt.show()


# In[ ]:





# In[75]:




