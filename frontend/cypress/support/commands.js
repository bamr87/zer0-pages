// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

/**
 * Login command - logs in a user via API and stores token
 */
Cypress.Commands.add('login', (username = 'admin', password = 'password') => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/auth/token/',
    body: {
      username,
      password,
    },
  }).then((response) => {
    expect(response.status).to.eq(200)
    const { access, refresh } = response.body
    window.localStorage.setItem('access_token', access)
    window.localStorage.setItem('refresh_token', refresh)
  })
})

/**
 * Logout command - clears authentication tokens
 */
Cypress.Commands.add('logout', () => {
  window.localStorage.removeItem('access_token')
  window.localStorage.removeItem('refresh_token')
})

/**
 * Authenticated request command
 */
Cypress.Commands.add('authenticatedRequest', (options) => {
  const token = window.localStorage.getItem('access_token')
  if (token) {
    options.headers = {
      ...options.headers,
      Authorization: `Bearer ${token}`,
    }
  }
  return cy.request(options)
})

/**
 * Wait for API response
 */
Cypress.Commands.add('waitForAPI', (alias) => {
  cy.wait(alias).then((interception) => {
    expect(interception.response.statusCode).to.be.oneOf([200, 201])
  })
})



