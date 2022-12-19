
## Integrador de Dados

O Integrador de Dados é um projeto com a finalidade demonstrativa de coletar, comparar, tratar, inserir e atualizar informações entre bases de dados utilizando Python e MariaDB.

## Dependências

Programas: <br />
Python 3.9.2 <br />
MariaDB 10.4 <br />

Bibliotecas: <br />
tkinter <br />
ttkbootstrap <br />
ttkwidgets <br />
pil <br />
logging <br />
datetime <br />
pymysql <br />
pyinstaller <br />

## Como compilar 

Acesse o diretório em que está o projeto. <br />

Execute o comando abaixo, precisará alterar apenas a estrutura final de diretório para Linux ou Windows: <br />
sudo pyinstaller --onefile -w main.py iteradorSQL.py SQLs.py --collect-all PIL --collect-all ttkbootstrap --collect-all ttkwidgets --collect-all pymysql --distpath /home/usuario/diretorio/

## Observações

O arquivo user.py contém a estrutura das informações necessárias para o tema do ttkbootstrap, maiores detalhes de como importar ou utilizar os dados presente na documentação da biblioteca citada.

## Adições & melhorias futuras

Tornar responsível <br />
Refatoramento do código para aperfeiçoamento de desempenho e legibilidade. <br />

## Vídeo completo (Execução, Validação e Comparação)

[![Assista o vídeo completo.](https://img.youtube.com/vi/V3au3J_NxVg/0.jpg)](https://youtu.be/V3au3J_NxVg)

## Documentação do aplicativo


### Conexões

Observação: Todos os campos necessitam de preenchimento dos dados. 

Se houver algum problema na conexão, a caixa informativa será trocada de 'Desconectado' para 'Falha', e então ao lado 
esquerdo irá trazer um botão com a identificação do erro. 

### Configurações Gerais

É possível, para todos os dados, filtrar aqueles que estão marcados como 'apagados'. 

[Produto] 

É comparado através do barras, desta forma importando apenas os não encontrados. 
Para os produtos que foram encontrados, o Integrador irá atribuir as informações de Barras Adicional, 
Estoque (com exceção de alguns campos como por exemplo de Último Preço de Entrada) e Lote ao cadastro existente. 
É possível filtrar os produtos que possuem 0 (zero) no ínicio do barras através 
da opção 'Não importar produtos com barras que iniciam com X ou mais zero(s). 

Observações: <br />
Somente irá trazer os produtos com a devida seleção dos grupos em 'Grupos de Produtos'. <br />
Para o funcionamento correto da aplicação é necessário selecionar ao menos uma das opções para Fabricante e Princípio Ativo. <br />

[Principio Ativo] 

Por Descrição - É comparado através de uma descrição idêntica, e então inserido os não encontrados no banco de destino. 
Para os registros encontrados e não encontrados, quando marcado a opção de Produto, 
o Integrador irá atualizar o id para corresponder ao cadastro equivalente da base de Destino. 
Esta opção pode ser utilizada para importar os Princípios Ativos sem a necessidade de marcar os produtos. 

Por ID - Para todos os produtos inseridos, o id do principio ativo será atualizado de acordo com o ID de destino informado. 
Esta opção não possui efeito se os produtos não foram importados. 

[Fabricante] 

Por CNPJ - É comparado os fabricantes da base de Origem e Destino, então somente será inserido na base de 
Destino os fabricantes que não foram encontrados pelo CNPJ. 
Para os registros encontrados e não encontrados, quando marcado a opção de Produto, 
o Integrador irá atualizar o id para corresponder ao cadastro equivalente da base de Destino. 
Esta opção pode ser utilizada para importar os Fabricantes sem a necessidade de marcar os produtos. 

Por ID - Para todos os produtos inseridos, o id de fabricante será atualizado de acordo com o ID de destino informado. 
Esta opção não possui efeito se os produtos não foram importados. 

### Grupos de Produtos

Para inserir os valores do Novo ID (que seria correspondente ao ID do grupo no Banco de Destino), 
basta clicar duas vezes na célula da linha desejada. 

Importante: <br />
O que define se o Integrador irá trazer os produtos ou não, será a marcação do checkbox das linhas no 
quadro do Banco de Origem, porém para todos marcados deve se colocar o Novo ID desejado. 

### Fornecedores e Pagar

Importante: <br />
O que define se o Integrador irá trazer os fornecedores ou não, será a marcação do checkbox das linhas. 
É comparado os fornecedores entre Origem e Destino através do CNPJ. 

### Pagar

Através da comparação de fornecedores pelo CNPJ, se o mesmo for encontrado na base Destino, então o 
pagar será redirecionado para o cadastro existente. 

### Empresas e Clientes

[Empresas e Clientes] 

Importante: <br />
O que define se o Integrador irá trazer as empresas ou não, será a marcação do checkbox das linhas. 
Os clientes que serão inseridos dependem que este esteja devidamente amarrado a empresa marcada, 
se houver inconsistência e o cliente não estiver vinculado corretamente, não irá trazer. 

### Receber

Possui a mesma condição informada anteriormente, desta forma somente irá trazer o receber dos clientes que estão 
devidamente vinculados.
