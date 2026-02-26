import React, { useState, useEffect } from 'react';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const [cartTotal, setCartTotal] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    const loadCart = () => {
        setIsLoading(true);
        fetch('/api/cart/')
            .then(res => res.json())
            .then(data => {
                // Convert object to array for mapping
                const itemsArray = Object.keys(data.cart_data).map(key => ({
                    ...data.cart_data[key],
                    product_id: key
                }));
                setCartItems(itemsArray);
                setCartTotal(data.cart_total_amount);
            })
            .catch(err => console.error("Error loading cart:", err))
            .finally(() => setIsLoading(false));
    };

    useEffect(() => {
        loadCart();
    }, []);

    const updateQuantity = (productId, newQty) => {
        if (newQty < 1) return; // Prevent 0 or negative quantities

        let formData = new FormData();
        formData.append('id', productId);
        formData.append('quantity', newQty);

        // Django expects CSRF tokens by default on POSTs.  Since we might not want to 
        // fetch it via cookies manually yet, we can try using the GET version of add-to-cart
        // for updates (which works similarly to append) - or use the csrf cookie.
        // Assuming CSRF is disabled on the API endpoints for now or using fetch defaults.
        fetch(`/update-cart/`, {
            method: 'POST',
            body: formData,
            headers: {
                // If CSRF is strictly enforced by Django for POST:
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    loadCart();
                }
            });
    };

    const deleteItem = (productId) => {
        fetch(`/delete-item-from-cart/?id=${productId}`)
            .then(res => res.json())
            .then(data => {
                loadCart();
            });
    };

    // Helper to get CSRF token if needed for POSTs
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    if (isLoading) {
        return <div className="text-center mt-50">Carregando carrinho...</div>;
    }

    if (cartItems.length === 0) {
        return (
            <div className="text-center mt-50 mb-50">
                <h2>Seu carrinho está vazio.</h2>
                <a className="btn mt-20" href="/produtos/"><i className="fi-rs-arrow-left mr-10"></i>Ir para Loja</a>
            </div>
        );
    }


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
                                        <th scope="col" className="end">Remover</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {cartItems.map((item, index) => (
                                        <tr className="pt-30" key={item.product_id}>
                                            <td className="custome-checkbox pl-30">
                                                <input className="form-check-input" type="checkbox" name="checkbox" id={`exampleCheckbox${index + 1}`} value="" />
                                                <label className="form-check-label" htmlFor={`exampleCheckbox${index + 1}`}></label>
                                            </td>
                                            <td className="image product-thumbnail pt-40"><img src={item.image} alt={item.title} /></td>
                                            <td className="product-des product-name">
                                                <h6 className="mb-5"><a className="product-name mb-10 text-heading" href={`/produto/${item.pid}`}>{item.title}</a></h6>
                                            </td>
                                            <td className="price" data-title="Price">
                                                <h4 className="text-body">R${parseFloat(item.price).toFixed(2)}</h4>
                                            </td>
                                            <td className="text-center detail-info" data-title="Stock">
                                                <div className="detail-extralink mr-15">
                                                    <div className="detail-qty border radius">
                                                        <a href="#" className="qty-down" onClick={(e) => { e.preventDefault(); updateQuantity(item.product_id, item.qty - 1); }}><i className="fi-rs-angle-small-down"></i></a>
                                                        <input type="number" className="qty-val" value={item.qty} readOnly />
                                                        <a href="#" className="qty-up" onClick={(e) => { e.preventDefault(); updateQuantity(item.product_id, item.qty + 1); }}><i className="fi-rs-angle-small-up"></i></a>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="price" data-title="Price">
                                                <h4 className="text-brand">R${parseFloat(item.subtotal).toFixed(2)}</h4>
                                            </td>
                                            <td className="action text-center" data-title="Remove">
                                                <button style={{ border: 'none', background: 'none' }} className="text-body delete-product" onClick={() => deleteItem(item.product_id)}>
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
                            <a className="btn  mr-10 mb-sm-15" onClick={(e) => { e.preventDefault(); loadCart(); }}><i className="fi-rs-refresh mr-10"></i>Atualizar Carrinho</a>
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
                                                <h4 className="text-brand text-end">R${parseFloat(cartTotal).toFixed(2)}</h4>
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
                                                <h4 className="text-brand text-end">R${parseFloat(cartTotal).toFixed(2)}</h4>
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
