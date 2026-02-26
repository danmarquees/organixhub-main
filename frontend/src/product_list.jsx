import React from 'react';
import { createRoot } from 'react-dom/client';
import ProductListPage from './components/ProductListPage';

const container = document.getElementById('react-product-list-page');
if (container) {
    const root = createRoot(container);
    root.render(<ProductListPage />);
}
