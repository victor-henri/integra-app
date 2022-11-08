query_select_grupo = 'SELECT id_grupo, descricao FROM grupo;'

query_select_produto = 'SELECT * FROM produto;'

query_insert_produto = 'INSERT INTO produto ' \
                       '(campo_auxiliar, barras, descricao, id_grupo, id_fabricante, id_principio_ativo, ' \
                       'inativo, apagado, medicamento, tipo_controle, unidade, preco_compra_cx, ' \
                       'und_por_cx, preco_compra_und, margem, preco_venda, desconto_avista, ' \
                       'desconto_promocao, margem_promocao, preco_promocao, inicio_promocao, ' \
                       'final_promocao, tipo_medicamento, registro_ms, data_cadastro, data_alteracao, ' \
                       'usuario_cadastro, usuario_alteracao) ' \
                       'VALUES (%(id_produto)s, %(barras)s, %(descricao)s, %(id_grupo)s, %(id_fabricante)s, ' \
                       '%(id_principio_ativo)s, %(inativo)s, %(apagado)s, %(medicamento)s, %(tipo_controle)s, ' \
                       '%(unidade)s, %(preco_compra_cx)s, %(und_por_cx)s, %(preco_compra_und)s, %(margem)s, ' \
                       '%(preco_venda)s, %(desconto_avista)s, %(desconto_promocao)s, %(margem_promocao)s, ' \
                       '%(preco_promocao)s, %(inicio_promocao)s, %(final_promocao)s, %(tipo_medicamento)s, ' \
                       '%(registro_ms)s, %(data_cadastro)s, %(data_alteracao)s, %(usuario_cadastro)s, ' \
                       '%(usuario_alteracao)s);'

query_select_barras = 'SELECT * FROM barras_adicional;'

query_insert_barras = 'INSERT INTO barras_adicional ' \
                      '(id_produto, campo_auxiliar, barras, apagado, data_cadastro, data_alteracao, ' \
                      'usuario_cadastro, usuario_alteracao) ' \
                      'VALUES (%(id_produto)s, %(id_produto_ant)s, %(barras)s, %(apagado)s, %(data_cadastro)s, ' \
                      '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

query_select_estoque = 'SELECT * FROM estoque;'

query_insert_estoque = 'INSERT INTO estoque ' \
                       '(id_produto, campo_auxiliar, id_filial, estoque, preco_ultima_entrada, apagado, ' \
                       'data_cadastro, data_alteracao, usuario_cadastro, usuario_alteracao) ' \
                       'VALUES (%(id_produto)s, %(id_produto_ant)s, %(id_filial)s, %(estoque)s, ' \
                       '%(preco_ultima_entrada)s, %(apagado)s, %(data_cadastro)s, ' \
                       '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

query_select_lote = 'SELECT * FROM lote;'

query_insert_lote = 'INSERT INTO lote ' \
                    '(id_produto, campo_auxiliar, id_filial, lote_descricao, lote_estoque, ' \
                    'data_fabricacao, data_validade, apagado, data_alteracao) ' \
                    'VALUES (%(id_produto)s, %(id_produto_ant)s, %(id_filial)s, %(lote_descricao)s, ' \
                    '%(lote_estoque)s, %(data_fabricacao)s, %(data_validade)s, %(apagado)s, %(data_alteracao)s);'

query_select_preco = 'SELECT * FROM preco_filial;'

query_insert_preco = 'INSERT INTO preco_filial ' \
                     '(id_produto, campo_auxiliar, id_filial, preco_compra_cx, und_por_cx, preco_compra_und, ' \
                     'margem, preco_venda, desconto_avista, margem_promocao, desconto_promocao, preco_promocao, ' \
                     'inicio_promocao, final_promocao, apagado, data_cadastro, data_alteracao, ' \
                     'usuario_cadastro, usuario_alteracao) ' \
                     'VALUES (%(id_produto)s, %(id_produto_ant)s, %(id_filial)s, %(preco_compra_cx)s, %(und_por_cx)s, ' \
                     '%(preco_compra_und)s, %(margem)s, %(preco_venda)s, %(desconto_avista)s, %(margem_promocao)s, ' \
                     '%(desconto_promocao)s, %(preco_promocao)s, %(inicio_promocao)s, ' \
                     '%(final_promocao)s, %(apagado)s, %(data_cadastro)s, %(data_alteracao)s, ' \
                     '%(usuario_cadastro)s, %(usuario_alteracao)s);'

query_select_fabricante = 'SELECT * FROM fabricante;'

query_insert_fabricante = 'INSERT INTO fabricante ' \
                          '(campo_auxiliar, cnpj, descricao, apagado, data_cadastro, data_alteracao, ' \
                          'usuario_cadastro, usuario_alteracao) ' \
                          'VALUES (%(id_fabricante)s, %(cnpj)s, %(descricao)s, %(apagado)s, ' \
                          '%(data_cadastro)s, %(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

query_select_principio = 'SELECT * FROM principio_ativo;'

query_insert_principio = 'INSERT INTO principio_ativo ' \
                         '(campo_auxiliar, descricao, apagado, data_cadastro, data_alteracao, ' \
                         'usuario_cadastro, usuario_alteracao) ' \
                         'VALUES (%(id_principio_ativo)s, %(descricao)s, %(apagado)s, %(data_cadastro)s, ' \
                         '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

query_select_fornecedor_origem = 'SELECT * FROM fornecedor WHERE id_fornecedor IN %s;'

query_select_fornecedor_destino = 'SELECT id_fornecedor, cnpj FROM fornecedor;'

