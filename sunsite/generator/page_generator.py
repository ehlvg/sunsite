import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class PageGenerator:
    def __init__(self, theme_manager, templates_dir="templates"):
        self.theme_manager = theme_manager
        self.templates_dir = templates_dir
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default templates if they don't exist"""
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Create base template
        base_template_path = Path(self.templates_dir) / "base.html"
        if not base_template_path.exists():
            base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if page.metadata.title %}{{ page.metadata.title }} - {% endif %}{{ site.title }}</title>
    <meta name="description" content="{{ page.metadata.description or site.description }}">
    
    <!-- Google Fonts -->
    <link rel="stylesheet" href="{{ theme.google_fonts_url }}">
    
    <!-- Styles -->
    <style>
    :root {
      {{ theme.css_variables }}
    }
    
    body {
      font-family: var(--primary-font);
      line-height: 1.6;
      margin: 0;
      padding: 0;
      color: #333;
      background-color: #fff;
    }
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1rem;
    }
    
    header {
      background-color: var(--accent-color);
      color: white;
      padding: 1rem 0;
      box-shadow: var(--box-shadow);
      max-width: 1200px;
      margin: 0.5rem auto;
      border-radius: var(--border-radius);
    }

    header .container {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    header h1 {
      margin: 0;
      font-size: 1.8rem;
    }
    
    nav {
      display: flex;
      gap: 1.5rem;
    }
    
    nav a {
      color: white;
      text-decoration: none;
      padding: 0.5rem 0.8rem;
      border-radius: var(--border-radius);
      transition: background-color 0.2s;
    }
    
    nav a:hover {
      background-color: rgba(255, 255, 255, 0.2);
      text-decoration: none;
    }
    
    main {
      padding: 2rem 0;
    }

    article {
        padding: 2rem;
        background-color: #fff;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        margin-bottom: 2rem;
      }
    
    .page-header {
      margin-bottom: 2rem;
      color: black;
      background-color: transparent;
      box-shadow: none;
      padding: 0;
    }
    
    .page-header h1 {
      margin-top: 0;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .page-icon {
      font-size: 1.5em;
    }
    
    footer {
      background-color: #f5f5f5;
      padding: 1rem 0;
      margin-top: 2rem;
      border-top: 1px solid #eee;
    }
    
    a {
      color: var(--accent-color);
      text-decoration: none;
    }
    
    a:hover {
      text-decoration: underline;
    }
    
    .btn {
      display: inline-block;
      background-color: var(--accent-color);
      color: white;
      padding: 0.5rem 1rem;
      border-radius: var(--border-radius);
      box-shadow: var(--box-shadow);
      transition: all 0.2s ease;
    }
    
    .btn:hover {
      background-color: var(--accent-color-dark);
      text-decoration: none;
    }
    
    img {
      max-width: 100%;
      height: auto;
      border-radius: var(--border-radius);
      box-shadow: var(--box-shadow);
    }
    
    @media (max-width: 768px) {
      header .container {
        flex-direction: column;
        align-items: flex-start;
      }
      
      nav {
        margin-top: 1rem;
        flex-wrap: wrap;
      }
      
      h1 {
        font-size: 2rem;
      }
      
      h2 {
        font-size: 1.5rem;
      }
    }
    </style>
    
    {% block head %}{% endblock %}
</head>
<body>
    <header>
        <div class="container">
            <h1>{{ site.title }}</h1>
            <nav>
                <a href="/">Home</a>
                {% for item in site.navigation %}
                <a href="{{ item.url }}">{{ item.title }}</a>
                {% endfor %}
            </nav>
        </div>
    </header>
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; {{ site.title }} - Built with sunsite</p>
        </div>
    </footer>
</body>
</html>
"""
            with open(base_template_path, "w") as f:
                f.write(base_template)
        
        # Create page template
        page_template_path = Path(self.templates_dir) / "page.html"
        if not page_template_path.exists():
            page_template = """{% extends "base.html" %}

{% block content %}
    <article>
        <header class="page-header">
            <h1>
                {% if page.metadata.icon %}<span class="page-icon">{{ page.metadata.icon }}</span>{% endif %}
                {{ page.metadata.title }}
            </h1>
        </header>
        
        <div class="content">
            {{ page.content | safe }}
        </div>
    </article>
{% endblock %}
"""
            with open(page_template_path, "w") as f:
                f.write(page_template)
    
    def generate_page(self, page_data, output_path, site_data=None):
        """Generate an HTML page from parsed markdown data"""
        site_data = site_data or {
            'title': 'Sunsite',
            'description': 'A site built with sunsite',
            'navigation': [],
        }
        
        # Prepare theme data
        theme_data = {
            'css_variables': self.theme_manager.get_css_variables(),
            'google_fonts_url': self.theme_manager.get_google_fonts_url(),
        }
        
        # Render the page template
        template = self.env.get_template("page.html")
        html = template.render(
            page=page_data,
            site=site_data,
            theme=theme_data
        )
        
        # Write to output file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        return output_path