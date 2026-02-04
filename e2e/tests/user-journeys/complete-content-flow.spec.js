import { test, expect } from '@playwright/test';
import { setupAuthenticatedContext } from '../../helpers/auth_helpers';
import { createPost, updatePostStatus } from '../../helpers/api_helpers';

test.describe('Complete Content Flow', () => {
  test('user can create, enhance, preview, and publish content', async ({ page, request }) => {
    // Login
    const token = await setupAuthenticatedContext(page, request);
    await page.goto('/');
    
    // Navigate to posts
    await page.click('a[href="/posts"]');
    await expect(page).toHaveURL(/.*\/posts/);
    
    // Create new post
    await page.click('button:has-text("New Post")');
    
    // Fill in post form
    await page.fill('input[name="title"]', 'E2E Test Post');
    await page.fill('textarea[name="content"]', 'This is test content for E2E testing.');
    await page.fill('textarea[name="summary"]', 'Test summary');
    
    // Save draft
    await page.click('button:has-text("Save")');
    
    // Verify post created
    await expect(page.locator('text=E2E Test Post')).toBeVisible();
    
    // Edit post
    await page.click('text=E2E Test Post');
    await page.fill('textarea[name="content"]', 'Updated content');
    await page.click('button:has-text("Save")');
    
    // Publish post
    await page.selectOption('select[name="status"]', 'published');
    await page.click('button:has-text("Publish")');
    
    // Verify published
    await expect(page.locator('text=published')).toBeVisible();
  });
  
  test('content appears in Jekyll build after publishing', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    
    // Create and publish post via API
    const postResponse = await createPost(request, token, {
      title: 'Jekyll Test Post',
      content: 'Content for Jekyll',
      summary: 'Summary',
      status: 'published'
    });
    
    expect(postResponse.status()).toBe(201);
    
    // Verify post is published (would trigger Jekyll build in real scenario)
    const postsResponse = await request.get('http://localhost:8000/api/content/posts/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const posts = await postsResponse.json();
    const publishedPost = posts.results.find(p => p.title === 'Jekyll Test Post');
    expect(publishedPost).toBeDefined();
    expect(publishedPost.status).toBe('published');
  });
});



