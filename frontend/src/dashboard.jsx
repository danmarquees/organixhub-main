import React from 'react';
import { createRoot } from 'react-dom/client';
import DashboardPage from './components/DashboardPage';

const container = document.getElementById('react-dashboard-page');
if (container) {
    // Collect data dumps from Django
    const csrfToken = container.getAttribute('data-csrf');

    // Safely parse JSON strings injected into data attributes securely (base64 encoded via Django ideally, but JSON standard for now)
    let userProfile = {};
    let ordersList = [];
    let addressesList = [];
    let monthLabels = [];
    let monthlyTotals = [];

    try {
        const rawProfile = container.getAttribute('data-profile');
        if (rawProfile) userProfile = JSON.parse(rawProfile);

        const rawOrders = container.getAttribute('data-orders');
        if (rawOrders) ordersList = JSON.parse(rawOrders);

        const rawAddresses = container.getAttribute('data-addresses');
        if (rawAddresses) addressesList = JSON.parse(rawAddresses);

        const rawMonths = container.getAttribute('data-months');
        if (rawMonths) monthLabels = JSON.parse(rawMonths);

        const rawTotals = container.getAttribute('data-totals');
        if (rawTotals) monthlyTotals = JSON.parse(rawTotals);

    } catch (e) {
        console.error("Failed parsing Dashboard data contexts: ", e);
    }

    const root = createRoot(container);
    root.render(
        <DashboardPage
            csrfToken={csrfToken}
            userProfile={userProfile}
            ordersList={ordersList}
            addressesList={addressesList}
            monthLabels={monthLabels}
            monthlyTotals={monthlyTotals}
        />
    );
}
