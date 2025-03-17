import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

def create_skill_will_quadrant(employee_data, output_file='/app/output/skill_will_quadrant'):
    """
    Create a skill/will quadrant chart for team members.

    Parameters:
    - employee_data: List of tuples with (name, skill_score, will_score, is_internal)
    - output_file: Base name for the output file (without extension)
    """
    # Extract data
    names = [emp[0] for emp in employee_data]
    skill_scores = [emp[1] for emp in employee_data]
    will_scores = [emp[2] for emp in employee_data]
    is_internal = [emp[3] for emp in employee_data]

    # Create figure and axis
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111)

    # Set limits for both axes
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    # Add grid lines
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.3)

    # Plot data points with different markers for internal vs external employees
    internals = []
    externals = []
    for i, (name, skill, will, internal) in enumerate(employee_data):
        marker = 'o' if internal else 's'  # Circle for internal, Square for external
        color = 'blue' if internal else 'red'
        ax.scatter(skill, will, s=100, marker=marker, color=color)
        ax.annotate(name, (skill, will), xytext=(5, 5), textcoords='offset points')

        if internal:
            internals.append((name, marker, color))
        else:
            externals.append((name, marker, color))

    # Add quadrant labels with background colors
    ax.text(50, 50, "High Skill\nHigh Will", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightgreen', alpha=0.3))
    ax.text(-50, 50, "Low Skill\nHigh Will", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightyellow', alpha=0.3))
    ax.text(50, -50, "High Skill\nLow Will", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightyellow', alpha=0.3))
    ax.text(-50, -50, "Low Skill\nLow Will", ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightcoral', alpha=0.3))

    # Set axis labels and title
    ax.set_xlabel('Skill', fontsize=14)
    ax.set_ylabel('Will', fontsize=14)
    ax.set_title('Team Performance: Skill/Will Quadrant', fontsize=16)

    # Add legend to distinguish internal vs external employees
    internal_marker = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Internal')
    external_marker = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=10, label='External')
    ax.legend(handles=[internal_marker, external_marker], loc='upper right')

    # Save as PNG and PDF
    plt.savefig(f'{output_file}.png', dpi=300, bbox_inches='tight')
    plt.savefig(f'{output_file}.pdf', bbox_inches='tight')

    print(f"Chart saved as {output_file}.png and {output_file}.pdf")

    # Don't show the plot when running in Docker
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a Skill/Will Quadrant Chart')
    parser.add_argument('--csv', help='Path to CSV file with employee data', default=None)
    args = parser.parse_args()
    
    if args.csv:
        import csv
        employee_data = []
        try:
            with open(args.csv, 'r') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # Skip header row if exists
                for row in reader:
                    if len(row) >= 4:
                        name = row[0]
                        skill = float(row[1])
                        will = float(row[2])
                        is_internal = row[3].lower() in ['true', 'yes', '1', 'internal']
                        employee_data.append((name, skill, will, is_internal))
            
            if not employee_data:
                print("No valid data found in CSV. Using sample data.")
                employee_data = get_sample_data()
                
        except Exception as e:
            print(f"Error reading CSV: {e}")
            print("Using sample data instead.")
            employee_data = get_sample_data()
    else:
        employee_data = get_sample_data()
    
    create_skill_will_quadrant(employee_data)

def get_sample_data():
    # Sample data: (name, skill_score, will_score, is_internal)
    return [
        ("Alice", 80, 90, True),
        ("Bob", -30, 70, True),
        ("Charlie", 60, -40, True),
        ("Diana", -50, -60, True),
        ("Eve", 10, 20, False),
        ("Frank", -20, 30, False)
    ]
