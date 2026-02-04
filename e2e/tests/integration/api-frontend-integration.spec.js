import { test, expect } from '@playwright/test';
import { setupAuthenticatedContext } from '../../helpers/auth_helpers';
import { createPost, getPosts, updatePostStatus } from '../../helpers/api_helpers';

test.describe('API-Frontend Integration', () => {
  test('frontend displays data from API', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    
    // Create post via API
    const postResponse = await createPost(request, token, {
      title: 'API Created Post',
      content: 'Content created via API',
      summary: 'Summary',
      status: 'published'
    });
    
    expect(postResponse.status()).toBe(201);
    const post = await postResponse.json();
    
    // Verify post appears in frontend
    await page.goto('/posts');
    await expect(page.locator('text=API Created Post')).toBeVisible();
  });
  
  test('frontend updates reflect in API', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    
    // Create post via API
    const postResponse = await createPost(request, token, {
      title: 'Post to Update',
      content: 'Original content',
      status: 'draft'
    });
    
    const post = await postResponse.json();
    
    // Update via frontend
    await page.goto(`/posts/${post.id}`);
    await page.fill('textarea[name="content"]', 'Updated content');
    await page.click('button:has-text("Save")');
    
    // Verify update via API
    const updatedResponse = await request.get(`http://localhost:8000/api/content/posts/${post.id}/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const updatedPost = await updatedResponse.json();
    expect(updatedPost.content).toBe('Updated content');
  });
  
  test('API changes reflect in frontend', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    
    // Create post via API
    const postResponse = await createPost(request, token, {
      title: 'Status Change Test',
      content: 'Content',
      status: 'draft'
    });
    
    const post = await postResponse.json();
    
    // View in frontend
    await page.goto(`/posts/${post.id}`);
    await expect(page.locator('text=draft')).toBeVisible();
    
    // Update status via API
    await updatePostStatus(request, token, post.id, 'published');
    
    // Refresh frontend
    await page.reload();
    
    // Verify status updated
    await expect(page.locator('text=published')).toBeVisible();
  });
});



