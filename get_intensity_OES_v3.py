# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 00:00:38 2019

@author: jmsong

v2: input spectrum file with information of measurement specification
v2.1: input spectrum file without header
v3: adding intensity calibration function by subtracting dark spectrum and muliplying calibration coefficient
"""
from tkinter import *
from tkinter import filedialog
import os
import re
import numpy as np

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
    
# Loading dark intensity folder path and calibration file
dark_intensity_folder_path = filedialog.askdirectory(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select dark data folder")
calibration_coeff_file = filedialog.askopenfilename(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select Calibration coefficient data")
file_list_dark = os.listdir(dark_intensity_folder_path)
new_file_list_dark = []
file_list_dark.sort()

# Making files for intensity ans ratio values depending on the experiment condition
new_file_name_intensity = "peak intensity"
new_file_name_ratio = "peak ratio"
new_file_intensity_total = open(new_file_path + "/" + new_file_name_intensity + ".dat",'w')
new_file_ratio_total = open(new_file_path + "/" + new_file_name_ratio + ".dat",'w')
new_file_intensity_total.write(f'filename \t')
new_file_ratio_total.write(f'filename \t')

# Targeting Wavelengths (up=numerator, lo=denominator), Loading files having wavelength values
up_input_wavelength_file = filedialog.askopenfilename(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select up wavelength file")
lo_input_wavelength_file = filedialog.askopenfilename(initialdir="C:\\Users\\jmsong\\Documents\\00_NFRI\\00_연구관리\\00_실험데이터\\01_OES", title="Select lo wavelength file")

# Opening Total files and Writing header of file with up and low wavelengths
# for intensities ans ratios
with open(up_input_wavelength_file) as data_up:
    lines_up = data_up.read().split()
    #new_file_intensity_total.write(f'{lines_up} \t')
with open(lo_input_wavelength_file) as data_lo:
    lines_lo = data_lo.read().split()
    #new_file_intensity_total.write(f'{lines_lo} \t')
for value_up in lines_up:
    new_file_intensity_total.write(f'{value_up} \t')
for value_lo in lines_lo:
    new_file_intensity_total.write(f'{value_lo} \t')
    for value_up_in in lines_up:
        new_file_ratio_total.write(f'{value_up_in}/{value_lo} \t')
new_file_intensity_total.write(f'\n')   # Moving cursor
new_file_ratio_total.write(f'\n')   # Moving cursor

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

# Defining new variables
Ne = []
Te = []

new_line = []
nnnew_line = []

intensity_up = 1
intensity_lo = 1
        
if len(file_list) == 0:
    print('!!No data files in this directory')
if len(file_list_dark) == 0:
    print('!!No dark data files in this directory')

# Loading Calibration coefficient file
with open(calibration_coeff_file) as data_cal:
    lines_cal = data_cal.readlines()
    cal_lines_array = np.array(lines_cal[0:])

for k in file_list:
    if k == 'new_output':
        continue
    with open(file_path + "/"+ k) as data:
        lines = data.readlines()
        lines_array = np.array(lines[0:])     # reading each line with string type with list format
        new_lines_array = np.zeros((len(lines_array),4),dtype = float)      # making new array with [n,2] matrix form for saving with floating type
        data.close()

    # Making new data file
    update_file = k + "_new"
    new_file_data = open(new_file_path + "/" + update_file + ".dat",'w')
    new_file_data.write(f'Wavelength(nm) \t Original intensity \t Subtracted intensity \t Calibrated intensity \n')
    
    # Finding exposure time in file name
    # If same file name is in folder, extracting is simple.
    where_time = k.find("ms")
    exp_time = k[where_time-4:where_time]
    for kk in file_list_dark:
        if exp_time in kk:
            with open(dark_intensity_folder_path + "/" + kk) as dark_data:
                dark_lines = dark_data.readlines()
                dark_lines_array = np.array(dark_lines[0:])
                dark_data.close()

    # Making and opening new output file (ph=peak height)
    ph_file_name = "ph_intensity_" + k
    ph_ratio_file_name = "ph_ratio_" + k
    intensity_file = open(file_path + "/new_output/" + ph_file_name,'w')
    ratio_file = open(file_path + "/new_output/" + ph_ratio_file_name,'w')
    intensity_file.write(f'Wavelength(nm) \t Intensity \n')
    ratio_file.write(f'Wavelength_numerator \t Wavelength_denominator \t ratio_value \n')
    new_file_ratio_total.write(f'{k} \t')
    new_file_intensity_total.write(f'{k} \t')
                
    for l, new_line in enumerate(lines_array):
        nnew_line = new_line.split('\t')  # Splitting with tap
        new_lines_array[l,0] = nnew_line[0]     # Wavelength
        new_lines_array[l,1] = nnew_line[1]     # raw intensity
        new_lines_array[l,2] = float(nnew_line[1]) - float(dark_lines_array[l].split('\t')[1])     # Intensity subtracted by dark intensity
        new_lines_array[l,3] = new_lines_array[l,2] * float(cal_lines_array[l].split('\t')[1])     # Multiplying calibration coefficient

        # For writing files
        temp_1 = new_lines_array[l,0]
        temp_2 = new_lines_array[l,1]
        temp_3 = new_lines_array[l,2]
        temp_4 = new_lines_array[l,3]
        new_file_data.write('f{temp_1} \t {temp_2} \t {temp_3} \t {temp_4} \n')
    new_file_data.close()

    for i,ii in enumerate(lines_up):
        peak_up_intensity[i,0] = new_lines_array[np.where(new_lines_array[:,0] == float(ii)), 0]
        peak_up_intensity[i,1] = new_lines_array[np.where(new_lines_array[:,0] == float(ii)), 3]
        
    for j,jj in enumerate(lines_lo):
        peak_lo_intensity[j,0] = new_lines_array[np.where(new_lines_array[:,0] == float(jj)), 0]
        peak_lo_intensity[j,1] = new_lines_array[np.where(new_lines_array[:,0] == float(jj)), 3]
        
    peak_intensity = np.r_[peak_up_intensity, peak_lo_intensity]
    a = 0
    for k1 in range(len(peak_lo_intensity)):
        for k2 in range(len(peak_up_intensity)):
            peak_ratio[a,0] = peak_up_intensity[k2, 0]
            peak_ratio[a,1] = peak_lo_intensity[k1, 0]
            peak_ratio[a,2] = peak_up_intensity[k2, 1] / peak_lo_intensity[k1, 1]
            
            # For writing files
            peak_ratio_wave_up = peak_up_intensity[k2, 0]
            peak_ratio_wave_lo = peak_lo_intensity[k1, 0]
            peak_ratio_one = peak_up_intensity[k2, 1] / peak_lo_intensity[k1, 1]
            ratio_file.write(f'{peak_ratio_wave_up} \t {peak_ratio_wave_lo} \t {peak_ratio_one} \n')
            new_file_ratio_total.write(f'{peak_ratio_one} \t')
    new_file_ratio_total.write(f'\n')   # Moving cursor

    for nnn in range(len(peak_intensity)):
        peak_intensity_wavelength = peak_intensity[nnn, 0]
        peak_intensity_one = peak_intensity[nnn, 1]
        intensity_file.write(f'{peak_intensity_wavelength} \t {peak_intensity_one} \n')
        new_file_intensity_total.write(f'{peak_intensity_one} \t')
    new_file_intensity_total.write(f'\n')   # Moving cursor

    ratio_file.close()
    intensity_file.close()
new_file_intensity_total.close()
new_file_ratio_total.close()