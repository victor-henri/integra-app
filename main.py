import tkinter as tk
from tkinter import *
import tkinter.font as font
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
from estoque import Estoque
from lote import Lote
from precofilial import PrecoFilial
from empresa import Empresa
from cliente import Cliente
from receber import Receber
from fornecedor import Fornecedor
from pagar import Pagar


root = Tk()
root.geometry("1175x525")
root.resizable(False, False)
root.title("IntegraApp")
theme = ttkb.Style()
theme.theme_use("integra_visual")
theme.configure('Treeviews', rowheight=23)


class Ui:

    def __init__(self, master):

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

        self.body_font = font.Font(family='Roboto', size=10)
        self.title_font = font.Font(family='Roboto', size=12)

        # Main Frame
        self.main_frame = ttkb.Frame(master)
        self.main_frame.configure(padding=10)
        self.main_frame.grid()
        self.tabs_notebook = ttkb.Notebook(self.main_frame)

        # CONNECTIONS
        self.connections_frame = ttkb.Frame(self.tabs_notebook)
        self.connections_frame.pack()
        self.connections_frame.grid_anchor(tk.CENTER)
        self.tabs_notebook.add(self.connections_frame, text="Conexões")

        # CONNECTIONS[Origin Database]
        self.origin_labelframe = ttkb.Labelframe(self.connections_frame)
        self.origin_labelframe.configure(labelanchor=tk.N, padding=20, text="Banco de Origem")
        self.origin_labelframe.grid(column=0, padx=50, row=0)
        self.origin_labelframe.columnconfigure(8, weight=1)

        self.ip_origin_label = ttkb.Label(self.origin_labelframe)
        self.ip_origin_label.configure(text="Ip do Servidor", font=self.body_font)
        self.ip_origin_label.grid(column=0, row=0)

        self.ip_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.ip_origin_entry.configure(justify=tk.CENTER)
        self.ip_origin_entry.grid(column=0, row=1)

        self.db_origin_label = ttkb.Label(self.origin_labelframe)
        self.db_origin_label.configure(text="Nome do Banco", font=self.body_font)
        self.db_origin_label.grid(column=0, row=2)

        self.db_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.db_origin_entry.configure(justify=tk.CENTER)
        self.db_origin_entry.grid(column=0, row=3)

        self.user_origin_label = ttkb.Label(self.origin_labelframe)
        self.user_origin_label.configure(text="Usuário", font=self.body_font)
        self.user_origin_label.grid(column=0, row=4)

        self.user_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.user_origin_entry.configure(justify=tk.CENTER)
        self.user_origin_entry.grid(column=0, row=5)

        self.pass_origin_label = ttkb.Label(self.origin_labelframe)
        self.pass_origin_label.configure(text="Senha", font=self.body_font)
        self.pass_origin_label.grid(column=0, row=6)

        self.pass_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.pass_origin_entry.configure(justify=tk.CENTER, show='*')
        self.pass_origin_entry.grid(column=0, row=7)

        self.port_origin_label = ttkb.Label(self.origin_labelframe)
        self.port_origin_label.configure(text="Porta", font=self.body_font)
        self.port_origin_label.grid(column=0, padx=20, row=8, sticky=tk.W)

        self.port_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.port_origin_entry.configure(justify=tk.CENTER, width=8)
        self.port_origin_entry.grid(column=0, row=9, sticky=tk.W)

        self.id_origin_label = ttkb.Label(self.origin_labelframe)
        self.id_origin_label.configure(text="ID Filial", font=self.body_font)
        self.id_origin_label.grid(column=0, row=8, sticky=tk.E, ipadx=6)

        self.id_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.id_origin_entry.configure(justify=tk.CENTER, width=8)
        self.id_origin_entry.grid(column=0, row=9, sticky=tk.E)

        self.conn_origin_button = ttkb.Button(self.origin_labelframe, command=self.conexao_origem)
        self.conn_origin_button.configure(text="Conectar", width=15)
        self.conn_origin_button.grid(column=0, pady=10, row=11)

        self.alert_origin_button = ttkb.Button()
        self.origin_message = tk.Message(self.origin_labelframe)
        self.origin_message.configure(font=self.body_font, text="Desconectado", width=100, foreground='red')
        self.origin_message.grid(column=0, row=12)

        # CONNECTIONS[Destiny Database]
        self.destiny_labelframe = ttkb.Labelframe(self.connections_frame)
        self.destiny_labelframe.configure(labelanchor=tk.N, padding=20, text="Banco de Destino")
        self.destiny_labelframe.grid(column=2, padx=50, row=0)
        self.destiny_labelframe.columnconfigure(8, weight=1)

        self.ip_destiny_label = ttkb.Label(self.destiny_labelframe)
        self.ip_destiny_label.configure(text="Ip do Servidor", font=self.body_font)
        self.ip_destiny_label.grid(column=0, row=0)

        self.ip_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.ip_destiny_entry.configure(justify=tk.CENTER)
        self.ip_destiny_entry.grid(column=0, row=1)

        self.db_destiny_label = ttkb.Label(self.destiny_labelframe)
        self.db_destiny_label.configure(text="Nome do Banco", font=self.body_font)
        self.db_destiny_label.grid(column=0, row=2)

        self.db_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.db_destiny_entry.configure(justify=tk.CENTER)
        self.db_destiny_entry.grid(column=0, row=3)

        self.user_destiny_label = ttkb.Label(self.destiny_labelframe)
        self.user_destiny_label.configure(text="Usuário", font=self.body_font)
        self.user_destiny_label.grid(column=0, row=4)

        self.user_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.user_destiny_entry.configure(justify=tk.CENTER)
        self.user_destiny_entry.grid(column=0, row=5)

        self.pass_destiny_label = ttkb.Label(self.destiny_labelframe)
        self.pass_destiny_label.configure(text="Senha", font=self.body_font)
        self.pass_destiny_label.grid(column=0, row=6)

        self.pass_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.pass_destiny_entry.configure(justify=tk.CENTER, show='*')
        self.pass_destiny_entry.grid(column=0, row=7)

        self.port_destiny_label = ttkb.Label(self.destiny_labelframe)
        self.port_destiny_label.configure(text="Porta", font=self.body_font)
        self.port_destiny_label.grid(column=0, padx=20, row=8, sticky=tk.W)

        self.port_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.port_destiny_entry.configure(justify=tk.CENTER, width=8)
        self.port_destiny_entry.grid(column=0, row=9, sticky=tk.W)

        self.id_destiny_label = ttkb.Label(self.destiny_labelframe)
        self.id_destiny_label.configure(text="ID Filial", font=self.body_font)
        self.id_destiny_label.grid(column=0, row=8, sticky=tk.E, ipadx=6)

        self.id_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.id_destiny_entry.configure(justify=tk.CENTER, width=8)
        self.id_destiny_entry.grid(column=0, row=9, sticky=tk.E)

        self.conn_destiny_button = ttkb.Button(self.destiny_labelframe, command=self.conexao_destino)
        self.conn_destiny_button.configure(text="Conectar", width=15)
        self.conn_destiny_button.grid(column=0, pady=10, row=11)

        self.alert_destiny_button = ttkb.Button()
        self.destiny_message = tk.Message(self.destiny_labelframe)
        self.destiny_message.configure(font=self.body_font, text="Desconectado", width=100, foreground='red')
        self.destiny_message.grid(column=0, row=12)

        # CONNECTIONS[Separator]
        self.database_separator = ttkb.Separator(self.connections_frame)
        self.database_separator.configure(orient=tk.HORIZONTAL)
        self.database_separator.place(anchor=tk.CENTER, height=350, x=465, y=230)

        # SETTINGS
        self.settings_frame = ttkb.Frame(self.tabs_notebook)
        self.settings_frame.configure(padding=15)
        self.settings_frame.pack()

        self.tabs_notebook.add(self.settings_frame, text="Configurações Gerais")

        self.settings_labelframe = ttkb.Labelframe(self.settings_frame)
        self.settings_labelframe.configure(labelanchor=tk.N, padding=20, text="Opções")
        self.settings_labelframe.pack(expand=True, fill=tk.BOTH)
        self.settings_labelframe.columnconfigure(0, weight=1)
        self.settings_labelframe.columnconfigure(1, weight=1)
        self.settings_labelframe.columnconfigure(2, weight=1)
        self.settings_labelframe.columnconfigure(3, weight=1)
        self.settings_labelframe.columnconfigure(4, weight=1)

        # SETTINGS[Top Options]
        self.sel_product = tk.BooleanVar()
        self.sel_product.set(False)
        self.product_checkbutton = ttkb.Checkbutton(self.settings_labelframe, command=self.troca_opcao_produto)
        self.product_checkbutton.configure(text="Produto", variable=self.sel_product)
        self.product_checkbutton.grid(column=0, row=0)

        self.sel_bars = tk.BooleanVar()
        self.sel_bars.set(False)
        self.bars_checkbutton = ttkb.Checkbutton(self.settings_labelframe)
        self.bars_checkbutton.configure(text="Barras Adicional", state=tk.DISABLED, variable=self.sel_bars)
        self.bars_checkbutton.grid(column=1, row=0)

        self.sel_stock = tk.BooleanVar()
        self.sel_stock.set(False)
        self.stock_checkbutton = ttkb.Checkbutton(self.settings_labelframe)
        self.stock_checkbutton.configure(text="Estoque", state=tk.DISABLED, variable=self.sel_stock)
        self.stock_checkbutton.grid(column=2, row=0)

        self.sel_partition = tk.BooleanVar()
        self.sel_partition.set(False)
        self.partition_checkbutton = ttkb.Checkbutton(self.settings_labelframe)
        self.partition_checkbutton.configure(text="Lote", state=tk.DISABLED, variable=self.sel_partition)
        self.partition_checkbutton.grid(column=3, row=0)

        self.sel_price = tk.BooleanVar()
        self.sel_price.set(False)
        self.price_checkbutton = ttkb.Checkbutton(self.settings_labelframe)
        self.price_checkbutton.configure(text="Preço Filial", state=tk.DISABLED, variable=self.sel_price)
        self.price_checkbutton.grid(column=4, row=0)

        # SETTINGS[Mid Options][Principle]
        self.left_settings_frame = ttkb.Frame(self.settings_labelframe)
        self.left_settings_frame.configure(padding=5)
        self.left_settings_frame.place(height=250, width=400, x=15, y=60)

        self.principle_labelframe = ttkb.Labelframe(self.left_settings_frame)
        self.principle_labelframe.configure(text="Principio Ativo", height=80, labelanchor=tk.N)
        self.principle_labelframe.pack(fill=tk.X)

        self.sel_principle_desc = tk.BooleanVar()
        self.sel_principle_desc.set(False)
        self.principle_desc_checkbutton = ttkb.Checkbutton(self.principle_labelframe,
                                                           command=self.troca_opcao_principio)
        self.principle_desc_checkbutton.configure(text="Por Descrição", variable=self.sel_principle_desc)
        self.principle_desc_checkbutton.place(x=25, y=22)

        self.sel_principle_id = tk.BooleanVar()
        self.sel_principle_id.set(False)
        self.principle_id_checkbutton = ttkb.Checkbutton(self.principle_labelframe, command=self.troca_opcao_principio)
        self.principle_id_checkbutton.configure(text="Por ID", variable=self.sel_principle_id)
        self.principle_id_checkbutton.place(x=160, y=22)

        self.principle_id_entry = ttkb.Entry(self.principle_labelframe)
        self.principle_id_entry.configure(justify=tk.CENTER, width=5)
        self.principle_id_entry.place(height=26, width=30, x=245, y=17)

        self.principle_id_label = ttkb.Label(self.principle_labelframe)
        self.principle_id_label.configure(text="Id de Destino")
        self.principle_id_label.place(x=280, y=20)

        # SETTINGS[Middle Options][Manufacturer]
        self.right_settings_frame = ttkb.Frame(self.settings_labelframe)
        self.right_settings_frame.configure(height=250, padding=5)
        self.right_settings_frame.place(height=250, width=400, x=450, y=60)

        self.manufacturer_labelframe = ttkb.Labelframe(self.right_settings_frame)
        self.manufacturer_labelframe.configure(text="Fabricante", height=80, labelanchor=tk.N)
        self.manufacturer_labelframe.pack(fill=tk.X)

        self.sel_manufacturer_cnpj = tk.BooleanVar()
        self.sel_manufacturer_cnpj.set(False)
        self.manufacturer_cnpj_checkbutton = ttkb.Checkbutton(self.manufacturer_labelframe,
                                                              command=self.troca_opcao_fabricante)
        self.manufacturer_cnpj_checkbutton.configure(text="Por CNPJ", variable=self.sel_manufacturer_cnpj)
        self.manufacturer_cnpj_checkbutton.place(x=25, y=22)

        self.sel_manufacturer_id = tk.BooleanVar()
        self.sel_manufacturer_id.set(False)
        self.manufacturer_id_checkbutton = ttkb.Checkbutton(self.manufacturer_labelframe,
                                                            command=self.troca_opcao_fabricante)
        self.manufacturer_id_checkbutton.configure(text="Por ID", variable=self.sel_manufacturer_id)
        self.manufacturer_id_checkbutton.place(x=145, y=22)

        self.manufacturer_id_entry = ttkb.Entry(self.manufacturer_labelframe)
        self.manufacturer_id_entry.configure(justify=tk.CENTER, width=5)
        self.manufacturer_id_entry.place(height=26, width=30, x=245, y=17)

        self.manufacturer_id_label = ttkb.Label(self.manufacturer_labelframe)
        self.manufacturer_id_label.configure(text="Id de Destino")
        self.manufacturer_id_label.place(x=280, y=20)

        # SETTINGS[Bottom Options]
        self.sel_productbar = tk.BooleanVar()
        self.sel_productbar.set(False)
        self.productbar_checkbutton = ttkb.Checkbutton(self.settings_labelframe)
        self.productbar_checkbutton.configure(text="Não importar produtos com barras que iniciam com ",
                                              variable=self.sel_productbar)
        self.productbar_checkbutton.place(x=10, y=325)

        self.sel_erased = tk.BooleanVar()
        self.sel_erased.set(False)
        self.erased_checkbutton = ttkb.Checkbutton(self.settings_labelframe)
        self.erased_checkbutton.configure(text="Não importar registros marcados como apagados.",
                                          variable=self.sel_erased)
        self.erased_checkbutton.place(x=10, y=350)

        self.zeros_label = ttkb.Label(self.settings_labelframe)
        self.zeros_label.configure(text="ou mais zero(s).")
        self.zeros_label.place(x=425, y=322)

        self.value_zeros_spinbox = tk.StringVar(value='1')
        self.zeros_spinbox = ttkb.Spinbox(self.settings_labelframe)
        self.zeros_spinbox.configure(from_=1, to=12, textvariable=self.value_zeros_spinbox)
        self.zeros_spinbox.place(width=50, x=370, y=317)

        # SETTINGS[Separators]
        self.top_separator = ttkb.Separator(self.settings_labelframe)
        self.top_separator.configure(orient=tk.HORIZONTAL)
        self.top_separator.place(anchor=tk.CENTER, width=850, x=430, y=40)

        self.bottom_separator = ttkb.Separator(self.settings_labelframe)
        self.bottom_separator.configure(orient=tk.HORIZONTAL)
        self.bottom_separator.place(anchor=tk.CENTER, width=850, x=430, y=310)

        # PRODUCT GROUPS
        self.product_groups_frame = ttkb.Frame(self.tabs_notebook)
        self.product_groups_frame.configure(padding=5)
        self.product_groups_frame.grid(column=0, row=0)

        self.tabs_notebook.add(self.product_groups_frame, text="Grupos de Produtos")

        self.groups_frame = ttkb.Frame(self.product_groups_frame)
        self.groups_frame.configure(padding=5)
        self.groups_frame.pack(expand=True, fill=tk.BOTH)

        # PRODUCT GROUPS[Origin Database]
        self.groups_origin_labelframe = ttkb.Labelframe(self.groups_frame)
        self.groups_origin_labelframe.configure(labelanchor=tk.N, text="Banco de Origem", borderwidth=0)
        self.groups_origin_labelframe.pack(expand=True, fill=tk.BOTH, padx=15, pady=15, side=tk.LEFT)
        self.groups_origin_labelframe.rowconfigure(0, weight=1)
        self.groups_origin_labelframe.columnconfigure(0, weight=1)

        self.groups_origin_checkboxtreeview = CheckboxTreeview(self.groups_origin_labelframe)
        self.groups_origin_checkboxtreeview.grid(column=0, row=0, padx=5, pady=5, sticky=tk.NSEW)
        self.groups_origin_checkboxtreeview['columns'] = ('Novo ID', 'ID', 'Nome')
        self.groups_origin_checkboxtreeview.column('#0', width=30, stretch=False)
        self.groups_origin_checkboxtreeview.column('Novo ID', anchor=tk.CENTER, width=70, stretch=False)
        self.groups_origin_checkboxtreeview.column('ID', anchor=tk.CENTER, width=30, stretch=False)
        self.groups_origin_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.groups_origin_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.groups_origin_checkboxtreeview.heading('Novo ID', text='Novo ID', anchor=tk.CENTER)
        self.groups_origin_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.groups_origin_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_erased_origin_groups = tk.BooleanVar()
        self.sel_erased_origin_groups.set(False)
        self.erased_groups_origin_checkbutton = ttkb.Checkbutton(self.groups_origin_labelframe,
                                                                 command=self.lista_grupo_origem)
        self.erased_groups_origin_checkbutton.configure(text="Não mostrar grupos apagados",
                                                        variable=self.sel_erased_origin_groups)
        self.erased_groups_origin_checkbutton.grid(column=0, row=1, sticky=tk.W)

        self.sel_all_origin_groups = tk.BooleanVar()
        self.sel_all_origin_groups.set(False)
        self.all_origin_groups_checkbutton = ttkb.Checkbutton(self.groups_origin_labelframe,
                                                              command=self.marca_grupos_origem)
        self.all_origin_groups_checkbutton.configure(text="Selecionar todos",
                                                     variable=self.sel_all_origin_groups)
        self.all_origin_groups_checkbutton.grid(column=0, row=1, sticky=tk.E)

        # PRODUCT GROUPS[Destiny Database]
        self.groups_destiny_labelframe = ttkb.Labelframe(self.groups_frame)
        self.groups_destiny_labelframe.configure(labelanchor=tk.N, text="Banco de Destino", borderwidth=0)
        self.groups_destiny_labelframe.pack(expand=True, fill=tk.BOTH, padx=15, pady=15, side=tk.LEFT)
        self.groups_destiny_labelframe.rowconfigure(0, weight=1)
        self.groups_destiny_labelframe.columnconfigure(0, weight=1)

        self.groups_destiny_checkboxtreeview = CheckboxTreeview(self.groups_destiny_labelframe)
        self.groups_destiny_checkboxtreeview.grid(column=0, padx=5, pady=5, row=0, sticky=tk.NSEW)
        self.groups_destiny_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.groups_destiny_checkboxtreeview.column('#0', width=0, stretch=False)
        self.groups_destiny_checkboxtreeview.column('ID', anchor=tk.CENTER, width=50, stretch=False)
        self.groups_destiny_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.groups_destiny_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.groups_destiny_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.groups_destiny_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_erased_destiny_groups = tk.BooleanVar()
        self.sel_erased_destiny_groups.set(False)
        self.erased_groups_origin_checkbutton = ttkb.Checkbutton(self.groups_destiny_labelframe,
                                                                 command=self.lista_grupo_destino)
        self.erased_groups_origin_checkbutton.configure(text="Não mostrar grupos apagados",
                                                        variable=self.sel_erased_destiny_groups)
        self.erased_groups_origin_checkbutton.grid(column=0, row=1, sticky=tk.W)

        # SUPPLIER & BILLS TO PAY
        self.suppliers_frame = ttkb.Frame(self.tabs_notebook)
        self.suppliers_frame.configure(padding=15)
        self.suppliers_frame.pack(side=tk.TOP)

        self.tabs_notebook.add(self.suppliers_frame, text="Fornecedores e Pagar")

        self.suppliers_options_labelframe = ttkb.Labelframe(self.suppliers_frame)
        self.suppliers_options_labelframe.configure(labelanchor=tk.N, padding=15, text="Opções")
        self.suppliers_options_labelframe.pack(anchor=tk.CENTER, fill=tk.X, side=tk.TOP)
        self.suppliers_options_labelframe.columnconfigure(tk.ALL, weight=1)

        self.suppliers_checkboxtreeview = CheckboxTreeview(self.suppliers_frame)
        self.suppliers_checkboxtreeview.pack(expand=True, fill=tk.X, side=tk.BOTTOM, ipady=5)
        self.suppliers_checkboxtreeview.configure(height=15)
        self.suppliers_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.suppliers_checkboxtreeview.column('#0', width=40, stretch=False)
        self.suppliers_checkboxtreeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.suppliers_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.suppliers_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.suppliers_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.suppliers_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_suppliers = tk.BooleanVar()
        self.sel_suppliers.set(False)
        self.suppliers_checkbutton = ttkb.Checkbutton(self.suppliers_options_labelframe)
        self.suppliers_checkbutton.configure(text="Fornecedores", variable=self.sel_suppliers)
        self.suppliers_checkbutton.grid(column=0, row=0, padx=160)

        self.sel_bills = tk.BooleanVar()
        self.sel_bills.set(False)
        self.bills_checkbutton = ttkb.Checkbutton(self.suppliers_options_labelframe)
        self.bills_checkbutton.configure(text="Pagar", variable=self.sel_bills)
        self.bills_checkbutton.grid(column=1, row=0, padx=160)

        self.sel_all_suppliers = tk.BooleanVar()
        self.sel_all_suppliers.set(False)
        self.all_suppliers_checkbutton = ttkb.Checkbutton(self.suppliers_frame, command=self.marca_fornecedores)
        self.all_suppliers_checkbutton.configure(text="Selecionar todos", variable=self.sel_all_suppliers)
        self.all_suppliers_checkbutton.place(x=770, y=413)

        # COMPANIES/CUSTOMERS & ACCOUNTS RECEIVABLE
        self.companies_frame = ttkb.Frame(self.tabs_notebook)
        self.companies_frame.configure(padding=15)
        self.companies_frame.pack(side=tk.TOP)

        self.tabs_notebook.add(self.companies_frame, text="Empresas e Clientes")

        self.companies_options_labelframe = ttkb.Labelframe(self.companies_frame)
        self.companies_options_labelframe.configure(labelanchor=tk.N, padding=15, text="Opções")
        self.companies_options_labelframe.pack(anchor=tk.CENTER, fill=tk.X, side=tk.TOP)
        self.companies_options_labelframe.columnconfigure(tk.ALL, weight=1)

        self.companies_checkboxtreeview = CheckboxTreeview(self.companies_frame)
        self.companies_checkboxtreeview.pack(expand=1, fill=tk.X, side=tk.BOTTOM, ipady=5)
        self.companies_checkboxtreeview.configure(height=15)
        self.companies_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.companies_checkboxtreeview.column('#0', width=40, stretch=False)
        self.companies_checkboxtreeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.companies_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.companies_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.companies_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.companies_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_companies = tk.BooleanVar()
        self.sel_companies.set(False)
        self.companies_checkbutton = ttkb.Checkbutton(self.companies_options_labelframe)
        self.companies_checkbutton.configure(text="Empresas e Clientes", variable=self.sel_companies)
        self.companies_checkbutton.grid(column=0, row=0, padx=160)

        self.sel_accounts_receivable = tk.BooleanVar()
        self.sel_accounts_receivable.set(False)
        self.accounts_receivable_checkbutton = ttkb.Checkbutton(self.companies_options_labelframe)
        self.accounts_receivable_checkbutton.configure(text="Receber", variable=self.sel_accounts_receivable)
        self.accounts_receivable_checkbutton.grid(column=1, row=0, padx=130)

        self.sel_all_companies = tk.BooleanVar()
        self.sel_all_companies.set(False)
        self.all_companies_checkbutton = ttkb.Checkbutton(self.companies_frame, command=self.marca_empresas)
        self.all_companies_checkbutton.configure(text="Selecionar todos", variable=self.sel_all_companies)
        self.all_companies_checkbutton.place(x=770, y=413)

        # LOGS
        self.logs_frame = ttkb.Frame(self.tabs_notebook)
        self.logs_frame.configure(padding=15)
        self.logs_frame.pack(side=tk.TOP)

        self.tabs_notebook.add(self.logs_frame, text="Execução e Logs")

        self.tabs_notebook.configure(padding=5)
        self.tabs_notebook.grid(column=1, row=0)

        self.logs_scrolledtext = ScrolledText(self.logs_frame)
        self.logs_scrolledtext.configure(borderwidth=5, font=self.body_font)
        self.logs_scrolledtext.place(width=905, height=383, x=0, y=0)

        self.start_button = ttkb.Button(self.logs_frame, command=self.iniciar)
        self.start_button.configure(text="Iniciar", width=20)
        self.start_button.place(height=30, x=30, y=400)

        self.progressbar = ttkb.Progressbar(self.logs_frame, mode='determinate')
        self.progressbar.configure(length=600, orient=tk.HORIZONTAL)
        self.progressbar.place(width=500, x=250, y=410)

        # DOCUMENTATION
        self.documentation_frame = ttkb.Frame(self.tabs_notebook)
        self.documentation_frame.configure(padding=15)
        self.documentation_frame.pack(side=tk.TOP)

        self.tabs_notebook.add(self.documentation_frame, text="Documentação")
        self.tabs_notebook.configure(padding=5)

        self.documentation_scrolledtext = ScrolledText(self.documentation_frame)
        self.documentation_scrolledtext.configure(borderwidth=5, font=self.body_font)
        self.documentation_scrolledtext.insert(tk.END, documentacao.informacao_doc)
        self.documentation_scrolledtext.configure(state=tk.DISABLED)
        self.documentation_scrolledtext.pack(fill=tk.BOTH)

        # LOGO BANNER
        self.logo_frame = ttkb.Frame(self.main_frame)
        self.logo_frame.configure(height=400, width=400)
        self.logo_frame.grid(column=0, row=0)

        self.logo_image = ImageTk.PhotoImage(Image.open('imgs/integrabanner.png'))

        self.logo_image_label = ttkb.Label(self.logo_frame, image=self.logo_image)
        self.logo_image_label.pack()

        # BINDS
        self.groups_origin_checkboxtreeview.bind("<Double-1>", self.double_click)

    # Métodos de Binds.
    @staticmethod
    def focus_out(event):
        event.widget.destroy()

    def double_click(self, event):

        regiao_clique = self.groups_origin_checkboxtreeview.identify_region(event.x, event.y)

        if regiao_clique not in ("tree", "cell"):
            return

        coluna = self.groups_origin_checkboxtreeview.identify_column(event.x)
        index_coluna = int(coluna[1:]) - 1
        iid_selecionado = self.groups_origin_checkboxtreeview.focus()
        valores_selecionados = self.groups_origin_checkboxtreeview.item(iid_selecionado)

        linha_selecionada = None
        if coluna != '#1':
            print("Coluna inválida")
        else:
            linha_selecionada = valores_selecionados.get('values')[index_coluna]
            print(linha_selecionada)

        caixa_coluna = self.groups_origin_checkboxtreeview.bbox(iid_selecionado, coluna)
        editavel_entry = ttk.Entry(self.groups_origin_checkboxtreeview)
        editavel_entry.identificador_coluna = index_coluna
        editavel_entry.identificador_item_iid = iid_selecionado
        editavel_entry.insert(0, linha_selecionada)
        editavel_entry.select_range(0, tk.END)

        editavel_entry.focus()
        editavel_entry.bind("<FocusOut>", self.focus_out)
        editavel_entry.bind("<Return>", self.press_enter)

        editavel_entry.place(x=caixa_coluna[0],
                             y=caixa_coluna[1],
                             w=caixa_coluna[2],
                             h=caixa_coluna[3])

    def press_enter(self, event):

        new_text = event.widget.get()
        iid_selecionado = event.widget.identificador_item_iid
        index_coluna = event.widget.identificador_coluna

        if index_coluna == 0:
            valor_atual = self.groups_origin_checkboxtreeview.item(iid_selecionado).get('values')
            valor_atual[index_coluna] = new_text
            self.groups_origin_checkboxtreeview.item(iid_selecionado, values=valor_atual)
        event.widget.destroy()

    # Métodos de conexão.
    def conexao_origem(self):

        self.dados_origem = {'host': self.ip_origin_entry.get(),
                             'user': self.user_origin_entry.get(),
                             'password': self.pass_origin_entry.get(),
                             'database': self.db_origin_entry.get(),
                             'port': int(self.port_origin_entry.get())}

        iterador = IteradorSql()
        retorno_origem = iterador.conexao_origem(dados_origem=self.dados_origem)

        if retorno_origem['retorno'] == 'Conectado':
            self.alert_origin_button.destroy()
            self.origin_message.configure(text="Conectado", foreground='green')
            self.lista_grupo_origem()
            self.lista_empresas()
            self.lista_fornecedores()

        elif retorno_origem['retorno'] == 'pymysql.err.OperationalError':
            self.alert_origin_button.destroy()
            self.origin_message.configure(text="Falha", foreground='orange')
            self.coderro = retorno_origem['codigo']
            self.descerro = retorno_origem['descricao']
            self.obotao_alerta(self.coderro, self.descerro)
            self.alert_origin_button.place(anchor="w", height=22, width=22, x=30, y=323)

        else:
            self.alert_origin_button.destroy()
            self.origin_message.configure(text="Falha", foreground='orange')
            self.coderro = 20
            self.descerro = retorno_origem['descricao']
            self.obotao_alerta(self.coderro, self.descerro)
            self.alert_origin_button.place(anchor="w", height=22, width=22, x=30, y=323)

    def conexao_destino(self):

        self.dados_destino = {'host': self.ip_destiny_entry.get(),
                              'user': self.user_destiny_entry.get(),
                              'password': self.pass_destiny_entry.get(),
                              'database': self.db_destiny_entry.get(),
                              'port': int(self.port_destiny_entry.get())}

        iterador = IteradorSql()
        retorno_destino = iterador.conexao_destino(dados_destino=self.dados_destino)

        if retorno_destino['retorno'] == 'Conectado':
            self.alert_destiny_button.destroy()
            self.destiny_message.configure(text="Conectado", foreground='green')
            self.lista_grupo_destino()

        elif retorno_destino['retorno'] == 'pymysql.err.OperationalError':
            self.alert_destiny_button.destroy()
            self.destiny_message.configure(text="Falha", foreground='orange')
            self.coderro = retorno_destino['codigo']
            self.descerro = retorno_destino['descricao']
            self.dbotao_alerta(self.coderro, self.descerro)
            self.alert_destiny_button.place(anchor="w", height=22, width=22, x=30, y=323)

        else:
            self.alert_destiny_button.destroy()
            self.destiny_message.configure(text="Falha", foreground='orange')
            self.coderro = 20
            self.descerro = retorno_destino['descricao']
            self.dbotao_alerta(self.coderro, self.descerro)
            self.alert_destiny_button.place(anchor="w", height=22, width=22, x=30, y=323)

    def obotao_alerta(self, coderro, descerro):

        self.oalerta_img = tk.PhotoImage(file="imgs/info.png")
        self.alert_origin_button = ttk.Button(
            self.origin_labelframe,
            image=self.oalerta_img,
            command=lambda: self.retorna_erro(coderro, descerro),
            bootstyle=ttkb.WARNING)
        self.alert_origin_button.configure(compound="left", padding=1)

    def dbotao_alerta(self, coderro, descerro):

        self.dalerta_img = tk.PhotoImage(file="imgs/info.png")
        self.alert_destiny_button = ttk.Button(
            self.destiny_labelframe,
            image=self.dalerta_img,
            command=lambda: self.retorna_erro(coderro, descerro),
            bootstyle="warning")
        self.alert_destiny_button.configure(compound="left", padding=1)

    def retorna_erro(self, coderro, descerro):

        erro = f"Código: {coderro} | Descrição: {descerro}"
        self.popup_top = tk.Toplevel()
        self.popup_top.title("Retorno do Erro")
        # self.grid_anchor("center")
        # self.theme.theme_use('integra_visual')
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
            self.logs_scrolledtext.insert(tk.INSERT, f"{separador}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{ident}{metodo}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{separador}\n")
            logging.warning(separador)
            logging.warning(f"{ident}{metodo}")
            logging.warning(separador)

        if registro_erro or retorno_erro:
            self.logs_scrolledtext.insert(tk.INSERT, f"{separador}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{ident}{registro_erro}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{ident}{retorno_erro}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{separador}\n")
            logging.warning(separador)
            logging.warning(f"{ident} {registro_erro}")
            logging.warning(f"{ident} {retorno_erro}")
            logging.warning(separador)

    # Métodos de listagem automática e exibição dos dados ao conectar.
    def lista_grupo_origem(self):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)

        try:
            if self.sel_erased_origin_groups.get():
                grupos = iterador.select_grupo_origem_sapagado()
                index = 0
                self.iid_lista_grupo_origem = []

                for grupo in grupos:
                    self.groups_origin_checkboxtreeview.insert(
                        "", index=tk.END, iid=index, text='', values=('', grupo['id_grupo'], grupo['descricao']))
                    self.iid_lista_grupo_origem.append(index)
                    index += 1

            else:
                grupos = iterador.select_grupo_origem_capagado()
                index = 0
                self.iid_lista_grupo_origem = []

                for grupo in grupos:
                    self.groups_origin_checkboxtreeview.insert(
                        "", index=tk.END, iid=index, text='', values=('', grupo['id_grupo'], grupo['descricao']))
                    self.iid_lista_grupo_origem.append(index)
                    index += 1

        except Exception as err_lista_grupo_origem:
            print(f"Exceção no método lista_grupo_origem: {err_lista_grupo_origem}")

    def lista_grupo_destino(self):

        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)

        try:
            if self.sel_erased_destiny_groups.get():
                grupos = iterador.select_grupo_destino_sapagado()
                index = 0
                iid_lista_grupos_destino = []

                for grupo in grupos:
                    self.groups_destiny_checkboxtreeview.insert(
                        "", index=tk.END, iid=index, text='', values=(grupo['id_grupo'], grupo['descricao']))
                    iid_lista_grupos_destino.append(index)
                    index += 1

            else:
                grupos = iterador.select_grupo_destino_capagado()
                index = 0
                iid_lista_grupos_destino = []

                for grupo in grupos:
                    self.groups_destiny_checkboxtreeview.insert(
                        "", index=tk.END, iid=index, text='', values=(grupo['id_grupo'], grupo['descricao']))
                    iid_lista_grupos_destino.append(index)
                    index += 1

        except Exception as err_lista_grupo_destino:
            print(f"Exceção no método lista_grupo_destino: {err_lista_grupo_destino}")

    def lista_empresas(self):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)

        try:
            empresas = iterador.select_listagem_empresa()
            index = 0
            self.iid_lista_empresas = []

            for empresa in empresas:
                self.companies_checkboxtreeview.insert(
                    "", index='end', iid=index, text='', values=(empresa['id_empresa'], empresa['nome_fantasia']))
                self.iid_lista_empresas.append(index)
                index += 1

        except Exception as err_lista_empresas:
            print(f"Exceção no método lista_empresas: {err_lista_empresas}")

    def lista_fornecedores(self):

        iterador = IteradorSql()
        iterador.conexao_origem(self.dados_origem)

        try:
            fornecedores = iterador.select_listagem_fornecedor()
            index = 0
            self.iid_lista_fornecedores = []

            for fornecedor in fornecedores:
                self.suppliers_checkboxtreeview.insert("",
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
            self.companies_checkboxtreeview.change_state(item=iid, state='checked')

    def marca_fornecedores(self):

        for iid in self.iid_lista_fornecedores:
            self.suppliers_checkboxtreeview.change_state(item=iid, state='checked')

    def marca_grupos_origem(self):

        for iid in self.iid_lista_grupo_origem:
            self.groups_origin_checkboxtreeview.change_state(item=iid, state='checked')

    # Métodos de coleta dos registros selecionados na Interface.
    def checa_empresas(self):

        empresas_selecionadas_l = []

        for empresa in self.companies_checkboxtreeview.get_checked():
            id_empresa = self.companies_checkboxtreeview.item(item=empresa, option='values')
            empresas_selecionadas_l.append(id_empresa[0])
        empresas_selecionadas = tuple(empresas_selecionadas_l)

        return empresas_selecionadas

    def checa_fornecedores(self):

        fornecedores_selecionadas_l = []

        for fornecedor in self.suppliers_checkboxtreeview.get_checked():
            id_fornecedor = self.suppliers_checkboxtreeview.item(item=fornecedor, option='values')
            fornecedores_selecionadas_l.append(id_fornecedor[0])
        fornecedores_selecionados = tuple(fornecedores_selecionadas_l)

        return fornecedores_selecionados

    def checa_grupos_origem(self):

        grupos_selecionados = []

        for grupo in self.groups_origin_checkboxtreeview.get_checked():
            valores = self.groups_origin_checkboxtreeview.item(item=grupo, option='values')
            grupo_selecionado = {'novo_id': int(valores[0]), 'antigo_id': int(valores[1])}
            grupos_selecionados.append(grupo_selecionado)

        return grupos_selecionados

    # Métodos de retorno de dados da Interface.
    def retorna_comunicador_destino(self):

        filial_id = str(self.id_destiny_entry.get())
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

        filial_id_origem = self.id_origin_entry.get()

        return filial_id_origem

    def retorna_filial_id_destino(self):

        filial_id_destino = self.id_destiny_entry.get()

        return filial_id_destino

    # Métodos de troca automática de estado dos botões.
    def troca_opcao_fabricante(self):

        if self.sel_manufacturer_cnpj.get():
            self.manufacturer_id_checkbutton.configure(state=tk.DISABLED)
            self.manufacturer_id_entry.configure(state=tk.DISABLED)
        else:
            self.manufacturer_id_checkbutton.configure(state=tk.NORMAL)
            self.manufacturer_id_entry.configure(state=tk.NORMAL)

        if self.sel_manufacturer_id.get():
            self.manufacturer_cnpj_checkbutton.configure(state=tk.DISABLED)
        else:
            self.manufacturer_cnpj_checkbutton.configure(state=tk.NORMAL)

    def troca_opcao_principio(self):

        if self.sel_principle_desc.get():
            self.principle_id_checkbutton.configure(state=tk.DISABLED)
            self.principle_id_entry.configure(state=tk.DISABLED)
        else:
            self.principle_id_checkbutton.configure(state=tk.NORMAL)
            self.principle_id_entry.configure(state=tk.NORMAL)

        if self.sel_principle_id.get():
            self.principle_desc_checkbutton.configure(state=tk.DISABLED)
        else:
            self.principle_desc_checkbutton.configure(state=tk.NORMAL)

    def troca_opcao_produto(self):

        if self.sel_product.get():
            self.bars_checkbutton.configure(state=tk.NORMAL)
            self.stock_checkbutton.configure(state=tk.NORMAL)
            self.partition_checkbutton.configure(state=tk.NORMAL)
            self.price_checkbutton.configure(state=tk.NORMAL)

        else:
            self.bars_checkbutton.configure(state=tk.DISABLED)
            self.stock_checkbutton.configure(state=tk.DISABLED)
            self.partition_checkbutton.configure(state=tk.DISABLED)
            self.price_checkbutton.configure(state=tk.DISABLED)

    # Método de incremento da barra de progresso
    def barra_progresso(self):

        self.progressbar['value'] += 5
        # self.update_idletasks()

    # Método de execução
    def iniciar(self):

        comunicador = self.retorna_comunicador_destino()
        filial_id_origem = int(self.retorna_filial_id_origem())
        filial_id_destino = int(self.retorna_filial_id_destino())
        id_fabricante = self.manufacturer_id_entry.get()
        id_principio = self.principle_id_entry.get()
        zeros_barras = int(self.zeros_spinbox.get())

        marcador_atualizacao_produto = {'fabricante_por_cnpj': 'nao',
                                        'fabricante_por_id': 'nao',
                                        'principio_por_desc': 'nao',
                                        'principio_por_id': 'nao',
                                        'classe_terapeutica_por_desc': 'nao',
                                        'classe_terapeutica_por_padrao': 'nao',
                                        'remover_produtos_barras_zerados': 'nao',
                                        'quantidade_zeros_barras': zeros_barras}

        marcador_limpeza = {'fabricante': 'nao',
                            'principio_ativo': 'nao',
                            'produto': 'nao',
                            'barras': 'nao',
                            'estoque': 'nao',
                            'lote': 'nao',
                            'preco_filial': 'nao',
                            'fornecedor': 'nao',
                            'pagar': 'nao',
                            'empresa': 'nao',
                            'cliente': 'nao',
                            'receber': 'nao'}

        marcador_apagado = {'apagado': 'nao'}
        if self.sel_erased.get():
            marcador_apagado.update({'apagado': 'sim'})

        self.progressbar['value'] = 0
        self.concluido_message = tk.Message(self.logs_frame, font=self.body_font)
        self.concluido_message.configure(text="Em Andamento",
                                         width=125,
                                         foreground='orange',
                                         relief=tk.FLAT,
                                         borderwidth=1)
        self.concluido_message.place(anchor=tk.NW, x=750, y=398)
        self.log(metodo='Integração Iniciada.')

        if self.sel_manufacturer_cnpj.get():
            self.log(metodo='Processamento de Fabricantes Iniciado.')
            fabricante = Fabricante(dados_origem=self.dados_origem,
                                    dados_destino=self.dados_destino,
                                    comunicador=comunicador)
            fabricantes_log = fabricante.inicia_fabricantes(marcador_apagado)
            marcador_limpeza.update({'fabricante': 'sim'})
            self.fabricantes_encontrados_tratados = fabricante.retorna_fabricantes_tratados()
            if fabricantes_log:
                for fabricante in fabricantes_log:
                    self.log(registro_erro=fabricante['registro_erro'], retorno_erro=fabricante['retorno_erro'])
            self.log(metodo='Processamento de Fabricantes Finalizado.')
        self.barra_progresso()

        if self.sel_principle_desc.get():
            self.log(metodo='Processamento de Principios Ativos Iniciado.')
            principio_ativo = PrincipioAtivo(dados_origem=self.dados_origem,
                                             dados_destino=self.dados_destino,
                                             comunicador=comunicador)
            principio_ativo_log = principio_ativo.inicia_principios_ativos(marcador_apagado)
            marcador_limpeza.update({'principio_ativo': 'sim'})
            self.principios_encontrados_tratados = principio_ativo.retorna_principios_tratados()
            if principio_ativo_log:
                for principio in principio_ativo_log:
                    self.log(registro_erro=principio['registro_erro'], retorno_erro=principio['retorno_erro'])
            self.log(metodo='Processamento de Principios Ativos Finalizado.')
        self.barra_progresso()

        if self.sel_product.get():
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

            if self.sel_productbar.get():
                marcador_atualizacao_produto.update({'remover_produtos_barras_zerados': 'sim'})

            if self.sel_manufacturer_cnpj.get():
                marcador_atualizacao_produto.update({'fabricante_por_cnpj': 'sim'})

            if self.sel_manufacturer_id.get():
                marcador_atualizacao_produto.update({'fabricante_por_id': 'sim'})

            if self.sel_principle_desc.get():
                marcador_atualizacao_produto.update({'principio_por_desc': 'sim'})

            if self.sel_principle_id.get():
                marcador_atualizacao_produto.update({'principio_por_id': 'sim'})

            produtos_log = produto.inicia_produtos(marcador_produto=marcador_atualizacao_produto,
                                                   apagado=marcador_apagado)
            marcador_limpeza.update({'produto': 'sim'})
            self.produtos_ids_separados = produto.retorna_produtos_ids()
            if produtos_log:
                for produto in produtos_log:
                    self.log(registro_erro=produto['registro_erro'], retorno_erro=produto['retorno_erro'])
            self.log(metodo='Processamento de Produtos Finalizado.')
        self.barra_progresso()

        if self.sel_bars.get():
            self.log(metodo='Processamento de Barras Adicionais Iniciado.')
            barras = BarrasAdicional(dados_origem=self.dados_origem,
                                     dados_destino=self.dados_destino,
                                     comunicador=comunicador,
                                     produtos_ids=self.produtos_ids_separados)
            barras_log = barras.inicia_barras(marcador_apagado)
            marcador_limpeza.update({'barras': 'sim'})
            if barras_log:
                for barras in barras_log:
                    self.log(registro_erro=barras['registro_erro'], retorno_erro=barras['retorno_erro'])
            self.log(metodo='Processamento de Barras Adicionais Finalizado.')
        self.barra_progresso()

        if self.sel_stock.get():
            self.log(metodo='Processamento de Estoque Iniciado.')
            estoque = Estoque(dados_origem=self.dados_origem,
                              dados_destino=self.dados_destino,
                              filial_id_origem=filial_id_origem,
                              filial_id_destino=filial_id_destino,
                              comunicador=comunicador,
                              produtos_ids=self.produtos_ids_separados)
            estoque_log = estoque.inicia_estoque(marcador_apagado)
            marcador_limpeza.update({'estoque': 'sim'})
            if estoque_log:
                for registro in estoque_log:
                    self.log(registro_erro=registro['registro_erro'], retorno_erro=registro['retorno_erro'])
            self.log(metodo='Processamento de Estoque Finalizado.')
        self.barra_progresso()

        if self.sel_partition.get():
            self.log(metodo='Processamento de Lotes Iniciado.')
            lotes = Lote(dados_origem=self.dados_origem,
                         dados_destino=self.dados_destino,
                         filial_id_origem=filial_id_origem,
                         filial_id_destino=filial_id_destino,
                         comunicador=comunicador,
                         produtos_ids=self.produtos_ids_separados)
            lotes_log = lotes.inicia_lotes(marcador_apagado)
            marcador_limpeza.update({'lote': 'sim'})
            if lotes_log:
                for lote in lotes_log:
                    self.log(registro_erro=lote['registro_erro'], retorno_erro=lote['retorno_erro'])
                self.log(metodo='Processamento de Lotes Finalizado.')
        self.barra_progresso()

        if self.sel_price.get():
            self.log(metodo='Processamento de Preço Filial Iniciado.')
            preco_filial = PrecoFilial(dados_origem=self.dados_origem,
                                       dados_destino=self.dados_destino,
                                       filial_id_origem=filial_id_origem,
                                       filial_id_destino=filial_id_destino,
                                       comunicador=comunicador,
                                       produtos_ids=self.produtos_ids_separados)
            preco_filial_log = preco_filial.inicia_precos_filial(marcador_apagado)
            marcador_limpeza.update({'preco_filial': 'sim'})
            if preco_filial_log:
                for preco in preco_filial_log:
                    self.log(registro_erro=preco['registro_erro'], retorno_erro=preco['retorno_erro'])
                self.log(metodo='Processamento de Preço Filial Finalizado.')
        self.barra_progresso()

        if self.sel_suppliers.get():
            self.fornecedores_selecionados = self.checa_fornecedores()

            self.log(metodo='Processamento de Fornecedores Iniciado.')
            fornecedor = Fornecedor(dados_origem=self.dados_origem,
                                    dados_destino=self.dados_destino,
                                    fornecedores_selecionados=self.fornecedores_selecionados,
                                    comunicador=comunicador)
            fornecedores_log = fornecedor.inicia_fornecedores(marcador_apagado)
            marcador_limpeza.update({'fornecedor': 'sim'})
            self.fornecedores_encontrados_tratados = fornecedor.retorna_fornecedores_tratados()
            self.fornecedores_pos_insert = fornecedor.retorna_fornecedores_pos_insert()
            if fornecedores_log:
                for fornecedor in fornecedores_log:
                    self.log(registro_erro=fornecedor['registro_erro'], retorno_erro=fornecedor['retorno_erro'])
            self.log(metodo='Processamento de Fornecedores Finalizado.')
        self.barra_progresso()

        if self.sel_bills.get():
            self.log(metodo='Processamento de Pagar Iniciado.')
            pagar = Pagar(dados_origem=self.dados_origem,
                          dados_destino=self.dados_destino,
                          filial_id_origem=filial_id_origem,
                          filial_id_destino=filial_id_destino,
                          fornecedores_encontrados=self.fornecedores_encontrados_tratados,
                          fornecedores_selecionados=self.fornecedores_selecionados,
                          fornecedores_pos_insert=self.fornecedores_pos_insert,
                          comunicador=comunicador)
            pagar_log = pagar.inicia_pagar(marcador_apagado)
            marcador_limpeza.update({'pagar': 'sim'})
            if pagar_log:
                for pagar in pagar_log:
                    self.log(registro_erro=pagar['registro_erro'], retorno_erro=pagar['retorno_erro'])
            self.log(metodo='Processamento de Pagar Finalizado.')
        self.barra_progresso()

        if self.sel_companies.get():
            self.empresas_selecionadas = self.checa_empresas()
            self.log(metodo='Processamento de Empresas Iniciado.')
            empresa = Empresa(dados_origem=self.dados_origem,
                              dados_destino=self.dados_destino,
                              empresas_selecionadas=self.empresas_selecionadas,
                              comunicador=comunicador)
            empresas_log = empresa.inicia_empresas(marcador_apagado)
            marcador_limpeza.update({'empresa': 'sim'})
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
            marcador_limpeza.update({'cliente': 'sim'})
            self.clientes_selecionados = cliente.retorna_clientes_ids()
            if clientes_log:
                for cliente in clientes_log:
                    self.log(registro_erro=cliente['registro_erro'], retorno_erro=cliente['retorno_erro'])
            self.log(metodo='Processamento de Clientes Finalizado.')

        if self.sel_accounts_receivable.get():
            self.log(metodo='Processamento do Receber Iniciado.')
            receber = Receber(dados_origem=self.dados_origem,
                              dados_destino=self.dados_destino,
                              filial_id_origem=filial_id_origem,
                              filial_id_destino=filial_id_destino,
                              empresas_selecionadas=self.empresas_selecionadas,
                              clientes_selecionados=self.clientes_selecionados,
                              comunicador=comunicador)
            receber_log = receber.inicia_receber(marcador_apagado)
            marcador_limpeza.update({'receber': 'sim'})
            if receber_log:
                for receber in receber_log:
                    self.log(registro_erro=receber['registro_erro'], retorno_erro=receber['retorno_erro'])
            self.log(metodo='Processamento do Receber Finalizado.')
        self.barra_progresso()

        iterador = IteradorSql()
        iterador.conexao_destino(self.dados_destino)
        iterador.limpa_campo_auxiliar(marcador_limpeza)

        self.done_message.configure(text="Concluído", foreground='green')
        self.progressbar['value'] = 100
        self.log(metodo='Integração Concluída.')


app = Ui(root)
root.mainloop()
