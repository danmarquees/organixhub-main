import React, { useState, useEffect, useRef } from 'react';

const CheckoutPage = ({
    csrfToken,
    cartData,
    orderData,
    enderecoData,
    totalCartItems,
    cartTotalAmount,
    shippingCost,
    taxAmount,
    finalAmount,
    stripePublishableKey,
    oid
}) => {

    // Addresses and Order States
    const [nome, setNome] = useState(orderData?.nome || '');
    const [email, setEmail] = useState(orderData?.email || '');
    const [logradouro, setLogradouro] = useState(orderData?.endereco || '');
    const [complemento, setComplemento] = useState(enderecoData?.complemento || '');
    const [uf, setUf] = useState(orderData?.estado || '');
    const [cidade, setCidade] = useState(orderData?.cidade || '');
    const [cep, setCep] = useState(orderData?.cep || '');
    const [telefone, setTelefone] = useState(orderData?.telefone || '');
    const [bairro, setBairro] = useState(enderecoData?.bairro || '');
    const [numero, setNumero] = useState(enderecoData?.numero || '');
    const [informacoesAdicionais, setInformacoesAdicionais] = useState(orderData?.informacoes_adicionais || '');

    const [isSaving, setIsSaving] = useState(false);
    const [paymentEnabled, setPaymentEnabled] = useState(false);
    const [isStripeProcessing, setIsStripeProcessing] = useState(false);

    const paypalRef = useRef(null);

    // Save Delivery Details
    const handleSaveDeliveryDetails = async (e) => {
        e.preventDefault();
        setIsSaving(true);

        // Serialize form data
        const formData = new URLSearchParams();
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('nome', nome);
        formData.append('email', email);
        formData.append('logradouro', logradouro);
        formData.append('complemento', complemento);
        formData.append('uf', uf);
        formData.append('localidade', cidade);
        formData.append('cep', cep);
        formData.append('telefone', telefone);
        formData.append('bairro', bairro);
        formData.append('numero', numero);
        formData.append('informacoes_adicionais', informacoesAdicionais);

        try {
            const response = await fetch('/save_checkout_info/', { // Usually matches core:save_delivery_details in urls.py
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData.toString()
            });

            const data = await response.json();

            if (data.success) {
                alert(data.message);
                setPaymentEnabled(true);
                // Initialize Paypal if it wasn't already initialized
                initializePaypal();
            } else {
                alert(data.message || 'Erro ao salvar os detalhes.');
            }
        } catch (error) {
            console.error(error);
            alert('Ocorreu um erro ao salvar os detalhes da entrega. Tente novamente.');
        } finally {
            setIsSaving(false);
        }
    };

    // Stripe Handler
    const handleStripeCheckout = async () => {
        if (!paymentEnabled) return;
        setIsStripeProcessing(true);

        try {
            const response = await fetch(`/api/create_checkout_session/${oid}/`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ email: email })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const session = await response.json();
            const stripe = window.Stripe(stripePublishableKey);
            const { error } = await stripe.redirectToCheckout({ sessionId: session.id });

            if (error) {
                alert(error.message);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Ocorreu um erro ao processar o pagamento. Por favor, tente novamente.");
        } finally {
            setIsStripeProcessing(false);
        }
    };

    // Paypal Initialization
    const initializePaypal = () => {
        // Clear old buttons if they exist
        if (paypalRef.current) {
            paypalRef.current.innerHTML = '';
        }

        if (window.paypal && paypalRef.current) {
            window.paypal.Buttons({
                style: {
                    shape: 'rect',
                    color: 'gold',
                    layout: 'vertical',
                    label: 'paypal',
                },
                createOrder: function (data, actions) {
                    return actions.order.create({
                        purchase_units: [{
                            amount: {
                                currency_code: "BRL",
                                value: finalAmount.toString(),
                            }
                        }]
                    });
                },
                onApprove: function (data, actions) {
                    return actions.order.capture().then(function (orderData) {
                        console.log('Pagamento aprovado:', orderData);
                        window.location.href = `/payment-completed/?status=${orderData.status}&orderId=${orderData.id}`;
                    }).catch(function (err) {
                        console.error('Erro ao capturar o pagamento:', err);
                        alert('Não foi possível concluir o pagamento. Por favor, tente novamente.');
                    });
                },
                onError: function (err) {
                    console.error('Erro no PayPal:', err);
                    alert('Ocorreu um erro ao processar o pagamento. Por favor, tente novamente.');
                },
                onCancel: function (data) {
                    console.log('Pagamento cancelado:', data);
                    alert('O pagamento foi cancelado.');
                }
            }).render(paypalRef.current);
        }
    };

    return (
        <main className="main">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Home</a>
                        <span></span> Loja <span></span> Checkout
                    </div>
                </div>
            </div>

            <div className="container mb-80 mt-50">
                <div className="row">
                    <div className="col-lg-8 mb-40">
                        <h1 className="heading-2 mb-10">Checkout</h1>
                        <div className="d-flex justify-content-between">
                            <h6 className="text-body">Você possui <span className="text-brand">{totalCartItems}</span> produtos em seu carrinho</h6>
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col-lg-7">
                        {/* ORDER ITEMS TABLE */}
                        <div className="border p-40 cart-totals ml-30 mb-50">
                            <h4 className="mb-30">Seu Pedido</h4>
                            <table className="table no-border table-wishlist">
                                <thead>
                                    <tr className="main-heading">
                                        <th className="text-brand"><h6>Item</h6></th>
                                        <th className="text-brand"><h6>Nome</h6></th>
                                        <th className="text-brand"><h6>Quantidade</h6></th>
                                        <th className="text-brand"><h6>Valor Unitário</h6></th>
                                        <th className="text-brand"><h6>Valor Total</h6></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.values(cartData).map((item, index) => (
                                        <tr key={index}>
                                            <td className="image product-thumbnail">
                                                <img style={{ aspectRatio: '1/1', objectFit: 'cover' }} src={item.image} alt="#" />
                                            </td>
                                            <td>
                                                <h6 className="w-160 mb-5">
                                                    <a href={`/produto/${item.pid}/`} className="text-heading">{item.title}</a>
                                                </h6>
                                            </td>
                                            <td><h6 className="text-muted pl-20 pr-20">X{item.qty}</h6></td>
                                            <td><h5 className="text-muted">R${item.price}</h5></td>
                                            <td><h5 className="text-brand">R${parseFloat(item.subtotal).toFixed(2)}</h5></td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        {/* DELIVERY DETAILS FORM */}
                        <div className="border p-40 cart-totals ml-30 mb-50">
                            <h4 className="mb-30">Detalhes para a Entrega</h4>
                            <form id="checkout-form" onSubmit={handleSaveDeliveryDetails}>
                                <div className="row">
                                    <div className="form-group col-lg-6">
                                        <input type="text" required value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Nome *" />
                                    </div>
                                    <div className="form-group col-lg-6">
                                        <input type="text" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="E-mail *" />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="form-group col-lg-6">
                                        <input type="text" required value={logradouro} onChange={(e) => setLogradouro(e.target.value)} placeholder="Endereço *" />
                                    </div>
                                    <div className="form-group col-lg-6">
                                        <input type="text" value={complemento} onChange={(e) => setComplemento(e.target.value)} placeholder="Complemento" />
                                    </div>
                                </div>
                                <div className="row shipping_calculator">
                                    <div className="form-group col-lg-6">
                                        <div className="custom_select">
                                            <select className="form-control select-active" value={uf} onChange={(e) => setUf(e.target.value)} required>
                                                <option value="">Selecione um estado...</option>
                                                <option value="AC">Acre</option>
                                                <option value="AL">Alagoas</option>
                                                <option value="AP">Amapá</option>
                                                <option value="AM">Amazonas</option>
                                                <option value="BA">Bahia</option>
                                                <option value="CE">Ceará</option>
                                                <option value="DF">Distrito Federal</option>
                                                <option value="ES">Espírito Santo</option>
                                                <option value="GO">Goiás</option>
                                                <option value="MA">Maranhão</option>
                                                <option value="MT">Mato Grosso</option>
                                                <option value="MS">Mato Grosso do Sul</option>
                                                <option value="MG">Minas Gerais</option>
                                                <option value="PA">Pará</option>
                                                <option value="PB">Paraíba</option>
                                                <option value="PR">Paraná</option>
                                                <option value="PE">Pernambuco</option>
                                                <option value="PI">Piauí</option>
                                                <option value="RJ">Rio de Janeiro</option>
                                                <option value="RN">Rio Grande do Norte</option>
                                                <option value="RS">Rio Grande do Sul</option>
                                                <option value="RO">Rondônia</option>
                                                <option value="RR">Roraima</option>
                                                <option value="SC">Santa Catarina</option>
                                                <option value="SP">São Paulo</option>
                                                <option value="SE">Sergipe</option>
                                                <option value="TO">Tocantins</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div className="form-group col-lg-6">
                                        <input type="text" required value={cidade} onChange={(e) => setCidade(e.target.value)} placeholder="Cidade *" />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="form-group col-lg-6">
                                        <input type="text" required value={cep} onChange={(e) => setCep(e.target.value)} placeholder="CEP *" />
                                    </div>
                                    <div className="form-group col-lg-6">
                                        <input type="text" required value={telefone} onChange={(e) => setTelefone(e.target.value)} placeholder="Telefone *" />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="form-group col-lg-6">
                                        <input type="text" value={bairro} onChange={(e) => setBairro(e.target.value)} placeholder="Bairro" />
                                    </div>
                                    <div className="form-group col-lg-6">
                                        <input type="text" value={numero} onChange={(e) => setNumero(e.target.value)} placeholder="Número" />
                                    </div>
                                </div>
                                <div className="form-group mb-30">
                                    <textarea rows="5" value={informacoesAdicionais} onChange={(e) => setInformacoesAdicionais(e.target.value)} placeholder="Informações Adicionais"></textarea>
                                </div>

                                <button type="submit" className="btn btn-fill-out btn-block" disabled={isSaving}>
                                    {isSaving ? (
                                        <>Salvando... <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true" style={{ marginLeft: '10px' }}></span></>
                                    ) : (
                                        "Salvar Detalhes da Entrega"
                                    )}
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* SUMMARY & PAYMENT METHODS */}
                    <div className="col-lg-5">
                        <div className="border p-40 cart-totals ml-30 mb-50">
                            <div className="d-flex align-items-end justify-content-between mb-30">
                                <h4>Sumário do Pedido</h4>
                                <h6 className="text-muted">Subtotal: <span className="text-brand">R${parseFloat(cartTotalAmount).toFixed(2)}</span></h6>
                            </div>

                            <div>
                                <form method="POST" action="/checkout/" className="apply-coupon">
                                    <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
                                    <input type="text" name="codigo" placeholder="Entre com o código promocional..." />
                                    <button className="btn btn-md" type="submit">Resgatar</button>
                                </form>
                            </div>

                            <a href="/carrinho/" className="btn btn-fill-out btn-block mt-30 mb-40">Voltar ao Carrinho</a>

                            <div className="order_table checkout">
                                <table className="table no-border no-line" style={{ borderCollapse: "collapse" }}>
                                    <tbody>
                                        <tr>
                                            <td className="cart_total_label"><h6>Subtotal</h6></td>
                                            <td className="cart_total_amount text-success"><h6>R${cartTotalAmount}</h6></td>
                                        </tr>
                                        <tr>
                                            <td className="cart_total_label"><h6>Taxa de Entrega</h6></td>
                                            <td className="cart_total_amount text-success"><h6>R${parseFloat(shippingCost).toFixed(2)}</h6></td>
                                        </tr>
                                        <tr>
                                            <td className="cart_total_label"><h6>Impostos</h6></td>
                                            <td className="cart_total_amount text-success"><h6>R${parseFloat(taxAmount).toFixed(2)}</h6></td>
                                        </tr>
                                        {/* Coupon Display - Note: Since Django handles coupon state natively via POST reload, we assume finalAmount is pre-calculated correctly */}
                                        <tr>
                                            <td className="text-brand"><strong><h6>Total Final</h6></strong></td>
                                            <td className="cart_total_amount">
                                                <strong className="text-brand">
                                                    <h6 className="text-success">R${parseFloat(finalAmount).toFixed(2)}</h6>
                                                </strong>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* PAYMENT PLATFORMS */}
                        <div className="border p-40 cart-totals ml-30 mb-50">
                            <div className="payment ml-30">
                                <h4 className="mb-30">Formas de Pagamento</h4>
                                <div className="payment_option">
                                    <button
                                        type="button"
                                        className="btn w-100 mb-10"
                                        disabled={!paymentEnabled || isStripeProcessing}
                                        onClick={handleStripeCheckout}
                                        style={{ backgroundColor: paymentEnabled ? "blueviolet" : "gray", color: 'white' }}
                                    >
                                        {isStripeProcessing ? "Processando..." : "Pagar com o Stripe (Cartão de Crédito)"}
                                    </button>

                                    {paymentEnabled && (
                                        <div className="mt-20" ref={paypalRef}></div>
                                    )}
                                </div>
                                <br />
                                <div className="payment-logo d-flex">
                                    <img className="mr-15" src="/static/assets/imgs/theme/icons/payment-paypal.svg" alt="" />
                                    <img className="mr-15" src="/static/assets/imgs/theme/icons/payment-visa.svg" alt="" />
                                    <img className="mr-15" src="/static/assets/imgs/theme/icons/payment-master.svg" alt="" />
                                    <img src="/static/assets/imgs/theme/icons/payment-zapper.svg" alt="" />
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </main>
    );
};

export default CheckoutPage;
