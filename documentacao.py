informacao_doc = "-----------------------------------------------------------------------------------Conexões------------------------------------------------------------------------------------ \n\n" \
                 "Observação: Todos os campos DEVEM sem preenchidos. \n\n" \
                 "Se houver algum problema na conexão, a caixa informativa será trocada de 'Desconectado' para 'Falha', e então ao lado \n" \
                 "esquerdo irá trazer um botão com a identificação do erro. \n\n" \
                 "-----------------------------------------------------------------------Configurações de Produtos----------------------------------------------------------------------- \n\n" \
                 "[Produtos] \n\n" \
                 "É dependente e somente irá trazer os produtos com a devida seleção dos grupos em 'Grupos de Produtos'. \n\n" \
                 "As opções: [Barras Adicionais] [Estoque/PMC] [Estoque Mín.2] [Lotes] [Preço Filial] e [Desconto Quantidade], \n" \
                 "são dependentes da opção [Produtos], e somente irão inserir dados se a condição anterior for satisfeita. \n\n" \
                 "Observação: Caso nenhuma opção seja selecionada anteriormente para Fabricantes e/ou Princípio Ativo, \n" \
                 "o Integrador irá atribuir para os produtos inseridos um Fabricante e/ou Principio Ativo como padrão. \n\n" \
                 "[Principio Ativo] \n\n" \
                 "Por Descrição - É comparado através de uma descrição idêntica, e então inserido os não encontrados no banco de destino. \n" \
                 "Se os [Produtos] foram marcados para importar, o Integrador irá atualizar os mesmos com o novo id dos principios \n" \
                 "não encontrados. \n" \
                 "Por ID - Para todos os produtos inseridos, o principio_ativo_id será atualizado de acordo com o ID de destino informado. \n" \
                 "Não possui efeito se os [Produtos] não forem marcados. \n\n" \
                 "[Fabricantes] \n\n" \
                 "Por CNPJ - É comparado os fabricantes da base de Origem e Destino, então somente será inserido na base de \n" \
                 "Destino os fabricantes que não foram encontrados pelo CNPJ. \n" \
                 "Para os produtos, os que possuem um fabricantes_id vinculado a um fabricante existente na base de Destino, \n" \
                 "o Integrador irá atualizar o fabricantes_id para corresponder ao cadastro equivalente da base de Destino. \n" \
                 "Por ID - Para todos os produtos inseridos, o fabricantes_id será atualizado de acordo com o ID de destino informado. \n\n" \
                 "-----------------------------------------------------------------------------Grupos de Produtos----------------------------------------------------------------------------- \n\n" \
                 "Para inserir os valores do Novo ID (que seria correspondente ao ID do grupo no Banco de Destino), \n" \
                 "basta clicar duas vezes na célula da linha desejada. \n\n" \
                 "Importante: O que define se o Integrador irá puxar os produtos ou não, será a marcação dos checkboxes das linhas no \n" \
                 "quadro do Banco de Origem, porém para todos marcados deve se colocar o Novo ID desejado. \n\n" \
                 "----------------------------------------------------------------------------Empresas e Clientes---------------------------------------------------------------------------- \n\n" \
                 "[Empresas(Clientes e Dependentes)] \n\n" \
                 "Importante: O que define se o Integrador irá puxar as empresas ou não, será a marcação dos checkboxes das linhas. \n" \
                 "Os clientes e dependentes que serão inseridos dependem que o cliente esteja devidamente amarrado a empresa marcada, \n" \
                 "se houver inconsistência e o cliente não estiver vinculado corretamente, não irá trazer. \n\n" \
                 "-------------------------------------------------------------------------------------Receber------------------------------------------------------------------------------------ \n\n" \
                 "Possui a mesma condição informada anteriormente, desta forma somente irá trazer o receber dos clientes que estão \n" \
                 "devidamente vinculados.\n"
