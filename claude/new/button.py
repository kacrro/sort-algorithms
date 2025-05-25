# button.py
"""
Button component for the sorting visualization application.
Handles button rendering, state management, and click detection.
"""

import pygame

from constants import BLACK, GRAY


class Button:
    """
    A clickable button with hover effects and active/inactive states.
    """

    def __init__(self, x, y, width, height, text, color):
        """
        Initialize the button.

        Args:
            x (int): X position of the button
            y (int): Y position of the button
            width (int): Width of the button
            height (int): Height of the button
            text (str): Text to display on the button
            color (tuple): RGB color of the button
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = self._darken_color(color)
        self.text = text
        self.font = pygame.font.SysFont('Arial', 18)
        self.is_active = True

    def _darken_color(self, color, amount=50):
        """
        Create a darker version of the given color for hover effect.

        Args:
            color (tuple): RGB color tuple
            amount (int): Amount to darken the color

        Returns:
            tuple: Darkened RGB color tuple
        """
        return tuple(max(0, c - amount) for c in color)

    def render(self, surface):
        """
        Render the button on the given surface.

        Args:
            surface (pygame.Surface): Surface to render the button on
        """
        if not self.is_active:
            self._render_inactive(surface)
            return

        color = self._get_current_color()

        # Draw button background
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        # Draw button text
        self._render_text(surface)

    def _render_inactive(self, surface):
        """
        Render the button in inactive state.

        Args:
            surface (pygame.Surface): Surface to render the button on
        """
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        self._render_text(surface)

    def _get_current_color(self):
        """
        Get the current color based on hover state.

        Returns:
            tuple: RGB color tuple
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.hover_color if self.rect.collidepoint(mouse_x, mouse_y) else self.color

    def _render_text(self, surface):
        """
        Render the button text centered on the button.

        Args:
            surface (pygame.Surface): Surface to render the text on
        """
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_click(self, mouse_pos):
        """
        Check if the button was clicked at the given position.

        Args:
            mouse_pos (tuple): Mouse position (x, y)

        Returns:
            bool: True if the button was clicked and is active
        """
        return self.is_active and self.rect.collidepoint(mouse_pos)

    def set_active(self, active):
        """
        Set the active state of the button.

        Args:
            active (bool): Whether the button should be active
        """
        self.is_active = active
