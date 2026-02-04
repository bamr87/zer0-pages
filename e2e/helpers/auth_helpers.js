/**
 * Authentication helpers for Playwright tests
 */

/**
 * Login via API and return token
 */
export async function loginViaAPI(request, username = 'admin', password = 'password') {
  const response = await request.post('http://localhost:8000/api/auth/token/', {
    data: {
      username,
      password,
    },
  });
  
  if (response.status() !== 200) {
    throw new Error(`Login failed: ${response.status()}`);
  }
  
  const { access, refresh } = await response.json();
  return { access, refresh };
}

/**
 * Set authentication token in browser context
 */
export async function setAuthToken(context, token) {
  await context.addCookies([
    {
      name: 'access_token',
      value: token,
      domain: 'localhost',
      path: '/',
    },
  ]);
  
  // Also set in localStorage
  await context.addInitScript((token) => {
    window.localStorage.setItem('access_token', token);
  }, token);
}

/**
 * Login and set up authenticated context
 */
export async function setupAuthenticatedContext(page, request, username = 'admin', password = 'password') {
  const { access } = await loginViaAPI(request, username, password);
  
  // Set token in page context
  await page.addInitScript((token) => {
    window.localStorage.setItem('access_token', token);
  }, access);
  
  return access;
}



