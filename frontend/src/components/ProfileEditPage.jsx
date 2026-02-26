import React, { useState } from 'react';

const ProfileEditPage = ({ csrfToken, userProfile, formErrors }) => {

    const [nome, setNome] = useState(userProfile?.nome || '');
    const [bio, setBio] = useState(userProfile?.bio || '');
    const [telefone, setTelefone] = useState(userProfile?.telefone || '');

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
                                                <a className="nav-link active" href="/user/dashboard/"><i className="fi-rs-user mr-10"></i>Perfil</a>
                                            </li>
                                            <li className="nav-item">
                                                <a className="nav-link" href="/user/sign-in/"><i className="fi-rs-sign-out mr-10"></i>Sair</a>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div className="col-md-9">
                                    <div className="tab-content account dashboard-content pl-50">
                                        <div className="tab-pane fade active show" id="profile">
                                            <div className="card">
                                                <div className="card-header border-bottom">
                                                    <h3 className="mb-0">Alterar Perfil</h3>
                                                </div>

                                                {formErrors && (
                                                    <div className="alert-danger alert" dangerouslySetInnerHTML={{ __html: formErrors }}></div>
                                                )}

                                                <div className="card-body mb-2" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                                    <div>
                                                        <img
                                                            src={userProfile?.imagem || "https://static.vecteezy.com/system/resources/thumbnails/009/292/244/small/default-avatar-icon-of-social-media-user-vector.jpg"}
                                                            style={{ width: '150px', objectFit: 'cover', height: '150px', borderRadius: '50%' }}
                                                            alt="Profile Avatar"
                                                        />
                                                    </div>
                                                    <div className="card-body mb-2">
                                                        <form method="POST" encType="multipart/form-data">
                                                            <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

                                                            <div className="mb-3">
                                                                <input type="text" name="nome" value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Nome" className="form-control" />
                                                            </div>
                                                            <div className="mb-3">
                                                                <input type="text" name="bio" value={bio} onChange={(e) => setBio(e.target.value)} placeholder="Bio" className="form-control" />
                                                            </div>
                                                            <div className="mb-3">
                                                                <input type="text" name="telefone" value={telefone} onChange={(e) => setTelefone(e.target.value)} placeholder="Telefone" className="form-control" />
                                                            </div>
                                                            <div className="mb-3">
                                                                {/* File input needs to be uncontrolled in React usually, but relying on standard form submission handles it */}
                                                                <input type="file" name="imagem" accept="image/*" className="form-control" />
                                                            </div>

                                                            <button className="btn btn-success" type="submit">
                                                                Salvar Mudanças
                                                            </button>
                                                        </form>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
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

export default ProfileEditPage;
