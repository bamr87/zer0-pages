describe('Posts Management', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('/posts')
  })

  it('should display posts list', () => {
    cy.contains('Posts').should('be.visible')
    cy.get('[data-testid="posts-table"]').should('exist')
  })

  it('should create a new post', () => {
    cy.get('button').contains('New Post').click()
    
    // Fill in post form
    cy.get('input[name="title"]').type('Test Post')
    cy.get('textarea[name="content"]').type('This is test content')
    cy.get('textarea[name="summary"]').type('Test summary')
    
    // Save
    cy.get('button').contains('Save').click()
    
    // Should see success message or redirect
    cy.contains('Test Post').should('be.visible')
  })

  it('should edit an existing post', () => {
    // Click edit on first post (adjust selector)
    cy.get('[data-testid="post-row"]').first().find('button').contains('Edit').click()
    
    // Update title
    cy.get('input[name="title"]').clear().type('Updated Post Title')
    cy.get('button').contains('Save').click()
    
    // Verify update
    cy.contains('Updated Post Title').should('be.visible')
  })

  it('should filter posts by status', () => {
    cy.get('select[name="status"]').select('published')
    cy.wait(500)
    
    // Verify filtered results
    cy.get('[data-testid="posts-table"]').should('exist')
  })

  it('should search posts', () => {
    cy.get('input[placeholder*="Search"]').type('test')
    cy.wait(500)
    
    // Verify search results
    cy.get('[data-testid="posts-table"]').should('exist')
  })

  it('should publish a draft post', () => {
    // Find a draft post and publish it
    cy.get('[data-testid="post-row"]').contains('draft').first().parent().find('button').contains('Publish').click()
    
    // Verify status changed
    cy.contains('published', { matchCase: false }).should('be.visible')
  })

  it('should delete a post', () => {
    // Click delete on first post
    cy.get('[data-testid="post-row"]').first().find('button').contains('Delete').click()
    
    // Confirm deletion
    cy.get('button').contains('Confirm').click()
    
    // Verify post removed
    cy.contains('Post deleted', { matchCase: false }).should('be.visible')
  })
})



