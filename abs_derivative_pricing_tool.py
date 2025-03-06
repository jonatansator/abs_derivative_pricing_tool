import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

# Step 1: Generate synthetic ABS portfolio data
np.random.seed(42)
t = np.linspace(0, 5, 60)
cf = 1000 * (1 + 0.03 * np.random.randn(60))
swap_rate = 0.025
n_sims = 1000

# Step 2: Simulate interest rate paths
rates = []
for _ in range(n_sims):
    r = np.random.normal(0.02, 0.005, len(t))
    rates.append(r.cumsum() * 0.01 + 0.02)
rates = np.array(rates)

# Step 3: Calculate swap-adjusted cash flows
disc = np.exp(-rates * t)
pv_fixed = swap_rate * cf * disc
pv_float = rates * cf * disc
swap_vals = pv_fixed.mean(axis=0) - pv_float.mean(axis=0)

# Step 4: Compute sensitivities
delta = np.gradient(swap_vals, t)

# Step 5: Prepare data
df = pd.DataFrame({'Time': t, 'SwapValue': swap_vals, 'Delta': delta})

# Step 6: Create Plotly visualization
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Time'], y=df['SwapValue'], mode='lines', name='Swap Value',
    line=dict(color='#FF6B6B', width=2)
))
fig.add_trace(go.Scatter(
    x=df['Time'], y=df['Delta'], mode='lines', name='Delta (Forecast)',
    line=dict(color='#4ECDC4', width=2, dash='dash')
))

# Step 7: Apply dark theme and corrected axis styling
fig.update_layout(
    title=dict(
        text='ABS Derivative Pricing & Sensitivity',
        font=dict(family='Arial', size=16, color='white')
    ),
    xaxis=dict(
        title=dict(  # Nest title properties under 'title'
            text='Time (Years)',
            font=dict(family='Arial', size=14, color='white')  # Corrected
        ),
        tickfont=dict(family='Arial', size=12, color='white'),  # Direct property
        tickangle=-45,
        tickcolor='white',
        ticks='outside',
        ticklen=8,
        tickwidth=1,
        zeroline=True,
        zerolinecolor='rgba(255, 255, 255, 0.5)',
        zerolinewidth=1,
        gridcolor='rgba(255, 255, 255, 0.1)',
        gridwidth=0.5
    ),
    yaxis=dict(
        title=dict(
            text='Value / Delta',
            font=dict(family='Arial', size=14, color='white')
        ),
        tickfont=dict(family='Arial', size=12, color='white'),
        gridcolor='rgba(255, 255, 255, 0.1)',
        gridwidth=0.5
    ),
    plot_bgcolor='rgb(40, 40, 40)',
    paper_bgcolor='rgb(40, 40, 40)',
    margin=dict(l=50, r=50, t=50, b=50),
    showlegend=True
)

# Step 8: Display the plot
fig.show()

# Optional: Save results
df.to_csv('abs_derivative_results.csv', index=False)