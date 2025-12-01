// Theme Toggle Script
(function() {
  const THEME_KEY = 'zer0-pages-theme';
  
  // Get stored theme or system preference
  function getPreferredTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored) return stored;
    
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  
  // Set theme
  function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    
    // Update icon visibility
    const lightIcon = document.getElementById('theme-icon-light');
    const darkIcon = document.getElementById('theme-icon-dark');
    
    if (lightIcon && darkIcon) {
      if (theme === 'dark') {
        lightIcon.classList.remove('d-none');
        darkIcon.classList.add('d-none');
      } else {
        lightIcon.classList.add('d-none');
        darkIcon.classList.remove('d-none');
      }
    }
  }
  
  // Initialize theme
  setTheme(getPreferredTheme());
  
  // Toggle button
  document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
      toggle.addEventListener('click', function() {
        const current = document.documentElement.getAttribute('data-bs-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
      });
    }
  });
  
  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
    if (!localStorage.getItem(THEME_KEY)) {
      setTheme(e.matches ? 'dark' : 'light');
    }
  });
})();
