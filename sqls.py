SELECT_GROUP = 'SELECT id_grupo, descricao FROM grupo;'

SELECT_PRODUCT = 'SELECT * FROM produto;'

INSERT_PRODUCT = 'INSERT INTO produto ' \
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

SELECT_BAR = 'SELECT * FROM barras_adicional;'

INSERT_BAR = 'INSERT INTO barras_adicional ' \
             '(id_produto, campo_auxiliar, barras, apagado, data_cadastro, data_alteracao, ' \
             'usuario_cadastro, usuario_alteracao) ' \
             'VALUES (%(id_produto)s, %(id_produto_ant)s, %(barras)s, %(apagado)s, %(data_cadastro)s, ' \
             '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

SELECT_STOCK = 'SELECT * FROM estoque;'

INSERT_STOCK = 'INSERT INTO estoque ' \
               '(id_produto, campo_auxiliar, id_filial, estoque, preco_ultima_entrada, apagado, ' \
               'data_cadastro, data_alteracao, usuario_cadastro, usuario_alteracao) ' \
               'VALUES (%(id_produto)s, %(id_produto_ant)s, %(id_filial)s, %(estoque)s, ' \
               '%(preco_ultima_entrada)s, %(apagado)s, %(data_cadastro)s, ' \
               '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

SELECT_PARTITION = 'SELECT * FROM lote;'

INSERT_PARTITION = 'INSERT INTO lote ' \
                   '(id_produto, campo_auxiliar, id_filial, lote_descricao, lote_estoque, ' \
                   'data_fabricacao, data_validade, apagado, data_alteracao) ' \
                   'VALUES (%(id_produto)s, %(id_produto_ant)s, %(id_filial)s, %(lote_descricao)s, ' \
                   '%(lote_estoque)s, %(data_fabricacao)s, %(data_validade)s, %(apagado)s, %(data_alteracao)s);'

SELECT_PRICE = 'SELECT * FROM preco_filial;'

INSERT_PRICE = 'INSERT INTO preco_filial ' \
               '(id_produto, campo_auxiliar, id_filial, preco_compra_cx, und_por_cx, preco_compra_und, ' \
               'margem, preco_venda, desconto_avista, margem_promocao, desconto_promocao, preco_promocao, ' \
               'inicio_promocao, final_promocao, apagado, data_cadastro, data_alteracao, ' \
               'usuario_cadastro, usuario_alteracao) ' \
               'VALUES (%(id_produto)s, %(id_produto_ant)s, %(id_filial)s, %(preco_compra_cx)s, %(und_por_cx)s, ' \
               '%(preco_compra_und)s, %(margem)s, %(preco_venda)s, %(desconto_avista)s, %(margem_promocao)s, ' \
               '%(desconto_promocao)s, %(preco_promocao)s, %(inicio_promocao)s, ' \
               '%(final_promocao)s, %(apagado)s, %(data_cadastro)s, %(data_alteracao)s, ' \
               '%(usuario_cadastro)s, %(usuario_alteracao)s);'

SELECT_MANUFACTURER = 'SELECT * FROM fabricante;'

INSERT_MANUFACTURER = 'INSERT INTO fabricante ' \
                      '(campo_auxiliar, cnpj, descricao, apagado, data_cadastro, data_alteracao, ' \
                      'usuario_cadastro, usuario_alteracao) ' \
                      'VALUES (%(id_fabricante)s, %(cnpj)s, %(descricao)s, %(apagado)s, ' \
                      '%(data_cadastro)s, %(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

SELECT_PRINCIPLE = 'SELECT * FROM principio_ativo;'

INSERT_PRINCIPLE = 'INSERT INTO principio_ativo ' \
                   '(campo_auxiliar, descricao, apagado, data_cadastro, data_alteracao, ' \
                   'usuario_cadastro, usuario_alteracao) ' \
                   'VALUES (%(id_principio_ativo)s, %(descricao)s, %(apagado)s, %(data_cadastro)s, ' \
                   '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

SELECT_SUPPLIER_ORIGIN = 'SELECT * FROM fornecedor WHERE id_fornecedor IN %s;'

SELECT_SUPPLIER_DESTINY = 'SELECT id_fornecedor, cnpj FROM fornecedor;'

INSERT_SUPPLIER = 'INSERT INTO fornecedor ' \
                  '(campo_auxiliar, razao_social, cnpj, inscricao_estadual, ' \
                  'endereco, numero, bairro, cidade, estado, cep, telefone, email, apagado, data_cadastro, ' \
                  'data_alteracao, usuario_cadastro, usuario_alteracao) ' \
                  'VALUES (%(id_fornecedor)s, %(razao_social)s, %(cnpj)s, ' \
                  '%(inscricao_estadual)s, %(endereco)s, %(numero)s, %(bairro)s, %(cidade)s, %(estado)s, ' \
                  '%(cep)s, %(telefone)s, %(email)s, %(apagado)s, %(data_cadastro)s, ' \
                  '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

