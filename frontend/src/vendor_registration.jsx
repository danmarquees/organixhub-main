import React from 'react';
import { createRoot } from 'react-dom/client';
import VendorRegistrationPage from './components/VendorRegistrationPage';

const container = document.getElementById('react-vendor-registration-page');
if (container) {
    const csrfToken = container.getAttribute('data-csrf') || '';
    let formErrors = {};

    try {
        const rawErrors = container.getAttribute('data-errors');
        if (rawErrors) formErrors = JSON.parse(rawErrors);
    } catch (e) {
        console.error("Failed parsing form errors: ", e);
    }

    const root = createRoot(container);
    root.render(<VendorRegistrationPage csrfToken={csrfToken} formErrors={formErrors} />);
}
