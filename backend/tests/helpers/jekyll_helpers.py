"""
Helper utilities for validating Jekyll output.
"""
import os
import yaml
from pathlib import Path


def validate_jekyll_config(config_path):
    """Validate Jekyll _config.yml file"""
    if not os.path.exists(config_path):
        return False, "Config file does not exist"
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        required_keys = ['title']
        missing = [key for key in required_keys if key not in config]
        
        if missing:
            return False, f"Missing required keys: {missing}"
        
        return True, config
    except yaml.YAMLError as e:
        return False, f"Invalid YAML: {e}"


def validate_post_front_matter(post_path):
    """Validate Jekyll post front matter"""
    if not os.path.exists(post_path):
        return False, "Post file does not exist"
    
    try:
        with open(post_path, 'r') as f:
            content = f.read()
        
        # Check for front matter delimiter
        if not content.startswith('---'):
            return False, "Missing front matter delimiter"
        
        # Extract front matter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Invalid front matter format"
        
        front_matter = yaml.safe_load(parts[1])
        
        required_keys = ['layout', 'title', 'date']
        missing = [key for key in required_keys if key not in front_matter]
        
        if missing:
            return False, f"Missing required front matter keys: {missing}"
        
        return True, front_matter
    except Exception as e:
        return False, f"Error validating post: {e}"


def validate_jekyll_structure(output_dir):
    """Validate basic Jekyll site structure"""
    required_dirs = ['_posts']
    required_files = ['_config.yml']
    
    issues = []
    
    for dir_name in required_dirs:
        dir_path = os.path.join(output_dir, dir_name)
        if not os.path.exists(dir_path):
            issues.append(f"Missing directory: {dir_name}")
    
    for file_name in required_files:
        file_path = os.path.join(output_dir, file_name)
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file_name}")
    
    if issues:
        return False, issues
    
    return True, "Structure valid"


def count_jekyll_posts(output_dir):
    """Count generated Jekyll posts"""
    posts_dir = os.path.join(output_dir, '_posts')
    if not os.path.exists(posts_dir):
        return 0
    
    return len([f for f in os.listdir(posts_dir) if f.endswith('.md')])


def count_jekyll_pages(output_dir):
    """Count generated Jekyll pages"""
    if not os.path.exists(output_dir):
        return 0
    
    # Pages are typically in root or _pages directory
    pages_dir = os.path.join(output_dir, '_pages')
    if os.path.exists(pages_dir):
        return len([f for f in os.listdir(pages_dir) if f.endswith('.md')])
    
    # Check root for page files (excluding _config.yml and index.md)
    root_files = [f for f in os.listdir(output_dir) 
                  if f.endswith('.md') and f not in ['index.md', '_config.yml']]
    return len(root_files)



