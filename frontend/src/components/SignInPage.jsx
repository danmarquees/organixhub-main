import React, { useState } from 'react';

const SignInPage = ({ csrfToken }) => {
    // For this migration, we're basically wrapping the standard Django form submission in React.
    // We could make this an AJAX call later, but currently maintaining the default form POST is sufficient.
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

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
                <div class="container">
                    <div className="row">
                        <div className="col-xl-8 col-lg-10 col-md-12 m-auto">
                            <div className="row">
                                <div className="col-lg-6 pr-30 d-none d-lg-block">
                                    <img
                                        className="border-radius-15"
                                        src="/static/assets/imgs/page/login-1.png"
                                        alt=""
                                    />
                                </div>
                                <div className="col-lg-6 col-md-8">
                                    <div className="login_wrap widget-taber-content background-white">
                                        <div className="padding_eight_all bg-white">
                                            <div className="heading_s1">
                                                <h1 className="mb-5">Login</h1>
                                                <p className="mb-30">
                                                    Não tem uma conta? <a href="/user/sign-up/">Crie aqui</a>
                                                </p>
                                            </div>
                                            <form method="POST" action="/user/sign-in/">
                                                <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

                                                <div className="form-group">
                                                    <input
                                                        type="text"
                                                        required
                                                        name="email"
                                                        placeholder="Usuário ou Email *"
                                                        value={email}
                                                        onChange={(e) => setEmail(e.target.value)}
                                                    />
                                                </div>
                                                <div className="form-group">
                                                    <input
                                                        required
                                                        type="password"
                                                        name="password"
                                                        placeholder="Sua senha *"
                                                        value={password}
                                                        onChange={(e) => setPassword(e.target.value)}
                                                    />
                                                </div>

                                                <div className="login_footer form-group mb-50">
                                                    <div className="chek-form">
                                                        <div className="custome-checkbox">
                                                            <input
                                                                className="form-check-input"
                                                                type="checkbox"
                                                                name="checkbox"
                                                                id="exampleCheckbox1"
                                                                value=""
                                                            />
                                                            <label className="form-check-label" htmlFor="exampleCheckbox1">
                                                                <span>Lembrar-me</span>
                                                            </label>
                                                        </div>
                                                    </div>
                                                    <a className="text-muted" href="#">Esqueceu a senha?</a>
                                                </div>
                                                <div className="form-group">
                                                    <button type="submit" className="btn btn-heading btn-block hover-up" name="login">Entrar</button>
                                                </div>
                                            </form>
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

export default SignInPage;
