import React from 'react';
import { createRoot } from 'react-dom/client';
import VendorListPage from './components/VendorListPage';

const container = document.getElementById('react-vendor-list-page');
if (container) {
    let vendedores = [];
    const totalCount = container.getAttribute('data-count') || '0';

    try {
        const rawContent = container.getAttribute('data-vendedores');
        if (rawContent) vendedores = JSON.parse(rawContent);
    } catch (e) {
        console.error("Failed parsing Vendor List data context: ", e);
    }

    const root = createRoot(container);
    root.render(<VendorListPage vendedores={vendedores} totalCount={totalCount} />);
}
