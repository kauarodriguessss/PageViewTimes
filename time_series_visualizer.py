import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates and set the index to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data by removing the top and bottom 2.5% of page views.
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month_name()
    df_bar['Month_Number'] = df_bar.index.month

    # Create a pivot table for the bar plot
    df_bar_pivot = df_bar.pivot_table(
        values='value',
        index='Year',
        columns='Month_Number',
        aggfunc='mean'
    )

    # Reorder the columns to have months in calendar order
    df_bar_pivot = df_bar_pivot.sort_index(axis=1)

    # Rename the columns to month names
    df_bar_pivot.columns = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Draw bar plot
    fig = df_bar_pivot.plot(
        kind='bar',
        figsize=(15, 10),
        xlabel='Years',
        ylabel='Average Page Views'
    ).figure
    plt.legend(title='Months')
    plt.xticks(rotation=45)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = df_box['date'].dt.year
    df_box['Month'] = df_box['date'].dt.strftime('%b')
    df_box['Month_Num'] = df_box['date'].dt.month

    # Sort the dataframe by Month_Num to get months in order
    df_box = df_box.sort_values('Month_Num')

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))

    # Year-wise Box Plot (Trend)
    sns.boxplot(
        x='Year',
        y='value',
        data=df_box,
        ax=axes[0]
    )
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(
        x='Month',
        y='value',
        data=df_box,
        ax=axes[1]
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Adjust the layout
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig