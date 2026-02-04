describe('Dashboard', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('/')
  })

  it('should display dashboard', () => {
    cy.contains('Dashboard').should('be.visible')
  })

  it('should display key metrics', () => {
    // Wait for API calls to complete
    cy.wait(1000)
    
    // Check for metrics (adjust based on your dashboard implementation)
    cy.get('[data-testid="metrics"]').should('exist')
  })

  it('should navigate to posts page', () => {
    cy.get('a[href="/posts"]').click()
    cy.url().should('include', '/posts')
  })

  it('should navigate to pages page', () => {
    cy.get('a[href="/pages"]').click()
    cy.url().should('include', '/pages')
  })

  it('should navigate to PRDs page', () => {
    cy.get('a[href="/prds"]').click()
    cy.url().should('include', '/prds')
  })

  it('should navigate to settings page', () => {
    cy.get('a[href="/settings"]').click()
    cy.url().should('include', '/settings')
  })
})



