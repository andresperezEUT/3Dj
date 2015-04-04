# -*- coding: utf-8 -*-
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Copyright ANDRÉS PÉREZ LÓPEZ, January 2014
contact@andresperezlopez.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; withot even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            AMBISONICS CSV READER

Provides utility functions for reading and plotting ambisonics channel values

- Open the text file defined in filepath 
  structure:
      [azimuth/elevation] , ch0 , ch1 , ...  , chN
  as defined in AmbEncTest.scd
  
- Plot differences between python implementation as defined in plotSphericalHarmonics.py
  and scsynth values obtained from the textfile
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import csv
import matplotlib.pyplot as plt
import numpy as np
import plotSphericalHarmonics as psh

def ambiErrorAzi(filepath):
    
    azimuth=[];
    azimuthString=[] # empty list
    numChannels=16;
    amb=[];
    ambString=[] # empty list
    f3=[];
    
    """""""""""""""""""""""""""""
    load file values into python
    """""""""""""""""""""""""""""

    
    with open(filePath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
#            azimuth in first row
            azimuthString.append(row[0])
#            ambisonic channels in enxt 16 rows 
            ambString.append(row[1:numChannels+1])

    """""""""""""""""""""""""""""
    some casting and array arrangement
    """""""""""""""""""""""""""""
    #cast amb into float
    array=[]    
    for i in ambString:
        for j in i:
            array.append(float(j))
        amb.append(array)
        array=[]
    # traspose in order to plot
    amb=np.asarray(amb)
    amb=amb.T
    
    # cast azimuth into floats
    for i in np.arange(len(azimuthString)):
        azimuth.append(float(azimuthString[i]))
        
    # cast values into floats
    for a in azimuth:
        f3.append(psh.AmbisonicsThirdOrder(0,float(a)))
    # traspose in order to plot
    f3=np.asarray(f3)
    f3=f3.T
    
    """""""""""""""""""""""""""""
    plot supercollider values versus python simulated values 
    """""""""""""""""""""""""""""

    plt.figure()
    for n in np.arange(numChannels): 
        plt.subplot(4,4,n+1)
        # plot levels
#        plt.plot(azimuth,f3[n],'b')
#        plt.plot(azimuth,amb[n],'k')
        # errors
        plt.plot(azimuth,abs(np.subtract(f3[n],amb[n])),'r')

    return   
    
def ambiErrorEle(filepath):
    
    elevation=[];
    elevationString=[] # empty list
    numChannels=16;
    amb=[];
    ambString=[] # empty list
    f3=[];
    
    """""""""""""""""""""""""""""
    load file values into python
    """""""""""""""""""""""""""""
    
    with open(filePath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
#            elevation in first row
            elevationString.append(row[0])
#            ambisonic channels in enxt 16 rows 
            ambString.append(row[1:numChannels+1])

    """""""""""""""""""""""""""""
    some casting and array arrangement
    """""""""""""""""""""""""""""
    #cast amb into float
    array=[]    
    for i in ambString:
        for j in i:
            array.append(float(j))
        amb.append(array)
        array=[]
    # traspose in order to plot
    amb=np.asarray(amb)
    amb=amb.T
    
    # cast elevation into floats
    for i in np.arange(len(elevationString)):
        elevation.append(float(elevationString[i]))
        
    # cast values into floats
    for a in elevation:
        f3.append(psh.AmbisonicsThirdOrder(float(a),0))
    # traspose in order to plot
    f3=np.asarray(f3)
    f3=f3.T

    """""""""""""""""""""""""""""
    plot supercollider values versus python simulated values 
    """""""""""""""""""""""""""""
    plt.figure()
    for n in np.arange(numChannels): 
        plt.subplot(4,4,n+1)

        # plot levels
#        plt.plot(elevation,f3[n],'b')
#        plt.plot(elevation,amb[n],'k')
        # errors
        plt.plot(elevation,abs(np.subtract(f3[n],amb[n])),'r')

    return   