query_insert_fornecedor = 'INSERT INTO fornecedor ' \
                          '(campo_auxiliar, razao_social, cnpj, inscricao_estadual, ' \
                          'endereco, numero, bairro, cidade, estado, cep, telefone, email, apagado, data_cadastro, ' \
                          'data_alteracao, usuario_cadastro, usuario_alteracao) ' \
                          'VALUES (%(id_fornecedor)s, %(razao_social)s, %(cnpj)s, ' \
                          '%(inscricao_estadual)s, %(endereco)s, %(numero)s, %(bairro)s, %(cidade)s, %(estado)s, ' \
                          '%(cep)s, %(telefone)s, %(email)s, %(apagado)s, %(data_cadastro)s, ' \
                          '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

query_consulta_pos_insert_fornecedor = 'SELECT id_fornecedor, campo_auxiliar ' \
                                       'FROM fornecedor ' \
                                       'WHERE campo_auxiliar IS NOT NULL;'

query_consulta_pos_insert_produto = 'SELECT id_produto, campo_auxiliar ' \
                                    'FROM produto ' \
                                    'WHERE campo_auxiliar IS NOT NULL;'

query_consulta_pos_insert_fabricante = 'SELECT id_fabricante, campo_auxiliar ' \
                                       'FROM fabricante ' \
                                       'WHERE campo_auxiliar IS NOT NULL;'

query_consulta_pos_insert_principio = 'SELECT id_principio_ativo, campo_auxiliar ' \
                                      'FROM principio_ativo ' \
                                      'WHERE campo_auxiliar IS NOT NULL;'

query_select_pagar = 'SELECT * FROM contas_pagar WHERE id_fornecedor IN %s;'

query_insert_pagar = 'INSERT INTO contas_pagar ' \
                     '(campo_auxiliar, id_filial, id_fornecedor, data_emissao, data_vencimento, ' \
                     'nota_fiscal, valor, pago, data_pagamento, apagado, data_cadastro, data_alteracao, ' \
                     'usuario_cadastro, usuario_alteracao) ' \
                     'VALUES (%(id_pagar)s, %(id_filial)s, %(id_fornecedor)s, %(data_emissao)s, ' \
                     '%(data_vencimento)s, %(nota_fiscal)s, %(valor)s, %(pago)s, %(data_pagamento)s, ' \
                     '%(apagado)s, %(data_cadastro)s, %(data_alteracao)s, ' \
                     '%(usuario_cadastro)s, %(usuario_alteracao)s);'

query_select_empresa = 'SELECT * FROM empresa WHERE id_empresa IN %s;'

query_insert_empresa = 'INSERT INTO empresa ' \
                       '(campo_auxiliar, nome_fantasia, razao_social, cnpj, inscricao_estadual, ' \
                       'endereco, numero, bairro, cidade, estado, cep, telefone, contato, ' \
                       'apagado, fechamento, recebimento, data_cadastro, data_alteracao, ' \
                       'usuario_cadastro, usuario_alteracao, comunicador) ' \
                       'VALUES (%(id_empresa)s, %(nome_fantasia)s, %(razao_social)s, %(cnpj)s, ' \
                       '%(inscricao_estadual)s, %(endereco)s, %(numero)s, %(bairro)s, %(cidade)s, ' \
                       '%(estado)s, %(cep)s, %(telefone)s, %(contato)s, %(apagado)s, ' \
                       '%(fechamento)s, %(recebimento)s, %(data_cadastro)s, %(data_alteracao)s, ' \
                       '%(usuario_cadastro)s, %(usuario_alteracao)s, %(comunicador)s);'

query_select_cliente = 'SELECT * FROM cliente WHERE id_empresa IN %s;'

query_insert_cliente = 'INSERT INTO cliente ' \
                       '(campo_auxiliar, id_empresa, nome, status_cliente, data_nascimento, ' \
                       'endereco, numero, bairro, cidade, estado, cep, telefone, celular, cpf, rg, ' \
                       'apagado, saldo_mes, saldo_total, limite_mes, limite_total, data_cadastro, ' \
                       'data_alteracao, usuario_cadastro, usuario_alteracao, comunicador) ' \
                       'VALUES (%(id_cliente)s, %(id_empresa)s, %(nome)s, %(status_cliente)s, ' \
                       '%(data_nascimento)s, %(endereco)s, %(numero)s, %(bairro)s, %(cidade)s, %(estado)s, ' \
                       '%(cep)s, %(telefone)s, %(celular)s, %(cpf)s, %(rg)s, %(apagado)s, %(saldo_mes)s, ' \
                       '%(saldo_total)s, %(limite_mes)s, %(limite_total)s, %(data_cadastro)s, ' \
                       '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s, %(comunicador)s);'

query_select_receber = 'SELECT * FROM contas_receber WHERE id_cliente IN %s;'

query_insert_receber = 'INSERT INTO contas_receber ' \
                       '(campo_auxiliar, id_filial, id_empresa, data_venda, ' \
                       'descricao_produto, quantidade, valor, valor_total, numero_nota, vencimento, data_baixa, ' \
                       'apagado, data_cadastro, data_alteracao, usuario_cadastro, usuario_alteracao, comunicador) ' \
                       'VALUES (%(id_cliente)s, %(id_filial)s, %(id_empresa)s, %(data_venda)s, ' \
                       '%(descricao_produto)s, %(quantidade)s, %(valor)s, %(valor_total)s, %(numero_nota)s, ' \
                       '%(vencimento)s, %(data_baixa)s, %(apagado)s, %(data_cadastro)s, %(data_alteracao)s, ' \
                       '%(usuario_cadastro)s, %(usuario_alteracao)s, %(comunicador)s);'
