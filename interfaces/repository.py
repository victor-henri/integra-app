from abc import ABC, abstractmethod
from typing import TypedDict, Type


class AccessDatabase(TypedDict):
    host: str
    user: str
    password: str
    database: str
    port: int

class RepositoryInterface(ABC):

    @classmethod @abstractmethod
    def select_produto(self):
        pass

    @classmethod @abstractmethod
    def insert_produto(self, produtos):
        pass

    @classmethod @abstractmethod
    def consulta_produto_pos_insert(self, dados_tabela):
        pass

    @classmethod @abstractmethod
    def atualiza_campo_produto_pos_insert(self, dados_atualizacao):
        pass

    @classmethod @abstractmethod
    def select_fabricante_origem(self):
        pass

    @classmethod @abstractmethod
    def insert_fabricante(self, fabricantes):
        pass

    @classmethod @abstractmethod
    def select_principio_ativo_origem(self):
        pass

    @classmethod @abstractmethod
    def select_principio_ativo_destino(self):
        pass

    @classmethod @abstractmethod
    def insert_principios(self, principios):
        pass

    @classmethod @abstractmethod
    def select_barras(self):
        pass

    @classmethod @abstractmethod
    def insert_barras(self, barras_selecionados):
        pass

    @classmethod @abstractmethod
    def select_estoque(self):
        pass

    @classmethod @abstractmethod
    def insert_estoque(self, estoques):
        pass

    @classmethod @abstractmethod
    def select_produto_pos_insert(self):
        pass

    @classmethod @abstractmethod
    def select_lote(self):
        pass

    @classmethod @abstractmethod
    def insert_lote(self, lotes):
        pass

    @classmethod @abstractmethod
    def select_preco_filial(self):
        pass

    @classmethod @abstractmethod
    def insert_precos_filial(self, precos):
        pass

    @classmethod @abstractmethod
    def select_empresas(self, empresas_selecionadas):
        pass

    @classmethod @abstractmethod
    def select_fornecedor_origem(self, fornecedores_selecionados):
        pass

    @classmethod @abstractmethod
    def select_fornecedor_destino(self):
        pass

    @classmethod @abstractmethod
    def select_cliente(self, empresas_selecionadas):
        pass

    @classmethod @abstractmethod
    def insert_empresa(self, empresas):
        pass

    @classmethod @abstractmethod
    def insert_fornecedor(self, fornecedores):
        pass

    @classmethod @abstractmethod
    def insert_cliente(self, clientes):
        pass

    @classmethod @abstractmethod
    def insert_receber(self, recebers):
        pass

    @classmethod @abstractmethod
    def consulta_fornecedor_pos_insert(self):
        pass

    @classmethod @abstractmethod
    def consulta_produto_comparacao(self):
        pass

    @classmethod @abstractmethod
    def consulta_pos_insert(self, produto):
        pass

    @classmethod @abstractmethod
    def insert_pagar(self, pagars):
        pass

    @classmethod @abstractmethod
    def select_receber(self, clientes_selecionados):
        pass

    @classmethod @abstractmethod
    def select_pagar(self, fornecedores_selecionados):
        pass

    @classmethod @abstractmethod
    def select_grupo_origem_sapagado(self):
        pass

    @classmethod @abstractmethod
    def select_grupo_origem_capagado(self):
        pass

    @classmethod @abstractmethod
    def select_grupo_destino_sapagado(self):
        pass

    @classmethod @abstractmethod
    def select_grupo_destino_capagado(self):
        pass

    @classmethod @abstractmethod
    def select_listagem_empresa(self):
        pass

    @classmethod @abstractmethod
    def select_listagem_fornecedor(self):
        pass

    @classmethod @abstractmethod
    def limpa_campo_auxiliar(self, marcador_limpeza):
        pass
