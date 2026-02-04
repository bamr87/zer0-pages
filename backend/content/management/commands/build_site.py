import os
import yaml
from django.core.management.base import BaseCommand
from django.conf import settings
from content.models import Post, Page, SiteSettings

class Command(BaseCommand):
    help = 'Generates Jekyll site source files from published content'

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='jekyll_site', help='Output directory for Jekyll site')

    def handle(self, *args, **options):
        output_dir = options['output']
        self.stdout.write(f"Generating Jekyll site in {output_dir}...")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, '_posts'), exist_ok=True)
        os.makedirs(os.path.join(output_dir, '_pages'), exist_ok=True)
        # os.makedirs(os.path.join(output_dir, 'assets'), exist_ok=True) # In real world, copy assets

        # 1. Generate _config.yml
        self.generate_config(output_dir)

        # 2. Generate Posts
        posts = Post.objects.filter(status='published')
        for post in posts:
            self.generate_post(post, output_dir)
        
        self.stdout.write(f"Generated {posts.count()} posts.")

        # 3. Generate Pages
        pages = Page.objects.filter(status='published')
        for page in pages:
            self.generate_page(page, output_dir)

        self.stdout.write(f"Generated {pages.count()} pages.")
        
        # 4. Generate default index.md if not present (simplified)
        if not os.path.exists(os.path.join(output_dir, 'index.md')):
            with open(os.path.join(output_dir, 'index.md'), 'w') as f:
                f.write("---\nlayout: home\n---\n")

        self.stdout.write(self.style.SUCCESS('Site generation complete.'))

    def generate_config(self, output_dir):
        site_settings = SiteSettings.objects.first()
        config = {
            'title': site_settings.site_name if site_settings else 'zer0-pages',
            'description': site_settings.site_description if site_settings else '',
            'theme': 'minima', # Default theme for now
            'plugins': ['jekyll-seo-tag', 'jekyll-feed', 'jekyll-sitemap'],
            'github': {
                'repo': site_settings.github_repo if site_settings else ''
            }
        }
        
        with open(os.path.join(output_dir, '_config.yml'), 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def generate_post(self, post, output_dir):
        # Jekyll expects YYYY-MM-DD-title.md
        date_str = post.published_at.strftime('%Y-%m-%d') if post.published_at else post.created_at.strftime('%Y-%m-%d')
        filename = f"{date_str}-{post.slug}.md"
        
        front_matter = {
            'layout': 'post',
            'title': post.title,
            'date': date_str,
            'categories': [], # Add logic for categories/tags
            'author': post.author.username,
            'meta_title': post.meta_title,
            'meta_description': post.meta_description
        }
        
        content = f"---\n{yaml.dump(front_matter, default_flow_style=False)}---\n\n{post.content}"
        
        with open(os.path.join(output_dir, '_posts', filename), 'w') as f:
            f.write(content)

    def generate_page(self, page, output_dir):
        filename = f"{page.slug}.md"
        
        front_matter = {
            'layout': 'page',
            'title': page.title,
            'permalink': f"/{page.slug}/"
        }
        
        content = f"---\n{yaml.dump(front_matter, default_flow_style=False)}---\n\n{page.content}"
        
        with open(os.path.join(output_dir, filename), 'w') as f: # Pages usually go in root or specific folder with permalink
            f.write(content)

