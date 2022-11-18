informacao_doc = "-------------------------------------------------------------------------------Conexões--------------------------------------------------------------------------------- \n\n" \
                 "Observação: Todos os campos necessitam de preenchimento dos dados. \n\n" \
                 "Se houver algum problema na conexão, a caixa informativa será trocada de 'Desconectado' para 'Falha', e então ao lado \n" \
                 "esquerdo irá trazer um botão com a identificação do erro. \n\n" \
                 "-----------------------------------------------------------------------Configurações Gerais-------------------------------------------------------------------------- \n\n" \
                 "É possível, para todos os dados, filtrar aqueles que estão marcados como 'apagados'. \n\n" \
                 "[Produtos] \n\n" \
                 "É comparado através do barras, desta forma importando apenas os não encontrados. \n" \
                 "Para os produtos que foram encontrados, o Integrador irá atribuir as informações de Barras Adicional, \n" \
                 "Estoque (com exceção de alguns campos como por exemplo de Último Preço de Entrada) e Lote ao cadastro existente. \n" \
                 "É possível filtrar os produtos que possuem 0 (zero) no ínicio do barras através \n" \
                 "da opção 'Não importar produtos com barras que iniciam com X ou mais zero(s). \n\n" \
                 "Observações: \n" \
                 "Somente irá trazer os produtos com a devida seleção dos grupos em 'Grupos de Produtos'. \n" \
                 "Para o funcionamento correto da aplicação é necessário selecionar ao menos uma das opções para Fabricante e Princípio Ativo. \n\n" \
                 "[Principio Ativo] \n\n" \
                 "Por Descrição - É comparado através de uma descrição idêntica, e então inserido os não encontrados no banco de destino. \n" \
                 "Para os registros encontrados e não encontrados, quando marcado a opção de Produto, \n" \
                 "o Integrador irá atualizar o id para corresponder ao cadastro equivalente da base de Destino. \n" \
                 "Esta opção pode ser utilizada para importar os Princípios Ativos sem a necessidade de marcar os produtos. \n\n" \
                 "Por ID - Para todos os produtos inseridos, o id do principio ativo será atualizado de acordo com o ID de destino informado. \n" \
                 "Esta opção não possui efeito se os produtos não foram importados. \n\n" \
                 "[Fabricantes] \n\n" \
                 "Por CNPJ - É comparado os fabricantes da base de Origem e Destino, então somente será inserido na base de \n" \
                 "Destino os fabricantes que não foram encontrados pelo CNPJ. \n" \
                 "Para os registros encontrados e não encontrados, quando marcado a opção de Produto, \n" \
                 "o Integrador irá atualizar o id para corresponder ao cadastro equivalente da base de Destino. \n" \
                 "Esta opção pode ser utilizada para importar os Fabricantes sem a necessidade de marcar os produtos. \n\n" \
                 "Por ID - Para todos os produtos inseridos, o id de fabricante será atualizado de acordo com o ID de destino informado. \n" \
                 "Esta opção não possui efeito se os produtos não foram importados. \n\n" \
                 "-------------------------------------------------------------------------Grupos de Produtos-------------------------------------------------------------------------- \n\n" \
                 "Para inserir os valores do Novo ID (que seria correspondente ao ID do grupo no Banco de Destino), \n" \
                 "basta clicar duas vezes na célula da linha desejada. \n\n" \
                 "Importante: O que define se o Integrador irá trazer os produtos ou não, será a marcação do checkbox das linhas no \n" \
                 "quadro do Banco de Origem, porém para todos marcados deve se colocar o Novo ID desejado. \n\n" \
                 "------------------------------------------------------------------------Fornecedores e Pagar------------------------------------------------------------------------- \n" \
                 "[Empresas e Clientes] \n\n" \
                 "Importante: O que define se o Integrador irá trazer os fornecedores ou não, será a marcação do checkbox das linhas. \n" \
                 "É comparado os fornecedores entre Origem e Destino através do CNPJ. \n\n" \
                 "---------------------------------------------------------------------------------Pagar--------------------------------------------------------------------------------- \n\n" \
                 "Através da comparação de fornecedores pelo CNPJ, se o mesmo for encontrado na base Destino, então o \n" \
                 "pagar será redirecionado para o cadastro existente. \n\n" \
                 "------------------------------------------------------------------------Empresas e Clientes-------------------------------------------------------------------------- \n\n" \
                 "[Empresas e Clientes] \n\n" \
                 "Importante: O que define se o Integrador irá trazer as empresas ou não, será a marcação do checkbox das linhas. \n" \
                 "Os clientes que serão inseridos dependem que este esteja devidamente amarrado a empresa marcada, \n" \
                 "se houver inconsistência e o cliente não estiver vinculado corretamente, não irá trazer. \n\n" \
                 "---------------------------------------------------------------------------------Receber--------------------------------------------------------------------------------- \n\n" \
                 "Possui a mesma condição informada anteriormente, desta forma somente irá trazer o receber dos clientes que estão \n" \
                 "devidamente vinculados.\n"
