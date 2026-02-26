import React, { useState } from 'react';

const SignUpPage = ({ csrfToken, formErrors }) => {
    // Note: The original template uses Django forms {{form.username}}, {{form.email}}, etc.
    // For this migration, we are re-creating the fields manually so they match the expected Django POST keys
    // which are standard: 'username', 'email', 'password1', 'password2'.

    // We parse the server-side formErrors if they exist, but normally they'll just render as static HTML
    // if we pass them down. For simplicity, we just display the raw text if provided.

    return (
        <main className="main pages">
            <div className="page-header breadcrumb-wrap">
                <div className="container">
                    <div className="breadcrumb">
                        <a href="/" rel="nofollow"><i className="fi-rs-home mr-5"></i>Início</a>
                        <span></span> Páginas <span></span> Minha Conta
                    </div>
                </div>
            </div>
            <div className="page-content pt-150 pb-150">
                <div className="container">
                    <div className="row">
                        <div className="col-xl-8 col-lg-10 col-md-12 m-auto">
                            <div className="row">
                                <div className="col-lg-6 col-md-8">
                                    <div className="login_wrap widget-taber-content background-white">
                                        <div className="padding_eight_all bg-white">

                                            {formErrors && (
                                                <div className="alert alert-danger" dangerouslySetInnerHTML={{ __html: formErrors }}></div>
                                            )}

                                            <div className="heading_s1">
                                                <h1 className="mb-5">Criar uma Conta</h1>
                                                <p className="mb-30">
                                                    Já tem uma conta? <a href="/user/sign-in/">Entrar</a>
                                                </p>
                                            </div>

                                            <form method="POST" action="/user/sign-up/">
                                                <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

                                                <div className="form-group">
                                                    <input type="text" name="username" placeholder="Nome de usuário *" required />
                                                </div>
                                                <div className="form-group">
                                                    <input type="email" name="email" placeholder="Email *" required />
                                                </div>
                                                <div className="form-group">
                                                    <input type="password" name="password1" placeholder="Senha *" required />
                                                </div>
                                                <div className="form-group">
                                                    <input type="password" name="password2" placeholder="Confirmar senha *" required />
                                                </div>

                                                <div className="payment_option mb-50"></div>

                                                <div className="login_footer form-group mb-50">
                                                    <div className="chek-form">
                                                        <div className="custome-checkbox">
                                                            <input
                                                                className="form-check-input"
                                                                type="checkbox"
                                                                name="checkbox"
                                                                id="exampleCheckbox12"
                                                                value=""
                                                                required
                                                            />
                                                            <label className="form-check-label" htmlFor="exampleCheckbox12">
                                                                <span>Concordo com os termos e políticas.</span>
                                                            </label>
                                                        </div>
                                                    </div>
                                                    <a href="/page-privacy-policy.html">
                                                        <i className="fi-rs-book-alt mr-5 text-muted"></i>Saiba mais
                                                    </a>
                                                </div>

                                                <div className="form-group mb-30">
                                                    <button type="submit" className="btn btn-fill-out btn-block hover-up font-weight-bold" name="login">
                                                        Enviar e Registrar
                                                    </button>
                                                    <div>
                                                        <a className="btn btn-fill-out btn-block hover-up font-weight-bold" href="/user/cadastro-vendedor/">
                                                            Cadastrar Como Vendedor
                                                        </a>
                                                    </div>
                                                </div>

                                                <p className="font-xs text-muted">
                                                    <strong>Nota:</strong> Seus dados pessoais serão usados para apoiar sua experiência em todo este site, para gerenciar o acesso à sua conta e para outros fins descritos em nossa política de privacidade.
                                                </p>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-lg-6 pr-30 d-none d-lg-block">
                                    <div className="card-login mt-115">
                                        <a href="#" className="social-login facebook-login">
                                            <img src="/static/assets/imgs/theme/icons/logo-facebook.svg" alt="" />
                                            <span>Continuar com Facebook</span>
                                        </a>
                                        <a href="#" className="social-login google-login">
                                            <img src="/static/assets/imgs/theme/icons/logo-google.svg" alt="" />
                                            <span>Continuar com Google</span>
                                        </a>
                                        <a href="#" className="social-login apple-login">
                                            <img src="/static/assets/imgs/theme/icons/logo-apple.svg" alt="" />
                                            <span>Continuar com Apple</span>
                                        </a>
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

export default SignUpPage;
