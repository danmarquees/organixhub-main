import React, { useState, useEffect } from 'react';

const ProductDetailPage = ({ pid }) => {
    const [produto, setProduto] = useState(null);
    const [relatedProducts, setRelatedProducts] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);
    const [activeTab, setActiveTab] = useState('Description');

    useEffect(() => {
        const fetchProduct = async () => {
            setIsLoading(true);
            try {
                // Fetch all products to find ours, as we don't have a single-item API endpoint yet.
                const res = await fetch('/api/produtos/');
                if (res.ok) {
                    const data = await res.json();
                    const productData = data.find(p => p.pid === pid);
                    if (productData) {
                        setProduto(productData);
                        // Also populate some related products for the bottom section
                        setRelatedProducts(data.filter(p => p.pid !== pid).slice(0, 4));
                    }
                }
            } catch (err) {
                console.error("Error fetching product details:", err);
            } finally {
                setIsLoading(false);
            }
        };
        fetchProduct();
    }, [pid]);

    const addToCart = (e) => {
        e.preventDefault();
        if (!produto) return;

        // POST to Django view to add to cart
        fetch(`/add-to-cart/?id=${produto.id}&qty=${quantity}`)
            .then(res => res.json())
            .then(data => alert('Adicionado ao carrinho com sucesso!'))
            .catch(err => console.error(err));
    };

    if (isLoading) {
        return <div className="text-center mt-50 mb-50">Carregando detalhes do produto...</div>;
    }

    if (!produto) {
        return <div className="text-center mt-50 mb-50">Produto não encontrado.</div>;
    }

    return (
        <main className="main">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Início</a>
                        <span></span> <a href="#">{produto.categoria?.titulo || 'Categoria'}</a>
                        <span></span> {produto.titulo}
                    </div>
                </div>
            </div>
            <div className="container mb-30">
                <div className="row">
                    <div className="col-xl-11 col-lg-12 m-auto">
                        <div className="row">
                            <div className="col-xl-9">
                                <div className="product-detail accordion-detail">
                                    <div className="row mb-50 mt-30">
                                        <div className="col-md-6 col-sm-12 col-xs-12 mb-md-0 mb-sm-5">
                                            <div className="detail-gallery">
                                                <div className="product-image-slider">
                                                    <figure className="border-radius-10">
                                                        <img src={produto.imagem} alt="product" style={{ aspectRatio: '1/1', objectFit: 'cover' }} />
                                                    </figure>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="col-md-6 col-sm-12 col-xs-12">
                                            <div className="detail-info pr-30 pl-30">
                                                <span className="stock-status out-stock"> Desconto </span>
                                                <h2 className="title-detail">{produto.titulo}</h2>
                                                <div className="clearfix product-price-cover mt-10">
                                                    <div className="product-price primary-color float-left">
                                                        <span className="current-price text-brand">R$</span>
                                                        <span className="current-price text-brand">{produto.preco}</span>
                                                        {produto.preco_antigo && (
                                                            <span>
                                                                <span className="old-price font-md ml-15">R${produto.preco_antigo}</span>
                                                            </span>
                                                        )}
                                                    </div>
                                                </div>
                                                <div className="short-desc mb-30 mt-20">
                                                    {/* In a real app we might use dangerouslySetInnerHTML if description is HTML */}
                                                    <p className="font-lg">{produto.descricao?.substring(0, 200)}...</p>
                                                </div>

                                                <div className="detail-extralink mb-50">
                                                    <div className="detail-qty border radius">
                                                        <a href="#" className="qty-down" onClick={(e) => { e.preventDefault(); setQuantity(Math.max(1, quantity - 1)); }}><i className="fi-rs-angle-small-down"></i></a>
                                                        <input type="number" min="1" value={quantity} readOnly className="qty-val" />
                                                        <a href="#" className="qty-up" onClick={(e) => { e.preventDefault(); setQuantity(quantity + 1); }}><i className="fi-rs-angle-small-up"></i></a>
                                                    </div>
                                                    <div className="product-extra-link2">
                                                        <button type="button" className="button button-add-to-cart" onClick={addToCart}>
                                                            <i className="fi-rs-shopping-cart"></i>Adicionar ao carrinho
                                                        </button>
                                                        <a aria-label="Add To Wishlist" className="action-btn hover-up" href="#"><i className="fi-rs-heart"></i></a>
                                                        <a aria-label="Compare" className="action-btn hover-up" href="#"><i className="fi-rs-shuffle"></i></a>
                                                    </div>
                                                </div>
                                                <div className="font-xs">
                                                    <ul className="mr-50 float-start">
                                                        <li className="mb-5">Tipo: <span className="text-brand">Orgânico</span></li>
                                                        <li className="mb-5">Stock: <span className="text-brand">{produto.em_estoque ? 'Em Estoque' : 'Indisponível'}</span></li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="product-info">
                                        <div className="tab-style3">
                                            <ul className="nav nav-tabs text-uppercase">
                                                <li className="nav-item">
                                                    <a className={`nav-link ${activeTab === 'Description' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('Description'); }} href="#Description">Descrição</a>
                                                </li>
                                                <li className="nav-item">
                                                    <a className={`nav-link ${activeTab === 'Additional-info' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('Additional-info'); }} href="#Additional-info">Informações adicionais</a>
                                                </li>
                                                <li className="nav-item">
                                                    <a className={`nav-link ${activeTab === 'Vendor-info' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('Vendor-info'); }} href="#Vendor-info">Vendedor</a>
                                                </li>
                                            </ul>
                                            <div className="tab-content shop_info_tab entry-main-content">
                                                {activeTab === 'Description' && (
                                                    <div className="tab-pane fade show active">
                                                        <div dangerouslySetInnerHTML={{ __html: produto.descricao || 'Nenhuma descrição fornecida.' }} />
                                                    </div>
                                                )}
                                                {activeTab === 'Additional-info' && (
                                                    <div className="tab-pane fade show active">
                                                        <p>Mais detalhes estarão disponíveis em breve.</p>
                                                    </div>
                                                )}
                                                {activeTab === 'Vendor-info' && (
                                                    <div className="tab-pane fade show active">
                                                        {produto.vendedor ? (
                                                            <div className="vendor-logo d-flex mb-30">
                                                                <div className="vendor-name ml-15">
                                                                    <h6>{produto.vendedor.titulo}</h6>
                                                                    <p>{produto.vendedor.endereco}</p>
                                                                </div>
                                                            </div>
                                                        ) : (
                                                            <p>Informação do Vendedor Indisponível</p>
                                                        )}
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="row mt-60">
                                        <div className="col-12">
                                            <h2 className="section-title style-1 mb-30">Produtos relacionados</h2>
                                        </div>
                                        <div className="col-12">
                                            <div className="row related-products">
                                                {relatedProducts.map(rp => (
                                                    <div className="col-lg-3 col-md-4 col-12 col-sm-6" key={rp.id}>
                                                        <div className="product-cart-wrap hover-up">
                                                            <div className="product-img-action-wrap">
                                                                <div className="product-img product-img-zoom">
                                                                    <a href={`/produto/${rp.pid}`}>
                                                                        <img className="default-img" src={rp.imagem} alt="" style={{ aspectRatio: '1/1', objectFit: 'cover' }} />
                                                                    </a>
                                                                </div>
                                                                <div className="product-badges product-badges-position product-badges-mrg">
                                                                    <span className="hot">Oferta</span>
                                                                </div>
                                                            </div>
                                                            <div className="product-content-wrap">
                                                                <h2><a href={`/produto/${rp.pid}`}>{rp.titulo?.substring(0, 20)}</a></h2>
                                                                <div className="product-price">
                                                                    <span>R$</span> <span>{rp.preco}</span>
                                                                    {rp.preco_antigo && <span className="old-price">R${rp.preco_antigo}</span>}
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="col-xl-3 primary-sidebar sticky-sidebar mt-30">
                                <div className="sidebar-widget widget-delivery mb-30 bg-grey-9 box-shadow-none">
                                    <h5 className="section-title style-3 mb-20">Endereço de Entrega</h5>
                                    <ul>
                                        <li>
                                            <i className="fi fi-rs-marker mr-10 text-brand"></i>
                                            <span>Faça login para ver informações de endereço.</span>
                                            <a href="#" className="change float-end">Login</a>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default ProductDetailPage;
