import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import data
df=pd.read_csv('fcc-forum-pageviews.csv')

# Format the 'date' column
df['date']=pd.to_datetime(df['date'])

# Set 'date' column as index                             
df.set_index('date',inplace=True)

# Filter data
df=df[
    (df['value'] >= df['value'].quantile(0.025))&
    (df['value'] <= df['value'].quantile(0.975))
]

# Draw line chart
def draw_line_plot():
    plt.figure(figsize=(12,6))
    plt.plot(df.index,df['value'],color='red',linewidth=1)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.savefig('line_plot.png')
    
    return plt.gcf()

# Draw bar chart
def draw_bar_plot():
    # Prepare data
    df_bar=df.copy()
    df_bar['year']=df.index.year
    df_bar['month']=df.index.month

    # Average
    df_bar=df_bar.groupby(['year','month'])['value'].mean().unstack()

    # Draw
    df_bar.plot(kind='bar',figsize=(12,8),legend=True)
    plt.title('Average Daily Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months',labels=[
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'])
    plt.savefig('bar_plot.png')

    return plt.gcf()

# Draw Box Plot
def draw_box_plot():
    # Prepare data
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month

    # Sort by month
    df_box = df_box.sort_values('month_num')

    # Draw
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig
    