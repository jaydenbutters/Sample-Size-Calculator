# Sample Size Calculator - Streamlit App

A comprehensive statistical sample size calculator built with Streamlit that helps researchers, data scientists, and analysts determine the required sample size for surveys, experiments, and studies.

## Features

### Core Functionality
- **Sample Size Calculation**: Calculate required sample sizes based on:
  - Confidence levels (90%, 95%, 99%, 99.9%)
  - Margin of error (0.5% to 10%)
  - Population proportion
  - Optional finite population correction

### Interactive Visualizations
1. **Sensitivity Analysis**: Three interactive charts showing how sample size changes with:
   - Different margins of error
   - Various confidence levels
   - Population proportion variations

2. **Quick Reference Table**: Pre-calculated sample sizes for common confidence levels and error margins

### Educational Content
- Mathematical formulas displayed with LaTeX
- Detailed explanations of statistical concepts
- Use case examples

## Installation

1. Clone or download the files:
   - `sample_size_calculator.py`
   - `requirements.txt`

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

Execute the following command in your terminal:
```bash
streamlit run sample_size_calculator.py
```

The app will open in your default web browser at `http://localhost:8501`

## How to Use

### Basic Calculation
1. **Select Confidence Level**: Choose your desired confidence level (95% is standard)
2. **Set Margin of Error**: Adjust the slider to your acceptable error margin
3. **View Results**: The required sample size is displayed immediately

### Advanced Options
- **Population Proportion**: Adjust if you have prior knowledge about the population
  - Use 0.5 (default) for maximum sample size when uncertain
- **Finite Population Correction**: Enable if sampling from a known, limited population

### Interpreting Results

#### Example Scenarios:
- **Customer Satisfaction Survey**: 
  - 95% confidence, 5% margin of error = 384 samples needed
  
- **Product Quality Testing**: 
  - 99% confidence, 3% margin of error = 1,844 samples needed

- **Political Polling**: 
  - 95% confidence, 3% margin of error = 1,067 samples needed

## Statistical Background

### Formula for Infinite Population:
```
n = (z² × p × (1-p)) / e²
```

### Formula with Finite Population Correction:
```
n_adjusted = n / (1 + (n-1)/N)
```

Where:
- n = sample size
- z = z-score (based on confidence level)
- p = population proportion
- e = margin of error
- N = population size

### Z-Score Values:
- 90% confidence: 1.645
- 95% confidence: 1.96
- 99% confidence: 2.576
- 99.9% confidence: 3.291

## Key Features Explained

### Sensitivity Analysis
The app provides three interactive charts:
1. **Margin of Error Impact**: Shows inverse relationship between precision and sample size
2. **Confidence Level Comparison**: Visualizes how higher confidence requires larger samples
3. **Population Proportion Effect**: Demonstrates that p=0.5 yields maximum sample size

### Quick Reference Table
Pre-calculated values for common scenarios allow for quick lookups without manual calculation.

## Use Cases

- **Market Research**: Determine survey sample sizes
- **A/B Testing**: Calculate test group sizes
- **Quality Control**: Sample size for product inspection
- **Medical Studies**: Clinical trial participant numbers
- **Academic Research**: Thesis and dissertation sampling
- **Political Polling**: Voter survey requirements

## Tips for Best Results

1. **When in Doubt**: Use p=0.5 for conservative estimates
2. **Balance Cost vs. Precision**: Smaller margins of error exponentially increase sample size
3. **Consider Response Rates**: Calculate based on expected responses, not invitations
4. **Account for Subgroups**: If analyzing subgroups, ensure each has adequate sample size

## Troubleshooting

If the app doesn't run:
1. Ensure Python 3.8+ is installed
2. Check all dependencies are installed: `pip install -r requirements.txt`
3. Update Streamlit: `pip install --upgrade streamlit`

## License

This tool is provided as-is for educational and research purposes.
