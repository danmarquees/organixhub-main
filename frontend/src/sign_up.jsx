import React from 'react';
import { createRoot } from 'react-dom/client';
import SignUpPage from './components/SignUpPage';

const container = document.getElementById('react-sign-up-page');
if (container) {
    // Extract CSRF token and Form errors dumped from Django template
    const csrfToken = container.getAttribute('data-csrf');
    const formErrors = container.getAttribute('data-errors');

    const root = createRoot(container);
    root.render(<SignUpPage csrfToken={csrfToken} formErrors={formErrors} />);
}
