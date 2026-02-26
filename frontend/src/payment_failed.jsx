import React from 'react';
import { createRoot } from 'react-dom/client';
import PaymentFailedPage from './components/PaymentFailedPage';

const container = document.getElementById('react-payment-failed-page');
if (container) {
    const root = createRoot(container);
    root.render(
        <PaymentFailedPage />
    );
}
