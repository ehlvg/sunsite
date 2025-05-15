#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

def init_project(args):
    """Initialize a new sunsite project"""
    project_dir = Path(args.directory)
    
    if project_dir.exists() and not args.force:
        print(f"Directory {args.directory} already exists. Use --force to overwrite.")
        return

    # Create project structure
    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(project_dir / "content", exist_ok=True)
    os.makedirs(project_dir / "static", exist_ok=True)
    os.makedirs(project_dir / "templates", exist_ok=True)
    
    # Create config file
    config = """# Sunsite Configuration
title: My Sunsite
description: A site built with sunsite
theme:
  accent_color: "#3498db"
  font: "Inter"
  roundness: "medium"  # none, small, medium, large
  shadows: true
"""
    with open(project_dir / "sunsite.yaml", "w") as f:
        f.write(config)
    
    # Create example content
    example_md = """---
title: Welcome to Sunsite
---

# Welcome to Sunsite

This is an example page created with sunsite.

## Features

- Markdown support
- Custom theming
- Semantic HTML
"""
    with open(project_dir / "content" / "index.md", "w") as f:
        f.write(example_md)
    
    print(f"Project initialized at {args.directory}")

def build_site(args):
    """Build the static site from markdown files"""
    from sunsite import build_site as build
    output = build(project_dir=".", output_dir=args.output)
    print(f"Site built successfully at {output}")


def serve_site(args):
    """Serve the site locally for development"""
    from sunsite.utils.server import serve
    
    # Создаем объект с атрибутом output для build_site
    class BuildArgs:
        def __init__(self, output_dir="_site"):
            self.output = output_dir
    
    # Вызываем build_site с правильными аргументами
    build_site(BuildArgs())
    
    # Serve the built site
    serve(directory="_site", port=args.port)


def create_page(args):
    """Create a new page from template"""
    page_path = Path(args.name)
    if not page_path.parent.exists():
        os.makedirs(page_path.parent, exist_ok=True)
    
    icon = args.icon or ""
    
    content = f"""---
title: {args.title or page_path.stem.title()}
icon: {icon}
---

# {args.title or page_path.stem.title()}

Content goes here.
"""
    with open(page_path, "w") as f:
        f.write(content)
    
    print(f"Created new page at {args.name}")


def main():
    parser = argparse.ArgumentParser(description="sunsite - Static site generator from markdown")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("directory", default=".", nargs="?", help="Project directory")
    init_parser.add_argument("--force", "-f", action="store_true", help="Force initialization even if directory exists")
    
    # build command
    build_parser = subparsers.add_parser("build", help="Build the static site")
    build_parser.add_argument("--output", "-o", default="_site", help="Output directory")
    
    # serve command
    serve_parser = subparsers.add_parser("serve", help="Serve the site locally")
    serve_parser.add_argument("--port", "-p", type=int, default=8000, help="Port to serve on")
    
    # new command
    new_parser = subparsers.add_parser("new", help="Create a new page")
    new_parser.add_argument("name", help="Page name (path relative to content directory)")
    new_parser.add_argument("--title", "-t", help="Page title")
    new_parser.add_argument("--icon", "-i", help="Page icon (emoji)")

    args = parser.parse_args()

    if args.command == "init":
        init_project(args)
    elif args.command == "build":
        build_site(args)
    elif args.command == "serve":
        serve_site(args)
    elif args.command == "new":
        create_page(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
