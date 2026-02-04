describe('Pages Management', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('/pages')
  })

  it('should display pages list', () => {
    cy.contains('Pages').should('be.visible')
    cy.get('[data-testid="pages-table"]').should('exist')
  })

  it('should create a new page', () => {
    cy.get('button').contains('New Page').click()
    
    // Fill in page form
    cy.get('input[name="title"]').type('Test Page')
    cy.get('textarea[name="content"]').type('This is test page content')
    
    // Save
    cy.get('button').contains('Save').click()
    
    // Should see success message
    cy.contains('Test Page').should('be.visible')
  })

  it('should edit an existing page', () => {
    // Click edit on first page
    cy.get('[data-testid="page-row"]').first().find('button').contains('Edit').click()
    
    // Update content
    cy.get('textarea[name="content"]').clear().type('Updated page content')
    cy.get('button').contains('Save').click()
    
    // Verify update
    cy.contains('Updated page content').should('be.visible')
  })

  it('should publish a page', () => {
    // Find a draft page and publish it
    cy.get('[data-testid="page-row"]').contains('draft').first().parent().find('button').contains('Publish').click()
    
    // Verify status changed
    cy.contains('published', { matchCase: false }).should('be.visible')
  })
})



