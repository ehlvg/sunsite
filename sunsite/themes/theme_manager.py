import yaml
import os
import json
from pathlib import Path

class ThemeManager:
    def __init__(self, config_path=None):
        self.config_path = config_path
        self.default_theme = {
            'accent_color': '#3498db',
            'font': 'Inter',
            'roundness': 'medium',
            'shadows': True,
        }
        self.theme = self.default_theme.copy()
        
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path):
        """Load theme configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            if 'theme' in config:
                self.theme.update(config['theme'])
        except Exception as e:
            print(f"Error loading theme config: {e}")
    

    def get_css_variables(self):
        """Generate CSS variables from theme settings"""
        variables = []
        
        # Color variables
        color = self.theme['accent_color']
        variables.append(f"--accent-color: {color};")
        variables.append(f"--accent-color-light: {self._lighten_color(color, 0.2)};")
        variables.append(f"--accent-color-dark: {self._darken_color(color, 0.2)};")
        variables.append(f"--accent-color-very-light: {self._lighten_color(color, 0.8)};")
        
        # Font variables
        font = self.theme['font']
        variables.append(f"--primary-font: '{font}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;")
        
        # Roundness variables
        roundness = {
            'none': '0',
            'small': '4px',
            'medium': '8px',
            'large': '16px',
        }.get(self.theme['roundness'], '8px')
        variables.append(f"--border-radius: {roundness};")
        
        # Shadow variables
        shadow = "0 4px 6px rgba(0, 0, 0, 0.1)" if self.theme['shadows'] else "none"
        variables.append(f"--box-shadow: {shadow};")
        
        return "\n  ".join(variables)
    
    def get_google_fonts_url(self):
        """Generate Google Fonts URL for the chosen font"""
        font = self.theme['font'].replace(' ', '+')
        return f"https://fonts.googleapis.com/css2?family={font}:wght@400;500;700&display=swap"
    
    def _lighten_color(self, color, amount):
        """Lighten a hex color by the given amount (0-1)"""
        # This is a simple implementation. A more robust one would use proper color manipulation
        if color.startswith('#'):
            color = color[1:]
        
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        r = min(255, int(r + (255 - r) * amount))
        g = min(255, int(g + (255 - g) * amount))
        b = min(255, int(b + (255 - b) * amount))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _darken_color(self, color, amount):
        """Darken a hex color by the given amount (0-1)"""
        if color.startswith('#'):
            color = color[1:]
        
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        r = max(0, int(r * (1 - amount)))
        g = max(0, int(g * (1 - amount)))
        b = max(0, int(b * (1 - amount)))
        
        return f"#{r:02x}{g:02x}{b:02x}"
