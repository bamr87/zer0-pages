// zer0-pages Privacy-First Analytics
(function() {
  const SESSION_KEY = 'zer0-pages-session';
  const CONSENT_KEY = 'zer0-pages-consent';
  const API_BASE = '/api/analytics';
  
  // Generate session ID
  function getSessionId() {
    let sessionId = sessionStorage.getItem(SESSION_KEY);
    if (!sessionId) {
      sessionId = 'sess_' + Math.random().toString(36).substr(2, 16) + Date.now().toString(36);
      sessionStorage.setItem(SESSION_KEY, sessionId);
    }
    return sessionId;
  }
  
  // Check consent
  function hasConsent(type) {
    const consent = JSON.parse(localStorage.getItem(CONSENT_KEY) || '{}');
    return consent[type] === true;
  }
  
  // Check Do Not Track
  function isDNT() {
    return navigator.doNotTrack === '1' || 
           window.doNotTrack === '1' || 
           navigator.msDoNotTrack === '1';
  }
  
  // Track event
  function trackEvent(eventType, eventName, properties = {}) {
    // Respect DNT
    if (isDNT()) return;
    
    // Check consent
    if (!hasConsent('analytics')) return;
    
    const payload = {
      session_id: getSessionId(),
      event_type: eventType,
      event_name: eventName,
      page_path: window.location.pathname,
      referrer: document.referrer || '',
      properties: properties
    };
    
    // Use sendBeacon for reliability
    if (navigator.sendBeacon) {
      navigator.sendBeacon(API_BASE + '/track/', JSON.stringify(payload));
    } else {
      fetch(API_BASE + '/track/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        keepalive: true
      }).catch(() => {});
    }
  }
  
  // Track page view
  function trackPageView() {
    trackEvent('page_view', 'Page View', {
      title: document.title,
      url: window.location.href
    });
  }
  
  // Track scroll depth
  function trackScrollDepth() {
    let maxScroll = 0;
    const thresholds = [25, 50, 75, 100];
    
    window.addEventListener('scroll', function() {
      const scrollPercent = Math.round(
        (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
      );
      
      for (const threshold of thresholds) {
        if (scrollPercent >= threshold && maxScroll < threshold) {
          maxScroll = threshold;
          trackEvent('scroll_depth', `Scroll ${threshold}%`, { depth: threshold });
        }
      }
    }, { passive: true });
  }
  
  // Track external links
  function trackExternalLinks() {
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a');
      if (link && link.hostname !== window.location.hostname) {
        trackEvent('external_link', 'External Link Click', {
          url: link.href,
          text: link.textContent.trim()
        });
      }
    });
  }
  
  // Initialize
  document.addEventListener('DOMContentLoaded', function() {
    if (hasConsent('analytics')) {
      trackPageView();
      trackScrollDepth();
      trackExternalLinks();
    }
  });
  
  // Expose for consent modal
  window.zer0Analytics = {
    trackEvent: trackEvent,
    trackPageView: trackPageView,
    getSessionId: getSessionId
  };
})();
