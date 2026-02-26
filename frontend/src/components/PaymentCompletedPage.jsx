import React from 'react';

const PaymentCompletedPage = ({ pedidoCarrinho }) => {
    return (
        <main className="main page-404">
            <div className="page-content pt-150 pb-150">
                <div className="container">
                    <div className="row">
                        <div className="col-xl-8 col-lg-10 col-md-12 m-auto text-center">
                            <p className="mb-20">
                                <img
                                    src="/static/assets/imgs/page/success.png"
                                    alt="Payment Success"
                                    className="hover-up"
                                />
                            </p>
                            <h1 className="display-2 mb-30">
                                Pagamento efetuado com sucesso!
                            </h1>

                            {pedidoCarrinho && pedidoCarrinho.map((p, index) => (
                                <h3 key={index} className="font-lg text-grey-700 mb-30">
                                    Seu pagamento foi aprovado com sucesso. O número do seu
                                    pedido é #{p.orderid}.
                                </h3>
                            ))}

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

export default PaymentCompletedPage;
