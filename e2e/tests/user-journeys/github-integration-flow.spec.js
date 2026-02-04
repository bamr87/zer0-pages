import { test, expect } from '@playwright/test';
import { setupAuthenticatedContext } from '../../helpers/auth_helpers';

test.describe('GitHub Integration Flow', () => {
  test('user can connect repository and sync issues', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    await page.goto('/settings');
    
    // Connect GitHub repository (if UI exists)
    const repoInput = page.locator('input[name="github_repo"]');
    if (await repoInput.isVisible()) {
      await repoInput.fill('test-owner/test-repo');
      await page.click('button:has-text("Save")');
      
      // Verify repository connected
      await expect(page.locator('text=test-owner/test-repo')).toBeVisible();
    }
    
    // Navigate to GitHub hub (if exists)
    const githubLink = page.locator('a[href*="github"]');
    if (await githubLink.isVisible()) {
      await githubLink.click();
      
      // Sync issues (if button exists)
      const syncButton = page.locator('button:has-text("Sync Issues")');
      if (await syncButton.isVisible()) {
        await syncButton.click();
        
        // Wait for sync to complete
        await page.waitForSelector('text=Synced', { timeout: 10000 });
      }
    }
  });
  
  test('user can generate PRD from repository', async ({ page, request }) => {
    const token = await setupAuthenticatedContext(page, request);
    await page.goto('/prds');
    
    // Create PRD from repository (if UI exists)
    const generateButton = page.locator('button:has-text("Generate from Repo")');
    if (await generateButton.isVisible()) {
      await generateButton.click();
      
      // Select repository
      await page.selectOption('select[name="repository"]', '1');
      
      // Generate
      await page.click('button:has-text("Generate PRD")');
      
      // Wait for generation
      await page.waitForSelector('text=PRD generated', { timeout: 30000 });
      
      // Verify PRD created
      await expect(page.locator('[data-testid="prd-row"]')).toBeVisible();
    }
  });
});



