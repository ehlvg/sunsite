import frontmatter
import markdown
import re
from pathlib import Path

class MarkdownParser:
    def __init__(self, extensions=None):
        self.extensions = extensions or [
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.attr_list',
        ]
        self.md = markdown.Markdown(extensions=self.extensions)
    
    def parse_file(self, file_path):
        """Parse a markdown file with frontmatter"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.parse_content(content, file_path)
    
    def parse_content(self, content, file_path=None):
        """Parse markdown content string with frontmatter"""
        post = frontmatter.loads(content)
        metadata = post.metadata
        
        # Add default values for required metadata
        if 'title' not in metadata and file_path:
            metadata['title'] = Path(file_path).stem.title()
        
        # Process content - remove the first h1 heading if it matches the title
        # to avoid duplication
        content_without_title = post.content
        title_pattern = fr'^# {re.escape(metadata["title"])}\s*\n'
        content_without_title = re.sub(title_pattern, '', content_without_title, count=1, flags=re.MULTILINE)
        
        html_content = self.md.convert(content_without_title)
        
        return {
            'metadata': metadata,
            'content': html_content,
            'toc': getattr(self.md, 'toc', ''),
        }