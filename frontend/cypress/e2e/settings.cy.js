describe('Settings', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('/settings')
  })

  it('should display settings page', () => {
    cy.contains('Settings').should('be.visible')
  })

  it('should update site name', () => {
    cy.get('input[name="site_name"]').clear().type('New Site Name')
    cy.get('button').contains('Save').click()
    
    // Verify update
    cy.contains('Settings saved', { matchCase: false }).should('be.visible')
  })

  it('should update site description', () => {
    cy.get('textarea[name="site_description"]').clear().type('New site description')
    cy.get('button').contains('Save').click()
    
    // Verify update
    cy.contains('Settings saved', { matchCase: false }).should('be.visible')
  })

  it('should toggle analytics', () => {
    cy.get('input[name="analytics_enabled"]').uncheck()
    cy.get('button').contains('Save').click()
    
    // Verify setting saved
    cy.contains('Settings saved', { matchCase: false }).should('be.visible')
  })

  it('should update GitHub repository', () => {
    cy.get('input[name="github_repo"]').clear().type('user/repo')
    cy.get('button').contains('Save').click()
    
    // Verify update
    cy.contains('Settings saved', { matchCase: false }).should('be.visible')
  })
})



