import matplotlib.pyplot as plt
# import numpy as np
import argparse
import os

def create_skill_will_quadrant(employee_data, output_file='/app/output/skill_will_quadrant'):
    """
    Create a skill/will quadrant chart for team members.

    Parameters:
    - employee_data: List of tuples with (name, skill_score, will_score, is_internal)
    - output_file: Base name for the output file (without extension)
    """

    names, skill_score, will_scores, prev_skill_scores, prev_will_scores, is_internal = _extract_employee_data(employee_data)
    _create_chart(employee_data, f"{output_file}_with_names", name_handler=_add_name_labels)
    _create_chart(employee_data, f"{output_file}_without_names", name_handler=None)


def _add_name_labels(ax, name, will, skill, prev_will, prev_skill):
    ax.annotate(name, (will, skill), xytext=(5, 5), textcoords='offset points')
    #do not annotate both nodes

def _create_chart(employee_data, output_file, name_handler=None):
    ax = _setup_plot()
    _plot_employee(ax, employee_data, name_handler)
    _add_quadrant_labels(ax)
    _add_chart_labels(ax)
    _add_legend(ax)
    _save_chart(output_file)
    print(f"Chart saved as {output_file}.png and {output_file}.pdf")

    # Don't show the plot when running in Docker
    plt.close()

def _extract_employee_data(employee_data):
    names = [emp[0] for emp in employee_data]
    skill_scores = [emp[1] for emp in employee_data]
    will_scores = [emp[2] for emp in employee_data]
    prev_skill_scores = [emp[3] for emp in employee_data]
    prev_will_scores = [emp[4] for emp in employee_data]
    is_internal = [emp[5] for emp in employee_data]
    return names, skill_scores, will_scores, prev_skill_scores, prev_will_scores, is_internal

def _setup_plot():
    # Create figure and axis
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111)

    # Set limits for both axes
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    _hide_labels(ax)

    # Add central grid lines
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)

    # Add background grid
    ax.grid(True, linestyle='--', alpha=0.3)

    return ax

def _plot_employee(ax, employee_data, name_handler=None):
    for name, skill, will, prev_skill, prev_will, internal in employee_data:
        # Determine shape and color based on internal/external status
        marker = 'o' if internal else 's'  # Circle for internal, Square for external
        color = 'blue' if internal else 'red'

        # Plot the point
        ax.scatter(will, skill, s=100, marker=marker, color=color)

        # Plot the previous point with an arrow
        if (prev_skill != skill or prev_will != will):
            ax.annotate("",
                xy=(will, skill),  # arrow tip
                xytext=(prev_will, prev_skill),  # arrow base
                arrowprops=dict(
                    arrowstyle="->",
                    color="gray" if internal else "darkred",
                    lw=1.5,
                    alpha=0.7
                    )
                )

        if name_handler:
            name_handler(ax, name, will, skill, prev_skill, prev_will)

def _add_quadrant_labels(ax):
    ax.text(120, 50, "High Will\nHigh Skill", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightgreen', alpha=0.3))
    ax.text(-120, 50, "Low Will\nHigh Skill", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightyellow', alpha=0.3))
    ax.text(120, -50, "High Will\nLow Skill", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightyellow', alpha=0.3))
    ax.text(-120, -50, "Low Will\nLow Skill", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightcoral', alpha=0.3))

def _add_chart_labels(ax):
    ax.set_xlabel('Will', fontsize=14)
    ax.set_ylabel('Skill', fontsize=14)
    ax.set_title('Skill/Will Quadrant', fontsize=16)

def _add_legend(ax):
    internal_marker = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Internal')
    external_marker = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10, label='External')
    ax.legend(handles=[internal_marker, external_marker], loc='lower left')

def _save_chart(output_file):
    plt.savefig(f'{output_file}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{output_file}.pdf', bbox_inches='tight')

def read_csv_data(csv_path):
    """Read employee data from a CSV file."""
    import csv
    employee_data = []

    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header row if exists

            for row in reader:
                if len(row) >= 4:
                    name = row[0]
                    skill = float(row[1])
                    will = float(row[2])
                    prev_skill = float(row[3])
                    prev_will = float(row[4])
                    is_internal = row[5].lower() in ['true', 'yes', '1', 'internal']
                    employee_data.append((name, skill, will, prev_skill, prev_will, is_internal))

        if not employee_data:
            print("No valid data found in CSV. Using sample data.")
            employee_data = get_sample_data()

    except Exception as e:
        print(f"Error reading CSV: {e}")
        print("Using sample data instead.")
        employee_data = get_sample_data()

    return employee_data

def get_sample_data():
    return [
        ("Alice", 80, 90, 70, 80, True),
        ("Bob", -30, 70, -10, 60, True),
        ("Charlie", 60, -40, 30, -20, True),
        ("Diana", -50, -60, -70, -80, True),
        ("Eve", 10, 20, 10, 10, False),
        ("Frank", -20, 30, -30, 10, False)
    ]

def _hide_labels(ax):
    # Hide the tick labels (numbers) on both axes
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Hide the tick marks themselves
    ax.set_xticks([])
    ax.set_yticks([])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a Skill/Will Quadrant Chart')
    parser.add_argument('--csv', help='Path to CSV file with employee data', default=None)
    args = parser.parse_args()

    if args.csv:
        employee_data = read_csv_data(args.csv)
    else:
        employee_data = get_sample_data()

    create_skill_will_quadrant(employee_data)
