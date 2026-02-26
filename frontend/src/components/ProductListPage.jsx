import React, { useState, useEffect } from 'react';

const ProductListPage = () => {
    const [produtos, setProdutos] = useState([]);
    const [categorias, setCategorias] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            try {
                // Fetch categories
                const catRes = await fetch('/api/categorias/');
                if (catRes.ok) {
                    const catData = await catRes.json();
                    setCategorias(catData);
                }

                // Fetch products 
                // We're just fetching the main ones for now. In a full implementation, 
                // the filter queries would dynamically adjust this URL: `/api/produtos/?categoria=X`
                const prodRes = await fetch('/api/produtos/');
                if (prodRes.ok) {
                    const prodData = await prodRes.json();
                    setProdutos(prodData);
                }
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleAddToCart = (e, productId) => {
        e.preventDefault();
        fetch(`/add-to-cart/?id=${productId}&qty=1`)
            .then(res => res.json())
            .then(data => alert('Adicionado ao carrinho com sucesso!'))
            .catch(err => console.error("Error adding to cart: ", err));
    };

    if (isLoading) {
        return <div className="text-center mt-50 mb-50">Carregando loja...</div>;
    }

    return (
        <main className="main">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Home</a>
                        <span></span> Loja <span></span> Filtros
                    </div>
                </div>
            </div>
            <div className="container mb-30 mt-30">
                <div className="row">
                    <div className="col-lg-12">
                        {/* Header Filtros (collapsible) */}
                        <a className="shop-filter-toogle" href="#">
                            <span className="fi-rs-filter mr-5"></span>
                            Filtros
                            <i className="fi-rs-angle-small-down angle-down"></i>
                            <i className="fi-rs-angle-small-up angle-up"></i>
                        </a>
                        <div className="shop-product-fillter-header">
                            <div className="row">
                                <div className="col-xl-3 col-lg-6 col-md-6 mb-lg-0 mb-md-2 mb-sm-2">
                                    <div className="card">
                                        <h5 className="mb-30">Por Categorias</h5>
                                        <div className="categories-dropdown-wrap font-heading" style={{ overflowY: 'auto', maxHeight: '200px' }}>
                                            <ul>
                                                {categorias.map(c => (
                                                    <li key={c.cid}>
                                                        <input data-filter="categoria" className="form-check-input filter-checkbox" type="checkbox" name="checkbox" id={`exampleCheckbox-${c.cid}`} value={c.id} />
                                                        &nbsp;&nbsp;
                                                        <a href={`/categoria/${c.cid}/`}> <img src={c.imagem} alt="" />{c.titulo}</a>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-xl-3 col-lg-6 col-md-6 mb-lg-0 mb-md-2 mb-sm-2">
                                    <div className="card">
                                        <h5 className="mb-30">Por Vendedores</h5>
                                        <div className="d-flex">
                                            <div className="customeeeee-checkbox mr-80">
                                                {/* Placeholder para vendedores */}
                                                <input className="form-check-input filter-checkbox" data-filter="vendedor" type="checkbox" name="checkbox" id="exampleCheckbox1" value="1" />
                                                <label className="form-check-label" htmlFor="exampleCheckbox1"><span>Vendedor Exemplo</span></label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-xl-3 col-lg-6 col-md-6 mb-lg-0 mb-md-2 mb-sm-2">
                                    <div className="card">
                                        <h5 className="mb-30">Por Tags</h5>
                                        <div className="sidebar-widget widget-tags">
                                            <ul className="tags-list">
                                                <li className="hover-up">
                                                    <a href="#"><i className="fi-rs-cross mr-10"></i>Leite</a>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-xl-3 col-lg-6 col-md-6 mb-lg-0 mb-md-5 mb-sm-5">
                                    <div className="card">
                                        <h5 className="mb-10">Por Preço</h5>
                                        <div className="sidebar-widget price_range range">
                                            <div className="price-filter mb-20">
                                                <div className="price-filter-inner">
                                                    <input type="range" name="range" defaultValue="0" id="range" className="slider-range" min="0" max="1000" />
                                                    <div className="d-flex justify-content-between">
                                                        <div className="caption">De: <strong id="slider-range-value1" className="text-brand">R$0.00</strong></div>
                                                        <div className="caption">Até: <strong id="slider-range-value2" className="text-brand">R$1000.00</strong></div>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="custome-checkbox">
                                                <button className="btn mt-20 w-100" type="button" id="price-filter-btn">Filtrar por Preço</button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-12">
                        <div className="shop-product-fillter">
                            <div className="totall-product">
                                <p>Encontramos <strong className="text-brand">{produtos.length}</strong> itens para você!</p>
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
                                </div>
                            </div>
                        </div>

                        <div className="row product-grid" id="filtered-product">
                            {produtos.map(p => (
                                <div className="col-lg-3 col-md-4 col-12 col-sm-6" key={p.id}>
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
                                            <div className="product-badges product-badges-position product-badges-mrg">
                                                <span className="hot">Oferta</span>
                                            </div>
                                        </div>
                                        <div className="product-content-wrap">
                                            <div className="product-category">
                                                <a href="#">{p.categoria?.titulo}</a>
                                            </div>
                                            <h2><a href={`/produto/${p.pid}`}>{p.titulo}</a></h2>
                                            <div className="product-rate-cover">
                                                <div className="product-rate d-inline-block">
                                                    <div className="product-rating" style={{ width: '90%' }}></div>
                                                </div>
                                                <span className="font-small ml-5 text-muted">(4.0)</span>
                                            </div>
                                            <div>
                                                {p.vendedor && (
                                                    <span className="font-small text-muted">Por <a href={`/vendor/${p.vendedor.vid}`}>{p.vendedor.titulo}</a></span>
                                                )}
                                            </div>
                                            <div className="product-card-bottom">
                                                <div className="product-price">
                                                    <span>R$</span><span>{p.preco}</span>
                                                    <br />
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

                        {/* Ofertas placeholder */}
                        <section className="section-padding pb-5">
                            <div className="section-title">
                                <h3 className="">Ofertas do Dia</h3>
                                <a className="show-all" href="#">
                                    Todas as Ofertas
                                    <i className="fi-rs-angle-right"></i>
                                </a>
                            </div>
                            <div className="row">
                                <div className="col-12">
                                    <div className="alert alert-info">As ofertas do dia serão carregadas dinamicamente aqui.</div>
                                </div>
                            </div>
                        </section>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default ProductListPage;
