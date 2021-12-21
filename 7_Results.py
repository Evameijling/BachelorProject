#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 12:37:28 2021

@author: evagmelichmeijling
"""
import numpy as np
from astropy.io import fits
from astropy.table import QTable
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from photutils import DAOStarFinder, CircularAperture, CircularAnnulus
from datetime import datetime
from photutils.datasets import make_100gaussians_image
from photutils import aperture_photometry
from photutils.background import Background2D, MedianBackground
from astropy.stats import sigma_clipped_stats, SigmaClip, sigma_clip
from scipy import stats
import glob
import csv
import pandas as pd
from pandas import read_csv
from matplotlib import pyplot
from scipy.optimize import curve_fit
import math

start = datetime.now()

DOUBLECLUSTERTXT = open('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/AnalysisResults.txt', 'a')
DOUBLECLUSTERTXT.write("7_RESULTS:\n")

DoubleCluster = pd.read_csv('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/6_Stardistribution/FinalDoubleCluster.csv')

#Define variables for simplicity
m_R = DoubleCluster['m_R']
m_V = DoubleCluster['m_V']
m_B = DoubleCluster['m_B']
Rerror = DoubleCluster['Rerror']
Verror = DoubleCluster['Verror']
Berror = DoubleCluster['Berror']

# # Scatter plots B-V vs V (different color for each of the two clusters) & Gaia data within range cluster
# for i in range(len(DoubleCluster)):
#     if DoubleCluster['SNR_B'][i] > 3:
#         if 'NGC869' in DoubleCluster['id'][i]:
#             NGC869_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='skyblue')
#             plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='skyblue',  elinewidth=0.5)
#             if 2000 < DoubleCluster['disttoearth'][i] < 3000:
#                 gaia_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='darkblue')
#         if 'NGC884' in DoubleCluster['id'][i]:
#             NGC884_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='mediumpurple')
#             plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='mediumpurple',  elinewidth=0.5)
#             if 2000 < DoubleCluster['disttoearth'][i] < 3000:
#                 gaia_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='indigo')
# plt.xlabel("B-V")
# plt.ylabel("V")
# plt.title('Color-magnitude diagram Double Cluster B-V')
# plt.xlim(-0.5, 2.5)
# plt.ylim(6, 17)
# plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
# plt.gca().invert_yaxis()
# plt.show()

for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        if 'NGC869' in DoubleCluster['id'][i]:
            NGC869_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='skyblue')
            if 2000 < DoubleCluster['disttoearth'][i] < 3000:
                gaia_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='darkblue')
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster B-V for NGC869 with Gaia Data within cluster range (2000-3000 parsec)')
plt.xlim(-0.5, 2.5)
plt.ylim(6, 17)
# plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        if 'NGC869' in DoubleCluster['id'][i]:
            NGC869_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='skyblue')
            if 2200 < DoubleCluster['disttoearth'][i] < 2800:
                gaia_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='darkblue')
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster B-V for NGC869 with Gaia Data within cluster range (2200-2800 parsec)')
plt.xlim(-0.5, 2.5)
plt.ylim(6, 17)
# plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        if 'NGC884' in DoubleCluster['id'][i]:
            NGC884_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='mediumpurple')
            if 2000 < DoubleCluster['disttoearth'][i] < 3000:
                gaia_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='indigo')
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster B-V for NGC884 with Gaia Data within cluster range (2000-3000 parsec)')
plt.xlim(-0.5, 2.5)
plt.ylim(6, 17)
# plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        if 'NGC884' in DoubleCluster['id'][i]:
            NGC884_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='mediumpurple')
            if 2200 < DoubleCluster['disttoearth'][i] < 2800:
                gaia_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='indigo')
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster B-V for NGC884 with Gaia Data within cluster range (2200-2800 parsec)')
plt.xlim(-0.5, 2.5)
plt.ylim(6, 17)
# plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

######test
for i in range(len(DoubleCluster)):
    plt.scatter(DoubleCluster['RA'][i], DoubleCluster['DEC'][i], color='plum', s=1.5, marker="*")
    if DoubleCluster['parallax'][i] > -0.003:
        plt.scatter(DoubleCluster['RA'][i], DoubleCluster['DEC'][i], color='indigo', s=1.5, marker="*")
plt.show()

#Scatter plot of found Gaia parallax points
for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        doublecluster_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='plum')
        if DoubleCluster['parallax'][i] > -0.003:
            gaia_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='indigo')
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster')
plt.xlim(-0.5, 2.5)
plt.ylim(6, 17)
plt.legend((doublecluster_scatter, gaia_scatter), ('Double Cluster', 'Gaia data'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

#Scatter plot B-V vs V (different color for each of the two clusters)
for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        if 'NGC869' in DoubleCluster['id'][i]:
            NGC869_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='darkblue')
            plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='darkblue',  elinewidth=0.5)
        if 'NGC884' in DoubleCluster['id'][i]:
            NGC884_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='plum')
            plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='plum',  elinewidth=0.5)    
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster B-V')
plt.xlim(-0.5, 2.5)
plt.ylim(6, 17)
plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

#Scatter plot V-R vs V (different color for each of the two clusters)
for i in range(len(DoubleCluster)):
    if 'NGC869' in DoubleCluster['id'][i]:
        NGC869_scatter = plt.scatter(m_V[i]-m_R[i], m_V[i], s=0.2, color='darkblue')
        plt.errorbar(m_V[i]-m_R[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Rerror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='darkblue',  elinewidth=0.5)   
    if 'NGC884' in DoubleCluster['id'][i]:
        NGC884_scatter = plt.scatter(m_V[i]-m_R[i], m_V[i], s=0.2, color='plum')
        plt.errorbar(m_V[i]-m_R[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Rerror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='plum',  elinewidth=0.5)   
plt.xlabel("V-R")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster V-R')
plt.xlim(-0.5, 2)
plt.ylim(6, 19)
plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

#Histogram of magnitude distribution per filter
plt.hist(m_R, bins=100)
plt.xlabel("magnitude")
plt.ylabel("amount of stars")
plt.title('R Magnitude distribution')
plt.show()

plt.hist(m_V, bins=100)
plt.xlabel("magnitude")
plt.ylabel("amount of stars")
plt.title('V Magnitude distribution')
plt.show()

m_B_SNR3 = []
for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        m_B_SNR3.append(m_B[i])
plt.hist(m_B_SNR3, bins=100)
plt.xlabel("magnitude")
plt.ylabel("amount of stars")
plt.title('B Magnitude distribution')
plt.show()

#Scatter plot B-V vs V for all stars within 0.1 degree from center
for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        if DoubleCluster['disttocenter'][i] < 0.1:
            if 'NGC869' in DoubleCluster['id'][i]:
                NGC869_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='darkblue', label='NGC869')
                plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='darkblue',  elinewidth=0.5)
            if 'NGC884' in DoubleCluster['id'][i]:
                NGC884_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='plum', label='NGC884')
                plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='plum',  elinewidth=0.5)    
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster disttocenter < 0.1')
plt.xlim(0.0, 2)
plt.ylim(8, 16)
plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

#Scatter plot B-V vs V for all stars within in outer radius from center
for i in range(len(DoubleCluster)):
    if DoubleCluster['SNR_B'][i] > 3:
        if DoubleCluster['disttocenter'][i] > 0.5:
            if 'NGC869' in DoubleCluster['id'][i]:
                NGC869_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='darkblue', label='NGC869')
                plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='darkblue',  elinewidth=0.5)
            if 'NGC884' in DoubleCluster['id'][i]:
                NGC884_scatter = plt.scatter(m_B[i]-m_V[i], m_V[i], s=0.2, color='plum', label='NGC884')
                plt.errorbar(m_B[i]-m_V[i], m_V[i], xerr=np.sqrt(Verror[i]**2+Berror[i]**2), yerr=Verror[i], fmt=',', ecolor='gray', color='plum',  elinewidth=0.5)    
plt.xlabel("B-V")
plt.ylabel("V")
plt.title('Color-magnitude diagram Double Cluster disttocenter > 0.5')
plt.xlim(-0.5, 2.5)
plt.ylim(6, 17)
plt.legend((NGC869_scatter, NGC884_scatter), ('NGC869', 'NGC884'), markerscale=5, fontsize=8)
plt.gca().invert_yaxis()
plt.show()

#############################################################NGC869 FIT##############################################################

#Read in DoubleCluster data
DoubleCluster = pd.read_csv('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/6_Stardistribution/FinalDoubleCluster.csv')
     
#Create Qtable from Double Cluster Data
m_R = []
m_V = []
m_B = []
Rerror = []
Verror = []
Berror = []
B_V = []
B_V_err = []

maxdisttocenter = 0.25

#Define variables for simplicity
for i in range(len(DoubleCluster)):
    if 'NGC869' in DoubleCluster['id'][i]:
        if DoubleCluster['disttocenter'][i] < maxdisttocenter:
           m_R.append(DoubleCluster['m_R'][i]) 
           m_V.append(DoubleCluster['m_V'][i])
           m_B.append(DoubleCluster['m_B'][i])
           Rerror.append(DoubleCluster['Rerror'][i]) 
           Verror.append(DoubleCluster['Verror'][i])
           Berror.append(DoubleCluster['Berror'][i])
           B_V.append(DoubleCluster['m_B'][i]-DoubleCluster['m_V'][i])
           B_V_err.append(np.sqrt(DoubleCluster['Verror'][i]**2+DoubleCluster['Berror'][i]**2))
       
Fitdata = QTable([m_R, m_V, m_B, Rerror, Verror, Berror, B_V, B_V_err],
                   names=('m_R', 'm_V', 'm_B', 'Rerror', 'Verror', 'Berror', 'B_V', 'B_V_err'))

print(len(Fitdata['m_R']))

#Scatter plot apparent B-V vs V magnitudes
plt.scatter(Fitdata['B_V'], Fitdata['m_V'], s=1, color='indigo')
plt.errorbar(Fitdata['B_V'], Fitdata['m_V'] , xerr=Fitdata['B_V_err'], yerr=Fitdata['Verror'], fmt=',', ecolor='gray', color='indigo',  elinewidth=0.5)
plt.xlabel("B-V")
plt.ylabel("V")
plt.title("Colour Magntide Diagram Double Cluster")
plt.xlim(0.0, 2)
plt.ylim(7, 19)
plt.gca().invert_yaxis()
plt.show()

#Load isochrone data
loga,logl,logte,mass, M_B, M_V = np.loadtxt('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/7_Results/Isochrones/Isoc_z0.019.txt',usecols=(0,3,4,2,8,9),unpack =True)

#Plot isochrone
w7 = np.where(loga == 7) #10^7 years / 10 million years  
plt.figure(figsize=[8,5])
plt.plot(M_B[w7] - M_V[w7], M_V[w7],label='4 Myr')
plt.xlabel("Absolute B-V")
plt.ylabel("Absolute V")
plt.title("Isochrone")
plt.gca().invert_yaxis()
plt.show()

#Create Qtables from isochrone data 
Isochrone = QTable([M_B[w7] - M_V[w7], M_V[w7], mass[w7]],
                   names=('B-V', 'V', 'massa'))

Isochrone2 = QTable([M_B[w7] - M_V[w7], M_V[w7], mass[w7]],
                   names=('B-V', 'V', 'massa'))

#Filter isochrones to obtain Main Sequence
filt = []
index = 0
for star in Isochrone:
    if star['massa'] > 6:
        filt.append(index)
    index = index + 1
Isochrone.remove_rows(filt)

filt = []
index = 0
for star in Isochrone2:
    if star['massa'] > 6:
        filt.append(index)
    elif star['massa'] < 1:
        filt.append(index)
    index = index + 1
Isochrone2.remove_rows(filt)

# #########DISTANCE GUESS TO FIT ISOCHRONE#######
# #Distance to cluster in parsec
# d = 2700

# #Color excess (E(B-V)) specific for Double Cluster (dependent on sight of view)
# #|B-V| ('intrinsieke waarde') = (B-V)obs - E(B-V)
# color_excess = 0.55 

# #Absortion of V (3.2 = ratio of redenning & attenuation magnitude)
# Av = 3.2*color_excess #3.2 standaard deel vd formule (ratio Ab en Av)

# #(B-V) (reddening) = E(B-V) (color_excess, =0.55) + (B-V)0 (=Isochrone)
# #Reddening = color_excess + Isochrone2['B-V']
# #Calculate new B-V value taking reddening into considertion
# Isochrone2['B-V'] = color_excess + Isochrone2['B-V']

# #Calculate delta M (distance modulus)
# delta_m = 5 * np.log10(d) - 5 + Av

# #Shift data depending on distance modulus
# Isochrone2['V'] = Isochrone2['V'] + delta_m

# #Plot untouched Isochrone and shifted Isochrone on scatter plot of data 
# plt.figure(figsize=[8,5])
# plt.scatter(Fitdata['B_V'], Fitdata['m_V'], s=1, color='indigo')
# plt.plot(Isochrone['B-V'], Isochrone['V'], label='Isochrone1')
# plt.plot(Isochrone2['B-V'], Isochrone2['V'], label='Isochrone2')
# plt.gca().invert_yaxis()
# plt.legend()
# plt.xlabel('B-V')
# plt.ylabel('V')
# plt.title("Data with Isochrone (manually fit)")
# plt.show()

#Plot Isochrone2 (original place) and data 
plt.figure(figsize=[8,5])
plt.scatter(Fitdata['m_V'], Fitdata['B_V'], s=1, color='indigo')
# plt.plot(Isochrone['V'], Isochrone['B-V'], label='Isochrone1')
# plt.plot(Isochrone2['V'], Isochrone2['B-V'], label='Isochrone2')

#Determine sumofsquares for multiple values of d
dist = []
sumofsquares = []
for d in range(1000, 2800, 5):
    tempB_V = []
    tempV = []
    color_excess = 0.55 
    Av = 3.2*color_excess 
    tempB_V = Isochrone2['B-V'] + color_excess 
    delta_m = 5 * np.log10(d) - 5 + Av
    tempV  = Isochrone2['V'] + delta_m
    
    fit = np.polynomial.polynomial.polyfit(tempV, tempB_V, 5)
    
    x_fit = []
    y_fit = []
    for x in tempV:
        y = 0
        # Calculate y_coordinate
        for n in range(len(fit)):
            y += fit[n] * (x)**n       
        # Save coordinates
        x_fit.append(x)
        y_fit.append(y)
    
    #Plot fitted isochrone for d value of loop
    plt.plot(x_fit, y_fit, label=f"{d}")
    
    #Determine distance from data point to fit 
    model = []
    error = []
    index = 0
    for x in Fitdata['m_V']:
        if 12 < x < 14:
            fitfunc = 0
            for n in range(len(fit)):
                fitfunc += fit[n] * (x)**n   
            error.append(Fitdata['Verror'][index])
            model.append((((y-fitfunc)**2)/((Fitdata['Verror'][index])**2))/len(Fitdata))
            index = index + 1
    
    sumofsquares.append(np.sum(model)) #deze wil je zo klein mogelijk
    dist.append(d)

plt.legend()
plt.xlabel('V')
plt.ylabel('B-V')
# plt.xlim(5, 20)
# plt.ylim(-1.5, 2)
plt.gca().invert_yaxis()
plt.title("Isochrone fit through data")
plt.show()

#Plot the sumofsquare value agains distance to find minimum
plt.figure(figsize = (20,16))
plt.scatter(dist, sumofsquares)
plt.title("Isochrone fitting for distance")
plt.xlabel('distance')
plt.ylabel('sumofsquares')
plt.legend()
plt.show()

DCdistance = dist[np.argmin(sumofsquares)]

print('found distance', DCdistance)

min_reduced_chi_2 = np.min(sumofsquares)

lstx = []
for i in range(len(sumofsquares)):
    if sumofsquares[i] < (min_reduced_chi_2+1):
        lstx.append(dist[i])
        
lower_errbound = np.min(lstx)
upper_errbound = np.max(lstx)

lower_err = dist[np.argmin(sumofsquares)] - lower_errbound
upper_err = upper_errbound - dist[np.argmin(sumofsquares)]  

VARIABLEPY = open('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/ResultsDC.py', 'w')
VARIABLEPY.write(f"DCdistance_NGC869 = {DCdistance}\n")
VARIABLEPY.write(f"lower_err_NGC869 = {lower_err}\n")
VARIABLEPY.write(f"upper_err_NGC869 = {upper_err}\n")
VARIABLEPY.close()

DOUBLECLUSTERTXT.write(f"Max distance from center for stars: {maxdisttocenter}\n") 
DOUBLECLUSTERTXT.write("Isochrone Metallicity: 0.019\n") 
DOUBLECLUSTERTXT.write(f"Color Excess value: {color_excess}\n") 
DOUBLECLUSTERTXT.write(f"Found distance for NGC869: {DCdistance} parsec + {upper_err} - {lower_err}\n") 

print('distance found:', DCdistance, "parsec", "+", upper_err, "-", lower_err)
# d = 2640 pc ^+... pijlje beneden _....

# M = 5 - 5logd - Av + m
M_V = 5 - 5*np.log10(DCdistance) - Av + Fitdata['m_V']

#(B-V) (reddening) = E(B-V) (color_excess, =0.55) + (B-V)0 (=Isochrone)
B_V_0 = Fitdata['B_V'] - color_excess

plt.scatter(B_V_0, M_V, s=1, color='indigo')

loga,logl,logte,mass, M_B, M_V = np.loadtxt('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/7_Results/Isochrones/Isoc_z0.019.txt',usecols=(0,3,4,2,8,9),unpack =True)

ages = np.unique(loga)
# for age in [6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8]:
for age in [7.4]:
# for age in ages[10:20]:
    wage = 'w{}'.format(age)
    wages = np.where(loga == age)
    
    M_B_Vlst = []
    M_Vlst = []
    for i in wages:
        M_B_Vlst.append(M_B[i] - M_V[i])
        M_Vlst.append(M_V[i])    

    plt.plot(M_B_Vlst[0], M_Vlst[0], label=age)  

plt.xlabel("B-V0")
plt.ylabel("V0")
plt.title("Isochrone Double Cluster")
# plt.xlim(-0.3, 0.1)
plt.ylim(-7, 5)
plt.gca().invert_yaxis()
plt.legend()
plt.show()



#############################################################NGC884 FIT##############################################################

#Read in DoubleCluster data
DoubleCluster = pd.read_csv('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/6_Stardistribution/FinalDoubleCluster.csv')
     
#Create Qtable from Double Cluster Data
m_R = []
m_V = []
m_B = []
Rerror = []
Verror = []
Berror = []
B_V = []
B_V_err = []

maxdisttocenter = 0.25

#Define variables for simplicity
for i in range(len(DoubleCluster)):
    if 'NGC884' in DoubleCluster['id'][i]:
        if DoubleCluster['disttocenter'][i] < maxdisttocenter:
           m_R.append(DoubleCluster['m_R'][i]) 
           m_V.append(DoubleCluster['m_V'][i])
           m_B.append(DoubleCluster['m_B'][i])
           Rerror.append(DoubleCluster['Rerror'][i]) 
           Verror.append(DoubleCluster['Verror'][i])
           Berror.append(DoubleCluster['Berror'][i])
           B_V.append(DoubleCluster['m_B'][i]-DoubleCluster['m_V'][i])
           B_V_err.append(np.sqrt(DoubleCluster['Verror'][i]**2+DoubleCluster['Berror'][i]**2))
       
Fitdata = QTable([m_R, m_V, m_B, Rerror, Verror, Berror, B_V, B_V_err],
                   names=('m_R', 'm_V', 'm_B', 'Rerror', 'Verror', 'Berror', 'B_V', 'B_V_err'))

print(len(Fitdata['m_R']))

#Scatter plot apparent B-V vs V magnitudes
plt.scatter(Fitdata['B_V'], Fitdata['m_V'], s=1, color='indigo')
plt.errorbar(Fitdata['B_V'], Fitdata['m_V'] , xerr=Fitdata['B_V_err'], yerr=Fitdata['Verror'], fmt=',', ecolor='gray', color='indigo',  elinewidth=0.5)
plt.xlabel("B-V")
plt.ylabel("V")
plt.title("Colour Magntide Diagram Double Cluster")
plt.xlim(0.0, 2)
plt.ylim(7, 19)
plt.gca().invert_yaxis()
plt.show()

#Load isochrone data
loga,logl,logte,mass, M_B, M_V = np.loadtxt('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/7_Results/Isochrones/Isoc_z0.019.txt',usecols=(0,3,4,2,8,9),unpack =True)

#Plot isochrone
w7 = np.where(loga == 7) #10^7 years / 10 million years  
plt.figure(figsize=[8,5])
plt.plot(M_B[w7] - M_V[w7], M_V[w7],label='4 Myr')
plt.xlabel("Absolute B-V")
plt.ylabel("Absolute V")
plt.title("Isochrone")
plt.gca().invert_yaxis()
plt.show()

#Create Qtables from isochrone data 
Isochrone = QTable([M_B[w7] - M_V[w7], M_V[w7], mass[w7]],
                   names=('B-V', 'V', 'massa'))

Isochrone2 = QTable([M_B[w7] - M_V[w7], M_V[w7], mass[w7]],
                   names=('B-V', 'V', 'massa'))

#Filter isochrones to obtain Main Sequence
filt = []
index = 0
for star in Isochrone:
    if star['massa'] > 6:
        filt.append(index)
    index = index + 1
Isochrone.remove_rows(filt)

filt = []
index = 0
for star in Isochrone2:
    if star['massa'] > 6:
        filt.append(index)
    elif star['massa'] < 1:
        filt.append(index)
    index = index + 1
Isochrone2.remove_rows(filt)

# #########DISTANCE GUESS TO FIT ISOCHRONE#######
# #Distance to cluster in parsec
# d = 2700

# #Color excess (E(B-V)) specific for Double Cluster (dependent on sight of view)
# #|B-V| ('intrinsieke waarde') = (B-V)obs - E(B-V)
# color_excess = 0.55 

# #Absortion of V (3.2 = ratio of redenning & attenuation magnitude)
# Av = 3.2*color_excess #3.2 standaard deel vd formule (ratio Ab en Av)

# #(B-V) (reddening) = E(B-V) (color_excess, =0.55) + (B-V)0 (=Isochrone)
# #Reddening = color_excess + Isochrone2['B-V']
# #Calculate new B-V value taking reddening into considertion
# Isochrone2['B-V'] = color_excess + Isochrone2['B-V']

# #Calculate delta M (distance modulus)
# delta_m = 5 * np.log10(d) - 5 + Av

# #Shift data depending on distance modulus
# Isochrone2['V'] = Isochrone2['V'] + delta_m

# #Plot untouched Isochrone and shifted Isochrone on scatter plot of data 
# plt.figure(figsize=[8,5])
# plt.scatter(Fitdata['B_V'], Fitdata['m_V'], s=1, color='indigo')
# plt.plot(Isochrone['B-V'], Isochrone['V'], label='Isochrone1')
# plt.plot(Isochrone2['B-V'], Isochrone2['V'], label='Isochrone2')
# plt.gca().invert_yaxis()
# plt.legend()
# plt.xlabel('B-V')
# plt.ylabel('V')
# plt.title("Data with Isochrone (manually fit)")
# plt.show()

#Plot Isochrone2 (original place) and data 
plt.figure(figsize=[8,5])
plt.scatter(Fitdata['m_V'], Fitdata['B_V'], s=1, color='indigo')
# plt.plot(Isochrone['V'], Isochrone['B-V'], label='Isochrone1')
# plt.plot(Isochrone2['V'], Isochrone2['B-V'], label='Isochrone2')

#Determine sumofsquares for multiple values of d
dist = []
sumofsquares = []
for d in range(1000, 2800, 5):
    tempB_V = []
    tempV = []
    color_excess = 0.55 
    Av = 3.2*color_excess 
    tempB_V = Isochrone2['B-V'] + color_excess 
    delta_m = 5 * np.log10(d) - 5 + Av
    tempV  = Isochrone2['V'] + delta_m
    
    fit = np.polynomial.polynomial.polyfit(tempV, tempB_V, 5)
    
    x_fit = []
    y_fit = []
    for x in tempV:
        y = 0
        # Calculate y_coordinate
        for n in range(len(fit)):
            y += fit[n] * (x)**n       
        # Save coordinates
        x_fit.append(x)
        y_fit.append(y)
    
    #Plot fitted isochrone for d value of loop
    plt.plot(x_fit, y_fit, label=f"{d}")
    
    #Determine distance from data point to fit 
    model = []
    error = []
    index = 0
    for x in Fitdata['m_V']:
        if 12 < x < 14:
            fitfunc = 0
            for n in range(len(fit)):
                fitfunc += fit[n] * (x)**n   
            error.append(Fitdata['Verror'][index])
            model.append((((y-fitfunc)**2)/((Fitdata['Verror'][index])**2))/len(Fitdata))
            index = index + 1
    
    sumofsquares.append(np.sum(model)) #deze wil je zo klein mogelijk
    dist.append(d)

plt.legend()
plt.xlabel('V')
plt.ylabel('B-V')
# plt.xlim(5, 20)
# plt.ylim(-1.5, 2)
plt.gca().invert_yaxis()
plt.title("Isochrone fit through data")
plt.show()

#Plot the sumofsquare value agains distance to find minimum
plt.figure(figsize = (20,16))
plt.scatter(dist, sumofsquares)
plt.title("Isochrone fitting for distance")
plt.xlabel('distance')
plt.ylabel('sumofsquares')
plt.legend()
plt.show()

DCdistance = dist[np.argmin(sumofsquares)]

print('found distance', DCdistance)

min_reduced_chi_2 = np.min(sumofsquares)

lstx = []
for i in range(len(sumofsquares)):
    if sumofsquares[i] < (min_reduced_chi_2+1):
        lstx.append(dist[i])
        
lower_errbound = np.min(lstx)
upper_errbound = np.max(lstx)

lower_err = dist[np.argmin(sumofsquares)] - lower_errbound
upper_err = upper_errbound - dist[np.argmin(sumofsquares)]  

VARIABLEPY = open('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/ResultsDC.py', 'a')
VARIABLEPY.write(f"DCdistance_NGC884 = {DCdistance}\n")
VARIABLEPY.write(f"lower_err_NGC884 = {lower_err}\n")
VARIABLEPY.write(f"upper_err_NGC884 = {upper_err}\n")
VARIABLEPY.close()

DOUBLECLUSTERTXT.write(f"Found distance for NGC884: {DCdistance} parsec + {upper_err} - {lower_err}\n") 

print('distance found:', DCdistance, "parsec", "+", upper_err, "-", lower_err)
# d = 2640 pc ^+... pijlje beneden _....

# M = 5 - 5logd - Av + m
M_V = 5 - 5*np.log10(DCdistance) - Av + Fitdata['m_V']

#(B-V) (reddening) = E(B-V) (color_excess, =0.55) + (B-V)0 (=Isochrone)
B_V_0 = Fitdata['B_V'] - color_excess

plt.scatter(B_V_0, M_V, s=1, color='indigo')

loga,logl,logte,mass, M_B, M_V = np.loadtxt('/Users/evagmelichmeijling/OneDrive/Capstone/BachelorProjectProgram/7_Results/Isochrones/Isoc_z0.019.txt',usecols=(0,3,4,2,8,9),unpack =True)

ages = np.unique(loga)
# for age in [6.6, 7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8]:
for age in [7.4]:
# for age in ages[10:20]:
    wage = 'w{}'.format(age)
    wages = np.where(loga == age)
    
    M_B_Vlst = []
    M_Vlst = []
    for i in wages:
        M_B_Vlst.append(M_B[i] - M_V[i])
        M_Vlst.append(M_V[i])    

    plt.plot(M_B_Vlst[0], M_Vlst[0], label=age)  

plt.xlabel("B-V0")
plt.ylabel("V0")
plt.title("Isochrone Double Cluster")
# plt.xlim(-0.3, 0.1)
plt.ylim(-7, 5)
plt.gca().invert_yaxis()
plt.legend()
plt.show()

DOUBLECLUSTERTXT.write("\n")
DOUBLECLUSTERTXT.close()

print(datetime.now() - start)
