# main.py
"""
Entry point for the sorting algorithm visualization application.
Contains the main function and sample data initialization.
"""

from visualization_app import SortingVisualizationApp


def main():
    """
    Main function to initialize and run the sorting visualization application.
    """
    # Sample values for visualization
    sample_values = [
        74, 19, 6, 58, 94, 42, 37, 22, 50, 3, 29, 95, 63, 81, 44, 1, 48, 86, 70, 15, 60, 13, 88, 32, 35, 71, 24, 26, 67,
        84, 9, 56, 8, 33, 99, 4, 97, 17, 20, 30, 38, 66, 92, 43, 25, 0, 100, 36, 28, 61, 11, 2, 14, 16, 52, 59, 5, 31,
        27, 47, 77, 73, 39, 41, 75, 85, 23, 7, 46, 96, 45, 12, 21, 10, 78, 93, 57, 49, 34, 18
    ]

    # Create and run the visualization application
    app = SortingVisualizationApp(sample_values)
    app.run()


if __name__ == "__main__":
    main()
