# bar_chart.py
"""
Bar chart visualization component for displaying sorting algorithm progress.
Handles rendering of bars with values and highlighting active elements.
"""

import pygame

from constants import (
    WHITE, GREEN, WINDOW_WIDTH, WINDOW_HEIGHT,
    TOP_MARGIN, BOTTOM_MARGIN, SIDE_MARGIN, VALUE_FONT_SIZE
)


class BarChart:
    """
    Visual representation of data as bars for sorting algorithm visualization.
    """

    def __init__(self, values):
        """
        Initialize the bar chart with given values.

        Args:
            values (list): List of values to visualize
        """
        self.values = values
        self.max_value = max(values) if values else 1
        self.active_indices = []
        self.font = pygame.font.SysFont('Arial', VALUE_FONT_SIZE)

    def set_active_indices(self, indices):
        """
        Set which bars should be highlighted as active.

        Args:
            indices (list): List of indices to highlight
        """
        self.active_indices = indices

    def render(self, surface):
        """
        Render the bar chart on the given surface.

        Args:
            surface (pygame.Surface): Surface to render the bars on
        """
        if not self.values:
            return

        bar_width = self._calculate_bar_width()
        draw_width = int(bar_width * 0.8)  # Leave some space between bars

        for i, value in enumerate(self.values):
            self._render_single_bar(surface, i, value, bar_width, draw_width)

    def _calculate_bar_width(self):
        """
        Calculate the width of each bar based on available space.

        Returns:
            float: Width of each bar in pixels
        """
        available_width = WINDOW_WIDTH - 2 * SIDE_MARGIN
        return available_width / len(self.values)

    def _render_single_bar(self, surface, index, value, bar_width, draw_width):
        """
        Render a single bar with its value.

        Args:
            surface (pygame.Surface): Surface to render on
            index (int): Index of the bar
            value (int): Value of the bar
            bar_width (float): Total width allocated for the bar
            draw_width (int): Actual drawing width of the bar
        """
        # Calculate bar dimensions
        bar_height = self._calculate_bar_height(value)
        x_pos = SIDE_MARGIN + index * bar_width
        y_pos = WINDOW_HEIGHT - BOTTOM_MARGIN - bar_height

        # Choose color based on whether the bar is active
        color = WHITE if index in self.active_indices else GREEN

        # Draw the bar
        pygame.draw.rect(surface, color, (x_pos, y_pos, draw_width, bar_height))

        # Draw the value above the bar
        self._render_value_label(surface, value, x_pos, y_pos, draw_width)

    def _calculate_bar_height(self, value):
        """
        Calculate the height of a bar based on its value.

        Args:
            value (int): Value to represent

        Returns:
            int: Height of the bar in pixels
        """
        available_height = WINDOW_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
        return int((value / self.max_value) * available_height)

    def _render_value_label(self, surface, value, x_pos, y_pos, bar_width):
        """
        Render the value label above a bar.

        Args:
            surface (pygame.Surface): Surface to render on
            value (int): Value to display
            x_pos (float): X position of the bar
            y_pos (float): Y position of the bar
            bar_width (int): Width of the bar
        """
        text_surface = self.font.render(str(value), True, GREEN)
        text_x = x_pos + bar_width // 2 - text_surface.get_width() // 2
        text_y = y_pos - 25
        surface.blit(text_surface, (text_x, text_y))
