import tkinter as tk
import tkinter.font as fonte
import tkinter.ttk as ttk
import ttkbootstrap as ttkb
from ttkwidgets import CheckboxTreeview
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
import logging
import documentacao
from iteradorSQL import IteradorSql
from fabricante import Fabricante
from principioativo import PrincipioAtivo
from produto import Produto
from barras import BarrasAdicional
from estoque import EstoqueMinimo
from lote import Lote
from precofilial import PrecoFilial
from empresa import Empresa
from cliente import Cliente
from receber import Receber
from fornecedor import Fornecedor
from pagar import Pagar


class Ui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.produtos_ids_separados = None
        self.fornecedores_selecionados = None
        self.empresas_selecionadas = None
        self.clientes_selecionados = None
        self.concluido_message = None
        self.fornecedores_pos_insert = None
        self.erro_label = None
        self.erro_frame = None
        self.popup_top = None
        self.dalerta_img = None
        self.oalerta_img = None
        self.descerro = None
        self.coderro = None
        self.fornecedores_encontrados_tratados = None
        self.iid_lista_fornecedores = None
        self.classes_encontradas = None
        self.iid_lista_grupo_origem = None
        self.iid_lista_empresas = None
        self.dados_destino = None
        self.dados_origem = None
        self.principios_encontrados_tratados = None
        self.fabricantes_encontrados_tratados = None

        # Topo
        self.configure(height=200, width=200)
        self.resizable(False, False)
        self.title("IntegraApp")
        self.tema_padrao = ttkb.Style()
        self.tema_padrao.theme_use('integra_visual')
        self.tema_padrao.configure('Treeview', rowheight=23)
        self.fonte_corpo = fonte.Font(family='Roboto', size=10)
        self.fonte_titulo = fonte.Font(family='Roboto', size=10)

        # Frame Principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.configure(height=250, padding=10)
        self.main_frame.grid(column=0, row=0)
        self.abas_notebook = ttk.Notebook(self.main_frame)

        # Conexões
        self.conexoes_frame = ttk.Frame(self.abas_notebook)
        self.conexoes_frame.pack(side=tk.TOP)
        self.conexoes_frame.grid_anchor(tk.CENTER)
        self.abas_notebook.add(self.conexoes_frame,
                               compound=tk.CENTER,
                               state=tk.NORMAL,
                               sticky=tk.NSEW,
                               text="Conexões")

        # Banco de Origem
        self.borigem_lframe = ttk.Labelframe(self.conexoes_frame)
        self.borigem_lframe.configure(labelanchor=tk.N, padding=20, text="Banco de Origem")
        self.borigem_lframe.grid(column=0, padx=50, row=0)
        self.borigem_lframe.columnconfigure(8, weight=1)
        self.borigem_lframe.grid_anchor(tk.CENTER)

        # Banco de Origem - Label
        self.oipservidor_label = ttk.Label(self.borigem_lframe, font=self.fonte_corpo)
        self.oipservidor_label.configure(text="Ip do Servidor")
        self.oipservidor_label.grid(column=0, row=0)
        self.obanco_label = ttk.Label(self.borigem_lframe, font=self.fonte_corpo)
        self.obanco_label.configure(text="Nome do Banco")
        self.obanco_label.grid(column=0, row=2)
        self.ousuario_label = ttk.Label(self.borigem_lframe, font=self.fonte_corpo)
        self.ousuario_label.configure(text="Usuário")
        self.ousuario_label.grid(column=0, row=4)
        self.osenha_label = ttk.Label(self.borigem_lframe, font=self.fonte_corpo)
        self.osenha_label.configure(text="Senha")
        self.osenha_label.grid(column=0, row=6)
        self.oporta_label = ttk.Label(self.borigem_lframe, font=self.fonte_corpo)
        self.oporta_label.configure(text="Porta")
        self.oporta_label.grid(column=0, padx=20, row=8, sticky=tk.W)
        self.oid_label = ttk.Label(self.borigem_lframe, font=self.fonte_corpo)
        self.oid_label.configure(text="ID Filial")
        self.oid_label.grid(column=0, row=8, sticky=tk.E, ipadx=6)

        # Banco de Origem - Entry
        self.oipservidor_entry = ttk.Entry(self.borigem_lframe, justify=tk.CENTER)
        self.oipservidor_entry.grid(column=0, row=1)
        self.obanco_entry = ttk.Entry(self.borigem_lframe, justify=tk.CENTER)
        self.obanco_entry.grid(column=0, row=3)
        self.ousuario_entry = ttk.Entry(self.borigem_lframe, justify=tk.CENTER)
        self.ousuario_entry.grid(column=0, row=5)
        self.osenha_entry = ttk.Entry(self.borigem_lframe, show='*', justify=tk.CENTER)
        self.osenha_entry.grid(column=0, row=7)
        self.oporta_entry = ttk.Entry(self.borigem_lframe, justify=tk.CENTER)
        self.oporta_entry.configure(width=8)
        self.oporta_entry.grid(column=0, row=9, sticky=tk.W)
        self.oid_entry = ttk.Entry(self.borigem_lframe, justify=tk.CENTER)
        self.oid_entry.configure(width=8)
        self.oid_entry.grid(column=0, row=9, sticky=tk.E)

        # Banco de Origem - Button
        self.oconectar_button = ttkb.Button(self.borigem_lframe, command=self.conexao_origem)
        self.oconectar_button.configure(text="Conectar", width=15)
        self.oconectar_button.grid(column=0, pady=10, row=11)
        self.oalerta_button = ttk.Button()

        # Banco de Origem - Message
        self.omensagem_message = tk.Message(self.borigem_lframe, font=self.fonte_corpo)
        self.omensagem_message.configure(text="Desconectado",
                                         width=100,
                                         foreground='red',
                                         relief=tk.FLAT,
                                         borderwidth=1)
        self.omensagem_message.grid(column=0, row=12)

        # Banco de Destino
        self.bdestino_lframe = ttk.Labelframe(self.conexoes_frame)
        self.bdestino_lframe.configure(labelanchor=tk.N, padding=20, text="Banco de Destino")
        self.bdestino_lframe.grid(column=2, padx=50, row=0)
        self.bdestino_lframe.columnconfigure(8, weight=1)
        self.bdestino_lframe.grid_anchor(tk.CENTER)

        # Banco de Destino - Label
        self.dipservidor_label = ttk.Label(self.bdestino_lframe, font=self.fonte_corpo)
        self.dipservidor_label.configure(text="Ip do Servidor")
        self.dipservidor_label.grid(column=0, row=0)
        self.dbanco_label = ttk.Label(self.bdestino_lframe, font=self.fonte_corpo)
        self.dbanco_label.configure(text="Nome do Banco")
        self.dbanco_label.grid(column=0, row=2)
        self.dusuario_label = ttk.Label(self.bdestino_lframe, font=self.fonte_corpo)
        self.dusuario_label.configure(text="Usuário")
        self.dusuario_label.grid(column=0, row=4)
        self.dsenha_label = ttk.Label(self.bdestino_lframe, font=self.fonte_corpo)
        self.dsenha_label.configure(text="Senha")
        self.dsenha_label.grid(column=0, row=6)
        self.dporta_label = ttk.Label(self.bdestino_lframe, font=self.fonte_corpo)
        self.dporta_label.configure(text="Porta")
        self.dporta_label.grid(column=0, padx=20, row=8, sticky=tk.W)
        self.did_label = ttk.Label(self.bdestino_lframe, font=self.fonte_corpo)
        self.did_label.configure(text="ID Filial")
        self.did_label.grid(column=0, row=8, sticky=tk.E, ipadx=6)

        # Banco de Destino - Entry
        self.dipservidor_entry = ttk.Entry(self.bdestino_lframe, justify=tk.CENTER)
        self.dipservidor_entry.grid(column=0, row=1)
        self.dbanco_entry = ttk.Entry(self.bdestino_lframe, justify=tk.CENTER)
        self.dbanco_entry.grid(column=0, row=3)
        self.dusuario_entry = ttk.Entry(self.bdestino_lframe, justify=tk.CENTER)
        self.dusuario_entry.grid(column=0, row=5)
        self.dsenha_entry = ttk.Entry(self.bdestino_lframe, show='*', justify=tk.CENTER)
        self.dsenha_entry.grid(column=0, row=7)
        self.dporta_entry = ttk.Entry(self.bdestino_lframe, justify=tk.CENTER)
        self.dporta_entry.configure(width=8)
        self.dporta_entry.grid(column=0, row=9, sticky=tk.W)
        self.did_entry = ttk.Entry(self.bdestino_lframe, justify=tk.CENTER)
        self.did_entry.configure(width=8)
        self.did_entry.grid(column=0, row=9, sticky=tk.E)

        # Banco de Destino - Button
        self.dconectar_button = ttk.Button(self.bdestino_lframe, command=self.conexao_destino)
        self.dconectar_button.configure(text="Conectar", width=15)
        self.dconectar_button.grid(column=0, pady=10, row=11)
        self.dalerta_button = ttk.Button()

        # Banco de Destino - Message
        self.dmensagem_message = tk.Message(self.bdestino_lframe, font=self.fonte_corpo)
        self.dmensagem_message.configure(text="Desconectado",
                                         width=100,
                                         foreground='red',
                                         relief=tk.FLAT,
                                         borderwidth=1)
        self.dmensagem_message.grid(column=0, row=12)

        # Banco de Destino - Separator
        self.sbanco_separator = ttk.Separator(self.conexoes_frame)
        self.sbanco_separator.configure(orient=tk.VERTICAL)
        self.sbanco_separator.place(anchor=tk.CENTER, height=350, x=470, y=230)

        # Configurações de Produtos
        self.configuracoes_frame = ttk.Frame(self.abas_notebook)
        self.configuracoes_lframe = ttk.Labelframe(self.configuracoes_frame)
        self.configuracoes_lframe.configure(height=100, labelanchor=tk.N, padding=20, text="Opções")
        self.configuracoes_lframe.pack(anchor=tk.N, expand=1, fill=tk.BOTH, side=tk.TOP)
        self.configuracoes_lframe.columnconfigure(0, weight=1)
        self.configuracoes_lframe.columnconfigure(1, weight=1)
        self.configuracoes_lframe.columnconfigure(2, weight=1)
        self.configuracoes_lframe.columnconfigure(3, weight=1)
        self.configuracoes_lframe.columnconfigure(4, weight=1)
        self.configuracoes_frame.configure(height=200, padding=15, width=200)
        self.configuracoes_frame.pack(side=tk.TOP)
        self.abas_notebook.add(self.configuracoes_frame,
                               compound=tk.TOP,
                               state=tk.NORMAL,
                               sticky=tk.NSEW,
                               text="Configurações de Produtos")

        # Configurações de Produtos - Frame
        self.grupoconfig1_frame = ttk.Frame(self.configuracoes_lframe)
        self.grupoconfig1_frame.configure(height=250, padding=5)
        self.grupoconfig1_frame.place(height=250, width=400, x=15, y=60)

        self.grupoconfig2_frame = ttk.Frame(self.configuracoes_lframe)
        self.grupoconfig2_frame.configure(height=250, padding=5)
        self.grupoconfig2_frame.place(height=250, width=400, x=450, y=60)

        self.principio_lframe = ttk.Labelframe(self.grupoconfig1_frame)
        self.principio_lframe.configure(text="Principio Ativo", height=80, labelanchor=tk.N)
        self.principio_lframe.pack(fill=tk.X)

        self.fabricante_lframe = ttk.Labelframe(self.grupoconfig2_frame)
        self.fabricante_lframe.configure(text="Fabricantes", height=80, labelanchor=tk.N)
        self.fabricante_lframe.pack(fill=tk.X)

        # Configurações de Produtos - Label
        self.zeros_label = ttk.Label(self.configuracoes_lframe)
        self.zeros_label.configure(text="ou mais zero(s).")
        self.zeros_label.place(anchor=tk.NW, x=415, y=322)

        self.id_fabricante_label = ttk.Label(self.fabricante_lframe)
        self.id_fabricante_label.configure(text="Id de Destino")
        self.id_fabricante_label.place(anchor=tk.NW, x=280, y=20)

        self.id_principio_label = ttk.Label(self.principio_lframe)
        self.id_principio_label.configure(text="Id de Destino")
        self.id_principio_label.place(anchor=tk.NW, x=280, y=20)

        # Configurações de Produtos - Entry
        self.id_fabricante_entry = ttk.Entry(self.fabricante_lframe, justify=tk.CENTER)
        self.id_fabricante_entry.configure(width=5)
        self.id_fabricante_entry.place(anchor=tk.NW, height=26, width=30, x=245, y=17)

        self.id_principio_entry = ttk.Entry(self.principio_lframe, justify=tk.CENTER)
        self.id_principio_entry.configure(width=5)
        self.id_principio_entry.place(anchor=tk.NW, height=26, width=30, x=245, y=17)

        # Configurações de Produtos - Button
        self.selprodutos_cbutton = tk.BooleanVar()
        self.selprodutos_cbutton.set(False)
        self.produtos_cbutton = ttk.Checkbutton(self.configuracoes_lframe,
                                                variable=self.selprodutos_cbutton,
                                                command=self.troca_opcao_produto)
        self.produtos_cbutton.configure(text="Produto")
        self.produtos_cbutton.grid(column=0, row=0)

        self.selbarras_cbutton = tk.BooleanVar()
        self.selbarras_cbutton.set(False)
        self.barras_cbutton = ttk.Checkbutton(self.configuracoes_lframe, variable=self.selbarras_cbutton)
        self.barras_cbutton.configure(text="Barras Adicional", state=tk.DISABLED)
        self.barras_cbutton.grid(column=1, row=0)

        self.selestoque_cbutton = tk.BooleanVar()
        self.selestoque_cbutton.set(False)
        self.estoque_cbutton = ttk.Checkbutton(self.configuracoes_lframe, variable=self.selestoque_cbutton)
        self.estoque_cbutton.configure(text="Estoque", state=tk.DISABLED)
        self.estoque_cbutton.grid(column=2, row=0)

        self.sellotes_cbutton = tk.BooleanVar()
        self.sellotes_cbutton.set(False)
        self.lotes_cbutton = ttk.Checkbutton(self.configuracoes_lframe, variable=self.sellotes_cbutton)
        self.lotes_cbutton.configure(text="Lote", state=tk.DISABLED)
        self.lotes_cbutton.grid(column=3, row=0)

        self.selpreco_filial_cbutton = tk.BooleanVar()
        self.selpreco_filial_cbutton.set(False)
        self.preco_filial_cbutton = ttk.Checkbutton(self.configuracoes_lframe, variable=self.selpreco_filial_cbutton)
        self.preco_filial_cbutton.configure(text="Preço Filial", state=tk.DISABLED)
        self.preco_filial_cbutton.grid(column=4, row=0)

        self.seldesconsiderar_prod_cbutton = tk.BooleanVar()
        self.seldesconsiderar_prod_cbutton.set(False)
        self.desconsiderar_prod_cbutton = ttk.Checkbutton(self.configuracoes_lframe,
                                                          variable=self.seldesconsiderar_prod_cbutton)
        self.desconsiderar_prod_cbutton.configure(text="Não importar produtos com barras que iniciam com ")
        self.desconsiderar_prod_cbutton.place(anchor=tk.NW, y=325)

        self.seldesconsiderar_apagados_cbutton = tk.BooleanVar()
        self.seldesconsiderar_apagados_cbutton.set(False)
        self.desconsiderar_apagados_cbutton = ttk.Checkbutton(self.configuracoes_lframe,
                                                              variable=self.seldesconsiderar_apagados_cbutton)
        self.desconsiderar_apagados_cbutton.configure(text="Não importar registros marcados como apagados.")
        self.desconsiderar_apagados_cbutton.place(anchor=tk.NW, y=350)

        self.selfabricante_cnpj_cbutton = tk.BooleanVar()
        self.selfabricante_cnpj_cbutton.set(False)
        self.fabricante_cnpj_cbutton = ttk.Checkbutton(self.fabricante_lframe,
                                                       variable=self.selfabricante_cnpj_cbutton,
                                                       command=self.troca_opcao_fabricante)
        self.fabricante_cnpj_cbutton.configure(text="Por CNPJ")
        self.fabricante_cnpj_cbutton.place(anchor=tk.NW, x=25, y=22)

        self.selfabricante_id_cbutton = tk.BooleanVar()
        self.selfabricante_id_cbutton.set(False)
        self.fabricante_id_cbutton = ttk.Checkbutton(self.fabricante_lframe,
                                                     variable=self.selfabricante_id_cbutton,
                                                     command=self.troca_opcao_fabricante)
        self.fabricante_id_cbutton.configure(text="Por ID")
        self.fabricante_id_cbutton.place(anchor=tk.NW, x=145, y=22)

        self.selprincipio_desc_cbutton = tk.BooleanVar()
        self.selprincipio_desc_cbutton.set(False)
        self.principio_desc_cbutton = ttk.Checkbutton(self.principio_lframe,
                                                      variable=self.selprincipio_desc_cbutton,
                                                      command=self.troca_opcao_principio)
        self.principio_desc_cbutton.configure(text="Por Descrição")
        self.principio_desc_cbutton.place(anchor=tk.NW, x=25, y=22)

        self.selprincipio_id_cbutton = tk.BooleanVar()
        self.selprincipio_id_cbutton.set(False)
        self.principio_id_cbutton = ttk.Checkbutton(self.principio_lframe,
                                                    variable=self.selprincipio_id_cbutton,
                                                    command=self.troca_opcao_principio)
        self.principio_id_cbutton.configure(text="Por ID")
        self.principio_id_cbutton.place(anchor=tk.NW, x=160, y=22)

        # Configurações de Produtos - Spinbox
        self.valor_zeros_spinbox = tk.StringVar(value='1')
        self.zeros_spinbox = ttk.Spinbox(self.configuracoes_lframe,
                                         from_=1,
                                         to=12,
                                         textvariable=self.valor_zeros_spinbox)
        self.zeros_spinbox.place(anchor=tk.NW, width=50, x=360, y=317)

        # Configurações de Produtos - Separator
        self.config1_separator = ttk.Separator(self.configuracoes_lframe)
        self.config1_separator.configure(orient=tk.HORIZONTAL)
        self.config1_separator.place(anchor=tk.CENTER, width=850, x=430, y=40)
        self.config2_separator = ttk.Separator(self.configuracoes_lframe)
        self.config2_separator.configure(orient=tk.HORIZONTAL)
        self.config2_separator.place(anchor=tk.CENTER, width=850, x=430, y=310)

        # Grupos de Produtos
        self.grupo_prod_frame = ttk.Frame(self.abas_notebook)
        self.grupo_prod_frame.configure(height=200, width=200, padding=5)
        self.grupo_prod_frame.grid(column=0, row=0, sticky=tk.NSEW)

        self.abas_notebook.add(self.grupo_prod_frame, sticky=tk.NSEW, text="Grupos de Produtos")

        self.grupos_frame = ttk.Frame(self.grupo_prod_frame)
        self.grupos_frame.configure(height=200, width=200, padding=5)
        self.grupos_frame.pack(side=tk.TOP, expand=1, fill=tk.BOTH)

        # Grupos de Produtos - LabelFrame
        self.gr_prod_origem_lframe = ttk.Labelframe(self.grupos_frame, borderwidth=0)
        self.gr_prod_origem_lframe.configure(height=200, labelanchor=tk.N, text="Banco de Origem", width=200)
        self.gr_prod_origem_lframe.pack(anchor=tk.W, expand=1, fill=tk.BOTH, padx=15, pady=15, side=tk.LEFT)
        self.gr_prod_origem_lframe.rowconfigure(0, weight=1)
        self.gr_prod_origem_lframe.columnconfigure(0, weight=1)

        self.gr_prod_destino_lframe = ttk.Labelframe(self.grupos_frame, borderwidth=0)
        self.gr_prod_destino_lframe.configure(height=200, labelanchor=tk.N, text="Banco de Destino", width=200)
        self.gr_prod_destino_lframe.pack(anchor=tk.W, expand=1, fill=tk.BOTH, padx=15, pady=15, side=tk.LEFT)
        self.gr_prod_destino_lframe.rowconfigure(0, weight=1)
        self.gr_prod_destino_lframe.columnconfigure(0, weight=1)

        # Grupos de Produtos - CheckboxTreeView
        self.gr_prod_origem_treeview = CheckboxTreeview(self.gr_prod_origem_lframe)
        self.gr_prod_origem_treeview.grid(column=0, padx=5, pady=5, row=0, sticky=tk.NSEW)
        self.gr_prod_origem_treeview['columns'] = ('Novo ID', 'ID', 'Nome')
        self.gr_prod_origem_treeview.column('#0', width=30, stretch=False)
        self.gr_prod_origem_treeview.column('Novo ID', anchor=tk.CENTER, width=70, stretch=False)
        self.gr_prod_origem_treeview.column('ID', anchor=tk.CENTER, width=30, stretch=False)
        self.gr_prod_origem_treeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.gr_prod_origem_treeview.heading('#0', text='', anchor=tk.CENTER)
        self.gr_prod_origem_treeview.heading('Novo ID', text='Novo ID', anchor=tk.CENTER)
        self.gr_prod_origem_treeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.gr_prod_origem_treeview.heading('Nome', text='Nome', anchor=tk.W)

        self.gr_prod_destino_treeview = CheckboxTreeview(self.gr_prod_destino_lframe)
        self.gr_prod_destino_treeview.grid(column=0, padx=5, pady=5, row=0, sticky=tk.NSEW)
        self.gr_prod_destino_treeview['columns'] = ('ID', 'Nome')
        self.gr_prod_destino_treeview.column('#0', width=0, stretch=False)
        self.gr_prod_destino_treeview.column('ID', anchor=tk.CENTER, width=50, stretch=False)
        self.gr_prod_destino_treeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.gr_prod_destino_treeview.heading('#0', text='')
        self.gr_prod_destino_treeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.gr_prod_destino_treeview.heading('Nome', text='Nome', anchor=tk.W)

        # Grupos de Produtos - CheckButton
        self.selapagado_grupo_origem_cbutton = tk.BooleanVar()
        self.selapagado_grupo_origem_cbutton.set(False)
        self.apagado_grupo_origem_cbutton = ttk.Checkbutton(self.gr_prod_origem_lframe,
                                                            variable=self.selapagado_grupo_origem_cbutton,
                                                            command=self.lista_grupo_origem)
        self.apagado_grupo_origem_cbutton.configure(text="Não mostrar grupos apagados")
        self.apagado_grupo_origem_cbutton.grid(column=0, row=1, sticky=tk.W)

        self.seltodos_grp_origem_cbutton = tk.BooleanVar()
        self.seltodos_grp_origem_cbutton.set(False)
        self.todos_grp_origem_cbutton = ttk.Checkbutton(self.gr_prod_origem_lframe,
                                                        variable=self.seltodos_grp_origem_cbutton,
                                                        command=self.marca_grupos_origem)
        self.todos_grp_origem_cbutton.configure(text="Selecionar todos")
        self.todos_grp_origem_cbutton.grid(column=0, row=1, sticky=tk.E)

        self.selapagado_grupo_destino_cbutton = tk.BooleanVar()
        self.selapagado_grupo_destino_cbutton.set(False)
        self.apagado_grupo_destino_cbutton = ttk.Checkbutton(self.gr_prod_destino_lframe,
                                                             variable=self.selapagado_grupo_destino_cbutton,
                                                             command=self.lista_grupo_destino)
        self.apagado_grupo_destino_cbutton.configure(text="Não mostrar grupos apagados")
        self.apagado_grupo_destino_cbutton.grid(column=0, row=1, sticky=tk.W)

        # Fornecedores e Pagar
        self.fornecedores_frame = ttk.Frame(self.abas_notebook)
        self.fornecedores_frame.configure(height=200, padding=15, width=200)
        self.fornecedores_frame.pack(side=tk.TOP)
        self.abas_notebook.add(self.fornecedores_frame, text="Fornecedores e Pagar")
        self.opcoes_fornecedores_frame = ttk.Labelframe(self.fornecedores_frame)
        self.opcoes_fornecedores_frame.configure(height=80, width=400, labelanchor=tk.N, padding=15, text="Opções")
        self.opcoes_fornecedores_frame.pack(anchor=tk.CENTER, fill=tk.X, side=tk.TOP)
        self.opcoes_fornecedores_frame.columnconfigure(tk.ALL, weight=1)

        # Fornecedores e Pagar - Treeview
        self.fornecedores_treeview = CheckboxTreeview(self.fornecedores_frame)
        self.fornecedores_treeview.pack(expand=1, fill=tk.X, side=tk.BOTTOM, anchor=tk.N, ipady=5)
        self.fornecedores_treeview.configure(height=13)
        self.fornecedores_treeview['columns'] = ('ID', 'Nome')
        self.fornecedores_treeview.column('#0', width=40, stretch=False)
        self.fornecedores_treeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.fornecedores_treeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.fornecedores_treeview.heading('#0', text='', anchor=tk.CENTER)
        self.fornecedores_treeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.fornecedores_treeview.heading('Nome', text='Nome', anchor=tk.W)

        # Fornecedores e Pagar - Button
        self.selfornecedores_cbutton = tk.BooleanVar()
        self.selfornecedores_cbutton.set(False)
        self.fornecedores_cbutton = ttk.Checkbutton(self.opcoes_fornecedores_frame,
                                                    variable=self.selfornecedores_cbutton)
        self.fornecedores_cbutton.configure(text="Fornecedores")
        self.fornecedores_cbutton.grid(column=0, row=0, sticky=tk.W, padx=160)

        self.selpagar_cbutton = tk.BooleanVar()
        self.selpagar_cbutton.set(False)
        self.pagar_cbutton = ttk.Checkbutton(self.opcoes_fornecedores_frame,
                                             variable=self.selpagar_cbutton)
        self.pagar_cbutton.configure(text="Pagar")
        self.pagar_cbutton.grid(column=1, row=0, sticky=tk.E, padx=160)

        self.seltodos_fornecedores_cbutton = tk.BooleanVar()
        self.seltodos_fornecedores_cbutton.set(False)
        self.todos_fornecedores_cbutton = ttk.Checkbutton(self.fornecedores_frame,
                                                          variable=self.seltodos_fornecedores_cbutton,
                                                          command=self.marca_fornecedores)
        self.todos_fornecedores_cbutton.configure(text="Selecionar todos")
        self.todos_fornecedores_cbutton.place(anchor=tk.NW, x=770, y=413)

        # Empresas e Clientes
        self.empresas_frame = ttk.Frame(self.abas_notebook)
        self.empresas_frame.configure(height=200, padding=15, width=200)
        self.empresas_frame.pack(side=tk.TOP)
        self.abas_notebook.add(self.empresas_frame, text=" Empresas e Clientes ")
        self.opcoesempresas_frame = ttk.Labelframe(self.empresas_frame)
        self.opcoesempresas_frame.configure(height=80, width=400, labelanchor=tk.N, padding=15, text="Opções")
        self.opcoesempresas_frame.pack(anchor=tk.CENTER, fill=tk.X, side=tk.TOP)
        self.opcoesempresas_frame.columnconfigure("all", weight=1)

        # Empresas e Clientes - Treeview
        self.empresas_treeview = CheckboxTreeview(self.empresas_frame)
        self.empresas_treeview.pack(expand=1, fill=tk.X, side=tk.BOTTOM, anchor=tk.N, ipady=5)
        self.empresas_treeview.configure(height=13)
        self.empresas_treeview['columns'] = ('ID', 'Nome')
        self.empresas_treeview.column('#0', width=40, stretch=False)
        self.empresas_treeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.empresas_treeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.empresas_treeview.heading('#0', text='', anchor=tk.CENTER)
        self.empresas_treeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.empresas_treeview.heading('Nome', text='Nome', anchor=tk.W)

        # Empresas e Clientes - Button
        self.selempresas_cbutton = tk.BooleanVar()
        self.selempresas_cbutton.set(False)
        self.empresas_cbutton = ttk.Checkbutton(self.opcoesempresas_frame,
                                                variable=self.selempresas_cbutton)
        self.empresas_cbutton.configure(text="Empresas (Clientes e Dependentes)")
        self.empresas_cbutton.grid(column=0, row=0, sticky=tk.W, padx=120)

        self.selreceber_cbutton = tk.BooleanVar()
        self.selreceber_cbutton.set(False)
        self.receber_cbutton = ttk.Checkbutton(self.opcoesempresas_frame,
                                               variable=self.selreceber_cbutton)
        self.receber_cbutton.configure(text="Receber")
        self.receber_cbutton.grid(column=1, row=0, sticky=tk.E, padx=120)

        self.seltodosempresas_cbutton = tk.BooleanVar()
        self.seltodosempresas_cbutton.set(False)
        self.todosempresas_cbutton = ttk.Checkbutton(self.empresas_frame,
                                                     variable=self.seltodosempresas_cbutton,
                                                     command=self.marca_empresas)
        self.todosempresas_cbutton.configure(text="Selecionar todos")
        self.todosempresas_cbutton.place(anchor=tk.NW, x=770, y=413)

        # Logs
        self.logs_frame = ttk.Frame(self.abas_notebook)
        self.logs_frame.configure(height=200, padding=15, width=200)
        self.logs_frame.pack(side=tk.TOP)
        self.abas_notebook.add(self.logs_frame, text="Execução e Logs")
        self.abas_notebook.configure(height=450, padding=5, width=800)
        self.abas_notebook.grid(column=1, row=0, sticky=tk.E)

        # Logs - ScrolledText
        self.logs_scrtext = ScrolledText(self.logs_frame)
        self.logs_scrtext.configure(borderwidth=5, font=self.fonte_corpo)
        self.logs_scrtext.place(anchor=tk.NW, width=940, height=383, x=0, y=0)

        # Logs - Button
        self.iniciar_button = ttk.Button(self.logs_frame, command=self.iniciar)
        self.iniciar_button.configure(text="Iniciar", width=20)
        self.iniciar_button.place(anchor=tk.NW, height=30, x=30, y=395)

        # Logs - ProgressBar
        self.progressbar = ttk.Progressbar(self.logs_frame, mode='determinate', bootstyle='success')
        self.progressbar.configure(length=600, orient=tk.HORIZONTAL)
        self.progressbar.place(anchor=tk.NW, width=470, x=250, y=404)

        # Documentação
        self.documentacao_frame = ttk.Frame(self.abas_notebook)
        self.documentacao_frame.configure(height=200, padding=15, width=200)
        self.documentacao_frame.pack(side=tk.TOP)
        self.abas_notebook.add(self.documentacao_frame, text="Documentação")
        self.abas_notebook.configure(height=450, padding=5, width=800)

        # Documentação - Text
        self.documentacao_text = ScrolledText(self.documentacao_frame)
        self.documentacao_text.configure(borderwidth=5, font=self.fonte_corpo)
        self.documentacao_text.insert(tk.END, documentacao.informacao_doc)
        self.documentacao_text.configure(state=tk.DISABLED)
        self.documentacao_text.pack(fill=tk.BOTH)

        # Logo
        self.logo_frame = ttk.Frame(self.main_frame)
        self.img = ImageTk.PhotoImage(Image.open('imgs/integrabanner.png'))
        self.imglogo_label = ttk.Label(self.logo_frame, image=self.img)
        self.imglogo_label.pack(anchor=tk.E, side=tk.TOP)
        self.logo_frame.configure(height=400, width=400)
        self.logo_frame.grid(column=0, row=0, sticky=tk.W)

        # Binds
        self.gr_prod_origem_treeview.bind("<Double-1>", self.duplo_clique_grp)

    # Métodos de Binds.
    @staticmethod
    def fora_foco(event):
        event.widget.destroy()

    def duplo_clique_grp(self, event):
        regiao_clique = self.gr_prod_origem_treeview.identify_region(event.x, event.y)

        if regiao_clique not in ("tree", "cell"):
            return

        coluna = self.gr_prod_origem_treeview.identify_column(event.x)
        index_coluna = int(coluna[1:]) - 1

        iid_selecionado = self.gr_prod_origem_treeview.focus()
        valores_selecionados = self.gr_prod_origem_treeview.item(iid_selecionado)

        if coluna != '#1':
            print("Coluna invalida")
        else:
            linha_selecionada = valores_selecionados.get('values')[index_coluna]
            print(linha_selecionada)

        caixa_coluna = self.gr_prod_origem_treeview.bbox(iid_selecionado, coluna)

        editavel_entry = ttk.Entry(self.gr_prod_origem_treeview)
        editavel_entry.identificador_coluna = index_coluna
        editavel_entry.identificador_item_iid = iid_selecionado
        editavel_entry.insert(0, linha_selecionada)
        editavel_entry.select_range(0, tk.END)

        editavel_entry.focus()
        editavel_entry.bind("<FocusOut>", self.fora_foco)
        editavel_entry.bind("<Return>", self.pressiona_enter_grp)

        editavel_entry.place(x=caixa_coluna[0],
                             y=caixa_coluna[1],
                             w=caixa_coluna[2],
                             h=caixa_coluna[3])

    def pressiona_enter_grp(self, event):
        novo_texto = event.widget.get()
        iid_selecionado = event.widget.identificador_item_iid
        index_coluna = event.widget.identificador_coluna

        if index_coluna == 0:
            valor_atual = self.gr_prod_origem_treeview.item(iid_selecionado).get('values')
            valor_atual[index_coluna] = novo_texto
            self.gr_prod_origem_treeview.item(iid_selecionado, values=valor_atual)
        event.widget.destroy()

    # Métodos de conexão.
    def conexao_origem(self):
        self.dados_origem = {'host': self.oipservidor_entry.get(),
                             'user': self.ousuario_entry.get(),
                             'password': self.osenha_entry.get(),
                             'database': self.obanco_entry.get(),
                             'port': int(self.oporta_entry.get())}

        iterador = IteradorSql()
        retorno_origem = iterador.conexao_origem(dados_origem=self.dados_origem)

        if retorno_origem['retorno'] == 'Conectado':
            self.oalerta_button.destroy()
            self.omensagem_message.configure(text="Conectado", foreground='green')
            self.lista_grupo_origem()
            self.lista_empresas()
            self.lista_fornecedores()

        elif retorno_origem['retorno'] == 'pymysql.err.OperationalError':
            self.oalerta_button.destroy()
            self.omensagem_message.configure(text="Falha", foreground='orange')
            self.coderro = retorno_origem['codigo']
            self.descerro = retorno_origem['descricao']
            self.obotao_alerta(self.coderro, self.descerro)
            self.oalerta_button.place(anchor="w", height=22, width=22, x=30, y=323)

        else:
            self.oalerta_button.destroy()
            self.omensagem_message.configure(text="Falha", foreground='orange')
            self.coderro = 20
            self.descerro = retorno_origem['descricao']
            self.obotao_alerta(self.coderro, self.descerro)
            self.oalerta_button.place(anchor="w", height=22, width=22, x=30, y=323)

    def conexao_destino(self):
        self.dados_destino = {'host': self.dipservidor_entry.get(),
                              'user': self.dusuario_entry.get(),
                              'password': self.dsenha_entry.get(),
                              'database': self.dbanco_entry.get(),
                              'port': int(self.dporta_entry.get())}

        iterador = IteradorSql()
        retorno_destino = iterador.conexao_destino(dados_destino=self.dados_destino)

        if retorno_destino['retorno'] == 'Conectado':
            self.dalerta_button.destroy()
            self.dmensagem_message.configure(text="Conectado", foreground='green')
            self.lista_grupo_destino()

        elif retorno_destino['retorno'] == 'pymysql.err.OperationalError':
            self.dalerta_button.destroy()
            self.dmensagem_message.configure(text="Falha", foreground='orange')
            self.coderro = retorno_destino['codigo']
            self.descerro = retorno_destino['descricao']
            self.dbotao_alerta(self.coderro, self.descerro)
            self.dalerta_button.place(anchor="w", height=22, width=22, x=30, y=323)

        else:
            self.dalerta_button.destroy()
            self.dmensagem_message.configure(text="Falha", foreground='orange')
            self.coderro = 20
            self.descerro = retorno_destino['descricao']
            self.dbotao_alerta(self.coderro, self.descerro)
            self.dalerta_button.place(anchor="w", height=22, width=22, x=30, y=323)

    def obotao_alerta(self, coderro, descerro):
        self.oalerta_img = tk.PhotoImage(file="imgs/info.png")
        self.oalerta_button = ttk.Button(
            self.borigem_lframe,
            image=self.oalerta_img,
            command=lambda: self.retorna_erro(coderro, descerro),
            bootstyle="warning")
        self.oalerta_button.configure(compound="left", padding=1)

    def dbotao_alerta(self, coderro, descerro):
        self.dalerta_img = tk.PhotoImage(file="imgs/info.png")
        self.dalerta_button = ttk.Button(
            self.bdestino_lframe,
            image=self.dalerta_img,
            command=lambda: self.retorna_erro(coderro, descerro),
            bootstyle="warning")
        self.dalerta_button.configure(compound="left", padding=1)

    def retorna_erro(self, coderro, descerro):

        erro = f"Código: {coderro} | Descrição: {descerro}"
        self.popup_top = tk.Toplevel()
        self.grid_anchor("center")
        self.popup_top.title("Retorno do Erro")
        self.tema_padrao.theme_use('integra_visual')
        self.erro_frame = ttk.Frame(self.popup_top)
        self.erro_frame.configure(height=200, padding=20, width=200)
        self.erro_frame.grid(column=0, row=0)
        self.erro_frame.rowconfigure(1, weight=1)
        self.erro_frame.columnconfigure(1, weight=1)
        self.erro_label = ttk.Label(self.erro_frame)
        self.erro_label.configure(text=erro)
        self.erro_label.grid(column=1, row=1)

    def log(self, metodo=None, registro_erro=None, retorno_erro=None):

        logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s:%(message)s')
        separador = "| ============================================================================= |"
        ident = "| "

        if metodo:
            self.logs_scrtext.insert(tk.INSERT, f"{separador}\n")
            self.logs_scrtext.insert(tk.INSERT, f"{ident}{metodo}\n")
            self.logs_scrtext.insert(tk.INSERT, f"{separador}\n")
            logging.warning(separador)
            logging.warning(f"{ident}{metodo}")
            logging.warning(separador)

        if registro_erro or retorno_erro:
            self.logs_scrtext.insert(tk.INSERT, f"{separador}\n")
            self.logs_scrtext.insert(tk.INSERT, f"{ident}{registro_erro}\n")
            self.logs_scrtext.insert(tk.INSERT, f"{ident}{retorno_erro}\n")
            self.logs_scrtext.insert(tk.INSERT, f"{separador}\n")
            logging.warning(separador)
            logging.warning(f"{ident} {registro_erro}")
            logging.warning(f"{ident} {retorno_erro}")
            logging.warning(separador)

    # Métodos de listagem automática e exibição dos dados ao conectar.
    def lista_grupo_origem(self):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)

        try:
            if self.selapagado_grupo_origem_cbutton.get():
                grupos = iterador.select_grupo_origem_sapagado()

                index = 0
                self.iid_lista_grupo_origem = []

                for grupo in grupos:
                    self.gr_prod_origem_treeview.insert(
                        "", index=tk.END, iid=index, text='', values=('', grupo['id_grupo'], grupo['descricao']))
                    self.iid_lista_grupo_origem.append(index)
                    index += 1

            else:
                grupos = iterador.select_grupo_origem_capagado()

                index = 0
                self.iid_lista_grupo_origem = []

                for grupo in grupos:
                    self.gr_prod_origem_treeview.insert(
                        "", index=tk.END, iid=index, text='', values=('', grupo['id_grupo'], grupo['descricao']))
                    self.iid_lista_grupo_origem.append(index)
                    index += 1

        except Exception as err_lista_grupo_origem:
            print(f"Exceção no método lista_grupo_origem: {err_lista_grupo_origem}")

    def lista_grupo_destino(self):
        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)

        try:
            if self.selapagado_grupo_destino_cbutton.get():
                grupos = iterador.select_grupo_destino_sapagado()

                index = 0
                iid_lista_grupos_destino = []

                for grupo in grupos:
                    self.gr_prod_destino_treeview.insert(
                        "", index=tk.END, iid=index, text='', values=(grupo['id_grupo'], grupo['descricao']))
                    iid_lista_grupos_destino.append(index)
                    index += 1

            else:
                grupos = iterador.select_grupo_destino_capagado()

                index = 0
                iid_lista_grupos_destino = []

                for grupo in grupos:
                    self.gr_prod_destino_treeview.insert(
                        "", index=tk.END, iid=index, text='', values=(grupo['id_grupo'], grupo['descricao']))
                    iid_lista_grupos_destino.append(index)
                    index += 1

        except Exception as err_lista_grupo_destino:
            print(f"Exceção no método lista_grupo_destino: {err_lista_grupo_destino}")

    def lista_empresas(self):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        # Faz a listagem das empresas do banco de origem após realizar a conexão.

        try:
            empresas = iterador.select_listagem_empresa()

            index = 0
            self.iid_lista_empresas = []

            for empresa in empresas:
                self.empresas_treeview.insert(
                    "", index='end', iid=index, text='', values=(empresa['id_empresa'], empresa['nome_fantasia']))
                self.iid_lista_empresas.append(index)
                index += 1

        except Exception as err_lista_empresas:
            print(f"Exceção no método lista_empresas: {err_lista_empresas}")

    def lista_fornecedores(self):
        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)
        # Faz a listagem dos fornecedores do banco de origem após realizar a conexão.

        try:
            fornecedores = iterador.select_listagem_fornecedor()

            index = 0
            self.iid_lista_fornecedores = []

            for fornecedor in fornecedores:
                self.fornecedores_treeview.insert("",
                                                  index='end',
                                                  iid=index,
                                                  text='',
                                                  values=(fornecedor['id_fornecedor'],
                                                          fornecedor['razao_social']))
                self.iid_lista_fornecedores.append(index)
                index += 1

        except Exception as err_lista_fornecedores:
            print(f"Exceção no método lista_fornecedores: {err_lista_fornecedores}")

    # Métodos de marcação de todos os registros na Interface.
    def marca_empresas(self):
        for iid in self.iid_lista_empresas:
            self.empresas_treeview.change_state(item=iid, state='checked')

    def marca_fornecedores(self):
        for iid in self.iid_lista_fornecedores:
            self.fornecedores_treeview.change_state(item=iid, state='checked')

    def marca_grupos_origem(self):
        for iid in self.iid_lista_grupo_origem:
            self.gr_prod_origem_treeview.change_state(item=iid, state='checked')

    # Métodos de coleta dos registros selecionados na Interface.
    def checa_empresas(self):
        empresas_selecionadas_l = []

        for empresa in self.empresas_treeview.get_checked():
            id_empresa = self.empresas_treeview.item(item=empresa, option='values')
            empresas_selecionadas_l.append(id_empresa[0])

        empresas_selecionadas = tuple(empresas_selecionadas_l)
        return empresas_selecionadas

    def checa_fornecedores(self):
        fornecedores_selecionadas_l = []

        for fornecedor in self.fornecedores_treeview.get_checked():
            id_fornecedor = self.fornecedores_treeview.item(item=fornecedor, option='values')
            fornecedores_selecionadas_l.append(id_fornecedor[0])

        fornecedores_selecionados = tuple(fornecedores_selecionadas_l)
        return fornecedores_selecionados

    def checa_grupos_origem(self):
        grupos_selecionados = []  # → Lista de Dicionários.

        for grupo in self.gr_prod_origem_treeview.get_checked():
            valores = self.gr_prod_origem_treeview.item(item=grupo, option='values')
            grupo_selecionado = {'novo_id': int(valores[0]), 'antigo_id': int(valores[1])}
            grupos_selecionados.append(grupo_selecionado)

        return grupos_selecionados

    # Métodos de retorno de dados da Interface.
    def retorna_comunicador_destino(self):
        filial_id = str(self.did_entry.get())

        tabela_comunicador = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
                              '7': '7', '8': '8', '9': '9', '10': 'A', '11': 'B', '12': 'C',
                              '13': 'D', '14': 'E', '15': 'F',
                              '16': 'G', '17': 'H', '18': 'I', '19': 'J', '20': 'K', '21': 'L',
                              '22': 'M', '23': 'N', '24': 'O', '25': 'P', '26': 'Q', '27': 'R',
                              '28': 'S', '29': 'T', '30': 'U', '31': 'V', '32': 'W', '33': 'X',
                              '34': 'Y', '35': 'Z', '36': '@', '37': '#', '38': '$', '39': '&',
                              '40': '+', '41': '-', '42': '!', '43': '(', '44': ')', '45': '=',
                              '46': '{', '47': '}', '48': '[', '49': ']', '50': '<', '51': '>',
                              '52': ';', '53': ':', '54': 'a', '55': 'b', '56': 'c', '57': 'd',
                              '58': 'e', '59': 'f', '60': 'g', '61': 'h', '62': 'i', '63': 'j',
                              '64': 'k', '65': 'l', '66': 'm', '67': 'n', '68': 'o', '69': 'p',
                              '70': 'q', '71': 'r', '72': 's', '73': 't', '74': 'u', '75': 'v',
                              '76': 'w', '77': 'x', '78': 'y', '79': 'z'}

        comunicador = tabela_comunicador.get(filial_id, 'not found')
        if comunicador == 'not found':
            print("caracter de comunicação não encontrado")

        return comunicador

    def retorna_filial_id_origem(self):
        filial_id_origem = self.oid_entry.get()

        return filial_id_origem

    def retorna_filial_id_destino(self):
        filial_id_destino = self.did_entry.get()

        return filial_id_destino

    # Métodos de troca automática de estado dos botões.
    def troca_opcao_fabricante(self):

        if self.selfabricante_cnpj_cbutton.get():
            self.fabricante_id_cbutton.configure(state=tk.DISABLED)
            self.id_fabricante_entry.configure(state=tk.DISABLED)
        else:
            self.fabricante_id_cbutton.configure(state=tk.NORMAL)
            self.id_fabricante_entry.configure(state=tk.NORMAL)

        if self.selfabricante_id_cbutton.get():
            self.fabricante_cnpj_cbutton.configure(state=tk.DISABLED)
        else:
            self.fabricante_cnpj_cbutton.configure(state=tk.NORMAL)

    def troca_opcao_principio(self):

        if self.selprincipio_desc_cbutton.get():
            self.principio_id_cbutton.configure(state=tk.DISABLED)
            self.id_principio_entry.configure(state=tk.DISABLED)
        else:
            self.principio_id_cbutton.configure(state=tk.NORMAL)
            self.id_principio_entry.configure(state=tk.NORMAL)

        if self.selprincipio_id_cbutton.get():
            self.principio_desc_cbutton.configure(state=tk.DISABLED)
        else:
            self.principio_desc_cbutton.configure(state=tk.NORMAL)

    def troca_opcao_produto(self):

        if self.selprodutos_cbutton.get():
            self.barras_cbutton.configure(state=tk.NORMAL)
            self.estoque_cbutton.configure(state=tk.NORMAL)
            self.lotes_cbutton.configure(state=tk.NORMAL)
            self.preco_filial_cbutton.configure(state=tk.NORMAL)

        else:
            self.barras_cbutton.configure(state=tk.DISABLED)
            self.estoque_cbutton.configure(state=tk.DISABLED)
            self.lotes_cbutton.configure(state=tk.DISABLED)
            self.preco_filial_cbutton.configure(state=tk.DISABLED)

    # Método de incremento da barra de progresso
    def barra_progresso(self):
        self.progressbar['value'] += 5
        self.update_idletasks()

    # Método de execução
    def iniciar(self):
        comunicador = self.retorna_comunicador_destino()
        filial_id_origem = int(self.retorna_filial_id_origem())
        filial_id_destino = self.retorna_filial_id_destino()
        id_fabricante = self.id_fabricante_entry.get()
        id_principio = self.id_principio_entry.get()
        zeros_barras = int(self.zeros_spinbox.get())

        marcador_atualizacao_produto = {'fabricante_por_cnpj': 'nao',
                                        'fabricante_por_id': 'nao',
                                        'principio_por_desc': 'nao',
                                        'principio_por_id': 'nao',
                                        'classe_terapeutica_por_desc': 'nao',
                                        'classe_terapeutica_por_padrao': 'nao',
                                        'remover_produtos_barras_zerados': 'nao',
                                        'quantidade_zeros_barras': zeros_barras}

        marcador_apagado = {'apagado': 'nao'}

        if self.seldesconsiderar_apagados_cbutton.get():
            marcador_apagado.update({'apagado': 'sim'})

        if self.selfabricante_cnpj_cbutton.get():
            self.log(metodo='Processamento de Fabricantes Iniciado.')
            fabricante = Fabricante(dados_origem=self.dados_origem,
                                    dados_destino=self.dados_destino,
                                    comunicador=comunicador)
            fabricantes_log = fabricante.inicia_fabricantes(marcador_apagado)
            self.fabricantes_encontrados_tratados = fabricante.retorna_fabricantes_tratados()
            if fabricantes_log:
                for fabricante in fabricantes_log:
                    self.log(registro_erro=fabricante['registro_erro'], retorno_erro=fabricante['retorno_erro'])
            self.log(metodo='Processamento de Fabricantes Finalizado.')
        self.barra_progresso()

        if self.selprincipio_desc_cbutton.get():
            self.log(metodo='Processamento de Principios Ativos Iniciado.')
            principio_ativo = PrincipioAtivo(dados_origem=self.dados_origem,
                                             dados_destino=self.dados_destino,
                                             comunicador=comunicador)
            principio_ativo_log = principio_ativo.inicia_principios_ativos(marcador_apagado)
            self.principios_encontrados_tratados = principio_ativo.retorna_principios_tratados()
            if principio_ativo_log:
                for principio in principio_ativo_log:
                    self.log(registro_erro=principio['registro_erro'], retorno_erro=principio['retorno_erro'])
            self.log(metodo='Processamento de Principios Ativos Finalizado.')
        self.barra_progresso()

        if self.selprodutos_cbutton.get():
            grupos_selecionados = self.checa_grupos_origem()
            self.log(metodo='Processamento de Produtos Iniciado.')
            produto = Produto(dados_origem=self.dados_origem,
                              dados_destino=self.dados_destino,
                              comunicador=comunicador,
                              fabricantes_encontrados_tratados=self.fabricantes_encontrados_tratados,
                              principios_encontrados_tratados=self.principios_encontrados_tratados,
                              id_fabricante=id_fabricante,
                              id_principio=id_principio,
                              grupos_selecionados=grupos_selecionados)

            if self.seldesconsiderar_prod_cbutton.get():
                marcador_atualizacao_produto.update({'remover_produtos_barras_zerados': 'sim'})

            if self.selfabricante_cnpj_cbutton.get():
                marcador_atualizacao_produto.update({'fabricante_por_cnpj': 'sim'})

            if self.selfabricante_id_cbutton.get():
                marcador_atualizacao_produto.update({'fabricante_por_id': 'sim'})

            if self.selprincipio_desc_cbutton.get():
                marcador_atualizacao_produto.update({'principio_por_desc': 'sim'})

            if self.selprincipio_id_cbutton.get():
                marcador_atualizacao_produto.update({'principio_por_id': 'sim'})

            produtos_log = produto.inicia_produtos(marcador_produto=marcador_atualizacao_produto,
                                                   apagado=marcador_apagado)
            self.produtos_ids_separados = produto.retorna_produtos_ids()
            if produtos_log:
                for produto in produtos_log:
                    self.log(registro_erro=produto['registro_erro'], retorno_erro=produto['retorno_erro'])
            self.log(metodo='Processamento de Produtos Finalizado.')
        self.barra_progresso()

        if self.selbarras_cbutton.get():
            self.log(metodo='Processamento de Barras Adicionais Iniciado.')
            barras = BarrasAdicional(dados_origem=self.dados_origem,
                                     dados_destino=self.dados_destino,
                                     comunicador=comunicador,
                                     produtos_ids=self.produtos_ids_separados)
            barras_log = barras.inicia_barras(marcador_apagado)
            if barras_log:
                for barras in barras_log:
                    self.log(registro_erro=barras['registro_erro'], retorno_erro=barras['retorno_erro'])
            self.log(metodo='Processamento de Barras Adicionais Finalizado.')
        self.barra_progresso()

        if self.selestoque_cbutton.get():
            self.log(metodo='Processamento de Estoque Mínimo Iniciado.')
            estoque_minimo = EstoqueMinimo(dados_origem=self.dados_origem,
                                           dados_destino=self.dados_destino,
                                           filial_id_origem=filial_id_origem,
                                           filial_id_destino=filial_id_destino,
                                           comunicador=comunicador,
                                           produtos_ids=self.produtos_ids_separados)
            estoque_minimo_log = estoque_minimo.inicia_estoque_minimo(marcador_apagado)
            if estoque_minimo_log:
                for estoque in estoque_minimo_log:
                    self.log(registro_erro=estoque['registro_erro'], retorno_erro=estoque['retorno_erro'])
            self.log(metodo='Processamento de Estoque Mínimo Finalizado.')
        self.barra_progresso()

        if self.sellotes_cbutton.get():
            self.log(metodo='Processamento de Lotes Iniciado.')
            lotes = Lote(dados_origem=self.dados_origem,
                         dados_destino=self.dados_destino,
                         filial_id_origem=filial_id_origem,
                         filial_id_destino=filial_id_destino,
                         comunicador=comunicador,
                         produtos_ids=self.produtos_ids_separados)
            lotes_log = lotes.inicia_lotes(marcador_apagado)
            if lotes_log:
                for lote in lotes_log:
                    self.log(registro_erro=lote['registro_erro'], retorno_erro=lote['retorno_erro'])
                self.log(metodo='Processamento de Lotes Finalizado.')
        self.barra_progresso()

        if self.selpreco_filial_cbutton.get():
            self.log(metodo='Processamento de Preço Filial Iniciado.')
            preco_filial = PrecoFilial(dados_origem=self.dados_origem,
                                       dados_destino=self.dados_destino,
                                       filial_id_origem=filial_id_origem,
                                       filial_id_destino=filial_id_destino,
                                       comunicador=comunicador,
                                       produtos_ids=self.produtos_ids_separados)
            preco_filial_log = preco_filial.inicia_precos_filial(marcador_apagado)
            if preco_filial_log:
                for preco in preco_filial_log:
                    self.log(registro_erro=preco['registro_erro'], retorno_erro=preco['retorno_erro'])
                self.log(metodo='Processamento de Preço Filial Finalizado.')
        self.barra_progresso()

        if self.selfornecedores_cbutton.get():
            self.fornecedores_selecionados = self.checa_fornecedores()

            self.log(metodo='Processamento de Fornecedores Iniciado.')
            fornecedor = Fornecedor(dados_origem=self.dados_origem,
                                    dados_destino=self.dados_destino,
                                    fornecedores_selecionados=self.fornecedores_selecionados,
                                    comunicador=comunicador)
            fornecedores_log = fornecedor.inicia_fornecedores(marcador_apagado)
            self.fornecedores_encontrados_tratados = fornecedor.retorna_fornecedores_tratados()
            self.fornecedores_pos_insert = fornecedor.retorna_fornecedores_pos_insert()
            if fornecedores_log:
                for fornecedor in fornecedores_log:
                    self.log(registro_erro=fornecedor['registro_erro'], retorno_erro=fornecedor['retorno_erro'])
            self.log(metodo='Processamento de Fornecedores Finalizado.')
        self.barra_progresso()

        if self.selpagar_cbutton.get():
            self.log(metodo='Processamento de Pagar Iniciado.')
            pagar = Pagar(dados_origem=self.dados_origem,
                          dados_destino=self.dados_destino,
                          filial_id_destino=filial_id_destino,
                          fornecedores_encontrados=self.fornecedores_encontrados_tratados,
                          fornecedores_selecionados=self.fornecedores_selecionados,
                          fornecedores_pos_insert=self.fornecedores_pos_insert,
                          comunicador=comunicador)
            pagar_log = pagar.inicia_pagar(marcador_apagado)
            if pagar_log:
                for pagar in pagar_log:
                    self.log(registro_erro=pagar['registro_erro'], retorno_erro=pagar['retorno_erro'])
            self.log(metodo='Processamento de Pagar Finalizado.')
        self.barra_progresso()

        if self.selempresas_cbutton.get():
            self.empresas_selecionadas = self.checa_empresas()
            self.log(metodo='Processamento de Empresas Iniciado.')
            empresa = Empresa(dados_origem=self.dados_origem,
                              dados_destino=self.dados_destino,
                              empresas_selecionadas=self.empresas_selecionadas,
                              comunicador=comunicador)
            empresas_log = empresa.inicia_empresas(marcador_apagado)
            if empresas_log:
                for empresa in empresas_log:
                    self.log(registro_erro=empresa['registro_erro'], retorno_erro=empresa['retorno_erro'])
            self.log(metodo='Processamento de Empresas Finalizado.')

            self.log(metodo='Processamento de Clientes Iniciado.')
            cliente = Cliente(dados_origem=self.dados_origem,
                              dados_destino=self.dados_destino,
                              empresas_selecionadas=self.empresas_selecionadas,
                              comunicador=comunicador)
            clientes_log = cliente.inicia_clientes(marcador_apagado)
            self.clientes_selecionados = cliente.retorna_clientes_ids()
            if clientes_log:
                for cliente in clientes_log:
                    self.log(registro_erro=cliente['registro_erro'], retorno_erro=cliente['retorno_erro'])
            self.log(metodo='Processamento de Clientes Finalizado.')

        if self.selreceber_cbutton.get():
            self.log(metodo='Processamento do Receber Iniciado.')
            receber = Receber(dados_origem=self.dados_origem,
                              dados_destino=self.dados_destino,
                              filial_id_destino=filial_id_destino,
                              empresas_selecionadas=self.empresas_selecionadas,
                              clientes_selecionados=self.clientes_selecionados,
                              comunicador=comunicador)
            receber_log = receber.inicia_receber(marcador_apagado)
            if receber_log:
                for receber in receber_log:
                    self.log(registro_erro=receber['registro_erro'], retorno_erro=receber['retorno_erro'])
            self.log(metodo='Processamento do Receber Finalizado.')
        self.barra_progresso()

        self.concluido_message = tk.Message(self.logs_frame, font=self.fonte_corpo)
        self.concluido_message.configure(text="Concluído", width=90, foreground='green', relief=tk.FLAT, borderwidth=1)
        self.concluido_message.place(anchor=tk.NW, x=750, y=398)

        self.progressbar['value'] = 100
        self.log(metodo='Integração concluída.')
        print("Integracao Concluida")


if __name__ == "__main__":
    app = Ui()
    app.mainloop()
