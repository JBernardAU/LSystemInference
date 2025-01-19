
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator


def plot_histogram(data, bins=10, title="Histogram", xlabel="Value", ylabel="Frequency",
                   color="blue", alpha=0.7, edgecolor="black", density=False):
    """
    General-purpose function to plot a histogram.

    Parameters:
        data (array-like): The data to plot.
        bins (int or sequence): Number of bins or bin edges.
        title (str): Title of the histogram.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        color (str): Color of the bars.
        alpha (float): Transparency level of the bars (0 to 1).
        edgecolor (str): Color of the bar edges.
        density (bool): If True, normalize the histogram.

    Returns:
        None
    """
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, color=color, alpha=alpha, edgecolor=edgecolor, density=density)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    ax = plt.gca()  # Get current axes
    ax.xaxis.set_major_locator(MultipleLocator(1))  # Ticks every 1 unit on x-axis
    plt.tight_layout()  # Adjust layout to avoid overlap
    plt.show()

def plot_dictionary_histogram(data, bins=10, title="Histogram", xlabel="Value", ylabel="Frequency",
                   color="blue", alpha=0.7, edgecolor="black", density=False):
    # Create the plot
    plt.figure(figsize=(10, 6))  # Set figure size for better readability
    plt.bar(data.keys(), data.values(), color='skyblue')
    # Customize the plot
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    ax = plt.gca()  # Get current axes
    ax.xaxis.set_major_locator(MultipleLocator(1))  # Ticks every 1 unit on x-axis
    plt.tight_layout()  # Adjust layout to avoid overlap
    plt.show()


# Example usage:
if __name__ == "__main__":
    # Generate random data
    data = np.random.normal(loc=0, scale=1, size=1000)

    # Plot the histogram
    plot_histogram(
        data,
        bins=20,
        title="Normal Distribution Histogram",
        xlabel="Values",
        ylabel="Frequency",
        color="green",
        alpha=0.75,
        density=True
    )