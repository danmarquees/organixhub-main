import React, { useState, useEffect } from 'react';

const IndexPage = () => {
    const [categorias, setCategorias] = useState([]);
    const [produtosDestaque, setProdutosDestaque] = useState([]);
    const [produtosRecentes, setProdutosRecentes] = useState([]);
    const [produtosPopulares, setProdutosPopulares] = useState([]);

    // For now we will map the tab content strictly, using the same endpoint initially 
    // to simulate the "Popular" vs "News" vs "Highlights" until more complex 
    // views are needed filtering by tag or sold quantities.

    useEffect(() => {
        // Fetch Categories
        fetch('/api/categorias/')
            .then(res => res.json())
            .then(data => setCategorias(data))
            .catch(err => console.error("Error fetching categories: ", err));

        // Fetch Featured Products
        fetch('/api/produtos/destaques/')
            .then(res => res.json())
            .then(data => setProdutosDestaque(data))
            .catch(err => console.error("Error fetching featured products: ", err));

        // Fetch Recent Products
        fetch('/api/produtos/recentes/')
            .then(res => res.json())
            .then(data => setProdutosRecentes(data))
            .catch(err => console.error("Error fetching recent products: ", err));

        // Fetch Popular Products (Mocking it as recent for now until we build a popularity filter)
        fetch('/api/produtos/')
            .then(res => res.json())
            .then(data => setProdutosPopulares(data))
            .catch(err => console.error("Error fetching popular products: ", err));

    }, []);


    return (
        <main className="main">
            {/* ... Modal and Hero Slider ... */}

            <div className="container mb-30">
                <div className="row flex-row-reverse">
                    <div className="col-lg-4-5">
                        {/* Hero Section Placeholder */}
                        <section className="home-slider position-relative mb-30">
                            {/* Converting slider structure ... */}
                        </section>

                        <section className="product-tabs section-padding position-relative">
                            <div className="section-title style-2">
                                <h3>Produtos Populares</h3>
                                <ul className="nav nav-tabs links" id="myTab" role="tablist">
                                    {categorias.slice(0, 5).map((c, index) => (
                                        <li className="nav-item" role="presentation" key={c.cid}>
                                            <a
                                                className={`nav-link ${index === 0 ? 'active' : ''}`}
                                                id={`nav-tab-${index}`}
                                                data-bs-toggle="tab"
                                                data-bs-target={`#tab-${index}`}
                                                type="button"
                                                role="tab"
                                                aria-controls={`tab-${index}`}
                                                aria-selected={index === 0 ? "true" : "false"}
                                                href={`/categoria/${c.cid}`}
                                            >
                                                {c.titulo}
                                            </a>
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <div className="tab-content" id="myTabContent">
                                <div className="tab-pane fade show active" id="tab-one" role="tabpanel" aria-labelledby="tab-one">
                                    <div className="row product-grid-4">
                                        {produtosPopulares.map(p => (
                                            <div className="col-lg-3 col-md-4 col-12 col-sm-6" key={p.pid}>
                                                <div className="product-cart-wrap mb-30 wow animate__animated animate__fadeIn" data-wow-delay=".1s">
                                                    <div className="product-img-action-wrap">
                                                        <div className="product-img product-img-zoom">
                                                            <a href={`/produto/${p.pid}/`}>
                                                                <img className="default-img" src={p.imagem} alt={p.titulo} style={{ aspectRatio: '1/1', objectFit: 'cover' }} />
                                                                <img className="hover-img" src={p.imagem} alt={p.titulo} style={{ aspectRatio: '3/4', objectFit: 'cover' }} />
                                                            </a>
                                                        </div>
                                                        <div className="product-action-1">
                                                            <a aria-label="Adicionar à Wishlist" className="action-btn add-to-wishlist" data-product-item={p.id}>
                                                                <i className="fi-rs-heart"></i>
                                                            </a>
                                                            <a aria-label="Comparar" className="action-btn" href="shop-compare.html"><i className="fi-rs-shuffle"></i></a>
                                                            <a aria-label="Visualização Rápida" className="action-btn" data-bs-toggle="modal" data-bs-target={`#quickViewModal${p.pid}`} href={`/produto/${p.pid}/`}>
                                                                <i className="fi-rs-eye"></i>
                                                            </a>
                                                        </div>
                                                        <div className="product-badges product-badges-position product-badges-mrg">
                                                            {p.badges && p.badges.map(badge => (
                                                                <span className={badge} key={badge}>{badge}</span>
                                                            ))}
                                                        </div>
                                                    </div>
                                                    <div className="product-content-wrap">
                                                        <div className="product-category">
                                                            <a href="shop-grid-right.html">{p.categoria?.titulo}</a>
                                                        </div>
                                                        <h2><a href={`/produto/${p.pid}/`}>{p.titulo}</a></h2>
                                                        <div className="product-rate-cover">
                                                            <div className="product-rate d-inline-block">
                                                                {/* Assuming product rating is out of 5 and calculated to % */}
                                                                <div className="product-rating" style={{ width: `${p.media_avaliacoes || 0}%` }}></div>
                                                            </div>
                                                            <span className="font-small ml-5 text-muted">({p.media_avaliacoes || 0})</span>
                                                        </div>
                                                        <div>
                                                            <span className="font-small text-muted">Por <a href={`/vendedor/${p.vendedor?.vid}`}>{p.vendedor?.titulo}</a></span>
                                                        </div>
                                                        <div className="product-card-bottom">
                                                            <div className="product-price">
                                                                <span>R$</span><span className={`current-product-price-${p.id}`}>{p.preco}</span>
                                                                {p.preco_antigo && (
                                                                    <>
                                                                        <br />
                                                                        <span className="old-price">R$ {p.preco_antigo}</span>
                                                                    </>
                                                                )}
                                                            </div>
                                                            <div className="progress">
                                                                {/* Example logic assuming calculation inside Django is rendered outside. In React: */}
                                                                <span className="progress-bar" role="progressbar" style={{ width: `${p.qtd_vendida}%` }} aria-valuenow={p.qtd_vendida} aria-valuemin="0" aria-valuemax="100">{p.qtd_vendida}% vendido</span>
                                                            </div>
                                                            <div className="add-cart">
                                                                <input type="hidden" defaultValue="1" id="product-quantity" className={`product-quantity-${p.id}`} />
                                                                <button className="add add-to-cart-btn btn w-100 hover-up" data-index={p.id} id="add-to-cart-btn">
                                                                    <i className="fi-rs-shopping-cart mr-5"></i>Adicionar
                                                                </button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* More sections like Deals and Banners placeholder */}
                    </div>
                </div>
            </div>
        </main>
    );
};

export default IndexPage;