SELECT_BILL = 'SELECT * FROM contas_pagar WHERE id_fornecedor IN %s;'

INSERT_BILL = 'INSERT INTO contas_pagar ' \
              '(campo_auxiliar, id_filial, id_fornecedor, data_emissao, data_vencimento, data_previsao_pgto,' \
              'nota_fiscal, duplicata, parcela, valor, valor_doc, pago, valor_pago, data_pagamento, apagado, ' \
              'data_cadastro, data_alteracao, usuario_cadastro, usuario_alteracao) ' \
              'VALUES (%(id_pagar)s, %(id_filial)s, %(id_fornecedor)s, %(data_emissao)s, ' \
              '%(data_vencimento)s, %(data_previsao_pgto)s, %(nota_fiscal)s, %(duplicata)s, %(parcela)s, ' \
              '%(valor)s, %(valor_doc)s, %(pago)s, %(valor_pago)s, %(data_pagamento)s, ' \
              '%(apagado)s, %(data_cadastro)s, %(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s);'

SELECT_COMPANY = 'SELECT * FROM empresa WHERE id_empresa IN %s;'

INSERT_COMPANY = 'INSERT INTO empresa ' \
                 '(campo_auxiliar, nome_fantasia, razao_social, cnpj, inscricao_estadual, ' \
                 'endereco, numero, bairro, cidade, estado, cep, telefone, contato, ' \
                 'apagado, fechamento, recebimento, data_cadastro, data_alteracao, ' \
                 'usuario_cadastro, usuario_alteracao, comunicador) ' \
                 'VALUES (%(id_empresa)s, %(nome_fantasia)s, %(razao_social)s, %(cnpj)s, ' \
                 '%(inscricao_estadual)s, %(endereco)s, %(numero)s, %(bairro)s, %(cidade)s, ' \
                 '%(estado)s, %(cep)s, %(telefone)s, %(contato)s, %(apagado)s, ' \
                 '%(fechamento)s, %(recebimento)s, %(data_cadastro)s, %(data_alteracao)s, ' \
                 '%(usuario_cadastro)s, %(usuario_alteracao)s, %(comunicador)s);'

SELECT_CUSTOMER = 'SELECT * FROM cliente WHERE id_empresa IN %s;'

INSERT_CUSTOMER = 'INSERT INTO cliente ' \
                  '(campo_auxiliar, campo_auxiliar2, id_empresa, nome, status_cliente, data_nascimento, ' \
                  'endereco, numero, bairro, cidade, estado, cep, telefone, celular, cpf, rg, ' \
                  'apagado, saldo_mes, saldo_total, limite_mes, limite_total, data_cadastro, ' \
                  'data_alteracao, usuario_cadastro, usuario_alteracao, comunicador) ' \
                  'VALUES (%(id_cliente)s, %(id_empresa)s, %(id_empresa)s, %(nome)s, %(status_cliente)s, ' \
                  '%(data_nascimento)s, %(endereco)s, %(numero)s, %(bairro)s, %(cidade)s, %(estado)s, ' \
                  '%(cep)s, %(telefone)s, %(celular)s, %(cpf)s, %(rg)s, %(apagado)s, %(saldo_mes)s, ' \
                  '%(saldo_total)s, %(limite_mes)s, %(limite_total)s, %(data_cadastro)s, ' \
                  '%(data_alteracao)s, %(usuario_cadastro)s, %(usuario_alteracao)s, %(comunicador)s);'

SELECT_ACCOUNT = 'SELECT * FROM contas_receber WHERE id_cliente IN %s;'

INSERT_ACCOUNT = 'INSERT INTO contas_receber ' \
                 '(campo_auxiliar, id_filial, id_empresa, data_venda, ' \
                 'descricao_produto, quantidade, valor, valor_total, numero_nota, vencimento, data_baixa, ' \
                 'apagado, data_cadastro, data_alteracao, usuario_cadastro, usuario_alteracao, comunicador) ' \
                 'VALUES (%(id_cliente)s, %(id_filial)s, %(id_empresa)s, %(data_venda)s, ' \
                 '%(descricao_produto)s, %(quantidade)s, %(valor)s, %(valor_total)s, %(numero_nota)s, ' \
                 '%(vencimento)s, %(data_baixa)s, %(apagado)s, %(data_cadastro)s, %(data_alteracao)s, ' \
                 '%(usuario_cadastro)s, %(usuario_alteracao)s, %(comunicador)s);'

# query_consulta_pos_insert_fornecedor
SELECT_SUPPLIER_AFTER_INSERT = 'SELECT id_fornecedor, campo_auxiliar ' \
                               'FROM fornecedor ' \
                               'WHERE campo_auxiliar IS NOT NULL;'

# query_consulta_pos_insert_produto
SELECT_PRODUCT_AFTER_INSERT = 'SELECT id_produto, campo_auxiliar ' \
                              'FROM produto ' \
                              'WHERE campo_auxiliar IS NOT NULL;'

