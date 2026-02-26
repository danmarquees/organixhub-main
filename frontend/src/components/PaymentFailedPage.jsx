import React from 'react';

const PaymentFailedPage = () => {
    return (
        <main className="main page-404">
            <div className="page-content pt-150 pb-150">
                <div className="container">
                    <div className="row">
                        <div className="col-xl-8 col-lg-10 col-md-12 m-auto text-center">
                            <p className="mb-20">
                                <img
                                    src="/static/assets/imgs/page/pay-fail.png"
                                    alt="Payment Failed"
                                    className="hover-up"
                                />
                            </p>
                            <h1 className="display-2 mb-30">Pagamento não aprovado</h1>
                            <p className="font-lg text-grey-700 mb-30">
                                Lamentamos, mas seu pagamento não foi aprovado. Por
                                favor, verifique seus dados bancários e tente novamente.
                                Se o problema persistir, entre em contato com nossa
                                equipe de suporte.
                            </p>
                            <div className="search-form">
                                <form action="#">
                                    <input type="text" placeholder="Buscar…" />
                                    <button type="submit">
                                        <i className="fi-rs-search"></i>
                                    </button>
                                </form>
                            </div>
                            <a
                                className="btn btn-default submit-auto-width font-xs hover-up mt-30"
                                href="/"
                            >
                                <i className="fi-rs-home mr-5"></i> Voltar para a Home Page
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default PaymentFailedPage;
