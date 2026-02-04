import { test, expect } from '@playwright/test';
import { setupAuthenticatedContext } from '../../helpers/auth_helpers';

test.describe('AI Generation Flow', () => {
  test('user can generate content using AI', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    await page.goto('/posts');
    
    // Create new post
    await page.click('button:has-text("New Post")');
    
    // Fill basic info
    await page.fill('input[name="title"]', 'AI Generated Post');
    
    // Use AI generation (if UI exists)
    // This would depend on your actual UI implementation
    const aiButton = page.locator('button:has-text("Generate with AI")');
    if (await aiButton.isVisible()) {
      await aiButton.click();
      
      // Enter prompt
      await page.fill('textarea[name="ai_prompt"]', 'Write a blog post about Django');
      
      // Generate
      await page.click('button:has-text("Generate")');
      
      // Wait for generation
      await page.waitForSelector('text=Generated', { timeout: 30000 });
      
      // Verify content was generated
      const content = await page.locator('textarea[name="content"]').inputValue();
      expect(content.length).toBeGreaterThan(0);
    }
  });
  
  test('user can enhance existing content with AI', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    
    // Create post via API first
    const response = await request.post('http://localhost:8000/api/content/posts/', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data: {
        title: 'Post to Enhance',
        content: 'Original content that needs improvement',
        status: 'draft'
      }
    });
    
    const post = await response.json();
    
    // Navigate to edit page
    await page.goto(`/posts/${post.id}`);
    
    // Use AI enhance feature (if UI exists)
    const enhanceButton = page.locator('button:has-text("Enhance with AI")');
    if (await enhanceButton.isVisible()) {
      await enhanceButton.click();
      
      // Wait for enhancement
      await page.waitForSelector('text=Enhanced', { timeout: 30000 });
      
      // Verify content was enhanced
      const content = await page.locator('textarea[name="content"]').inputValue();
      expect(content).not.toBe('Original content that needs improvement');
    }
  });
});



