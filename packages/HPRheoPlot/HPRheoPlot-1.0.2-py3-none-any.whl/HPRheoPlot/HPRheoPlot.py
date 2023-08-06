#!/usr/bin/env python3

# Import libraries
import pandas as pd
import numpy as np
from tabulate import tabulate
import seaborn as sns
import matplotlib.pyplot as plt
import time
import os
import sys 
import glob
import pyfiglet
from matplotlib import rcParams
import xlrd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from matplotlib import ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import csv

# Print the title 
os.system('cls' if os.name == 'nt' else 'clear')
title = pyfiglet.figlet_format('HPRheoPlot', font = 'small')
print('\n')
print(title+'\n')
print('\n')
print('------------------------------------------------')
print('If you have any questions, please send your questions to my email.')
print('\nOr, please suggest errors and areas that need updating.')
print('\n 📨 woo_go@yahoo.com')
print('\nVisit https://github.com/wjgoarxiv/hprheoplot for more information.')
print('------------------------------------------------')

# Read the settings from `settings.txt` file written by the user. 
try:
  with open('settings.txt', 'r') as f:
    lines = f.readlines()
    for line in lines: 
      if line.startswith('#'):
        continue
      else:
        line = line.split('=')
        if line[0].strip() == 'DW-directory': 
          dw_input_dirloc = line[1].strip()
        elif line[0].strip() == 'TRIOS-directory':
          trios_input_dirloc = line[1].strip()
        elif line[0].strip() == 'graph-type': 
          graph_type = line[1].strip()
        elif line[0].strip() == 'graph-style':
          graph_style = line[1].strip()
        elif line[0].strip() == 'line-width':
          line_width = float(line[1].strip())
        elif line[0].strip() == 'graph-decorate':
          graph_decorate = line[1].strip()
        elif line[0].strip() == 'curve-fit-equation':
          curvefit_equation = line[1].strip()
    
    #  Check the validity of the settings
    if not os.path.isdir(dw_input_dirloc):
      print('ERROR The directory that you specified does not exist.')
      sys.exit()
    elif not os.path.isdir(trios_input_dirloc):
      print('ERROR The directory that you specified does not exist.')
      sys.exit()
    elif graph_type not in ['eta-t', 'eta-gamma', 'eta-delp', 'gamma-sigma']:
      print('ERROR The graph type you specified is not valid.')
      sys.exit()
    elif graph_style not in ['line', 'scatter']:
      print('ERROR The graph style you specified is not valid.')
      sys.exit()
    elif graph_decorate not in ['y', 'n']:
      print('ERROR The graph decoration option must be either y or n.')
      sys.exit()
    elif curvefit_equation not in ['Powerlaw', 'Cross', 'Sisko']:
      print('ERROR The curve fit equation you specified is not valid.')
      sys.exit()

except FileNotFoundError:
  print('ERROR There is no `settings.txt` file in the current directory. I will make a new `settings.txt` file for you.')
  with open('settings.txt', 'w') as f:
    f.write("###################################\n")
    f.write("############ SETTINGS.TXT #############\n")
    f.write("###################################\n")
    f.write("\n")
    f.write("# This file is for the settings of the HPRheoPlot program. \n")
    f.write("# NOTE: This file should be named as `settings.txt`. If isn't, the program cannot load the settings. \n")
    f.write("\n")
    f.write("###########################################################")
    f.write("\n")
    f.write("# DW-directory: The directory location where the csv files from DWStemp program are located. \n")
    f.write("DW-directory = ./DW/ \n")
    f.write("\n")
    f.write("# TRIOS-directory: The directory location where the csv files from TRIOS program are located. \n")
    f.write("TRIOS-directory = ./TRIOS/ \n")
    f.write("\n")
    f.write("# graph-type: The type of graph that you want to plot (options: eta-t, eta-gamma, eta-delp, gamma-sigma) \n")
    f.write("graph-type = eta-t \n")
    f.write("\n")
    f.write("# graph-style: The style of graph that you want to plot (options: line, scatter) \n")
    f.write("graph-style = line \n")
    f.write("\n")
    f.write("# line-width: The line width of the graph (example: 0.5, 1, 2.3, etc.) - this works when graph-style is line. \n")
    f.write("line-width = 2 \n")
    f.write("\n")
    f.write("# graph-decorate: Whether you want to decorate the graph (options: y, n) \n")
    f.write("graph-decorate = y \n")
    f.write("\n")
    f.write("# curve-fit-equation: The equation that you want to use for the curve fit (options: Powerlaw, Cross, Sisko) \n")
    f.write("curve-fit-equation = Powerlaw \n")

  print('INFO The `settings.txt` file has been created. Please edit the file and run the program again.')
  sys.exit()

