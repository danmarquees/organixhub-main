import React from 'react';
import { createRoot } from 'react-dom/client';
import ProfileEditPage from './components/ProfileEditPage';

const container = document.getElementById('react-profile-edit-page');
if (container) {
    const csrfToken = container.getAttribute('data-csrf');
    const formErrors = container.getAttribute('data-errors');

    let userProfile = {};
    try {
        const rawProfile = container.getAttribute('data-profile');
        if (rawProfile) userProfile = JSON.parse(rawProfile);
    } catch (e) {
        console.error("Failed parsing Profile data context: ", e);
    }

    const root = createRoot(container);
    root.render(
        <ProfileEditPage
            csrfToken={csrfToken}
            userProfile={userProfile}
            formErrors={formErrors}
        />
    );
}
