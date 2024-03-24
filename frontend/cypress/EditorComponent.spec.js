describe('EditorComponent', () => {
    beforeEach(() => {
      mount(EditorComponent);
    });
  
    it('displays the editor component properly within the viewport', () => {
      cy.viewport(1200, 800); // Set viewport size
  
      cy.get('.canvas').should('be.visible'); // Check if the canvas element is visible
      cy.get('.drop-button').should('exist'); // Check if the drop button exists
      // Add more assertions to test other elements and layout
    });
  
    it('handles error states properly', () => {
      // Simulate an error condition (e.g., by providing invalid data to the component)
      // Verify how errors are displayed or handled within the component
    });
  });
  