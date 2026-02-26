import React from 'react';
import { createRoot } from 'react-dom/client';
import TagPage from './components/TagPage';

const container = document.getElementById('react-tag-page');
if (container) {
    let produtos = [];
    const tag = container.getAttribute('data-tag') || '';
    const resultCount = container.getAttribute('data-count') || '0';

    try {
        const rawProdutos = container.getAttribute('data-produtos');
        if (rawProdutos) produtos = JSON.parse(rawProdutos);
    } catch (e) {
        console.error("Failed parsing Tag Produtos data context: ", e);
    }

    const root = createRoot(container);
    root.render(
        <TagPage tag={tag} resultCount={resultCount} produtos={produtos} />
    );
}
