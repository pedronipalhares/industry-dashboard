import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from .charts import (
    create_line_chart, create_bar_chart, create_dual_line_chart,
    create_seasonal_analysis_chart, create_volume_yoy_growth_chart
)
from ..styles.theme import COLORS

def render_layer_herd_section(filtered_df):
    col1, col2 = st.columns(2)
    
    with col1:
        chart_data = filtered_df[['Date']].copy()
        chart_data["LTM Layer Herd"] = filtered_df["LTM_Layer_Herd"]
        chart = create_line_chart(
            chart_data, 'Date', 'LTM Layer Herd',
            "Layer Herd Analysis", 'Layer Herd (HEAD)'
        )
        st.altair_chart(chart, use_container_width=True)

    with col2:
        if len(filtered_df) > 12:
            filtered_df['YoY_Change'] = filtered_df['Layer_Herd'].pct_change(12) * 100
            yoy_data = pd.DataFrame({
                'Date': filtered_df['Date'],
                'YoY % Change': filtered_df['YoY_Change'],
                'Color': np.where(filtered_df['YoY_Change'] >= 0, 'Positive', 'Negative')
            })
            chart = create_bar_chart(
                yoy_data, 'Date', 'YoY % Change', 'Color',
                "Year-over-Year Change", 'Year-over-Year % Change'
            )
            st.altair_chart(chart, use_container_width=True)

