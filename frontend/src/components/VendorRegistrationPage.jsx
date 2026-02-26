import React from 'react';

const VendorRegistrationPage = ({ csrfToken, formErrors }) => {
    return (
        <main className="main">
            <div className="container mb-30 mt-50">
                <section className="content-main">
                    <form method="POST" encType="multipart/form-data">
                        <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />

                        <div className="row justify-content-center">
                            <div className="col-lg-9">
                                <div className="card mb-4">
                                    <div className="card-header">
                                        <h4>Informações Pessoais e Empresariais</h4>
                                    </div>
                                    <div className="card-body">
                                        {formErrors && Object.keys(formErrors).length > 0 && (
                                            <div className="alert alert-danger">
                                                <strong>Existem erros no formulário. Verifique os campos abaixo.</strong>
                                                <ul className="mb-0 mt-2">
                                                    {Object.entries(formErrors).map(([field, errors]) => (
                                                        <li key={field}>{field}: {errors.join(', ')}</li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}

                                        <div className="mb-4">
                                            <label htmlFor="id_nome_completo" className="form-label">Nome completo</label>
                                            <input type="text" name="nome_completo" className="form-control" id="id_nome_completo" required />
                                        </div>
                                        <div className="row">
                                            <div className="col-lg-4">
                                                <div className="mb-4">
                                                    <label className="form-label">RG</label>
                                                    <input type="text" name="rg" className="form-control" />
                                                </div>
                                            </div>
                                            <div className="col-lg-4">
                                                <div className="mb-4">
                                                    <label className="form-label">CPF/CNPJ</label>
                                                    <input type="text" name="cpf_cnpj" className="form-control" required />
                                                </div>
                                            </div>
                                            <div className="col-lg-4">
                                                <div className="mb-4">
                                                    <label className="form-label">Data de Nascimento</label>
                                                    <input type="date" name="data_nascimento" className="form-control" />
                                                </div>
                                            </div>
                                        </div>
                                        <div className="row">
                                            <div className="col-lg-4">
                                                <div className="mb-4">
                                                    <label className="form-label">Email</label>
                                                    <input type="email" name="email" className="form-control" required />
                                                </div>
                                            </div>
                                            <div className="col-lg-4">
                                                <div className="mb-4">
                                                    <label className="form-label">Telefone Celular</label>
                                                    <input type="text" name="telefone_celular" className="form-control" />
                                                </div>
                                            </div>
                                            <div className="col-lg-4">
                                                <div className="mb-4">
                                                    <label className="form-label">Telefone Comercial</label>
                                                    <input type="text" name="telefone_comercial" className="form-control" />
                                                </div>
                                            </div>
                                        </div>
                                        <div className="mb-4">
                                            <label className="form-label">Endereço Completo</label>
                                            <input type="text" name="endereco" className="form-control" required />
                                        </div>
                                    </div>
                                </div>

                                <div className="card mb-4">
                                    <div className="card-header">
                                        <h4>Informações da Loja</h4>
                                    </div>
                                    <div className="card-body">
                                        <div className="mb-4">
                                            <label htmlFor="id_nome_loja" className="form-label">Nome da Loja</label>
                                            <input type="text" name="nome_loja" className="form-control" id="id_nome_loja" required />
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="id_categoria_produtos" className="form-label">Categoria de Produtos</label>
                                            <input type="text" name="categoria_produtos" className="form-control" id="id_categoria_produtos" />
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="id_descricao_loja" className="form-label">Descrição da Loja</label>
                                            <textarea name="descricao_loja" className="form-control" id="id_descricao_loja" rows="4"></textarea>
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="id_logotipo" className="form-label">Logotipo ou Foto Representativa</label>
                                            <input type="file" name="logotipo" className="form-control" id="id_logotipo" />
                                        </div>
                                    </div>
                                </div>

                                <div className="card mb-4">
                                    <div className="card-header">
                                        <h4>Informações Bancárias</h4>
                                    </div>
                                    <div className="card-body">
                                        <div className="mb-4">
                                            <label htmlFor="id_nome_banco" className="form-label">Nome do Banco</label>
                                            <input type="text" name="nome_banco" className="form-control" id="id_nome_banco" />
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="id_numero_conta" className="form-label">Número da Conta</label>
                                            <input type="text" name="numero_conta" className="form-control" id="id_numero_conta" />
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="id_agencia" className="form-label">Agência</label>
                                            <input type="text" name="agencia" className="form-control" id="id_agencia" />
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="id_tipo_conta" className="form-label">Tipo de Conta</label>
                                            <input type="text" name="tipo_conta" className="form-control" id="id_tipo_conta" />
                                        </div>
                                        <div className="mb-4">
                                            <label htmlFor="id_titular_conta" className="form-label">Nome do Titular da Conta</label>
                                            <input type="text" name="titular_conta" className="form-control" id="id_titular_conta" />
                                        </div>
                                    </div>
                                </div>
                                <div className="mb-4 custome-checkbox">
                                    <input className="form-check-input" type="checkbox" name="aceite_termos" id="id_aceite_termos" required />
                                    <label className="form-check-label" htmlFor="id_aceite_termos"><span>Aceito os Termos e Condições</span></label>
                                </div>
                                <button type="submit" className="btn btn-md rounded font-sm hover-up">
                                    Salvar Alterações
                                </button>
                            </div>
                            <div className="col-lg-3">
                                <div className="card mb-4">
                                    <div className="card-header">
                                        <h4>Mídia (Doc. Identificação)</h4>
                                    </div>
                                    <div className="card-body">
                                        <div className="input-upload">
                                            <input type="file" name="imagem" className="form-control" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </section>
            </div>
        </main>
    );
};

export default VendorRegistrationPage;
