import altair as alt
import pandas as pd
from ..styles.theme import COLORS
import numpy as np

def create_line_chart(data, x_col, y_col, title, y_title, color=COLORS['primary'], min_buffer=0.98, max_buffer=1.02):
    min_value = data[y_col].min() * min_buffer
    max_value = data[y_col].max() * max_buffer
    
    chart = alt.Chart(data).mark_line(
        strokeWidth=3,
        color=color
    ).encode(
        x=alt.X(f'{x_col}:T', title='Date'),
        y=alt.Y(f'{y_col}:Q', title=y_title, 
               scale=alt.Scale(domain=[min_value, max_value])),
        tooltip=[f'{x_col}:T', f'{y_col}:Q']
    ).properties(
        height=500,
        title=title
    ).interactive()
    
    return chart

def create_bar_chart(data, x_col, y_col, color_col, title, y_title, tooltip_fields=None):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f'{x_col}:T', title='Date', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y(f'{y_col}:Q', title=y_title),
        color=alt.Color(f'{color_col}:N', scale=alt.Scale(
            domain=['Positive', 'Negative'],
            range=[COLORS['positive'], COLORS['negative']]
        )),
        tooltip=tooltip_fields or [f'{x_col}:T', f'{y_col}:Q']
    ).properties(
        height=500,
        title=title
    ).interactive()
    
    # Add a reference line at 0%
    zero_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(
        color='black',
        strokeDash=[3, 3],
        opacity=0.5
    ).encode(y='y')
    
    return chart + zero_line

def create_dual_line_chart(data, x_col, y1_col, y2_col, title, y_title):
    min_value = min(
        data[y1_col].min(),
        data[y2_col].dropna().min() if not data[y2_col].dropna().empty else float('inf')
    ) * 0.95
    
    max_value = max(
        data[y1_col].max(),
        data[y2_col].dropna().max() if not data[y2_col].dropna().empty else 0
    ) * 1.05
    
    actual_line = alt.Chart(data).mark_line(
        strokeWidth=2,
        strokeDash=[3, 3],
        color=COLORS['primary'],
        opacity=0.7
    ).encode(
        x=alt.X(f'{x_col}:T', title='Date'),
        y=alt.Y(f'{y1_col}:Q', scale=alt.Scale(domain=[min_value, max_value])),
        tooltip=[f'{x_col}:T', f'{y1_col}:Q']
    )
    
    ltm_line = alt.Chart(data).mark_line(
        strokeWidth=3,
        color=COLORS['primary']
    ).encode(
        x=alt.X(f'{x_col}:T', title='Date'),
        y=alt.Y(f'{y2_col}:Q', title=y_title, scale=alt.Scale(domain=[min_value, max_value])),
        tooltip=[f'{x_col}:T', f'{y2_col}:Q']
    )
    
    return (actual_line + ltm_line).properties(
        height=500,
        title=title
    ).interactive()

def create_seasonal_analysis_chart(data):
    """Create a seasonal analysis chart with lines for the last three years"""
    # Get the last three years of data
    years = sorted(data['Date'].dt.year.unique(), reverse=True)[:3]
    
    # Prepare data for each year
    seasonal_data = []
    for year in years:
        year_data = data[data['Date'].dt.year == year].copy()
        year_data['Month'] = year_data['Date'].dt.strftime('%b')
        year_data['Volume_Millions'] = year_data['Volume'] / 1000000
        year_data['Year'] = year
        seasonal_data.append(year_data)
    
    # Combine all years' data
    seasonal_df = pd.concat(seasonal_data)
    
    # Calculate min and max with tighter buffer
    min_value = seasonal_df['Volume_Millions'].min() * 0.99  # Tighter buffer
    max_value = seasonal_df['Volume_Millions'].max() * 1.01  # Tighter buffer
    
    # Create the chart
    chart = alt.Chart(seasonal_df).mark_line(
        point=True  # Add points at each data point
    ).encode(
        x=alt.X('Month:N', 
                title='Month',
                sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
        y=alt.Y('Volume_Millions:Q',
                title='Volume (Million Head × lb)',
                scale=alt.Scale(domain=[min_value, max_value])),  # Set y-axis range
        color=alt.Color('Year:N', 
                       title='Year',
                       scale=alt.Scale(scheme='category10')),
        tooltip=[
            alt.Tooltip('Year:N'),
            alt.Tooltip('Month:N'),
            alt.Tooltip('Volume_Millions:Q', format=',.2f', title='Volume (M)')
        ]
    ).properties(
        height=500,
        title='Seasonal Analysis of Chicken Meat Production'
    ).interactive()
    
    return chart

def create_volume_yoy_growth_chart(data):
    """Create a YoY growth chart for chicken meat volume"""
    # Make a copy of the data
    chart_data = data.copy()
    
    # Calculate YoY growth correctly by comparing the same month of the previous year
    chart_data['Year'] = chart_data['Date'].dt.year
    chart_data['Month'] = chart_data['Date'].dt.month
    
    # Sort by date to ensure proper calculations
    chart_data = chart_data.sort_values('Date')
    
    # Calculate the YoY growth for each month compared to the same month of the previous year
    chart_data['Previous_Year_Volume'] = chart_data.groupby('Month')['Volume'].shift(1)
    chart_data['Volume_YoY_Growth'] = ((chart_data['Volume'] - chart_data['Previous_Year_Volume']) / 
                                      chart_data['Previous_Year_Volume'] * 100)
    
    # Filter out rows with NaN values
    chart_data = chart_data.dropna(subset=['Volume_YoY_Growth'])
    
    # Create color column for bars
    chart_data['Color'] = np.where(chart_data['Volume_YoY_Growth'] >= 0, 'Positive', 'Negative')
    
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Date:T', 
                title='Date',
                axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Volume_YoY_Growth:Q',
                title='Year-over-Year Growth (%)'),
        color=alt.Color('Color:N',
                       scale=alt.Scale(
                           domain=['Positive', 'Negative'],
                           range=[COLORS['positive'], COLORS['negative']]
                       )),
        tooltip=[
            alt.Tooltip('Date:T'),
            alt.Tooltip('Volume_YoY_Growth:Q', format='.2f', title='YoY Growth (%)'),
            alt.Tooltip('Volume:Q', format=',.0f', title='Volume (Head × lb)'),
            alt.Tooltip('Previous_Year_Volume:Q', format=',.0f', title='Previous Year Volume')
        ]
    ).properties(
        height=500,
        title='Year-over-Year Growth in Chicken Meat Production'
    ).interactive()
    
    # Add a reference line at 0%
    zero_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(
        color='black',
        strokeDash=[3, 3],
        opacity=0.5
    ).encode(y='y')
    
    return chart + zero_line 