def render_yield_mortality_section(filtered_yield_df, filtered_mortality_df):
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_yield_df.empty:
            yield_chart_data = filtered_yield_df[['Date']].copy()
            yield_chart_data["LTM Yield"] = filtered_yield_df["LTM_Yield"]
            chart = create_line_chart(
                yield_chart_data, 'Date', 'LTM Yield',
                "LTM Yield Analysis", 'Eggs per Layer'
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No yield data available for the selected time period.")

    with col2:
        if not filtered_mortality_df.empty:
            mortality_chart_data = filtered_mortality_df[['Date']].copy()
            mortality_chart_data["Mortality Rate"] = filtered_mortality_df["Mortality_Rate"]
            mortality_chart_data["LTM Mortality Rate"] = filtered_mortality_df["Mortality_Rate_LTM"]
            chart = create_dual_line_chart(
                mortality_chart_data, 'Date', 'Mortality Rate', 'LTM Mortality Rate',
                "Layer Mortality Rate Analysis", 'Mortality Rate (%)'
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No mortality data available for the selected time period.")

def render_egg_analysis_section(filtered_egg_break_df, filtered_egg_set_yoy):
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_egg_break_df.empty:
            egg_break_chart_data = filtered_egg_break_df[['Date']].copy()
            egg_break_chart_data["15-Month Rolling Break Ratio"] = filtered_egg_break_df["Rolling_15M_Break_Ratio"]
            egg_break_chart_data = egg_break_chart_data.dropna()
            
            if not egg_break_chart_data.empty:
                chart = create_line_chart(
                    egg_break_chart_data, 'Date', '15-Month Rolling Break Ratio',
                    "Egg Break Ratio Analysis", 'Egg Break Ratio (%)'
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("No 15-month rolling egg break ratio data available for the selected time period.")
        else:
            st.warning("No egg break data available for the selected time period.")

    with col2:
        if not filtered_egg_set_yoy.empty:
            filtered_egg_set_yoy['Color'] = np.where(filtered_egg_set_yoy['YoY_Growth'] >= 0, 'Positive', 'Negative')
            tooltip_fields = [
                alt.Tooltip('Date:T', title='Week'),
                alt.Tooltip('YoY_Growth:Q', format='.2f', title='YoY Growth (%)'),
                alt.Tooltip('Eggs Set:Q', format=',', title='Eggs Set'),
                alt.Tooltip('Previous Year Eggs Set:Q', format=',', title='Previous Year')
            ]
            chart = create_bar_chart(
                filtered_egg_set_yoy, 'Date', 'YoY_Growth', 'Color',
                "Egg Set Year-over-Year Growth", 'Year-over-Year Growth (%)',
                tooltip_fields=tooltip_fields
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No Egg Set YoY growth data available for the selected time period.")

def render_placement_hatchability_section(filtered_placement_yoy, filtered_hatchability_df):
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_placement_yoy.empty:
            filtered_placement_yoy['Color'] = np.where(filtered_placement_yoy['YoY_Growth'] >= 0, 'Positive', 'Negative')
            tooltip_fields = [
                alt.Tooltip('Date:T', title='Week'),
                alt.Tooltip('YoY_Growth:Q', format='.2f', title='YoY Growth (%)'),
                alt.Tooltip('Placements:Q', format=',', title='Placements'),
                alt.Tooltip('Previous Year Placements:Q', format=',', title='Previous Year')
            ]
            chart = create_bar_chart(
                filtered_placement_yoy, 'Date', 'YoY_Growth', 'Color',
                "Placement Year-over-Year Growth", 'Year-over-Year Growth (%)',
                tooltip_fields=tooltip_fields
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No Placement YoY growth data available for the selected time period.")

    with col2:
        if not filtered_hatchability_df.empty:
            chart = create_line_chart(
                filtered_hatchability_df, 'Date', 'Hatchability LTM (%)',
                "LTM Average Hatchability Rate", 'Hatchability Rate (%)'
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No hatchability data available for the selected time period.")

def render_slaughter_analysis_section(filtered_slaughter_data):
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_slaughter_data.empty:
            chart = create_seasonal_analysis_chart(filtered_slaughter_data)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No slaughter data available for the selected time period.")

    with col2:
        if not filtered_slaughter_data.empty:
            chart = create_volume_yoy_growth_chart(filtered_slaughter_data)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No slaughter volume data available for the selected time period.")

def render_chicken_weights_mortality_section(filtered_weights_data, filtered_mortality_data, filtered_pullet_data=None, filtered_pullet_yoy_data=None, filtered_pullet_monthly_yoy_data=None):
    st.markdown("---")
    
    # First row - Chicken weights and mortality rate
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_weights_data.empty:
            weights_chart_data = filtered_weights_data[['Date', 'LTM_Weight']].dropna().copy()
            
            if not weights_chart_data.empty:
                chart = create_line_chart(
                    weights_chart_data, 'Date', 'LTM_Weight',
                    "LTM Average Chicken Weights", 'Weight (LB/HEAD)'
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("No LTM weight data available for the selected time period.")
        else:
            st.warning("No weight data available for the selected time period.")
    
    with col2:
        if not filtered_mortality_data.empty:
            mortality_chart_data = filtered_mortality_data[['Date', 'Mortality_Rate']].dropna().copy()
            
            if not mortality_chart_data.empty:
                chart = create_line_chart(
                    mortality_chart_data, 'Date', 'Mortality_Rate',
                    "Chicken Mortality Rate Analysis", 'Mortality Rate (%)'
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.warning("No mortality rate data available for the selected time period.")
        else:
            st.warning("No mortality data available for the selected time period.")
    
    # Add a small spacing
    st.markdown("###")
    
    # Second row - Pullet flock size and YoY growth side by side
    if (filtered_pullet_data is not None and not filtered_pullet_data.empty) or (filtered_pullet_yoy_data is not None and not filtered_pullet_yoy_data.empty):
        pullet_col1, pullet_col2 = st.columns(2)
        
        # Potential pullet flock size chart
        with pullet_col1:
            if filtered_pullet_data is not None and not filtered_pullet_data.empty:
                # Since we now support both column names, try using the available one
                pullet_chart_data = filtered_pullet_data.copy()
                
                if 'Cumulative_Placements' in pullet_chart_data.columns:
                    placement_column = 'Cumulative_Placements'
                elif 'Cumulative_Potential_Placements' in pullet_chart_data.columns:
                    placement_column = 'Cumulative_Potential_Placements'
                    pullet_chart_data['Cumulative_Placements'] = pullet_chart_data[placement_column]
                    placement_column = 'Cumulative_Placements'
                else:
                    st.warning("No placement data found in the dataset.")
                    return
                
                # Use the projected date for x-axis if available
                date_column = 'Projected_Date' if 'Projected_Date' in pullet_chart_data.columns else 'Date'
                
                # Filter and prepare data for the chart
                pullet_chart_data = pullet_chart_data[[date_column, placement_column]].dropna().copy()
                
                if not pullet_chart_data.empty:
                    # Convert to millions for better readability
                    pullet_chart_data['Cumulative_Placements_Millions'] = pullet_chart_data[placement_column] / 1000000
                    
                    chart = create_line_chart(
                        pullet_chart_data, date_column, 'Cumulative_Placements_Millions',
                        "Potential Pullet Flock Size by Projected Date", 'Pullets (Millions)'
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning("No potential pullet flock size data available for the selected time period.")
            else:
                st.warning("No pullet flock size data available.")
        
        # YoY growth chart for potential pullet flock size
        with pullet_col2:
            if filtered_pullet_yoy_data is not None and not filtered_pullet_yoy_data.empty:
                pullet_yoy_chart_data = filtered_pullet_yoy_data.copy()
                
                # Ensure we have the YoY_Growth column
                if 'YoY_Growth' in pullet_yoy_chart_data.columns:
                    # Add color column based on positive or negative growth
                    pullet_yoy_chart_data['Color'] = np.where(pullet_yoy_chart_data['YoY_Growth'] >= 0, 'Positive', 'Negative')
                    
                    # Create tooltip fields
                    tooltip_fields = [
                        alt.Tooltip('Date:T', title='Date'),
                        alt.Tooltip('YoY_Growth:Q', format='.2f', title='YoY Growth (%)'),
                        alt.Tooltip('Cumulative_Potential_Placements:Q', format=',', title='Potential Placements'),
                        alt.Tooltip('Value_12M_Ago:Q', format=',', title='Previous Year')
                    ]
                    
                    # Create bar chart
                    chart = create_bar_chart(
                        pullet_yoy_chart_data, 'Date', 'YoY_Growth', 'Color',
                        "Potential Pullet Flock Size YoY Growth", 'Year-over-Year Growth (%)',
                        tooltip_fields=tooltip_fields
                    )
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning("No YoY growth data found for potential pullet flock size.")
            else:
                st.warning("No pullet flock YoY growth data available.")
    
    # Add a small spacing
    st.markdown("###")
    
    # Third row - Monthly pullet placements YoY growth
    if filtered_pullet_monthly_yoy_data is not None and not filtered_pullet_monthly_yoy_data.empty:
        # Ensure we have the YoY_Growth column
        if 'YoY_Growth' in filtered_pullet_monthly_yoy_data.columns:
            # Remove the redundant subheader to fix the double title issue
            
            # Create a copy of the data for manipulation
            monthly_yoy_data = filtered_pullet_monthly_yoy_data.copy()
            
            # Add color column based on positive or negative growth
            monthly_yoy_data['Color'] = np.where(monthly_yoy_data['YoY_Growth'] >= 0, 'Positive', 'Negative')
            
            # Create tooltip fields
            tooltip_fields = [
                alt.Tooltip('Date:T', title='Month'),
                alt.Tooltip('YoY_Growth:Q', format='.2f', title='YoY Growth (%)'),
                alt.Tooltip('Pullet Placements:Q', format=',', title='Pullet Placements'),
                alt.Tooltip('Value_12M_Ago:Q', format=',', title='Previous Year')
            ]
            
            # Create bar chart
            chart = create_bar_chart(
                monthly_yoy_data, 'Date', 'YoY_Growth', 'Color',
                "Monthly Pullet Placements YoY Growth", 'Year-over-Year Growth (%)',
                tooltip_fields=tooltip_fields
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No YoY growth data found for monthly pullet placements.") 