# Sunsite

_Static site generator from Markdown_

Sunsite allows you to quickly and easily create beautiful static websites based on Markdown files. With a flexible theme, customizable configuration, and a convenient CLI, you can focus on your content instead of routine setup.

## Features

- Generate HTML from Markdown using Jinja2 templates
- Customizable theme (colors, fonts, border radius, shadows)
- Simple directory structure: `content`, `static`, `templates`
- Local development server with automatic rebuild
- Create new pages via CLI

## Quick Start

### 1. Installation

Clone the repository and install the package:

```bash
git clone https://github.com/yourusername/sunsite.git
cd sunsite
pip install .
```

Or install from PyPI:

```bash
pip install sunsite
```

### 2. Initialize a Project

```bash
sunsite init my_site
```

This will create the structure:

```
my_site/
├── content/
│   └── index.md
├── static/
├── templates/
├── sunsite.yaml
```

### 3. Configuration

The `sunsite.yaml` file contains the main settings:

```yaml
title: My Sunsite
description: Example site on Sunsite
theme:
  accent_color: "#3498db"
  font: "Inter"
  roundness: "medium" # none, small, medium, large
  shadows: true
```

### 4. Build the Site

```bash
cd my_site
sunsite build -o _site
```

The generated site will be in the `_site` folder.

### 5. Local Development Server

```bash
sunsite serve -p 8000
```

Open `http://localhost:8000` in your browser to view and automatically rebuild on changes.

### 6. Create a New Page

```bash
sunsite new content/about.md -t "About Us" -i "ℹ️"
```

This will create the file `content/about.md` with a title and metadata.

## Project Structure

```text
.
├── content/       # Markdown files
├── static/        # CSS, JS, images
├── templates/     # Jinja2 templates (base.html, page.html)
├── sunsite.yaml   # Project configuration
└── _site/         # Generated site (after build)
```

## Advanced Features

- Customize your templates in the `templates` folder
- Add static resources to `static`
- Change the theme via `sunsite.yaml` parameters
