/**
 * API interaction helpers for Playwright tests
 */

/**
 * Make authenticated API request
 */
export async function authenticatedRequest(request, method, endpoint, data = null, token = null) {
  const headers = {};
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const options = {
    headers,
  };
  
  if (data) {
    options.data = data;
  }
  
  return await request[method.toLowerCase()](`http://localhost:8000${endpoint}`, options);
}

/**
 * Create a post via API
 */
export async function createPost(request, token, postData) {
  return await authenticatedRequest(request, 'post', '/api/content/posts/', postData, token);
}

/**
 * Create a page via API
 */
export async function createPage(request, token, pageData) {
  return await authenticatedRequest(request, 'post', '/api/content/pages/', pageData, token);
}

/**
 * Create a PRD via API
 */
export async function createPRD(request, token, prdData) {
  return await authenticatedRequest(request, 'post', '/api/prd/prds/', prdData, token);
}

/**
 * Get posts via API
 */
export async function getPosts(request, token) {
  return await authenticatedRequest(request, 'get', '/api/content/posts/', null, token);
}

/**
 * Update post status via API
 */
export async function updatePostStatus(request, token, postId, status) {
  return await authenticatedRequest(request, 'patch', `/api/content/posts/${postId}/`, { status }, token);
}



