import React, { useState, useEffect } from 'react';

const CartPage = () => {
    // Note: To fully migrate the cart data dynamically, we would need a Cart API endpoint in Django.
    // For this progressive migration step, we are just mapping the layout and keeping static placeholders
    // until a Cart API is implemented, similar to how the initial 'contact' and 'about' pages were migrated.

    // We will simulate cart state to allow UI interactions (like removing items locally before integrating backend).
    const [cartItems, setCartItems] = useState([
        // Mock data matching the Django template structure for visual testing
        { pid: '1', title: 'Produto Exemplo 1', price: 10.00, qty: 1, image: '/static/assets/imgs/shop/product-1-1.jpg' }
    ]);
    const [cartTotal, setCartTotal] = useState(10.00);


    return (
        <main className="main" id="cart-list">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Home</a>
                        <span></span> Loja
                        <span></span> Carrinho
                    </div>
                </div>
            </div>
            <div className="container mb-80 mt-50">
                <div className="row">
                    <div className="col-lg-8 mb-40">
                        <h1 className="heading-2 mb-10">Seu Carrinho</h1>
                        <div className="d-flex justify-content-between">
                            <h6 className="text-body">Há <span className="text-brand">{cartItems.length}</span> produtos em seu carrinho</h6>
                            <h6 className="text-body"><a href="#" className="text-muted"><i className="fi-rs-trash mr-5"></i>Esvaziar Carrinho</a></h6>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-lg-8">
                        <div className="table-responsive shopping-summery">
                            <table className="table table-wishlist">
                                <thead>
                                    <tr className="main-heading">
                                        <th className="custome-checkbox start pl-30">
                                            <input className="form-check-input" type="checkbox" name="checkbox" id="exampleCheckbox11" />
                                            <label className="form-check-label" htmlFor="exampleCheckbox11"></label>
                                        </th>
                                        <th scope="col" colSpan="1">Produto</th>
                                        <th scope="col">Nome</th>
                                        <th scope="col">Preço Unitário</th>
                                        <th scope="col" className="text-center">Quantidade</th>
                                        <th scope="col">Subtotal</th>
                                        <th scope="col">Refresh</th>
                                        <th scope="col" className="end">Remover</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {cartItems.map((item, index) => (
                                        <tr className="pt-30" key={item.pid}>
                                            <td className="custome-checkbox pl-30">
                                                <input className="form-check-input" type="checkbox" name="checkbox" id={`exampleCheckbox${index + 1}`} value="" />
                                                <label className="form-check-label" htmlFor={`exampleCheckbox${index + 1}`}></label>
                                            </td>
                                            <td className="image product-thumbnail pt-40"><img src={item.image} alt={item.title} /></td>
                                            <td className="product-des product-name">
                                                <h6 className="mb-5"><a className="product-name mb-10 text-heading" href={`/produto/${item.pid}`}>{item.title}</a></h6>
                                            </td>
                                            <td className="price" data-title="Price">
                                                <h4 className="text-body">R${item.price.toFixed(2)}</h4>
                                            </td>
                                            <td className="text-center detail-info" data-title="Stock">
                                                <div className="detail-extralink mr-15">
                                                    <div className="detail-qty border radius">
                                                        <a href="#" className="qty-down"><i className="fi-rs-angle-small-down"></i></a>
                                                        <input type="number" className="qty-val" defaultValue={item.qty} min="1" />
                                                        <a href="#" className="qty-up"><i className="fi-rs-angle-small-up"></i></a>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="price" data-title="Price">
                                                <h4 className="text-brand">R${(item.price * item.qty).toFixed(2)}</h4>
                                            </td>
                                            <td className="action text-center" data-title="Refresh">
                                                <button style={{ border: 'none', background: 'none' }} className="text-body update-product">
                                                    <i className="fi-rs-refresh"></i>
                                                </button>
                                            </td>
                                            <td className="action text-center" data-title="Remove">
                                                <button style={{ border: 'none', background: 'none' }} className="text-body delete-product">
                                                    <i className="fi-rs-trash"></i>
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                        <div className="divider-2 mb-30"></div>
                        <div className="cart-action d-flex justify-content-between">
                            <a className="btn " href="/produtos/"><i className="fi-rs-arrow-left mr-10"></i>Continuar Comprando</a>
                            <a className="btn  mr-10 mb-sm-15"><i className="fi-rs-refresh mr-10"></i>Atualizar Carrinho</a>
                        </div>
                    </div>

                    <div className="col-lg-4">
                        <div className="border p-md-4 cart-totals ml-30">
                            <div className="table-responsive">
                                <table className="table no-border">
                                    <tbody>
                                        <tr>
                                            <td className="cart_total_label">
                                                <h6 className="text-muted">Subtotal</h6>
                                            </td>
                                            <td className="cart_total_amount">
                                                <h4 className="text-brand text-end">R${cartTotal.toFixed(2)}</h4>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td scope="col" colSpan="2">
                                                <div className="divider-2 mt-10 mb-10"></div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="cart_total_label">
                                                <h6 className="text-muted">Frete</h6>
                                            </td>
                                            <td className="cart_total_amount">
                                                <h5 className="text-heading text-end">Grátis</h5>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td scope="col" colSpan="2">
                                                <div className="divider-2 mt-10 mb-10"></div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td className="cart_total_label">
                                                <h6 className="text-muted">Total</h6>
                                            </td>
                                            <td className="cart_total_amount">
                                                <h4 className="text-brand text-end">R${cartTotal.toFixed(2)}</h4>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            {cartItems.length > 0 && (
                                <a href="/checkout/" className="btn mb-20 w-100">Prosseguir para o Checkout<i className="fi-rs-sign-out ml-15"></i></a>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default CartPage;
