"""
E2E tests for Jekyll site generation.
"""
import pytest
import os
from django.core.management import call_command
from django.core.management.base import CommandError
from content.models import Post, Page
from tests.helpers.jekyll_helpers import (
    validate_jekyll_config,
    validate_post_front_matter,
    validate_jekyll_structure,
    count_jekyll_posts,
    count_jekyll_pages
)


@pytest.mark.django_db
@pytest.mark.e2e
@pytest.mark.jekyll
class TestJekyllBuild:
    """Test Jekyll site generation end-to-end"""
    
    def test_build_jekyll_site(self, jekyll_output_dir, test_posts, test_pages):
        """Test building Jekyll site from published content"""
        # Ensure we have published content
        for post in test_posts[:3]:
            post.status = 'published'
            post.save()
        
        for page in test_pages[:2]:
            page.status = 'published'
            page.save()
        
        # Build site
        call_command('build_site', '--output', jekyll_output_dir)
        
        # Validate structure
        is_valid, result = validate_jekyll_structure(jekyll_output_dir)
        assert is_valid, result
        
        # Validate config
        config_path = os.path.join(jekyll_output_dir, '_config.yml')
        is_valid, config = validate_jekyll_config(config_path)
        assert is_valid, config
    
    def test_jekyll_config_generation(self, jekyll_output_dir):
        """Test Jekyll config file generation"""
        from content.models import SiteSettings
        from tests.factories import SiteSettingsFactory
        
        SiteSettingsFactory()
        
        call_command('build_site', '--output', jekyll_output_dir)
        
        config_path = os.path.join(jekyll_output_dir, '_config.yml')
        assert os.path.exists(config_path)
        
        is_valid, config = validate_jekyll_config(config_path)
        assert is_valid
        assert 'title' in config
    
    def test_jekyll_post_generation(self, jekyll_output_dir, test_posts):
        """Test Jekyll post file generation"""
        # Publish some posts
        published_posts = test_posts[:2]
        for post in published_posts:
            post.status = 'published'
            post.save()
        
        call_command('build_site', '--output', jekyll_output_dir)
        
        posts_dir = os.path.join(jekyll_output_dir, '_posts')
        assert os.path.exists(posts_dir)
        
        post_count = count_jekyll_posts(jekyll_output_dir)
        assert post_count >= len(published_posts)
        
        # Validate first post
        post_files = [f for f in os.listdir(posts_dir) if f.endswith('.md')]
        if post_files:
            post_path = os.path.join(posts_dir, post_files[0])
            is_valid, front_matter = validate_post_front_matter(post_path)
            assert is_valid, front_matter
            assert 'title' in front_matter
            assert 'date' in front_matter
    
    def test_jekyll_page_generation(self, jekyll_output_dir, test_pages):
        """Test Jekyll page file generation"""
        # Publish some pages
        published_pages = test_pages[:2]
        for page in published_pages:
            page.status = 'published'
            page.save()
        
        call_command('build_site', '--output', jekyll_output_dir)
        
        page_count = count_jekyll_pages(jekyll_output_dir)
        assert page_count >= len(published_pages)
    
    def test_only_published_content_included(self, jekyll_output_dir, test_posts):
        """Test that only published content is included in Jekyll build"""
        # Mix of published and draft
        test_posts[0].status = 'published'
        test_posts[0].save()
        test_posts[1].status = 'draft'
        test_posts[1].save()
        
        call_command('build_site', '--output', jekyll_output_dir)
        
        post_count = count_jekyll_posts(jekyll_output_dir)
        # Should only include published post
        assert post_count == 1
    
    def test_jekyll_output_directory_creation(self, jekyll_output_dir):
        """Test that output directory is created if it doesn't exist"""
        # Remove directory if exists
        if os.path.exists(jekyll_output_dir):
            import shutil
            shutil.rmtree(jekyll_output_dir)
        
        call_command('build_site', '--output', jekyll_output_dir)
        
        assert os.path.exists(jekyll_output_dir)
        assert os.path.exists(os.path.join(jekyll_output_dir, '_posts'))

