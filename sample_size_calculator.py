import streamlit as st
import math
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Sample Size Calculator",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Statistical Sample Size Calculator")
st.markdown("""
Calculate the required sample size to achieve a desired confidence level and margin of error 
for your surveys, experiments, or research studies.
""")

# Create two columns for the main layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("Input Parameters")
    
    # Confidence level selection
    confidence_level = st.selectbox(
        "Confidence Level",
        options=[90, 95, 99, 99.9],
        index=1,
        help="The probability that the true value lies within the margin of error"
    )
    
    # Margin of error
    margin_of_error = st.slider(
        "Margin of Error (%)",
        min_value=0.5,
        max_value=10.0,
        value=5.0,
        step=0.5,
        help="The maximum expected difference between the true population parameter and sample estimate"
    )
    
    # Population proportion
    st.markdown("### Advanced Options")
    
    population_proportion = st.slider(
        "Population Proportion (p)",
        min_value=0.01,
        max_value=0.99,
        value=0.5,
        step=0.01,
        help="Expected proportion of the population with the characteristic of interest. Use 0.5 for maximum sample size (most conservative estimate)."
    )
    
    # Population size (optional)
    use_finite_population = st.checkbox("Use Finite Population Correction")
    
    population_size = None
    if use_finite_population:
        population_size = st.number_input(
            "Population Size",
            min_value=1,
            value=10000,
            help="Total size of the population you're sampling from"
        )

# Calculate Z-score based on confidence level
def get_z_score(confidence_level):
    z_scores = {
        90: 1.645,
        95: 1.96,
        99: 2.576,
        99.9: 3.291
    }
    return z_scores[confidence_level]

# Calculate sample size
def calculate_sample_size(confidence_level, margin_of_error, population_proportion, population_size=None):
    z = get_z_score(confidence_level)
    e = margin_of_error / 100  # Convert percentage to decimal
    p = population_proportion
    q = 1 - p
    
    # Basic sample size formula (infinite population)
    n = (z**2 * p * q) / e**2
    
    # Apply finite population correction if population size is provided
    if population_size:
        n_adjusted = n / (1 + (n - 1) / population_size)
        return math.ceil(n_adjusted)
    
    return math.ceil(n)

# Calculate the sample size
sample_size = calculate_sample_size(
    confidence_level, 
    margin_of_error, 
    population_proportion, 
    population_size
)

with col2:
    st.header("Results")
    
    # Display the calculated sample size
    st.metric(
        label="Required Sample Size",
        value=f"{sample_size:,}"
    )
    
    # Display formula used
    st.markdown("### Formula Used")
    if use_finite_population:
        st.latex(r"n = \frac{n_0}{1 + \frac{n_0 - 1}{N}}")
        st.latex(r"\text{where } n_0 = \frac{z^2 \times p \times (1-p)}{e^2}")
        st.markdown(f"""
        Where:
        - n = adjusted sample size
        - N = population size ({population_size:,})
        - z = z-score ({get_z_score(confidence_level)})
        - p = population proportion ({population_proportion})
        - e = margin of error ({margin_of_error}%)
        """)
    else:
        st.latex(r"n = \frac{z^2 \times p \times (1-p)}{e^2}")
        st.markdown(f"""
        Where:
        - n = sample size
        - z = z-score ({get_z_score(confidence_level)})
        - p = population proportion ({population_proportion})
        - e = margin of error ({margin_of_error}%)
        """)

# Sensitivity Analysis Section
st.header("📈 Sensitivity Analysis")

tab1, tab2, tab3 = st.tabs(["Margin of Error", "Confidence Level", "Population Proportion"])

