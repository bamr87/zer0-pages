describe('PRDs Management', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('/prds')
  })

  it('should display PRDs list', () => {
    cy.contains('PRDs').should('be.visible')
    cy.get('[data-testid="prds-table"]').should('exist')
  })

  it('should create a new PRD', () => {
    cy.get('button').contains('New PRD').click()
    
    // Fill in PRD form
    cy.get('input[name="title"]').type('Test PRD')
    cy.get('input[name="version"]').type('1.0.0')
    cy.get('textarea[name="content"]').type('PRD content here')
    
    // Save
    cy.get('button').contains('Save').click()
    
    // Should see success message
    cy.contains('Test PRD').should('be.visible')
  })

  it('should update PRD status', () => {
    // Click on first PRD
    cy.get('[data-testid="prd-row"]').first().click()
    
    // Change status to review
    cy.get('select[name="status"]').select('review')
    cy.get('button').contains('Save').click()
    
    // Verify status changed
    cy.contains('review', { matchCase: false }).should('be.visible')
  })

  it('should create new PRD version', () => {
    // Click on first PRD
    cy.get('[data-testid="prd-row"]').first().click()
    
    // Click create new version
    cy.get('button').contains('New Version').click()
    
    // Update version number
    cy.get('input[name="version"]').clear().type('2.0.0')
    cy.get('button').contains('Save').click()
    
    // Verify new version created
    cy.contains('2.0.0').should('be.visible')
  })
})