# query_consulta_pos_insert_fabricante
SELECT_MANUFACTURER_AFTER_INSERT = 'SELECT id_fabricante, campo_auxiliar ' \
                                   'FROM fabricante ' \
                                   'WHERE campo_auxiliar IS NOT NULL;'

# query_consulta_pos_insert_principio
SELECT_PRINCIPLE_AFTER_INSERT = 'SELECT id_principio_ativo, campo_auxiliar ' \
                                'FROM principio_ativo ' \
                                'WHERE campo_auxiliar IS NOT NULL;'

# query_consulta_comparacao_produto
SELECT_PRODUCT_COMPARISON = 'SELECT id_produto, barras FROM produto;'

# query_select_atualizacao_estoque
SELECT_UPDATE_STOCK = 'SELECT id_produto, estoque FROM estoque WHERE id_produto = %(id_produto)s;'

# query_update_estoque
UPDATE_STOCK = 'UPDATE estoque SET estoque = %(estoque)s WHERE id_produto = %(id_produto)s;'

# query_update_cliente
UPDATE_CUSTOMER = 'UPDATE cliente ' \
                  'INNER JOIN empresa ' \
                  'ON cliente.campo_auxiliar2 = empresa.campo_auxiliar ' \
                  'SET cliente.id_empresa = empresa.id_empresa;'

# query_atualiza_receber_cliente
UPDATE_CUSTOMER_ACCOUNT = 'UPDATE contas_receber ' \
                          'INNER JOIN cliente ' \
                          'ON contas_receber.campo_auxiliar = cliente.campo_auxiliar ' \
                          'SET contas_receber.id_cliente = cliente.id_cliente;'

# query_atualiza_receber_empresa
UPDATE_COMPANY_ACCOUNT = 'UPDATE contas_receber ' \
                         'INNER JOIN cliente ' \
                         'ON contas_receber.id_cliente = cliente.id_cliente ' \
                         'SET contas_receber.id_empresa = cliente.id_empresa;'

# query_select_grporigem_sapagado
SELECT_ORIGIN_GROUP_NERASED = 'SELECT id_grupo, descricao FROM grupo WHERE apagado = "N" ORDER BY id_grupo;'

# query_select_grporigem_capagado
SELECT_ORIGIN_GROUP_ERASED = 'SELECT id_grupo, descricao FROM grupo ORDER BY id_grupo;'

# query_select_grpdestino_sapagado
SELECT_GROUP_DESTINY_NERASED = 'SELECT id_grupo, descricao FROM grupo WHERE apagado = "N" ORDER BY id_grupo;'

# query_select_grpdestino_capagado
SELECT_GROUP_DESTINY_ERASED = 'SELECT id_grupo, descricao FROM grupo ORDER BY id_grupo;'

# query_select_listagem_empresa
SELECT_LISTING_COMPANY = 'SELECT id_empresa, nome_fantasia FROM empresa ORDER BY id_empresa;'

# query_select_listagem_fornecedor
SELECT_LISTING_SUPPLIER = 'SELECT id_fornecedor, razao_social FROM fornecedor ORDER BY id_fornecedor;'

# query_update_limpeza_fabricante
UPDATE_CLEANING_MANUFACTURER = 'UPDATE fabricante SET campo_auxiliar = NULL;'

# query_update_limpeza_principio_ativo
UPDATE_CLEANING_PRINCIPLE = 'UPDATE principio_ativo SET campo_auxiliar = NULL;'

# query_update_limpeza_produto
UPDATE_CLEANING_PRODUCT = 'UPDATE produto SET campo_auxiliar = NULL;'

# query_update_limpeza_barras
UPDATE_CLEANING_BARS = 'UPDATE barras_adicional SET campo_auxiliar = NULL;'

# query_update_limpeza_estoque
UPDATE_CLEANING_STOCK = 'UPDATE estoque SET campo_auxiliar = NULL;'

# query_update_limpeza_lote
UPDATE_CLEANING_PARTITION = 'UPDATE lote SET campo_auxiliar = NULL;'

# query_update_limpeza_preco_filial
UPDATE_CLEANING_PRICE = 'UPDATE preco_filial SET campo_auxiliar = NULL;'

# query_update_limpeza_fornecedor
UPDATE_CLEANING_SUPPLIER = 'UPDATE fornecedor SET campo_auxiliar = NULL;'

# query_update_limpeza_pagar
UPDATE_CLEANING_BILL = 'UPDATE contas_pagar SET campo_auxiliar = NULL;'

# query_update_limpeza_empresa
UPDATE_CLEANING_COMPANY = 'UPDATE empresa SET campo_auxiliar = NULL;'

# query_update_limpeza_cliente
UPDATE_CLEANING_CUSTOMER = 'UPDATE cliente SET campo_auxiliar = NULL;'

# query_update_limpeza_cliente2
UPDATE_CLEANING_CUSTOMER2 = 'UPDATE cliente SET campo_auxiliar2 = NULL;'

# query_update_limpeza_receber
UPDATE_CLEANING_ACCOUNT = 'UPDATE contas_receber SET campo_auxiliar = NULL;'
