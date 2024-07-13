import json
import math
import numpy as np
from scipy.stats import norm

maxY = 0  # Global variable


# Function to generate normal distribution data
def generate_normal_distribution(mean=15, stdDev=50, numPoints=100):
    data = []
    step = 1
    global maxY
    # Define the x range to cover a broader interval
    x = np.linspace(norm.ppf(0.001, loc=mean, scale=stdDev), norm.ppf(0.999, loc=mean, scale=stdDev), numPoints)
    # Calculate the y values for the normal distribution
    y = np.round(norm.pdf(x, loc=mean, scale=stdDev), 5)
    # y = norm(3, 1).pdf(x)
    maxY = max(y)

    # Transforming the array
    data = [{"x": idx, "y": value} for idx, value in enumerate(y)]
    # print(transformed_array)
    return data


# Function for generating gradient bars
def generate_bars(numBars=100):
    global maxY
    data = []
    step = 1
    for i in range(0, numBars + 1, step):
        x = i / (numBars / 100)
        y = -0.04 * maxY
        data.append({'x': x, 'y': y})

    return data


# Generate anotations at the bottom
def generate_annotations(start=0, end=35, color="rgba(0, 255, 0, 0.1)", text=["Most individuals have", "average risk"]):
    return {
        "type": "box",
        "xMin": start,
        "xMax": end,
        "yMin": -0.4 * maxY,
        "yMax": -0.04 * maxY,
        "backgroundColor": color,
        "borderWidth": 0,
        "label": {
            "display": True,
            "content": text,
            "position": "center",
            "color": "black",
            "textAlign": "center",
            "font": {
                "size": 12,
                "weight": "bold"
            }
        }
    }


# Generate gradient colors for bar charts
def generate_gradient_colors(total_steps, opacity):
    """
    Generate an array of colors in a gradient from green to red with specified opacity.

    Args:
    total_steps (int): The total number of steps in the gradient.
    opacity (float): The opacity of the colors (between 0 and 1).

    Returns:
    list: A list of colors in RGBA format.
    """
    if not (0 <= opacity <= 1):
        raise ValueError("Opacity must be between 0 and 1.")

    colors = []
    for idx in range(total_steps + 1):
        # Calculate the ratio of the current position
        ratio = idx / (total_steps - 1)

        # Calculate the red and green components
        red = int(255 * ratio)
        green = int(255 * (1 - ratio))

        # Format the color as an rgba string
        color = f'rgba({red}, {green}, 0, {opacity})'
        colors.append(color)

    return colors


# Draw line with your score and label
def draw_your_score(score, low=["Somewhat low", "Your risk is withing the 0th percentile"],
                    medium=["Medium", "Your risk is withing the 0th percentile"],
                    high=["Somewhat high", "Your risk is withing the 0th percentile"]):
    global maxY
    if score < 35:
        content = low
        color = "green"
        bg = "rgba(255, 255, 255, 0.9)"
    elif score < 65:
        content = medium
        color = "yellow"
        bg = "rgba(255, 255, 255, 0.9)"
    else:
        content = high
        color = "red"
        bg = "rgba(255, 255, 255, 0.9)"
    return {
        "type": "line",
        "xMin": score,
        "xMax": score,
        "yMin": 0,
        "yMax": maxY,
        "borderColor": "black",
        "borderWidth": 2,
        "label": {
            "display": True,
            "content": content,
            "position": "middle",
            "backgroundColor": bg,
            "color": color,
            "font": {
                "size": 12
            },
            "padding": {
                "top": 5,
                "bottom": 5,
                "left": 10,
                "right": 10
            },
            "cornerRadius": 4,
            "borderColor": color,
            "borderWidth": 2,
        }
    }


