describe('Authentication Flow', () => {
  beforeEach(() => {
    cy.logout()
  })

  it('should display login page', () => {
    cy.visit('/login')
    cy.contains('Login').should('be.visible')
  })

  it('should login with valid credentials', () => {
    cy.visit('/login')
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('password')
    cy.get('button[type="submit"]').click()
    
    // Should redirect to dashboard
    cy.url().should('include', '/')
    cy.contains('Dashboard').should('be.visible')
  })

  it('should show error with invalid credentials', () => {
    cy.visit('/login')
    cy.get('input[name="username"]').type('invalid')
    cy.get('input[name="password"]').type('wrong')
    cy.get('button[type="submit"]').click()
    
    // Should show error message
    cy.contains('error', { matchCase: false }).should('be.visible')
  })

  it('should logout successfully', () => {
    cy.login()
    cy.visit('/')
    
    // Click logout button (adjust selector based on your UI)
    cy.get('[data-testid="logout"]').click()
    
    // Should redirect to login
    cy.url().should('include', '/login')
  })

  it('should redirect to login when accessing protected route', () => {
    cy.visit('/posts')
    cy.url().should('include', '/login')
  })
})



