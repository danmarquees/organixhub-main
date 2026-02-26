import React from 'react';
import { createRoot } from 'react-dom/client';
import CheckoutPage from './components/CheckoutPage';

const container = document.getElementById('react-checkout-page');
if (container) {
    const csrfToken = container.getAttribute('data-csrf');
    const totalCartItems = container.getAttribute('data-totalcartitems');
    const cartTotalAmount = container.getAttribute('data-carttotalamount');
    const shippingCost = container.getAttribute('data-shippingcost');
    const taxAmount = container.getAttribute('data-taxamount');
    const finalAmount = container.getAttribute('data-finalamount');
    const stripePublishableKey = container.getAttribute('data-stripe-key');
    const oid = container.getAttribute('data-oid');

    let cartData = {};
    let orderData = {};
    let enderecoData = {};

    try {
        const rawCart = container.getAttribute('data-cart');
        if (rawCart) cartData = JSON.parse(rawCart);

        const rawOrder = container.getAttribute('data-order');
        if (rawOrder) orderData = JSON.parse(rawOrder);

        const rawEndereco = container.getAttribute('data-endereco');
        if (rawEndereco) enderecoData = JSON.parse(rawEndereco);
    } catch (e) {
        console.error("Failed parsing Checkout Data contexts: ", e);
    }

    const root = createRoot(container);
    root.render(
        <CheckoutPage
            csrfToken={csrfToken}
            cartData={cartData}
            orderData={orderData}
            enderecoData={enderecoData}
            totalCartItems={totalCartItems}
            cartTotalAmount={cartTotalAmount}
            shippingCost={shippingCost}
            taxAmount={taxAmount}
            finalAmount={finalAmount}
            stripePublishableKey={stripePublishableKey}
            oid={oid}
        />
    );
}
