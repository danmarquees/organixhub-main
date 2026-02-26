import React from 'react';

const VendorDetailPage = ({ vendedor, produtos, categorias, totalCount }) => {
    const handleAddToCart = (e, productId) => {
        e.preventDefault();
        fetch(`/add-to-cart/?id=${productId}&qty=1`)
            .then(res => res.json())
            .then(data => alert('Adicionado ao carrinho com sucesso!'))
            .catch(err => console.error("Error adding to cart: ", err));
    };

    return (
        <main className="main">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Home</a>
                        <span></span> Loja <span></span> {vendedor.titulo}
                    </div>
                </div>
            </div>
            <div className="container mb-30">
                <div className="archive-header-3 mt-30 mb-80" style={{ backgroundImage: `url(${vendedor.capa_imagem})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
                    <div className="archive-header-3-inner">
                        <div className="vendor-logo mr-50">
                            <img src={vendedor.imagem} alt={vendedor.titulo} />
                        </div>
                        <div className="vendor-content">
                            <div className="product-category">
                                <span className="text-muted">Desde {vendedor.data_ano}</span>
                            </div>
                            <h3 className="mb-5 text-white"><a href="#" className="text-white">{vendedor.titulo}</a></h3>
                            <div className="product-rate-cover mb-15">
                                <div className="product-rate d-inline-block">
                                    <div className="product-rating" style={{ width: '90%' }}></div>
                                </div>
                                <span className="font-small ml-5 text-muted"> (4.0)</span>
                            </div>
                            <div className="row">
                                <div className="col-lg-4" id="vendor-description">
                                    <div className="vendor-des mb-15">
                                        <p className="font-sm text-white" id="description-text" dangerouslySetInnerHTML={{ __html: vendedor.descricao }} />
                                    </div>
                                </div>
                                <div className="col-lg-3" id="vendor-information">
                                    <div className="vendor-info mb-15">
                                        <ul className="font-sm" id="info-list">
                                            <li>
                                                <img className="mr-5" src="/static/assets/imgs/theme/icons/icon-location.svg" alt="" />
                                                <strong>Endereço: </strong> <span className="text-white" id="address-text">{vendedor.endereco}</span>
                                            </li>
                                            <li>
                                                <img className="mr-5" src="/static/assets/imgs/theme/icons/icon-contact.svg" alt="" />
                                                <strong>Telefone:</strong><span className="text-white" id="phone-text">{vendedor.contato}</span>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="col-lg-4">
                                    <div className="follow-social">
                                        <h6 className="mb-15 text-white">Siga-nos</h6>
                                        <ul className="social-network">
                                            <li className="hover-up"><a href="#"><img src="/static/assets/imgs/theme/icons/social-tw.svg" alt="" /></a></li>
                                            <li className="hover-up"><a href="#"><img src="/static/assets/imgs/theme/icons/social-fb.svg" alt="" /></a></li>
                                            <li className="hover-up"><a href="#"><img src="/static/assets/imgs/theme/icons/social-insta.svg" alt="" /></a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="row flex-row-reverse">
                    <div className="col-lg-4-5">
                        <div className="shop-product-fillter">
                            <div className="totall-product">
                                <p>Encontramos <strong className="text-brand">{totalCount}</strong> itens para você!</p>
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
                                            <li><a href="#">Menor Preço</a></li>
                                            <li><a href="#">Maior Preço</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="row product-grid">
                            {produtos.map(p => (
                                <div className="col-lg-1-5 col-md-4 col-12 col-sm-6" key={p.id}>
                                    <div className="product-cart-wrap mb-30">
                                        <div className="product-img-action-wrap">
                                            <div className="product-img product-img-zoom">
                                                <a href={`/produto/${p.pid}`}>
                                                    <img className="default-img" src={p.imagem} alt={p.titulo} />
                                                    <img className="hover-img" src={p.imagem} alt={p.titulo} />
                                                </a>
                                            </div>
                                            <div className="product-action-1">
                                                <a aria-label="Adicionar à lista de desejos" className="action-btn" href="#"><i className="fi-rs-heart"></i></a>
                                                <a aria-label="Comparar" className="action-btn" href="#"><i className="fi-rs-shuffle"></i></a>
                                                <a aria-label="Visualização rápida" className="action-btn" data-bs-toggle="modal" data-bs-target="#quickViewModal"><i className="fi-rs-eye"></i></a>
                                            </div>
                                            <div className="product-badges product-badges-position product-badges-mrg">
                                                <span className="hot">{p.obter_porcentagem}</span>
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
                                                <span className="font-small ml-5 text-muted"> (4.0)</span>
                                            </div>
                                            <div>
                                                <span className="font-small text-muted">Por <a href="#">{vendedor.titulo}</a></span>
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

                    <div className="col-lg-1-5 primary-sidebar sticky-sidebar">
                        <div className="sidebar-widget widget-store-info mb-30 bg-3 border-0">
                            <div className="vendor-logo mb-30">
                                <img src={vendedor.imagem} alt={vendedor.titulo} />
                            </div>
                            <div className="vendor-info">
                                <div className="product-category">
                                    <span className="text-muted">Desde {vendedor.data_ano}</span>
                                </div>
                                <h4 className="mb-5"><a href="#" className="text-heading">{vendedor.titulo}</a></h4>
                                <div className="product-rate-cover mb-15">
                                    <div className="product-rate d-inline-block">
                                        <div className="product-rating" style={{ width: '90%' }}></div>
                                    </div>
                                    <span className="font-small ml-5 text-muted"> (4.0)</span>
                                </div>
                                <div className="vendor-des mb-30">
                                    <p className="font-sm text-heading" dangerouslySetInnerHTML={{ __html: vendedor.descricao }} />
                                </div>
                                <div className="vendor-info">
                                    <ul className="font-sm mb-20">
                                        <li><img className="mr-5" src="/static/assets/imgs/theme/icons/icon-location.svg" alt="" /><strong>Endereço: </strong> <span>{vendedor.endereco}</span></li>
                                        <li><img className="mr-5" src="/static/assets/imgs/theme/icons/icon-contact.svg" alt="" /><strong>Telefone:</strong><span>{vendedor.contato}</span></li>
                                    </ul>
                                    <a href="#" className="btn btn-xs">Contatar Vendedor <i className="fi-rs-arrow-small-right"></i></a>
                                </div>
                            </div>
                        </div>

                        <div className="sidebar-widget widget-category-2 mb-30">
                            <h5 className="section-title style-1 mb-30">Categorias</h5>
                            <ul>
                                {categorias.map((c, i) => (
                                    <li key={i}>
                                        <a href="#"> <img src={c.imagem} alt="" />{c.titulo}</a><span className="count">{c.count}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default VendorDetailPage;
