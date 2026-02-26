import React from 'react';
import { createRoot } from 'react-dom/client';
import CategoryProductListPage from './components/CategoryProductListPage';

const container = document.getElementById('react-category-product-list-page');
if (container) {
    let produtos = [];
    const categoria = container.getAttribute('data-categoria') || '';
    const resultCount = container.getAttribute('data-count') || '0';

    try {
        const rawProdutos = container.getAttribute('data-produtos');
        if (rawProdutos) produtos = JSON.parse(rawProdutos);
    } catch (e) {
        console.error("Failed parsing Category Produtos data context: ", e);
    }

    const root = createRoot(container);
    root.render(
        <CategoryProductListPage containerTitle={categoria} resultCount={resultCount} produtos={produtos} />
    );
}
