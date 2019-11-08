# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 00:00:38 2019

@author: jmsong
"""
from tkinter import *
from tkinter import filedialog
import os
import re

# Wavelengths to be found (up=numerator, lo=denominator)
up_f = input('upper wavelength: ')
lo_f = input('lower wavelength: ')
up = float(up_f)
lo = float(lo_f)

# Loading Standard Peaks of Hg/Ar spectrum for Wavelength Calibration
# root = Tk()
file_path = filedialog.askdirectory(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select Folder")

root = Tk()

# File path containing OES data
# Spectrum data only
# file_path = '/Users/jmsong/Documents/00_NFRI/00_연구관리/00_실험데이터/05_CR/data'
file_list = os.listdir(file_path)
new_file_list = []
file_list.sort()

# Defining new directory for new output file
new_file_path = file_path + '/new_output'

# Defining new variables with initial values
#Ne = []
#Te = []
x = 111
y = 111
new_line = []
intensity_up = 1
intensity_lo = 1


for i in file_list:
    if i.count('Ar') >= 1:
        new_file_list.append(i)

if len(new_file_list) == 0:
    print('!!No data files in this directory')
else:
    # Making new folder in directory
    if not os.path.exists(new_file_path):
        os.mkdir(new_file_path)

    # Making and open new output file
    new_file_name = up_f + "_" + lo_f
    new_file = open(file_path + "/new_output/" + new_file_name + ".dat",'w')
    new_file.write(f'RF power(W) \t Pressure(mTorr) \t x(mm) \t y(mm) \t Intensity({up} nm) \t Intensity({lo} nm) \t Line-ratio({up}/{lo})\n')

    for i in new_file_list:        
        # Detecting Experimental conditions (pressure, RF power, position)
        pressure = i[3:5]
        RFpower = i[8:11] 

        # Detecting position
        if 'top_p1' in i:
            x = 50
            y = 0
        elif 'p2' in i:
            x = 0
            y = 50
        elif 'p3' in i:
            x = 25
            y = 0
        elif 'p4' in i:
            x = 0
            y = 25
        elif 'p5' in i:
            x = 0
            y = 0
        elif 'p6' in i:
            x = 0
            y = -25
        elif 'p7' in i:
            x = -25
            y = 0
        elif 'p8' in i:
            x = 0
            y = -50
        elif 'p9' in i:
            x = -50
            y = 0
        elif 'side' in i:
            x = 1111
            y = 1111

        with open(file_path + "/"+ i) as data:
            lines = data.readlines()
            data.close()
            
        for j, new_line in enumerate(lines):
            # variables to check if the wavelengths were in the file
            check_up = 0
            check_lo = 0
            
            new_line = re.sub('\s{1,}','\t',new_line)  # Replacing random space between data with 1 tap
            nnew_line = new_line.split('\t')  # Splitting with tap
            '''
            # Finding Ne in data file
            if j is 1:
                Ne = float(nnew_line[1])
                # Finding Te in data file
            elif j is 2:
                Te = float(nnew_line[4])
            '''
            # Finding intensities of given wavelengths and checking
            if str(up) in new_line:
                intensity_up = float(nnew_line[1])
                check_up = 1
            if str(lo) in new_line:
                intensity_lo = float(nnew_line[1])
                check_lo = 1

            # Calculating line ratio
            Line_ratio = float(intensity_up / intensity_lo)
        
        # Printing messeges if the wavelegth is not in the file
        if check_up == 0:
            print(f'!! Wavelength {up} is not in the file of {i}')
        if check_lo == 0:
            print(f'!! Wavelength {lo} is not in the file of {i}')
        
        # Writing new output data file
        new_file.write(f'{RFpower}\t{pressure}\t{x}\t{y}\t{intensity_up}\t{intensity_lo}\t{Line_ratio}\n')
        
    new_file.close()