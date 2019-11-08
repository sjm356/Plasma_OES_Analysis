# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 00:00:38 2019

@author: jmsong

v2: input spectrum file with information of measurement specification
v2.1: input spectrum file without header
v3: Code edited from CR post processing code
"""
from tkinter import *
from tkinter import filedialog
import os
import re
import numpy as np

# Wavelengths to be found (up=numerator, lo=denominator)
up_input_wavelength_file = filedialog.askopenfilename(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select up wavelength file")
lo_input_wavelength_file = filedialog.askopenfilename(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select lo wavelength file")

with open(up_input_wavelength_file) as data_up:
    lines_up = data_up.read().split()
with open(lo_input_wavelength_file) as data_lo:
    lines_lo = data_lo.read().split()
    
n_up = len(lines_up)
n_lo = len(lines_lo)

peak_up_intensity = np.zeros((n_up, 2), dtype = float)
peak_lo_intensity = np.zeros((n_lo, 2), dtype = float)
peak_ratio = np.zeros((n_up * n_lo, 3), dtype = float)

'''
up_f = input('upper wavelength: ')
lo_f = input('lower wavelength: ')
up = float(up_f)
lo = float(lo_f)
'''

# Loading OES data files
# root = Tk()
file_path = filedialog.askdirectory(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select OES data Folder")

root = Tk()

# File path containing NOMADlite data
# Spectrum data only
# file_path = '/Users/jmsong/Documents/00_NFRI/00_연구관리/00_실험데이터/05_CR/data'
file_list = os.listdir(file_path)
new_file_list = []
file_list.sort()

# Defining new directory for new output file
new_file_path = file_path + '/new_output'
# Making new folder in directory
if not os.path.exists(new_file_path):
    os.mkdir(new_file_path)

# Defining new variables
Ne = []
Te = []

new_line = []
nnnew_line = []

intensity_up = 1
intensity_lo = 1
        
if len(file_list) == 0:
    print('!!No data files in this directory')

for k in file_list:
    if k == 'new_output':
        continue
    with open(file_path + "/"+ k) as data:
        lines = data.readlines()
        data.close()
    
    lines_array = np.array(lines[17:-1])
    new_lines_array = np.zeros((len(lines_array),2),dtype = float)
    
        # Making and open new output file
    ph_file_name = "ph_intensity_" + k
    ph_ratio_file_name = "ph_ratio_" + k
    intensity_file = open(file_path + "/new_output/" + ph_file_name,'w')
    ratio_file = open(file_path + "/new_output/" + ph_ratio_file_name,'w')
    intensity_file.write(f'Wavelength(nm) \t Intensity \n')
    ratio_file.write(f'Wavelength_numerator \t Wavelength_denominator \t ratio_value \n')
                
    for l, new_line in enumerate(lines_array):
        nnew_line = new_line.split('\t')  # Splitting with tap
        new_lines_array[l,0] = nnew_line[0]
        new_lines_array[l,1] = nnew_line[1]
    
    for i,ii in enumerate(lines_up):
        peak_up_intensity[i,0] = new_lines_array[np.where(new_lines_array[:,0] == float(ii)), 0]
        peak_up_intensity[i,1] = new_lines_array[np.where(new_lines_array[:,0] == float(ii)), 1]
        
    for j,jj in enumerate(lines_lo):
        peak_lo_intensity[j,0] = new_lines_array[np.where(new_lines_array[:,0] == float(jj)), 0]
        peak_lo_intensity[j,1] = new_lines_array[np.where(new_lines_array[:,0] == float(jj)), 1]
        
    peak_intensity = np.r_[peak_up_intensity, peak_lo_intensity]
    a = 0
    for k1 in range(len(peak_lo_intensity)):
        for k2 in range(len(peak_up_intensity)):
            peak_ratio[a,0] = peak_up_intensity[k2, 0]
            peak_ratio[a,1] = peak_lo_intensity[k1, 0]
            peak_ratio[a,2] = peak_up_intensity[k2, 1] / peak_lo_intensity[k1, 1]
            
            peak_ratio_wave_up = peak_up_intensity[k2, 0]
            peak_ratio_wave_lo = peak_lo_intensity[k1, 0]
            peak_ratio_one = peak_up_intensity[k2, 1] / peak_lo_intensity[k1, 1]
            ratio_file.write(f'{peak_ratio_wave_up} \t {peak_ratio_wave_lo} \t {peak_ratio_one} \n')
    for nnn in range(len(peak_intensity)):
        peak_intensity_wavelength = peak_intensity[nnn, 0]
        peak_intensity_one = peak_intensity[nnn, 1]
        intensity_file.write(f'{peak_intensity_wavelength} \t {peak_intensity_one} \n')
    ratio_file.close()
    intensity_file.close()
            