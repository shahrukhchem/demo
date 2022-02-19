# -*- coding: utf-8 -*-
"""
Created on Sun May  9 00:52:51 2021

@author: Shahrukh
"""
#nurses_pandas.ipynb

import docplex.mp
import pandas as pd
import xlrd
from pandas import DataFrame
data_url = "https://github.com/IBMDecisionOptimization/docplex-examples/blob/master/examples/mp/jupyter/nurses_data.xls?raw=true"
nurse_xls_file = pd.ExcelFile(data_url)
#preparing df
#nurse_xls_file.parse()
#nurse_xls_file.read
nurse_xls_file.sheet_names  #Get names of all Sheets 
'''['Departments',
 'Skills',
 'Shifts',
 'SkillRequirements',
 'Nurses',
 'NurseSkills',
 'NurseVacations',
 'NurseAssociations',
 'NurseIncompatibilities']'''
df_skills=nurse_xls_file.parse('Skills')
df_depts = nurse_xls_file.parse('Departments')
df_shifts = nurse_xls_file.parse('Shifts')
df_shifts.index.name = 'shiftId'
df_nurse_skills = nurse_xls_file.parse('NurseSkills')
df_vacations = nurse_xls_file.parse('NurseVacations')
df_associations = nurse_xls_file.parse('NurseAssociations')
df_incompatibilities = nurse_xls_file.parse('NurseIncompatibilities')  
df_nurses = nurse_xls_file.parse('Nurses', header=0, index_col=0)
# maximum work time (in hours)
max_work_time = 40

# maximum number of shifts worked in a week.
max_nb_shifts = 5
#We start by adding an extra column dow (day of week) which converts the string "day" into an integer in 0..6 (Monday is 0, Sunday is 6).
days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
days_of_week=dict(zip(days,range(0,7)))
#Convering days of week to number in data frame
def days_of_week_from_day(day):
    day=day.lower()
    return(days_of_week[day])

df_shifts['dow']=df_shifts.day.apply(days_of_week_from_day)
df_shifts['w_start']=df_shifts.start_time+24*df_shifts.dow

def calculate_endtime(start,end,dow):
    return(24*dow+end+(24 if start>end else 0))
df_shifts['w_end']=df_shifts.apply(lambda x: calculate_endtime(x.start_time,x.end_time,x.dow),axis=1)

#compute_duration_of_each_shift
df_shifts['duration']=df_shifts.w_end-df_shifts.w_start

#Compute Minimum demand in nurse-hour
df_shifts['min-demand']=df_shifts.min_req*df_shifts.duration

#SETUP CPLEX
from docplex.mp.environment import Environment
env=Environment()
env.print_information()

from docplex.mp.model import Model
m = Model(name="nurses_scheduling")


all_nurses = df_nurses.index.values  #global collections to iterate upon
all_shifts = df_shifts.index.values  #global collections to iterate upon

#if a particular nurse is assighned in a shift we declare binary variable 

assigned = m.binary_var_matrix(keys1=all_nurses, keys2=all_shifts, name="assign_%s_%s")

df_assigned = DataFrame({'assigned': assigned})
df_assigned.index.names=['all_nurses', 'all_shifts']
df_assigned_pivot = df_assigned.unstack(level='all_shifts') #Conver into matrix #Open the df
# Create a Data Frame representing a list of shifts sorted by wstart and duration.
# One keeps only the three relevant columns: 'shiftId', 'wstart' and 'wend' in the resulting Data Frame 
df_sorted_shifts=df_shifts.sort_values(['w_start','duration']).reset_index()[['shiftId', 'w_start', 'w_end']]

number_of_incompatible_shift_constraints = 0
for shift in df_sorted_shifts.itertuples() : #itertuple gives an iteratuble tuple for data frame
    #print(shift)
    for shift_2 in df_sorted_shifts.iloc[shift[0] + 1:].itertuples(): #iloc integer based location selection 
        #print(shift_2)
        if (shift_2.w_start < shift.w_end):
            #starting & ending time should not overlap 
            for nurse_assignments in df_assigned_pivot.iloc[:,[shift.shiftId, shift_2.shiftId]].itertuples():
                m.add_constraint(nurse_assignments[1] + nurse_assignments[2] <= 1)
                print(nurse_assignments)
                number_of_incompatible_shift_constraints += 1
            


# Add 'day of week' column to vacations Data Frame
df_vacations['dow'] = df_vacations.day.apply(days_of_week_from_day)

df_assigned_reindexed = df_assigned.reset_index()
df_shifts=df_shifts.reset_index()
a=df_shifts[['dow', 'shiftId']]
abc=df_vacations.merge(a,how="inner")
df_vacation_forbidden_assignments=abc.merge(df_assigned_reindexed, left_on=['nurse', 'shiftId'], right_on=['all_nurses', 'all_shifts'])

for forbidden_assignment in df_vacation_forbidden_assignments.itertuples():
    # to forbid an assignment just set the variable to zero.
    #print(forbidden_assignment)
    m.add_constraint(forbidden_assignment.assigned == 0)


print("# vacation forbids: {} assignments".format(len(df_vacation_forbidden_assignments)))












