# visualization_app.py
"""
Main application class for the sorting algorithm visualization.
Coordinates the UI, animation, and sorting algorithms.
"""

import copy
import sys

import pygame

from bar_chart import BarChart
from button import Button
from constants import (
    BLACK, GREEN, BLUE, RED, PURPLE, LIGHT_GRAY,
    WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT,
    BUTTON_SPACING, BOTTOM_MARGIN, ANIMATION_DELAY, FPS
)
from sorting_algorithms import SortingAlgorithms


class SortingVisualizationApp:
    """
    Main application class that manages the sorting visualization interface.
    """

    def __init__(self, values):
        """
        Initialize the visualization application.

        Args:
            values (list): Initial values to sort and visualize
        """
        self.original_values = copy.deepcopy(values)
        self.current_values = copy.deepcopy(values)

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.clock = pygame.time.Clock()
        self.buffer = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Initialize components
        self.bar_chart = BarChart(self.current_values)
        self.buttons = self._create_sorting_buttons()
        self.reset_button = self._create_reset_button()

        # Animation state
        self.sorting_generator = None
        self.is_sorting = False
        self.animation_counter = 0

    def _create_sorting_buttons(self):
        """
        Create buttons for different sorting algorithms.

        Returns:
            list: List of Button objects for sorting algorithms
        """
        button_configs = [
            ("Bubble Sort", GREEN),
            ("Merge Sort", BLUE),
            ("Quick Sort", RED),
            ("Bucket Sort", PURPLE)
        ]

        buttons = []
        total_width = len(button_configs) * BUTTON_WIDTH + (len(button_configs) - 1) * BUTTON_SPACING
        start_x = (WINDOW_WIDTH - total_width) // 2
        button_y = WINDOW_HEIGHT - BOTTOM_MARGIN // 2

        for i, (text, color) in enumerate(button_configs):
            x_pos = start_x + i * (BUTTON_WIDTH + BUTTON_SPACING)
            button = Button(x_pos, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, text, color)
            buttons.append(button)

        return buttons

    def _create_reset_button(self):
        """
        Create the reset button.

        Returns:
            Button: Reset button object
        """
        return Button(WINDOW_WIDTH - 100, 10, 80, 30, "Reset", LIGHT_GRAY)

    def _set_active_indices(self, indices):
        """
        Callback function to set active indices for visualization.

        Args:
            indices (list): List of indices to highlight
        """
        self.bar_chart.set_active_indices(indices)

    def _start_sorting_algorithm(self, algorithm_name):
        """
        Start the specified sorting algorithm.

        Args:
            algorithm_name (str): Name of the sorting algorithm to start
        """
        algorithm_map = {
            "Bubble Sort": SortingAlgorithms.bubble_sort_generator,
            "Merge Sort": SortingAlgorithms.merge_sort_generator,
            "Quick Sort": SortingAlgorithms.quick_sort_generator,
            "Bucket Sort": SortingAlgorithms.bucket_sort_generator
        }

        if algorithm_name in algorithm_map:
            self.sorting_generator = algorithm_map[algorithm_name](
                self.current_values, self._set_active_indices
            )
            self.is_sorting = True
            self._set_buttons_active(False)

    def _set_buttons_active(self, active):
        """
        Set the active state of all sorting buttons.

        Args:
            active (bool): Whether buttons should be active
        """
        for button in self.buttons:
            button.set_active(active)

    def _reset_visualization(self):
        """
        Reset the visualization to its initial state.
        """
        self.current_values = copy.deepcopy(self.original_values)
        self.bar_chart = BarChart(self.current_values)
        self.bar_chart.set_active_indices([])
        self.sorting_generator = None
        self.is_sorting = False
        self.animation_counter = 0
        self._set_buttons_active(True)

    def _handle_button_clicks(self, mouse_pos):
        """
        Handle button click events.

        Args:
            mouse_pos (tuple): Mouse position (x, y)
        """
        # Handle reset button (always active)
        if self.reset_button.handle_click(mouse_pos):
            self._reset_visualization()
            return

        # Handle sorting buttons (only when not sorting)
        if not self.is_sorting:
            for button in self.buttons:
                if button.handle_click(mouse_pos):
                    self._start_sorting_algorithm(button.text)
                    break

    def _update_sorting_animation(self):
        """
        Update the sorting animation by advancing one step.
        """
        if not self.is_sorting or not self.sorting_generator:
            return

        # Control animation speed
        self.animation_counter += 1
        if self.animation_counter < ANIMATION_DELAY:
            return

        self.animation_counter = 0

        try:
            next(self.sorting_generator)
        except StopIteration:
            # Sorting completed
            self.bar_chart.set_active_indices([])
            self.sorting_generator = None
            self.is_sorting = False
            self._set_buttons_active(True)

    def _render(self):
        """
        Render all visual components to the screen.
        """
        # Clear buffer
        self.buffer.fill(BLACK)

        # Render components
        self.bar_chart.render(self.buffer)

        for button in self.buttons:
            button.render(self.buffer)

        self.reset_button.render(self.buffer)

        # Transfer buffer to screen
        self.screen.blit(self.buffer, (0, 0))
        pygame.display.flip()

    def run(self):
        """
        Main game loop for the visualization application.
        """
        running = True

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_button_clicks(event.pos)

            # Update animation
            self._update_sorting_animation()

            # Render
            self._render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
