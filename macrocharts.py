#%%
import pandas as pd
import matplotlib.pyplot as plt
from xbbg import blp
import seaborn as sns
import matplotlib.dates as mdates

#%%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import pandas as pd

def plot_custom_line_chart(df, title=None, secondary=None, labels=None):
    """
    Plots a line chart with specific styling: Arial 9pt, no borders/grid,
    horizontal y-labels on top, and datetime formatting.

    Parameters:
    - df: Pandas DataFrame (Index must be Datetime).
    - title: String (optional).
    - secondary: List of column names to plot on the secondary Y-axis (optional).
    - labels: List or Dict of custom names for the legend (optional).
    """
    
    # 1. Setup Global Font Configuration (Arial, Size 9)
    # Note: If Arial is not installed on the system, Matplotlib will fallback to default sans-serif.
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 9
    plt.rcParams['axes.labelsize'] = 9
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['axes.titlesize'] = 9

    # Create Figure and Primary Axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # 2. Data Preparation
    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except Exception as e:
            print("Error: DataFrame index could not be converted to Datetime.")
            return

    # Identify primary vs secondary columns
    secondary_cols = secondary if secondary else []
    primary_cols = [col for col in df.columns if col not in secondary_cols]

    # Handle Labels (Map columns to custom labels if provided as a dict/list)
    # If labels is a list, we assume order matches columns [primary..., secondary...]
    legend_map = {}
    if isinstance(labels, dict):
        legend_map = labels
    elif isinstance(labels, list):
        all_cols = primary_cols + secondary_cols
        legend_map = dict(zip(all_cols, labels))

    # 3. Plotting Primary Data
    lines = []
    for col in primary_cols:
        label = legend_map.get(col, col)
        # Plot and track the line object for the combined legend later
        line_plot = ax.plot(df.index, df[col], label=label, linewidth=2)
        lines.extend(line_plot)

    # 4. Plotting Secondary Data (if applicable)
    if secondary_cols:
        ax2 = ax.twinx()
        for i, col in enumerate(secondary_cols):
            label = legend_map.get(col, col)
            # Use a different style or color sequence for secondary
            line_plot = ax2.plot(df.index, df[col], label=label, 
                                 linewidth=2, linestyle='--', color=f'C{i+len(primary_cols)}')
            lines.extend(line_plot)
            
        # Clean secondary axis styling
        ax2.grid(False)
        for spine in ax2.spines.values():
            spine.set_visible(False)
        ax2.tick_params(axis='y', length=0) # Hide tick marks
        
        # Secondary Y-Axis Label placement (Horizontal, Top)
        ax2.set_ylabel("", loc='top', rotation=0)

    # 5. X-Axis Formatting
    # Display in Year format
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Optional: Locate by year if data is dense
    ax.xaxis.set_major_locator(mdates.YearLocator())
    
    # 6. "Extra space at the end" logic
    # Calculate time span to add a proportional pad (e.g., 5%)
    min_date = df.index.min()
    max_date = df.index.max()
    time_span = max_date - min_date
    padding = time_span * 0.05 
    
    # Set limit: Left is min date, Right is max date + padding
    ax.set_xlim(left=min_date, right=max_date + padding)

    # 7. Y-Axis Formatting (Primary)
    # "Place labels horizontally, not vertically, and on top of the y-axis"
    # This aligns the axis title to the top and rotates it 0 degrees.
    ax.set_ylabel("", loc='top', rotation=0)
    
    # Ensure tick labels are horizontal (default is usually horizontal, but forcing it)
    ax.tick_params(axis='y', labelrotation=0, length=0) # length=0 hides tick marks for cleaner look

    # 8. Visual Cleanup (No borders, No gridlines)
    ax.grid(False)
    
    # Remove spines (the borders)
    # We remove Top, Right, Left. We usually keep Bottom for the timeline, 
    # but strictly "no borders" might imply removing that too. 
    # Here I remove the box, but keep the axis line for the timeline for readability.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False) # Hides the Y-axis line
    ax.spines['bottom'].set_visible(True) # Keep bottom line for dates styling
    # Color the bottom spine grey for a softer look
    ax.spines['bottom'].set_color('#DDDDDD')

    # 9. Title and Legend
    if title:
        plt.title(title, loc='left', pad=20, fontweight='bold')

    # Combine legends from both axes
    all_labels = [l.get_label() for l in lines]
    plt.legend(lines, all_labels, frameon=False, loc='best')

    plt.tight_layout()
    plt.show()

    
#%%
data = blp.bdh(
    tickers=['SPX Index', 'VIX Index', 'USGG10YR Index'],
    flds=['PX_LAST'])
data.columns = ['S&P 500', 'VIX', 'US 10Y Yield']
data = data.dropna()

# %%
fig, ax = plot_line_chart(
    data.loc[:,['S&P 500', 'US 10Y Yield']],
    secondary=['US 10Y Yield'],
    title='S&P 500 with VIX and US 10Y Yield',
    label='Date',
)

# %%
