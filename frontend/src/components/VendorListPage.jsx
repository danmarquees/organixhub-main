import React from 'react';

const VendorListPage = ({ vendedores, totalCount }) => {
    return (
        <main className="main pages mb-80">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Home</a>
                        <span></span> Lista de Vendedores
                    </div>
                </div>
            </div>
            <div className="page-content pt-50">
                <div className="container">
                    <div className="archive-header-2 text-center">
                        <h1 className="display-2 mb-50">Lista de Vendedores</h1>
                        <div className="row">
                            <div className="col-lg-5 mx-auto">
                                <div className="sidebar-widget-2 widget_search mb-50">
                                    <div className="search-form">
                                        <form action="#">
                                            <input type="text" placeholder="Pesquisar fornecedores (por nome ou ID)..." />
                                            <button type="submit">
                                                <i className="fi-rs-search"></i>
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="row mb-50">
                        <div className="col-12 col-lg-8 mx-auto">
                            <div className="shop-product-fillter">
                                <div className="totall-product">
                                    <p>
                                        Temos <strong className="text-brand">{totalCount}</strong> vendedor{totalCount !== 1 ? 'es' : ''} agora
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
                                                <li><a className="active" href="#">Shopping</a></li>
                                                <li><a href="#">Destaques</a></li>
                                                <li><a href="#">Preferidos</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="row vendor-grid">
                        {vendedores.map(v => (
                            <div className="col-lg-6 col-md-6 col-12 col-sm-6" key={v.vid}>
                                <div className="vendor-wrap style-2 mb-40">
                                    <div className="vendor-img-action-wrap">
                                        <div className="vendor-img">
                                            <a href={`/vendor/${v.vid}`}>
                                                <img className="default-img" src={v.imagem} alt={v.titulo} />
                                            </a>
                                        </div>
                                        <div className="mt-10">
                                            <span className="font-small total-product">{v.quantidade_produtos} Produtos</span>
                                        </div>
                                    </div>
                                    <div className="vendor-content-wrap">
                                        <div className="mb-30">
                                            <div className="product-category">
                                                <span className="text-muted">{v.data_ano}</span>
                                            </div>
                                            <h4 className="mb-5">
                                                <a href={`/vendor/${v.vid}`}>{v.titulo}</a>
                                            </h4>
                                            <div className="product-rate-cover">
                                                <div className="product-rate d-inline-block">
                                                    <div className="product-rating" style={{ width: '90%' }}></div>
                                                </div>
                                                <span className="font-small ml-5 text-muted"> (4.0)</span>
                                            </div>
                                            <div className="vendor-info d-flex justify-content-between align-items-end mt-30">
                                                <ul className="contact-infor text-muted">
                                                    <li>
                                                        <img src="/static/assets/imgs/theme/icons/icon-location.svg" alt="" />
                                                        <strong>Endereço: </strong>
                                                        <span>{v.endereco}</span>
                                                    </li>
                                                    <li>
                                                        <img src="/static/assets/imgs/theme/icons/icon-contact.svg" alt="" />
                                                        <strong>Telefone: </strong>
                                                        <span>{v.contato}</span>
                                                    </li>
                                                </ul>
                                            </div>
                                            <br />
                                            <a href={`/vendor/${v.vid}`} className="btn btn-xs">
                                                Visitar Loja<i className="fi-rs-arrow-small-right"></i>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="pagination-area mt-20 mb-20">
                        <nav aria-label="Page navigation example">
                            <ul className="pagination justify-content-start">
                                <li className="page-item"><a className="page-link" href="#"><i className="fi-rs-arrow-small-left"></i></a></li>
                                <li className="page-item active"><a className="page-link" href="#">1</a></li>
                                <li className="page-item"><a className="page-link" href="#">2</a></li>
                                <li className="page-item"><a className="page-link dot" href="#">...</a></li>
                                <li className="page-item"><a className="page-link" href="#"><i className="fi-rs-arrow-small-right"></i></a></li>
                            </ul>
                        </nav>
                    </div>

                </div>
            </div>
        </main>
    );
};

export default VendorListPage;