# A function to treat csv data from DWStemp program. 
def dwcsvtreat():
  dw_file_list = glob.glob(dw_input_dirloc+'/*.csv')
  dw_file_list.sort()
  try:
    if len(dw_file_list) == 0:
      raise Exception
    else: 
      pass
  except: 
    print('\nINFO There is no csv file in the directory. Please check the directory location again.') 
    print('\nINFO The program will stop.')
    exit()

  # Label file numbers and show all the files
  dw_file_num = []
  for i in range(len(dw_file_list)):
    dw_file_num.append(i)
  print(tabulate({'File number': dw_file_num, 'File name': dw_file_list}, headers='keys', tablefmt = 'psql'))

  file_number = int(input('\nINFO These are the DWStemp raw files that are in the folder. Please type the file number that you want to use: '))
  try:
    print("\nINFO The file name that would be used is: ", dw_file_list[file_number])
  except IndexError:
    print("\nERROR Your input number is out of range. Please check the file number again.")
    print("ERROR The program will stop.") 
    exit()

  global df_dw, time, pressure, raw_temp, time_min, time_hr
  df_dw = pd.read_csv(dw_file_list[file_number], encoding='cp949')

  # Get pressure & temperature data (time -> 2nd, pressure -> 3rd, temperature -> 5th)
  time = df_dw.iloc[1:,1]
  pressure = df_dw.iloc[1:,2]
  raw_temp = df_dw.iloc[1:,4]

  # Note that all data are 'object', therefore, we need to convert them to float
  pressure = pressure.astype(float)
  time = time.astype(float)
  time_min = time/60 # Convert time to minute
  time_hr = time/3600 # Convert time to hour

  # Delta P calculation = P0 - P 
  global pressure_delta
  pressure_delta = pressure[1] - pressure

# A function to treat csv data from TRIOS program.
def trioscsvtreat():
  trios_file_list = glob.glob(trios_input_dirloc+'/*.xls')
  trios_file_list.sort()
  try: 
    if len(trios_file_list) == 0:
      raise Exception
    else:
      pass
  except:
    print('\nINFO There is no xls file in the directory. Please check the directory location again.')
    print('\nINFO The program will stop.')
    exit()

  # Label file numbers and show all the files
  trios_file_num = []
  for i in range(len(trios_file_list)):
    trios_file_num.append(i)
  print(tabulate({'File number': trios_file_num, 'File name': trios_file_list}, headers='keys', tablefmt = 'psql'))
  trios_file_number = int(input('\nINFO These are the TRIOS raw excel files that are in the folder. Please type the file number that you want to use: '))
  try:
    print("\nINFO The file name that would be used is: ", trios_file_list[trios_file_number])
  except IndexError:
    print("\nERROR Your input number is out of range. Please check the file number again.")
    print("ERROR The program will stop.")
    exit()

  # Read the xls file
  xls = pd.ExcelFile(trios_file_list[trios_file_number])

  # Read the first sheet
  global df_peakhold2
  df_peakhold2 = pd.read_excel(xls, 'Peak hold - 2', skiprows=3)

  # Second page
  global df_flowsweep3
  try: 
    df_flowsweep3 = pd.read_excel(xls, 'Flow sweep - 3', skiprows=3)
  except:
    pass

  # Third page
  global df_flowsweep4
  try:
    df_flowsweep4 = pd.read_excel(xls, 'Flow sweep - 4', skiprows=3)
  except:
    pass

  # Fourth page
  global df_timesweep5
  try:
    df_timesweep5 = pd.read_excel(xls, 'Time sweep - 5', skiprows=3)
  except:
    pass

  # Last page
  global df_flowramp6
  try:
    df_flowramp6 = pd.read_excel(xls, 'Flow ramp - 6', skiprows=3)
  except:
    pass

