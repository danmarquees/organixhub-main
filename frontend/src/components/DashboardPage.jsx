import React, { useEffect, useRef, useState } from 'react';
import Chart from 'chart.js/auto';

const DashboardPage = ({ csrfToken, userProfile, ordersList, addressesList, monthLabels, monthlyTotals }) => {
    const chartRef = useRef(null);
    const chartInstance = useRef(null);
    const [activeTab, setActiveTab] = useState('profile');

    useEffect(() => {
        if (activeTab === 'dashboard' && chartRef.current) {
            if (chartInstance.current) {
                chartInstance.current.destroy();
            }

            chartInstance.current = new Chart(chartRef.current, {
                type: 'bar',
                data: {
                    labels: monthLabels || [],
                    datasets: [{
                        label: 'Histórico de Pedidos',
                        data: monthlyTotals || [],
                        backgroundColor: 'rgb(59, 183, 126)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        return () => {
            if (chartInstance.current) {
                chartInstance.current.destroy();
            }
        };
    }, [activeTab, monthLabels, monthlyTotals]);

    return (
        <main className="main pages">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Home</a>
                        <span></span> Páginas <span></span> Minha Conta
                    </div>
                </div>
            </div>

            <div className="page-content pt-150 pb-150">
                <div className="container">
                    <div className="row">
                        <div className="col-lg-10 m-auto">
                            <div className="row">
                                <div className="col-md-3">
                                    <div className="dashboard-menu">
                                        <ul className="nav flex-column" role="tablist">
                                            <li className="nav-item">
                                                <a className={`nav-link ${activeTab === 'profile' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('profile'); }} href="#profile">
                                                    <i className="fi-rs-user mr-10"></i>Perfil
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('dashboard'); }} href="#dashboard">
                                                    <i className="fi-rs-settings-sliders mr-10"></i>Dashboard
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className={`nav-link ${activeTab === 'orders' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('orders'); }} href="#orders">
                                                    <i className="fi-rs-shopping-bag mr-10"></i>Pedidos
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className={`nav-link ${activeTab === 'track-orders' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('track-orders'); }} href="#track-orders">
                                                    <i className="fi-rs-shopping-cart-check mr-10"></i>Rastreie seu pedido
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className={`nav-link ${activeTab === 'address' ? 'active' : ''}`} onClick={(e) => { e.preventDefault(); setActiveTab('address'); }} href="#address">
                                                    <i className="fi-rs-marker mr-10"></i>Meu endereço
                                                </a>
                                            </li>
                                            <li className="nav-item">
                                                <a className="nav-link" href="/user/sign-in/"> {/* Reusing standard logout route logic */}
                                                    <i className="fi-rs-sign-out mr-10"></i>Sair
                                                </a>
                                            </li>
                                        </ul>
                                    </div>
                                    <span className="mt-3 block text-center font-bold">{userProfile?.username || 'Nome de Usuário'}</span>
                                </div>

                                <div className="col-md-9">
                                    <div className="tab-content account dashboard-content pl-50">

                                        {/* PROFILE TAB */}
                                        {activeTab === 'profile' && (
                                            <div className="tab-pane fade active show" id="profile">
                                                <div className="card">
                                                    <div className="card-header border-bottom">
                                                        <h3 className="mb-0">Meu Perfil</h3>
                                                    </div>
                                                    <div className="card-body mb-2" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                                        <div>
                                                            <img
                                                                src={userProfile?.imagem || "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"}
                                                                style={{ width: '150px', objectFit: 'cover', height: '150px', borderRadius: '50%' }}
                                                                alt="Avatar"
                                                            />
                                                        </div>
                                                        <div>
                                                            <span><input className="mb-2 form-control" type="text" readOnly value={`Nome: ${userProfile?.nome || ''}`} /></span>
                                                            <span><input className="mb-2 form-control" type="text" readOnly value={`Bio: ${userProfile?.bio || ''}`} /></span>
                                                            <span><input className="mb-2 form-control" type="text" readOnly value={`Telefone: ${userProfile?.telefone || ''}`} /></span>

                                                            {userProfile?.verificado ? (
                                                                <div className="p-4 border rounded mt-2">
                                                                    <span>Verificado </span><span className="text-success"><i className="fas fa-check-circle"></i></span>
                                                                </div>
                                                            ) : (
                                                                <div className="p-4 border rounded mt-2">
                                                                    <span>Não Verificado </span><span className="text-danger"><i className="fas fa-times"></i></span>
                                                                </div>
                                                            )}
                                                            <div className="p-4">
                                                                <a className="btn btn-success" href="/user/profile/update/">Editar Perfil</a>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                        {/* DASHBOARD TAB */}
                                        {activeTab === 'dashboard' && (
                                            <div className="tab-pane fade active show" id="dashboard">
                                                <div className="card">
                                                    <div className="card-header">
                                                        <h3 className="mb-0">Olá {userProfile?.username || 'Usuário'}!</h3>
                                                    </div>
                                                    <div className="card-body">
                                                        <p>
                                                            Do seu painel de conta, você pode facilmente verificar e visualizar seus
                                                            <a href="#" onClick={(e) => { e.preventDefault(); setActiveTab('orders'); }}> pedidos recentes</a>,<br />
                                                            gerenciar seus <a href="#" onClick={(e) => { e.preventDefault(); setActiveTab('address'); }}>endereços de envio e cobrança</a> e <a
                                                                href="/user/profile/update/">editar sua senha e detalhes da conta.</a>
                                                        </p>
                                                    </div>
                                                    <div>
                                                        <canvas style={{ height: '300px' }} ref={chartRef}></canvas>
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                        {/* ORDERS TAB */}
                                        {activeTab === 'orders' && (
                                            <div className="tab-pane fade active show" id="orders">
                                                <div className="card">
                                                    <div className="card-header">
                                                        <h3 className="mb-0">Seus Pedidos</h3>
                                                    </div>
                                                    <div className="card-body">
                                                        <div className="table-responsive">
                                                            <table className="table">
                                                                <thead>
                                                                    <tr>
                                                                        <th>Pedido</th>
                                                                        <th>Data</th>
                                                                        <th>Status</th>
                                                                        <th>Status de Pgto.</th>
                                                                        <th>Total</th>
                                                                        <th>Ações</th>
                                                                    </tr>
                                                                </thead>
                                                                <tbody>
                                                                    {ordersList && ordersList.length > 0 ? ordersList.map(o => (
                                                                        <tr key={o.id}>
                                                                            <td>PEDIDO_Nº{o.id}</td>
                                                                            <td>{o.data_pedido}</td>
                                                                            <td style={{ textTransform: 'capitalize' }}>{o.status_produto}</td>
                                                                            <td>
                                                                                {o.status_pagamento ?
                                                                                    <i className="fas fa-check-circle text-success"></i> :
                                                                                    <i className="fas fa-times text-danger"></i>
                                                                                }
                                                                            </td>
                                                                            <td>R${o.preco}</td>
                                                                            <td><a href={`/order-detail/${o.id}/`} className="btn-small d-block">Ver</a></td>
                                                                        </tr>
                                                                    )) : (
                                                                        <tr>
                                                                            <td colSpan="6" className="text-center">Nenhum pedido encontrado.</td>
                                                                        </tr>
                                                                    )}
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                        {/* TRACK ORDERS TAB */}
                                        {activeTab === 'track-orders' && (
                                            <div className="tab-pane fade active show" id="track-orders">
                                                <div className="card">
                                                    <div className="card-header">
                                                        <h3 className="mb-0">Rastreio de pedidos</h3>
                                                    </div>
                                                    <div className="card-body contact-from-area">
                                                        <p>Para rastrear seu pedido, insira seu ID de pedido na caixa abaixo e
                                                            pressione o botão "Rastrear". Isso foi fornecido a você em seu recibo e
                                                            no e-mail de confirmação que você deve ter recebido.</p>
                                                        <div className="row">
                                                            <div className="col-lg-8">
                                                                <form className="contact-form-style mt-30 mb-50" action="#" method="post">
                                                                    <div className="input-style mb-20">
                                                                        <label>ID do pedido</label>
                                                                        <input name="order-id" placeholder="Encontrado no seu e-mail de confirmação de pedido" type="text" />
                                                                    </div>
                                                                    <div className="input-style mb-20">
                                                                        <label>E-mail de cobrança</label>
                                                                        <input name="billing-email" placeholder="E-mail usado durante o checkout" type="email" />
                                                                    </div>
                                                                    <button className="submit submit-auto-width" type="button" onClick={() => alert('Integração de rastreio não implementada nesta fase.')}>Rastrear</button>
                                                                </form>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                        {/* ADDRESS TAB */}
                                        {activeTab === 'address' && (
                                            <div className="tab-pane fade active show" id="address">
                                                <div className="row">
                                                    <div className="col-lg-12">
                                                        <div className="card">
                                                            <div className="card-header">
                                                                <h5 className="mb-0">Adicionar endereço</h5>
                                                            </div>
                                                            <div className="card-body">
                                                                {/* For Phase 6 we submit standard form to Django */}
                                                                <form method="POST">
                                                                    <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />
                                                                    <input type="hidden" name="num_addresses" value="1" />
                                                                    <div className="row">
                                                                        <div className="form-group col-md-6">
                                                                            <label>Logradouro</label>
                                                                            <input type="text" className="form-control" name="logradouro_0" placeholder="Logradouro" required />
                                                                        </div>
                                                                        <div className="form-group col-md-6">
                                                                            <label>Número</label>
                                                                            <input type="text" className="form-control" name="numero_0" placeholder="Número" />
                                                                        </div>
                                                                        <div className="form-group col-md-6">
                                                                            <label>Complemento</label>
                                                                            <input type="text" className="form-control" name="complemento_0" placeholder="Complemento" />
                                                                        </div>
                                                                        <div className="form-group col-md-6">
                                                                            <label>Bairro</label>
                                                                            <input type="text" className="form-control" name="bairro_0" placeholder="Bairro" required />
                                                                        </div>
                                                                        <div className="form-group col-md-6">
                                                                            <label>Localidade</label>
                                                                            <input type="text" className="form-control" name="localidade_0" placeholder="Localidade" required />
                                                                        </div>
                                                                        <div className="form-group col-md-6">
                                                                            <label>UF</label>
                                                                            <input type="text" className="form-control" name="uf_0" placeholder="UF" required />
                                                                        </div>
                                                                        <div className="form-group col-md-6">
                                                                            <label>CEP</label>
                                                                            <input type="text" className="form-control" name="cep_0" placeholder="CEP" required />
                                                                        </div>
                                                                        <div className="form-group col-md-6">
                                                                            <label>Celular</label>
                                                                            <input type="tel" className="form-control" name="celular_0" placeholder="Celular" />
                                                                        </div>
                                                                        <div className="col-md-12">
                                                                            <button type="submit" className="btn btn-fill-out submit font-weight-bold">Salvar endereço</button>
                                                                        </div>
                                                                    </div>
                                                                </form>
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <div className="row mt-4">
                                                        {addressesList && addressesList.length > 0 ? addressesList.map((addr, idx) => (
                                                            <div className="col-lg-6" key={addr.id}>
                                                                <div className="card mb-3">
                                                                    <div className="card-header">
                                                                        <h4 className="mb-0">Endereço de Entrega {idx + 1}</h4>
                                                                    </div>
                                                                    <div className="card-body border rounded">
                                                                        <address>
                                                                            <p><strong>Logradouro:</strong> {addr.logradouro}, <strong>Número:</strong> {addr.numero}</p>
                                                                            <p><strong>Bairro:</strong> {addr.bairro}, <strong>Localidade:</strong> {addr.localidade}, <strong>UF:</strong> {addr.uf}</p>
                                                                            <p><strong>CEP:</strong> {addr.cep}</p>
                                                                            <p><strong>Celular:</strong> {addr.celular}</p>
                                                                        </address>
                                                                        <br />
                                                                        {addr.status ? (
                                                                            <>
                                                                                <i className="fa fa-check-circle text-success check-icon"> Padrão Ativo</i>
                                                                                <button className="btn btn-danger delete-address action_btn ms-2">Deletar</button>
                                                                            </>
                                                                        ) : (
                                                                            <>
                                                                                <button className="btn make-default-address action_btn">Tornar Padrão</button>
                                                                                <button className="btn btn-danger delete-address action_btn ms-2">Deletar</button>
                                                                            </>
                                                                        )}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        )) : null}
                                                    </div>
                                                </div>
                                            </div>
                                        )}

                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default DashboardPage;
