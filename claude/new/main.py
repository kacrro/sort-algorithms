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
        10, 8, 15, 12, 4, 1, 22, 18, 5, 7,
        3, 6, 14, 11, 9, 2, 13, 20, 19, 17, 16
    ]

    # Create and run the visualization application
    app = SortingVisualizationApp(sample_values)
    app.run()


if __name__ == "__main__":
    main()