with tab1:
    # Create a range of margin of errors
    margins = [i/2 for i in range(1, 21)]  # 0.5% to 10% in 0.5% increments
    sample_sizes_margin = []
    
    for margin in margins:
        size = calculate_sample_size(
            confidence_level,
            margin,
            population_proportion,
            population_size
        )
        sample_sizes_margin.append(size)
    
    # Create plot
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=margins,
        y=sample_sizes_margin,
        mode='lines+markers',
        name='Sample Size',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    # Add current value marker
    fig1.add_trace(go.Scatter(
        x=[margin_of_error],
        y=[sample_size],
        mode='markers',
        name='Current Selection',
        marker=dict(size=12, color='red', symbol='star')
    ))
    
    fig1.update_layout(
        title="Sample Size vs. Margin of Error",
        xaxis_title="Margin of Error (%)",
        yaxis_title="Required Sample Size",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    # Create different confidence levels
    confidence_levels = [90, 95, 99, 99.9]
    sample_sizes_conf = []
    
    for conf in confidence_levels:
        size = calculate_sample_size(
            conf,
            margin_of_error,
            population_proportion,
            population_size
        )
        sample_sizes_conf.append(size)
    
    # Create bar chart
    fig2 = go.Figure()
    colors = ['#1f77b4' if cl != confidence_level else 'red' for cl in confidence_levels]
    
    fig2.add_trace(go.Bar(
        x=[f"{cl}%" for cl in confidence_levels],
        y=sample_sizes_conf,
        marker_color=colors,
        text=sample_sizes_conf,
        textposition='outside'
    ))
    
    fig2.update_layout(
        title="Sample Size by Confidence Level",
        xaxis_title="Confidence Level",
        yaxis_title="Required Sample Size",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    # Create a range of population proportions
    proportions = [i/100 for i in range(5, 100, 5)]
    sample_sizes_prop = []
    
    for prop in proportions:
        size = calculate_sample_size(
            confidence_level,
            margin_of_error,
            prop,
            population_size
        )
        sample_sizes_prop.append(size)
    
    # Create plot
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=proportions,
        y=sample_sizes_prop,
        mode='lines+markers',
        name='Sample Size',
        line=dict(color='#2ca02c', width=2),
        marker=dict(size=6)
    ))
    
    # Add current value marker
    fig3.add_trace(go.Scatter(
        x=[population_proportion],
        y=[sample_size],
        mode='markers',
        name='Current Selection',
        marker=dict(size=12, color='red', symbol='star')
    ))
    
    fig3.update_layout(
        title="Sample Size vs. Population Proportion",
        xaxis_title="Population Proportion (p)",
        yaxis_title="Required Sample Size",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.info("💡 **Note:** p = 0.5 gives the maximum sample size (most conservative estimate)")

# Comparison Table
st.header("📋 Quick Reference Table")

# Create a comparison table
error_margins = [1, 2, 3, 4, 5, 7, 10]
conf_levels = [90, 95, 99]

data = []
for conf in conf_levels:
    for error in error_margins:
        size = calculate_sample_size(conf, error, 0.5, None)
        data.append({
            'Confidence Level': f"{conf}%",
            'Margin of Error': f"±{error}%",
            'Sample Size': f"{size:,}"
        })

df = pd.DataFrame(data)
pivot_df = df.pivot(index='Margin of Error', columns='Confidence Level', values='Sample Size')

st.dataframe(pivot_df, use_container_width=True)

# Additional Information
with st.expander("ℹ️ Understanding Sample Size Calculations"):
    st.markdown("""
    ### Key Concepts:
    
    **Confidence Level:** The probability that the true population parameter lies within the confidence interval. 
    Common values are 95% (standard) and 99% (more conservative).
    
    **Margin of Error:** The range of values above and below the sample statistic in a confidence interval. 
    For example, a 5% margin of error means the true value is within ±5% of your sample estimate.
    
    **Population Proportion:** The expected proportion of the population with a certain characteristic. 
    When unknown, use 0.5 for the most conservative (largest) sample size.
    
    **Finite Population Correction:** Applied when sampling from a small, known population. 
    This reduces the required sample size since you're sampling a significant portion of the total population.
    
    ### When to Use:
    - **Market Research:** Determining how many customers to survey
    - **Quality Control:** Sampling products for inspection
    - **A/B Testing:** Calculating test group sizes
    - **Medical Studies:** Determining clinical trial participant numbers
    - **Political Polling:** Surveying voters for election predictions
    """)

# Footer
st.markdown("---")
st.markdown("📊 **Sample Size Calculator** | Built with Streamlit")
