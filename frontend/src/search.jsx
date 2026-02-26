import React from 'react';
import { createRoot } from 'react-dom/client';
import SearchPage from './components/SearchPage';

const container = document.getElementById('react-search-page');
if (container) {
    let produtos = [];
    const query = container.getAttribute('data-query') || '';
    const resultCount = container.getAttribute('data-count') || '0';

    try {
        const rawProdutos = container.getAttribute('data-produtos');
        if (rawProdutos) produtos = JSON.parse(rawProdutos);
    } catch (e) {
        console.error("Failed parsing Search Produtos data context: ", e);
    }

    const root = createRoot(container);
    root.render(
        <SearchPage query={query} resultCount={resultCount} produtos={produtos} />
    );
}
