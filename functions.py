#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import the modules that we need for analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Create a function to generate a countplot for one categorical variable
# it should provide a dataset as 'df', a name of categorical variable as 'vb' and number of color as 'i'.
def count_plot_one_vb(df, vb , i):
    base_color = sns.color_palette()[i]
    sns.countplot(data = df, x = vb, color = base_color)
    plt.xlabel(vb.upper())
    plt.ylabel('Number of patients \n ')
    plt.title('Number of patients by '+ vb +' \n',fontsize=16)
    # add annotations
    n_points = df.shape[0]
    gen_counts = df[vb].value_counts()
    locs, labels = plt.xticks() # get the current tick locations and labels

    # loop through each pair of locations and labels
    for loc, label in zip(locs, labels):

        # get the text property for the label to get the correct count
        count = gen_counts[label.get_text()]
        pct_string = '{:0.1f}%'.format(100*count/n_points)

        # print the annotation just below the top of the bar
        plt.text(loc, count-8, pct_string, ha = 'center', fontsize=11, color = 'black')
    return 


# In[3]:


# Create a funtion with 3 arguments >> (dataframe as 'df', variable 1 as 'vb1' and variable 2 as 'vb2') to generate:
# 1)- a pivot table between the two variables,
# 2)- a rate bar chart with:
# - the first variable as 'vb1' in horizontal axis(x),
# - the second variable as 'vb2' proportion in (y) axis, and show in legend),
# -- this function concerns only categorical variables --
def rate_bar_chart_2vb(df, vb1,vb2):
    """  
    Creates a pivot table between the two variables and a rate bar chart. 
    Parameters:
    - df (Pandas Dataframe): dataframe containing the data
    - vb1: column in the dataframe (categorical)
    - vb2: column in the dataframe(categorical)
    """
    # pivot-table 
    df_by_vb_count = df.pivot_table(index = vb1, columns = vb2, values = 'age', aggfunc = 'count',margins = True)
    #rate bar chart
    df_by_vb = pd.crosstab(df[vb1], df[vb2], normalize = 'index')
    df_by_vb = np.round((df_by_vb * 100), decimals=2)
    ax = df_by_vb.plot.bar(figsize=(10,5));
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:3.0f}%'.format(x) for x in vals]);
    ax.set_xticklabels(df_by_vb.index,rotation = 0, fontsize = 15);
    ax.set_title('\n '+ vb2.upper() + ' (%) by ' + df_by_vb.index.name + '\n', fontsize = 15)
    ax.set_xlabel(df_by_vb.index.name.upper(), fontsize = 12)
    ax.set_ylabel('(Percentage %)', fontsize = 12)
    ax.legend(loc = 'upper left',bbox_to_anchor=(1.0,1.0), fontsize= 12)
    rects = ax.patches
    # Add Data Labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, 
                height + 2, 
                str(height)+'%', 
                ha='center', 
                va='bottom',
                fontsize = 12)   
    return  df_by_vb_count 


# In[4]:


# Create a funtion with 2 arguments >> (datafram as 'df' and binary variable as 'vb') to generate:
# 1)- a pivot table between the appointment variable and the binary variable in arguments,
# 2)- stacked bar chart with:
# - the variable 'vb' in horizontal axis(x),
# - the 'appointment' variable in (y) axis.

def stacked_bar_appointment_with_vb(df, vb):
    # pivot table 'gender' by 'appointment' 
    group_vb_all= df.pivot_table(index = vb, columns = 'appointment', values = 'age', aggfunc = 'count',margins = True)
    
    # plot
    group_vb = pd.pivot_table(df,index = vb, columns = 'appointment', values = 'age',aggfunc = 'count')
    ind = range(len(df[vb].value_counts()))
    width = 0.8
    p1=plt.bar(ind, group_vb.Show, width)
    p2 = plt.bar(ind, group_vb['No Show'], width)
    plt.legend(['Show','No Show'])
    plt.xticks(ind, group_vb.index)
    plt.ylabel('Number of patients')
    plt.title('Number of patients (Show/No Show) appointment by ' + vb + '\n ', fontsize=16)
    
    return group_vb_all