# Rcparams settings
def rcparams():
  if graph_decorate == 'y' or graph_decorate == 'Y':
    rcParams['figure.figsize'] = 5, 4
    rcParams['font.family'] = 'sans-serif'

    # Check whether Arial or SF Pro Display are installed in the computer
    try:
        rcParams['font.sans-serif'] = ['SF Pro Display']
    except:
        try:
            rcParams['font.sans-serif'] = ['Arial']
        except:
            print("ERROR Note that Arial and SF Pro are not installed in the computer. The program will use the default font.")
            pass

    # Label should be far away from the axes
    rcParams['axes.labelpad'] = 8
    rcParams['xtick.major.pad'] = 7
    rcParams['ytick.major.pad'] = 7

    # Add minor ticks
    rcParams['xtick.minor.visible'] = True
    rcParams['ytick.minor.visible'] = True

    # Tick width
    rcParams['xtick.major.width'] = 1
    rcParams['ytick.major.width'] = 1
    rcParams['xtick.minor.width'] = 0.5
    rcParams['ytick.minor.width'] = 0.5

    # Tick length
    rcParams['xtick.major.size'] = 5
    rcParams['ytick.major.size'] = 5
    rcParams['xtick.minor.size'] = 3
    rcParams['ytick.minor.size'] = 3

    # Tick color
    rcParams['xtick.color'] = 'black'
    rcParams['ytick.color'] = 'black'

    rcParams['font.size'] = 14
    rcParams['axes.titlepad'] = 10
    rcParams['axes.titleweight'] = 'bold'
    rcParams['axes.titlesize'] = 18

    # Axes settings
    rcParams['axes.labelweight'] = 'bold'
    rcParams['xtick.labelsize'] = 12
    rcParams['ytick.labelsize'] = 12
    rcParams['axes.labelsize'] = 16
    rcParams['xtick.direction'] = 'in'
    rcParams['ytick.direction'] = 'in'

  elif graph_decorate == 'n' or graph_decorate == 'N':
    pass

  else: 
    print("ERROR Something is wrong. Please check the graph decoration option again.")
    sys.exit()

