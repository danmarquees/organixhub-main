import React from 'react';
import { createRoot } from 'react-dom/client';
import SignInPage from './components/SignInPage';

const container = document.getElementById('react-sign-in-page');
if (container) {
    // Extract CSRF token dumped from Django template
    const csrfToken = container.getAttribute('data-csrf');
    const root = createRoot(container);
    root.render(<SignInPage csrfToken={csrfToken} />);
}
