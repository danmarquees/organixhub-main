import React from 'react';

const SearchPage = ({ query, produtos, resultCount }) => {
    const handleAddToCart = (e, productId) => {
        e.preventDefault();
        fetch(`/add-to-cart/?id=${productId}&qty=1`)
            .then(res => res.json())
            .then(data => alert('Adicionado ao carrinho com sucesso!'))
            .catch(err => console.error("Error adding to cart: ", err));
    };

    return (
        <main className="main">
            <div className="page-header mt-30 mb-50">
                <div className="container">
                    <div className="archive-header">
                        <div className="row align-items-center">
                            <div className="col-xl-3">
                                {query ? (
                                    <h1 className="mb-15">{query}</h1>
                                ) : (
                                    <h3 className="mb-15">Ítem Não Encontrado</h3>
                                )}
                                <div className="breadcrumb">
                                    <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Home</a>
                                    <span></span> Loja <span></span> Busca <span></span> {query}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="container mb-30">
                <div className="row">
                    <div className="col-12">
                        <div className="shop-product-fillter">
                            <div className="totall-product">
                                <p>
                                    Encontramos <strong className="text-brand">{resultCount}</strong> itens
                                </p>
                            </div>
                            <div className="sort-by-product-area">
                                <div className="sort-by-cover mr-10">
                                    <div className="sort-by-product-wrap">
                                        <div className="sort-by">
                                            <span><i className="fi-rs-apps"></i>Mostrar:</span>
                                        </div>
                                        <div className="sort-by-dropdown-wrap">
                                            <span> 50 <i className="fi-rs-angle-small-down"></i></span>
                                        </div>
                                    </div>
                                    <div className="sort-by-dropdown">
                                        <ul>
                                            <li><a className="active" href="#">50</a></li>
                                            <li><a href="#">100</a></li>
                                            <li><a href="#">150</a></li>
                                            <li><a href="#">200</a></li>
                                            <li><a href="#">Todos</a></li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="sort-by-cover">
                                    <div className="sort-by-product-wrap">
                                        <div className="sort-by">
                                            <span><i className="fi-rs-apps-sort"></i>Ordenar por:</span>
                                        </div>
                                        <div className="sort-by-dropdown-wrap">
                                            <span> Destaques <i className="fi-rs-angle-small-down"></i></span>
                                        </div>
                                    </div>
                                    <div className="sort-by-dropdown">
                                        <ul>
                                            <li><a className="active" href="#">Destaques</a></li>
                                            <li><a href="#">Preço: Menor para Maior</a></li>
                                            <li><a href="#">Preço: Maior para Menor</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="row product-grid">
                            {produtos.map(p => (
                                <div className="col-lg-2 col-md-4 col-12 col-sm-6" key={p.id}>
                                    <div className="product-cart-wrap mb-30 wow animate__animated animate__fadeIn" data-wow-delay=".1s">
                                        <div className="product-img-action-wrap">
                                            <div className="product-img product-img-zoom">
                                                <a href={`/produto/${p.pid}`}>
                                                    <img className="default-img" src={p.imagem} alt="" style={{ aspectRatio: '1/1', objectFit: 'cover' }} />
                                                    <img className="hover-img" src={p.imagem} alt="" style={{ aspectRatio: '1/1', objectFit: 'cover' }} />
                                                </a>
                                            </div>
                                            <div className="product-action-1">
                                                <a aria-label="Adicionar à Lista de Desejos" className="action-btn" href="#"><i className="fi-rs-heart"></i></a>
                                                <a aria-label="Comparar" className="action-btn" href="#"><i className="fi-rs-shuffle"></i></a>
                                                <a aria-label="Visualização Rápida" className="action-btn" data-bs-toggle="modal" data-bs-target="#quickViewModal"><i className="fi-rs-eye"></i></a>
                                            </div>
                                        </div>
                                        <div className="product-content-wrap">
                                            <div className="product-category">
                                                <a href="#">{p.categoria_titulo}</a>
                                            </div>
                                            <h2><a href={`/produto/${p.pid}`}>{p.titulo}</a></h2>
                                            <div className="product-rate-cover">
                                                <div className="product-rate d-inline-block">
                                                    <div className="product-rating" style={{ width: `${p.media_avaliacoes || 80}%` }}></div>
                                                </div>
                                                <span className="font-small ml-5 text-muted">(4.0)</span>
                                            </div>
                                            <div>
                                                {p.vendedor_titulo && (
                                                    <span className="font-small text-muted">Por <a href="#">{p.vendedor_titulo}</a></span>
                                                )}
                                            </div>
                                            <div className="product-card-bottom">
                                                <div className="product-price">
                                                    <span>R$ {p.preco}</span>
                                                    {p.preco_antigo && <span className="old-price">R$ {p.preco_antigo}</span>}
                                                </div>
                                                <div className="add-cart">
                                                    <button
                                                        className="add btn w-100 hover-up"
                                                        style={{ border: 'none' }}
                                                        onClick={(e) => handleAddToCart(e, p.id)}
                                                    >
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
            </div>
        </main>
    );
};

export default SearchPage;