# PLOT1: A function to plot the eta-t graph
def etatplot():
  # 4th column is the time
  time_peakhold2 = df_peakhold2.iloc[:, 3] # df_peakhold2 comes from the trioscsvtreat function

  # 3rd column is the viscosity 
  global viscosity
  viscosity = df_peakhold2.iloc[:, 2]

  # 2nd column is the pressure
  global pressure
  pressure = df_dw.iloc[1:,2]

  # Note that all data are 'object', therefore, we need to convert them to float
  time_peakhold2 = time_peakhold2.astype(float)
  viscosity = viscosity.astype(float)
  pressure = pressure.astype(float)

  # Convert the time unit
  time_peakhold2_min = time_peakhold2 / 60
  time_peakhold2_hr = time_peakhold2 / 3600

  if graph_style == 'line':
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Time (hr)')
    ax1.set_ylabel('Pressure (bar)', color=color)
    ax1.plot(time_hr, pressure, color=color, linewidth = line_width) #time_hr comes from `dwcsvtreat` function.
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlim(0, )
    ax1.set_ylim()

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Viscosity (Pa·s)', color=color)  # we already handled the x-label with ax1
    ax2.plot(time_peakhold2_hr, viscosity, color=color, linewidth = line_width)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xlim(0, max(time_peakhold2_hr))
    ax2.set_ylim()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

  elif graph_style == 'scatter':
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_xlabel('Time (hr)')
    ax1.set_ylabel('Pressure (bar)', color=color)
    ax1.scatter(time_hr, pressure, color=color, s = None, edgecolors=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlim(0, )
    ax1.set_ylim()

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('Viscosity (Pa·s)', color=color)  # we already handled the x-label with ax1
    ax2.scatter(time_peakhold2_hr, viscosity, color=color, s = None, edgecolors=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_xlim(0, max(time_peakhold2_hr))
    ax2.set_ylim()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped

  # Maximum viscosity expression
  ax2.axhline(y = max(viscosity), color = 'red', linestyle = '--', linewidth = 0.5)

  # The text location is important. Place the text at the adjusted location.
  etatplot_text_x = max(time_peakhold2_hr) * 0.9
  etatplot_text_y = max(viscosity) * 0.9

  ax2.text(etatplot_text_x, etatplot_text_y, "$η_{max}$ =" + str(round(max(viscosity), 2)) + ' Pa*s', color = 'red', fontsize = 10, horizontalalignment = 'right', verticalalignment = 'bottom')
  plt.savefig('eta-t.png', dpi = 250, bbox_inches = 'tight')
  print("\nINFO The eta-t graph is saved as 'eta-t.png'.")

# PLOT2: A function to plot the eta-delp graph
def etadelpplot():
  global pressure_delta
  global viscosity

  # Match the dim. of pressure_delta & viscosity. Since x and y must have same first dimension, but have different shapes. 
  
  if len(pressure_delta) > len(viscosity):
    pressure_delta = pressure_delta[0:len(viscosity)]
  elif len(pressure_delta) < len(viscosity):
    viscosity = viscosity[0:len(pressure_delta)]

  # Plot 
  # LINE
  if graph_style == 'line':
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('$\Delta P$ (bar)')
    ax1.set_ylabel('Viscosity (Pa·s)', color=color)
    ax1.plot(pressure_delta, viscosity, color=color, linewidth = line_width)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlim(0, )
    ax1.set_ylim() 
    fig.tight_layout()

  # SCATTER
  elif graph_style == 'scatter':
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Pressure (bar)')
    ax1.set_ylabel('Viscosity (Pa·s)', color=color)
    ax1.scatter(pressure_delta, viscosity, color=color, s = None)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlim(0, )
    ax1.set_ylim()
    fig.tight_layout()

  # Save figure
  fig.savefig('eta-delp.png', dpi = 250, bbox_inches = 'tight')
  print("\nINFO The eta-delp graph is saved as 'eta-delp.png'.")

# PLOT3: A function to plot the gamma-sigma graph
def gammasigmaplot():
  # Check whether df_flowramp6 is empty or not 
  if df_flowramp6.empty:
    print("ERROR The flow ramp 6 is empty. Please check the data again.")
    sys.exit()
  else:
    pass

  # Stress is 0th column, Shear rate is 1st column. 
  stress = df_flowramp6.iloc[:, 0]
  shear_rate = df_flowramp6.iloc[:, 1]

  # PLOT
  # LINE
  if graph_style == 'line':
    fig, ax1 = plt.subplots()
    color = 'black'
    ax1.set_xlabel('Stress (Pa)')
    ax1.set_ylabel('Shear rate (s$^{-1}$)', color=color)
    ax1.plot(stress, shear_rate, color=color, linewidth = line_width)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlim(0, )
    ax1.set_ylim(0, )
    fig.tight_layout()

    # SCATTER
  elif graph_style == 'scatter':
    fig, ax1 = plt.subplots()
    color = 'black'
    ax1.set_xlabel('Stress (Pa)')
    ax1.set_ylabel('Shear rate (s$^{-1}$)', color=color, fontsize=16)
    ax1.scatter(stress, shear_rate, color=color, s = None)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xlim(0, )
    ax1.set_ylim(0, )

  # At the largest stress value, write ahvline
  ax1.axvline(x = max(stress), color = 'black', linestyle = '--', linewidth = 1)

  # Find the adjustable position of the text
  # Find the index of the largest stress value
  index = stress.idxmax()
  # Find the shear rate value at the largest stress value
  shear_rate_max = shear_rate[index]
  # Find the stress value at the largest stress value
  stress_max = stress[index]

  # Find the position of the text
  x_text = stress_max - 0.1* stress_max
  y_text = shear_rate_max + 0.1 * shear_rate_max

  # Write the text
  ax1.text(x_text, y_text, "$\sigma_{yield}$ =" + str(round(stress_max, 2)) + '$Pa$', color = 'black', fontsize = 12, horizontalalignment = 'right', verticalalignment = 'bottom', rotation = 0)

  # Save figure
  plt.savefig('gamma-sigma.png', dpi = 250, bbox_inches = 'tight')
  print("\nINFO The gamma-sigma graph is saved as 'gamma-sigma.png'.")

# PLOT4: A function to plot the eta-gamma graph
def etagammaplot():
  # Check whether df_flowsweep3 is empty or not 
  if df_flowsweep3.empty:
    print("ERROR The flow sweep 3 is empty. Please check the data again.")
    sys.exit()
  else:
    pass

  # Check whether df_flowsweep4 is empty or not
  if df_flowsweep4.empty:
    print("ERROR The flow sweep 4 is empty. Please check the data again.")
    sys.exit()
  else:
    pass

  # In flowsweep3, the 2nd column is shear rate, and the 3rd column is viscosity. Note that flowsweep3 starts from the low shear to the high shear. 
  shear_rate3 = df_flowsweep3.iloc[:, 1]
  viscosity3 = df_flowsweep3.iloc[:, 2]

  # In flowsweep4, the 2nd column is shear rate, and the 3rd column is viscosity. Note that flowsweep4 starts from the high shear to the low shear.
  shear_rate4 = df_flowsweep4.iloc[:, 1]
  viscosity4 = df_flowsweep4.iloc[:, 2]

  # PLOT: flow sweep 3
  # NOTE: y-scale should be logaritmic
  # LINE
  if graph_style == 'line':
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Shear rate (s$^{-1}$)')
    ax1.set_ylabel('Viscosity (Pa·s)', color='black')
    ax1.plot(shear_rate3, viscosity3, color=color, linewidth = line_width)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_xlim(0, )
    ax1.set_ylim()
    ax1.set_yscale('log')
    fig.tight_layout()
    
    # SCATTER
  elif graph_style == 'scatter':
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Shear rate (s$^{-1}$)')
    ax1.set_ylabel('Viscosity (Pa·s)', color='black', fontsize=16)
    ax1.scatter(shear_rate3, viscosity3, color=color, s = None, alpha = 0.8)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_xlim(0, )
    ax1.set_ylim()
    ax1.set_yscale('log')
    fig.tight_layout()

  # PLOT: flow sweep 4
  # LINE
  if graph_style == 'line':
    color = 'tab:blue'
    ax1.plot(shear_rate4, viscosity4, color=color, linewidth = line_width)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_xlim(0, )
    ax1.set_ylim()
    ax1.set_yscale('log')
    fig.tight_layout()

    # SCATTER
  elif graph_style == 'scatter':
    color = 'tab:blue'
    ax1.scatter(shear_rate4, viscosity4, color=color, s = None, alpha = 0.8)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_xlim(0, )
    ax1.set_ylim()
    ax1.set_yscale('log')
    fig.tight_layout()

  # Legend
  ax1.legend(['Flow sweep 3', 'Flow sweep 4'], loc = 'upper right', fontsize = 12, frameon = False)

  # Tick interval control & notation
  ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))

  # Curve fitting to the Power-law model, and the Cross model.
  # NOTE: The Power-law model is defined as eta = K * gamma^(n-1), and the Cross model is defined as eta = (eta0 - eta_infty) / (1 + (K * gamma)^n) + eta_infty.
  # NOTE: The Sisko model is defined as eta = eta_infty + K * gamma^(n-1)

  # Define the Power-law model
  def powerlaw(x, K, n):
    return K * x ** (n - 1)
  
  # Define the Cross model
  def cross(x, K, n, eta0, eta_infty):
    return (eta0 - eta_infty) / (1 + (K * x) ** n) + eta_infty
  
  # Define the Sisko model
  def sisko(x, K, n, eta_infty):
    return eta_infty + K * x ** (n - 1)
  
  # Power-law model fitting
  if curvefit_equation == 'Powerlaw':
    # (1) flow sweep 3 fitting
    # NOTE: The initial values of K and n are set to 1.0 and 1.0, respectively.
    popt3, pcov3 = curve_fit(powerlaw, shear_rate3, viscosity3, p0 = [1.0, 1.0])
    K3 = popt3[0]
    n3 = popt3[1]
    eta3 = powerlaw(shear_rate3, K3, n3)
    # (2) flow sweep 4 fitting
    # NOTE: The initial values of K and n are set to 1.0 and 1.0, respectively.
    popt4, pcov4 = curve_fit(powerlaw, shear_rate4, viscosity4, p0 = [1.0, 1.0])
    K4 = popt4[0]
    n4 = popt4[1]
    eta4 = powerlaw(shear_rate4, K4, n4)
    # (3) Plot
    half_linewidth = line_width / 2
    ax1.plot(shear_rate3, eta3, color = 'tab:red', linestyle = '--', linewidth = half_linewidth, alpha = 0.7)
    ax1.plot(shear_rate4, eta4, color = 'tab:blue', linestyle = '--', linewidth = half_linewidth, alpha = 0.7)
    ax1.text(0.05, 0.9, 'Flow sweep 3: K = %f, n = %f, R$^2$ = %f' % (K3, n3, r2_score(viscosity3, eta3)), transform = ax1.transAxes, fontsize = 11)
    ax1.text(0.05, 0.85, 'Flow sweep 4: K = %f, n = %f, R$^2$ = %f' % (K4, n4, r2_score(viscosity4, eta4)), transform = ax1.transAxes, fontsize = 11)

    # (4) Print
    print("INFO The Power-law model is selected.")
    print("INFO The Power-law model fitting results are as follows.")
    print("INFO Flow sweep 3: K = %f, n = %f, R^2 = %f" % (K3, n3, r2_score(viscosity3, eta3)))
    print("INFO Flow sweep 4: K = %f, n = %f, R^2 = %f" % (K4, n4, r2_score(viscosity4, eta4)))
    # (5) Legend
    ax1.legend(['Flow sweep 3', 'Flow sweep 4', 'Power-law fitted (flow sweep 3)', 'Power-law fitted (flow sweep 4)'], loc = 'upper right', fontsize = 11, frameon = False)

  elif curvefit_equation == 'Cross':
    # (1) flow sweep 3 fitting
    # NOTE: The initial values of K, n, eta0, and eta_infty are set to 1.0, 1.0, 1.0, and 1.0, respectively.
    popt3, pcov3 = curve_fit(cross, shear_rate3, viscosity3, p0 = [1.0, 1.0, 1.0, 1.0], maxfev = 1000000)
    K3 = popt3[0]
    n3 = popt3[1]
    eta0_3 = popt3[2]
    eta_infty_3 = popt3[3]
    eta3 = cross(shear_rate3, K3, n3, eta0_3, eta_infty_3)
    # (2) flow sweep 4 fitting
    # NOTE: The initial values of K, n, eta0, and eta_infty are set to 1.0, 1.0, 1.0, and 1.0, respectively.
    popt4, pcov4 = curve_fit(cross, shear_rate4, viscosity4, p0 = [1.0, 1.0, 1.0, 1.0], maxfev = 1000000)
    K4 = popt4[0]
    n4 = popt4[1]
    eta0_4 = popt4[2]
    eta_infty_4 = popt4[3]
    eta4 = cross(shear_rate4, K4, n4, eta0_4, eta_infty_4)
    # (3) Plot
    half_linewidth = line_width / 2
    ax1.plot(shear_rate3, eta3, color = 'tab:red', linestyle = '--', linewidth = half_linewidth, alpha = 0.7)
    ax1.plot(shear_rate4, eta4, color = 'tab:blue', linestyle = '--', linewidth = half_linewidth, alpha = 0.7)
    ax1.text(0.05, 0.95, r'$\eta_0 = $' + str(round(eta0_3, 2)), color = 'tab:red', fontsize = 11, transform = ax1.transAxes, verticalalignment = 'top')
    ax1.text(0.05, 0.90, r'$\eta_\infty = $' + str(round(eta_infty_3, 2)), color = 'tab:red', fontsize = 11, transform = ax1.transAxes, verticalalignment = 'top')
    ax1.text(0.05, 0.80, r'$\eta_0 = $' + str(round(eta0_4, 2)), color = 'tab:blue', fontsize = 11, transform = ax1.transAxes, verticalalignment = 'top')
    ax1.text(0.05, 0.75, r'$\eta_\infty = $' + str(round(eta_infty_4, 2)), color = 'tab:blue', fontsize = 11, transform = ax1.transAxes, verticalalignment = 'top')

    # (4) Print
    print("INFO The Cross model is selected.")
    print("INFO The Cross model fitting results are as follows.")
    print("INFO Flow sweep 3: K = %f, n = %f, eta0 = %f, eta_infty = %f, R^2 = %f" % (K3, n3, eta0_3, eta_infty_3, r2_score(viscosity3, eta3)))
    print("INFO Flow sweep 4: K = %f, n = %f, eta0 = %f, eta_infty = %f, R^2 = %f" % (K4, n4, eta0_4, eta_infty_4, r2_score(viscosity4, eta4)))
    # (5) Legend
    ax1.legend(['Flow sweep 3', 'Flow sweep 4', 'Cross fitted (flow sweep 3)', 'Cross fitted (flow sweep 4)'], loc = 'upper right', fontsize = 11, frameon = False)

  elif curvefit_equation == 'Sisko':
    # (1) flow sweep 3 fitting
    # NOTE: The initial values of K, n, and eta_infty are set to 1.0, 1.0, and 1.0, respectively.
    popt3, pcov3 = curve_fit(sisko, shear_rate3, viscosity3, p0 = [1.0, 1.0, 1.0])
    K3 = popt3[0]
    n3 = popt3[1]
    eta_infty_3 = popt3[2]
    eta3 = sisko(shear_rate3, K3, n3, eta_infty_3)
    # (2) flow sweep 4 fitting
    # NOTE: The initial values of K, n, and eta_infty are set to 1.0, 1.0, and 1.0, respectively.
    popt4, pcov4 = curve_fit(sisko, shear_rate4, viscosity4, p0 = [1.0, 1.0, 1.0])
    K4 = popt4[0]
    n4 = popt4[1]
    eta_infty_4 = popt4[2]
    eta4 = sisko(shear_rate4, K4, n4, eta_infty_4)
    # (3) Plot
    half_linewidth = line_width / 2
    ax1.plot(shear_rate3, eta3, color = 'tab:red', linestyle = '--', linewidth = half_linewidth, alpha = 0.7)
    ax1.plot(shear_rate4, eta4, color = 'tab:blue', linestyle = '--', linewidth = half_linewidth, alpha = 0.7)
    ax1.text(0.05, 0.95, r'$\eta_\infty = $' + str(round(eta_infty_3, 2)), color = 'tab:red', fontsize = 11, transform = ax1.transAxes, verticalalignment = 'top')
    ax1.text(0.05, 0.90, r'$\eta_\infty = $' + str(round(eta_infty_4, 2)), color = 'tab:blue', fontsize = 11, transform = ax1.transAxes, verticalalignment = 'top')

    # (4) Print
    print("INFO The Sisko model is selected.")
    print("INFO The Sisko model fitting results are as follows.")
    print("INFO Flow sweep 3: K = %f, n = %f, eta_infty = %f, R^2 = %f" % (K3, n3, eta_infty_3, r2_score(viscosity3, eta3)))
    print("INFO Flow sweep 4: K = %f, n = %f, eta_infty = %f, R^2 = %f" % (K4, n4, eta_infty_4, r2_score(viscosity4, eta4)))
    # (5) Legend
    ax1.legend(['Flow sweep 3', 'Flow sweep 4', 'Sisko model fitted (flow sweep 3)', 'Sisko model fitted (flow sweep 4)'], loc = 'upper right', fontsize = 11, frameon = False)

  else: 
    print("ERROR The selected equation is not defined. Please select among 'Power', 'Cross', and 'Sisko'.")

  # Save figure
  plt.savefig('eta-gamma.png', dpi = 250, bbox_inches = 'tight')
  print("INFO The eta-gamma graph is saved as 'eta-gamma.png'.")
  

def main():
  # Function execution
  # NOTE: 'eta-t', 'eta-gamma', 'eta-delp', 'gamma-sigma' are selected by user (graph_type)
  # 1. If 'eta-t' is selected, execute dwcsvtreat() -> trioscsvtreat() -> etatplot()
  if graph_type == 'eta-t':
    dwcsvtreat()
    trioscsvtreat()
    rcparams()
    etatplot()

  # 2. If 'eta-delp' is selected, execute dwcsvtreat() -> trioscsvtreat() -> etatplot() -> etadelpplot()
  elif graph_type == 'eta-delp':
    dwcsvtreat()
    trioscsvtreat()
    rcparams()
    etatplot()
    etadelpplot()

  # 3. If 'gamma-sigma' is selected, execute trioscsvtreat() -> gammasigmaplot()
  elif graph_type == 'gamma-sigma':
    trioscsvtreat()
    rcparams()
    gammasigmaplot()

  # 4. If 'eta-gamma' is selected, execute dwcsvtreat() -> trioscsvtreat() -> etatplot() -> etagammaplot()
  elif graph_type == 'eta-gamma':
    trioscsvtreat()
    rcparams()
    etagammaplot()

if __name__ == "__main__":
  main()