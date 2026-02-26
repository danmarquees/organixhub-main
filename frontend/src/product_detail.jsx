import React from 'react';
import { createRoot } from 'react-dom/client';
import ProductDetailPage from './components/ProductDetailPage';

const container = document.getElementById('react-product-detail-page');
if (container) {
    const pid = container.getAttribute('data-product-id');
    const root = createRoot(container);
    root.render(<ProductDetailPage pid={pid} />);
}