# Generates ChartJS config for the risk score chart
def generate_risk_score_chartjs(mean=50, stdDev=15, numPoints=101, score=30, lang='lv'):
    global maxY

    score = int(score)

    if score > 100:
        score = 100
    if score < 0:
        score = 0

    # Generate the normal distribution data
    normal_data = generate_normal_distribution(mean, stdDev, numPoints)
    numbars = 100
    bar_data = generate_bars(numbars)
    bgs = generate_gradient_colors(numbars, 0.7)
    max_yaxis = maxY * 1.03

    if lang == 'lv':

        title = "Poligēnā riska grafiks"
        label_low = ["Zems", "Jūsu risks ir " + str(score) + " percentiles robežās"]
        label_medium = ["Vidējs", "Jūsu risks ir " + str(score) + " percentiles robežās"]
        label_high = ["Augsts", "Jūsu risks ir " + str(score) + " percentiles robežās"]

        anotation_low = generate_annotations(-0.5, 35, color="rgba(0, 255, 0, 0.2)",
                                             text=["Mazāk indivīdiem ir", "pazemināts risks"])

        anotation_medium = generate_annotations(35, 65, color="rgba(255, 255, 0, 0.2)",
                                                text=["Vairumam indivīdu ir", "vidējs risks"])

        anotation_high = generate_annotations(65, 100, color="rgba(255, 0, 0, 0.2)",
                                              text=["Mazāk indivīdiem ir", "augsts risks"])
        x_label = 'Percentile'
    else:
        title = "Polygenic risk chart"
        label_low = ["Somewhat low", "Your risk is withing the " + str(score) + "th percentile"]
        label_medium = ["Medium", "Your risk is withing the " + str(score) + "th percentile"]
        label_high = ["Somewhat high", "Your risk is withing the " + str(score) + "th percentile"]

        anotation_low = generate_annotations(-0.5, 35, "rgba(0, 255, 0, 0.2)",
                                             ["Fewer individuals have", "decreased risk"])

        anotation_medium = generate_annotations(35, 65, "rgba(255, 255, 0, 0.2)",
                                                ["Most individuals have", "average risk"])

        anotation_high = generate_annotations(65, 100, "rgba(255, 0, 0, 0.2)",
                                              ["Fewer individuals have", "high risk"])
        x_label = 'Percentile'
    # Create the Chart.js configuration
    config = {
        'type': 'bar',  # Base type
        'data': {
            'labels': [d['x'] for d in normal_data],
            'datasets': [
                # Normal distribution line
                {
                    'type': 'line',
                    'data': [d['y'] for d in normal_data],
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 2,
                    'fill': 'origin',
                    'backgroundColor': 'rgba(128, 128, 128, 0.5)',
                    'pointRadius': 0,
                    'tension': 0.4  # Smooth the line
                },
                # Gradient bar charts
                {
                    'type': 'bar',
                    # 'data': [d['y'] for d in bar_data],
                    'data': bar_data,
                    'backgroundColor': bgs,
                    'borderWidth': 0,  # Remove the border
                    'barPercentage': 0.9999,  # Slightly less than 1.0 to avoid overlap and gaps
                    'categoryPercentage': 0.9999,  # Slightly less than 1.0 to avoid overlap and gaps
                }
            ]
        },
        'options': {
            'responsive': True,
            'scales': {
                'x': {
                    'type': 'linear',
                    'position': 'bottom',
                    'title': {
                        'display': True,
                        'text': x_label
                    },
                    'ticks': {
                        'min': 0,  # Ensure the x-axis starts at 0
                        'max': 100,
                        'stepSize': 10
                    },
                    "min": 0,
                    "max": 100,
                    'grid': {
                        'drawOnChartArea': True,  # Ensure the x-axis grid is drawn
                        'drawTicks': True,
                        'offset': False
                    }
                },
                "y": {"beginAtZero": True, "display": False, "min": -0.2 * maxY, "max": max_yaxis}
            },
            'plugins': {
                'legend': {
                    'display': False  # Turn off legend display
                },
                'title': {
                    'display': True,
                    'text': title,
                    'font': {
                        'size': 16,
                        'weight': 'bold'
                    },
                    'color': '#000',
                    'padding': 10
                },
                'annotation': {
                    'annotations': {
                        'score': draw_your_score(score, low=label_low, medium=label_medium, high=label_high),
                        'lowRisk': anotation_low,
                        'mediumRisk': anotation_medium,
                        'highRisk': anotation_high,
                    }
                },
                'tooltip': {
                    'enabled': False  # Disable tooltips
                }
            }
        }
    }
    return config

# Generate the Chart.js configuration as a JSON string
# chart_config_json = generate_chartjs_config(score=30, lang='lv')
# print(chart_config_json)
