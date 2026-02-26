import React from 'react';
import { createRoot } from 'react-dom/client';
import PaymentCompletedPage from './components/PaymentCompletedPage';

const container = document.getElementById('react-payment-completed-page');
if (container) {
    let pedidoCarrinho = [];
    try {
        const rawPedidos = container.getAttribute('data-pedidos');
        if (rawPedidos) pedidoCarrinho = JSON.parse(rawPedidos);
    } catch (e) {
        console.error("Failed parsing Pedidos data context: ", e);
    }

    const root = createRoot(container);
    root.render(
        <PaymentCompletedPage pedidoCarrinho={pedidoCarrinho} />
    );
}
