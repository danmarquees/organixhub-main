import React from 'react';
import { createRoot } from 'react-dom/client';
import VendorDetailPage from './components/VendorDetailPage';

const container = document.getElementById('react-vendor-detail-page');
if (container) {
    let vendedor = {};
    let produtos = [];
    let categorias = [];
    const totalCount = container.getAttribute('data-count') || '0';

    try {
        const rawVendedor = container.getAttribute('data-vendedor');
        if (rawVendedor) vendedor = JSON.parse(rawVendedor);

        const rawProdutos = container.getAttribute('data-produtos');
        if (rawProdutos) produtos = JSON.parse(rawProdutos);

        const rawCategorias = container.getAttribute('data-categorias');
        if (rawCategorias) categorias = JSON.parse(rawCategorias);
    } catch (e) {
        console.error("Failed parsing Vendor Detail data context: ", e);
    }

    const root = createRoot(container);
    root.render(<VendorDetailPage vendedor={vendedor} produtos={produtos} categorias={categorias} totalCount={totalCount} />);
}
