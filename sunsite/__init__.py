import os
import yaml
import shutil
from pathlib import Path
from .parser.markdown_parser import MarkdownParser
from .themes.theme_manager import ThemeManager
from .generator.page_generator import PageGenerator

def build_site(project_dir=".", output_dir="_site"):
    """Build a static site from markdown files"""
    project_dir = Path(project_dir)
    output_dir = Path(output_dir)
    content_dir = project_dir / "content"
    templates_dir = project_dir / "templates"
    static_dir = project_dir / "static"
    config_file = project_dir / "sunsite.yaml"
    
    # Load config
    if not config_file.exists():
        print(f"Config file not found at {config_file}")
        return
    
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    
    # Initialize components
    theme_manager = ThemeManager(config_file)
    parser = MarkdownParser()
    generator = PageGenerator(theme_manager, templates_dir=str(templates_dir))
    
    # Clean output directory
    if output_dir.exists():
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy static files
    if static_dir.exists():
        shutil.copytree(static_dir, output_dir, dirs_exist_ok=True)
    
    # Build site data
    site_data = {
        'title': config.get('title', 'Sunsite'),
        'description': config.get('description', ''),
        'navigation': [],
    }
    
    # Process markdown files
    markdown_files = list(content_dir.glob("**/*.md"))
    
    # First pass: collect navigation items
    for md_file in markdown_files:
        rel_path = md_file.relative_to(content_dir)
        url_path = "/" + str(rel_path).replace(".md", ".html")
        
        # Use index.html for index.md
        if rel_path.name == "index.md":
            if rel_path.parent == Path("."):
                url_path = "/"
            else:
                url_path = "/" + str(rel_path.parent) + "/"
        
        # Parse frontmatter for nav info
        page_data = parser.parse_file(md_file)
        
        # Skip if hidden in nav
        if page_data['metadata'].get('hide_in_nav', False):
            continue
        
        # Add to navigation
        site_data['navigation'].append({
            'title': page_data['metadata'].get('nav_title', page_data['metadata'].get('title', rel_path.stem.title())),
            'url': url_path,
            'weight': page_data['metadata'].get('nav_weight', 999)
        })
    
    # Sort navigation by weight
    site_data['navigation'].sort(key=lambda x: x['weight'])
    
    # Second pass: generate HTML
    for md_file in markdown_files:
        rel_path = md_file.relative_to(content_dir)
        output_path = output_dir / rel_path.with_suffix(".html")
        
        # Use index.html for index.md
        if rel_path.name == "index.md":
            if rel_path.parent == Path("."):
                output_path = output_dir / "index.html"
            else:
                os.makedirs(output_dir / rel_path.parent, exist_ok=True)
                output_path = output_dir / rel_path.parent / "index.html"
        
        # Parse and generate
        page_data = parser.parse_file(md_file)
        generator.generate_page(page_data, output_path, site_data)
        
        print(f"Generated {output_path}")
    
    return output_dir