import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
import logging
from PIL import ImageTk, Image
from ttkwidgets import CheckboxTreeview
import ttkbootstrap as ttkb
import doc
from run import Run


run = Run()
root = tk.Tk()
root.resizable(False, False)
root.title("IntegraApp")
theme = ttkb.Style()
theme.theme_use("integra_visual")


class Ui:

    def __init__(self, master):

        self.body_font = font.Font(family='Roboto', size=10)
        self.title_font = font.Font(family='Roboto', size=12)
        self.iid_companies = None
        self.iid_suppliers = None
        self.__iid_origin_groups = None

        # MAIN FRAME
        self.main_frame = ttkb.Frame(master)
        self.main_frame.configure(padding=10)
        self.main_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.tabs_notebook = ttkb.Notebook(self.main_frame)
        self.tabs_notebook.configure(padding=5)
        self.tabs_notebook.grid(row=0, column=1, sticky=tk.NSEW)
        self.tabs_notebook.columnconfigure(0, weight=1)
        self.tabs_notebook.rowconfigure(0, weight=1)

        # LOGO BANNER
        self.logo_main_frame = ttkb.Frame(self.main_frame)
        self.logo_main_frame.grid(column=0, row=0)

        self.logo_image = ImageTk.PhotoImage(Image.open('imgs/integrabanner.png'))
        self.logo_image_label = ttkb.Label(self.logo_main_frame, image=self.logo_image)
        self.logo_image_label.grid(sticky=tk.NSEW)

        # CONNECTIONS
        self.connection_main_frame = ttkb.Frame(self.tabs_notebook)
        self.connection_main_frame.configure(padding=25)
        self.connection_main_frame.grid(sticky=tk.NSEW)
        self.connection_main_frame.grid_anchor(tk.CENTER)
        self.connection_main_frame.columnconfigure(0, weight=1)
        self.connection_main_frame.columnconfigure(1, weight=1)
        self.connection_main_frame.columnconfigure(2, weight=1)

        self.tabs_notebook.add(self.connection_main_frame, text="Conexões")

        # CONNECTIONS[Origin Database]
        self.origin_labelframe = ttkb.Labelframe(self.connection_main_frame)
        self.origin_labelframe.configure(labelanchor=tk.N, padding=15, text="Banco de Origem")
        self.origin_labelframe.grid(column=0, row=0, sticky=tk.E)
        self.origin_labelframe.columnconfigure(0, weight=1)

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
        self.port_origin_label.grid(column=0, padx=17, row=8, sticky=tk.W)

        self.port_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.port_origin_entry.configure(justify=tk.CENTER, width=8)
        self.port_origin_entry.grid(column=0, row=9, sticky=tk.W)

        self.id_origin_label = ttkb.Label(self.origin_labelframe)
        self.id_origin_label.configure(text="ID Filial", font=self.body_font)
        self.id_origin_label.grid(column=0, row=8, sticky=tk.E, ipadx=5)

        self.id_origin_entry = ttkb.Entry(self.origin_labelframe)
        self.id_origin_entry.configure(justify=tk.CENTER, width=8)
        self.id_origin_entry.grid(column=0, row=9, sticky=tk.E)

        self.conn_origin_button = ttkb.Button(self.origin_labelframe, command=self.__origin)
        self.conn_origin_button.configure(text="Conectar", width=15)
        self.conn_origin_button.grid(column=0, pady=10, row=11)

        self.alert_origin_button = ttkb.Button()

        self.origin_message = tk.Message(self.origin_labelframe)
        self.origin_message.configure(font=self.body_font,
                                      text="Desconectado",
                                      width=100,
                                      foreground='red')
        self.origin_message.grid(column=0, row=12)

        # CONNECTIONS[Separator]
        self.database_separator = ttkb.Separator(self.connection_main_frame)
        self.database_separator.configure(orient=tk.HORIZONTAL)
        self.database_separator.grid(column=1, row=0)

        # CONNECTIONS[Destiny Database]
        self.destiny_labelframe = ttkb.Labelframe(self.connection_main_frame)
        self.destiny_labelframe.configure(labelanchor=tk.N, padding=15, text="Banco de Destino")
        self.destiny_labelframe.grid(column=2, row=0, sticky=tk.W)
        self.destiny_labelframe.columnconfigure(0, weight=1)

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
        self.port_destiny_label.grid(column=0, padx=17, row=8, sticky=tk.W)

        self.port_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.port_destiny_entry.configure(justify=tk.CENTER, width=8)
        self.port_destiny_entry.grid(column=0, row=9, sticky=tk.W)

        self.id_destiny_label = ttkb.Label(self.destiny_labelframe)
        self.id_destiny_label.configure(text="ID Filial", font=self.body_font)
        self.id_destiny_label.grid(column=0, row=8, sticky=tk.E, ipadx=5)

        self.id_destiny_entry = ttkb.Entry(self.destiny_labelframe)
        self.id_destiny_entry.configure(justify=tk.CENTER, width=8)
        self.id_destiny_entry.grid(column=0, row=9, sticky=tk.E)

        self.conn_destiny_button = ttkb.Button(self.destiny_labelframe, command=self.__destiny)
        self.conn_destiny_button.configure(text="Conectar", width=15)
        self.conn_destiny_button.grid(column=0, pady=10, row=11)

        self.alert_destiny_button = ttkb.Button()

        self.destiny_message = tk.Message(self.destiny_labelframe)
        self.destiny_message.configure(font=self.body_font,
                                       text="Desconectado",
                                       width=100,
                                       foreground='red')
        self.destiny_message.grid(column=0, row=12)

        # SETTINGS
        self.settings_main_frame = ttkb.Frame(self.tabs_notebook)
        self.settings_main_frame.configure(padding=15)
        self.settings_main_frame.grid(sticky=tk.NSEW)
        self.settings_main_frame.columnconfigure(0, weight=1)
        self.settings_main_frame.rowconfigure(0, weight=1)

        self.tabs_notebook.add(self.settings_main_frame, text="Configurações Gerais")

        self.settings_labelframe = ttkb.Labelframe(self.settings_main_frame)
        self.settings_labelframe.configure(labelanchor=tk.N, padding=20, text="Opções")
        self.settings_labelframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.settings_labelframe.columnconfigure(0, weight=1)
        self.settings_labelframe.rowconfigure(2, weight=1)

        # SETTINGS[Top Options]
        self.top_options_frame = ttkb.Frame(self.settings_labelframe)
        self.top_options_frame.configure(padding=25)
        self.top_options_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.top_options_frame.columnconfigure(0, weight=1)
        self.top_options_frame.columnconfigure(1, weight=1)
        self.top_options_frame.columnconfigure(2, weight=1)
        self.top_options_frame.columnconfigure(3, weight=1)
        self.top_options_frame.columnconfigure(4, weight=1)

        self.sel_product = tk.BooleanVar()
        self.sel_product.set(False)
        self.product_checkbutton = ttkb.Checkbutton(self.top_options_frame,
                                                    command=self.__swap_product)
        self.product_checkbutton.configure(text="Produto", variable=self.sel_product)
        self.product_checkbutton.grid(column=0, row=0)

        self.sel_bars = tk.BooleanVar()
        self.sel_bars.set(False)
        self.bars_checkbutton = ttkb.Checkbutton(self.top_options_frame)
        self.bars_checkbutton.configure(text="Barras Adicional",
                                        state=tk.DISABLED,
                                        variable=self.sel_bars)
        self.bars_checkbutton.grid(column=1, row=0)

        self.sel_stock = tk.BooleanVar()
        self.sel_stock.set(False)
        self.stock_checkbutton = ttkb.Checkbutton(self.top_options_frame)
        self.stock_checkbutton.configure(text="Estoque",
                                         state=tk.DISABLED,
                                         variable=self.sel_stock)
        self.stock_checkbutton.grid(column=2, row=0)

        self.sel_partition = tk.BooleanVar()
        self.sel_partition.set(False)
        self.partition_checkbutton = ttkb.Checkbutton(self.top_options_frame)
        self.partition_checkbutton.configure(text="Lote",
                                             state=tk.DISABLED,
                                             variable=self.sel_partition)
        self.partition_checkbutton.grid(column=3, row=0)

        self.sel_price = tk.BooleanVar()
        self.sel_price.set(False)
        self.price_checkbutton = ttkb.Checkbutton(self.top_options_frame)
        self.price_checkbutton.configure(text="Preço Filial",
                                         state=tk.DISABLED,
                                         variable=self.sel_price)
        self.price_checkbutton.grid(column=4, row=0)

        # SETTINGS[Top Separator]
        self.top_separator = ttkb.Separator(self.settings_labelframe)
        self.top_separator.configure(orient=tk.HORIZONTAL)
        self.top_separator.grid(column=0, row=1, sticky=tk.EW)

        # SETTINGS[Mid Options]
        self.mid_options_frame = ttkb.Frame(self.settings_labelframe)
        self.mid_options_frame.configure(padding=25)
        self.mid_options_frame.grid(column=0, row=2, sticky=tk.EW)
        self.mid_options_frame.columnconfigure(0, weight=1)
        self.mid_options_frame.columnconfigure(1, weight=1)
        self.mid_options_frame.rowconfigure(0, weight=1)

        # SETTINGS[Mid Options][Principle]
        self.principle_labelframe = ttkb.Labelframe(self.mid_options_frame)
        self.principle_labelframe.configure(text="Principio Ativo",
                                            labelanchor=tk.N,
                                            padding=10,
                                            borderwidth=0)
        self.principle_labelframe.grid(column=0, row=0, sticky=tk.NW)

        self.sel_principle_desc = tk.BooleanVar()
        self.sel_principle_desc.set(False)
        self.principle_desc_checkbutton = ttkb.Checkbutton(self.principle_labelframe,
                                                           command=self.__swap_principle)
        self.principle_desc_checkbutton.configure(text="Por Descrição",
                                                  variable=self.sel_principle_desc,
                                                  padding=5)
        self.principle_desc_checkbutton.grid(column=0, row=0)

        self.sel_principle_id = tk.BooleanVar()
        self.sel_principle_id.set(False)
        self.principle_id_checkbutton = ttkb.Checkbutton(self.principle_labelframe,
                                                         command=self.__swap_principle)
        self.principle_id_checkbutton.configure(text="Por ID",
                                                variable=self.sel_principle_id,
                                                padding=5)
        self.principle_id_checkbutton.grid(column=1, row=0)

        self.principle_id_entry = ttkb.Entry(self.principle_labelframe)
        self.principle_id_entry.configure(justify=tk.CENTER, width=2)
        self.principle_id_entry.grid(column=2, row=0)

        self.principle_id_label = ttkb.Label(self.principle_labelframe)
        self.principle_id_label.configure(text="Id de Destino", padding=5)
        self.principle_id_label.grid(column=3, row=0)

        # SETTINGS[Middle Options][Manufacturer]
        self.manufacturer_labelframe = ttkb.Labelframe(self.mid_options_frame)
        self.manufacturer_labelframe.configure(text="Fabricante",
                                               labelanchor=tk.N,
                                               padding=10,
                                               borderwidth=0)
        self.manufacturer_labelframe.grid(column=1, row=0, sticky=tk.NE)

        self.sel_manufacturer_cnpj = tk.BooleanVar()
        self.sel_manufacturer_cnpj.set(False)
        self.manufacturer_cnpj_checkbutton = ttkb.Checkbutton(self.manufacturer_labelframe,
                                                              command=self.__swap_manufacturer)
        self.manufacturer_cnpj_checkbutton.configure(text="Por CNPJ",
                                                     variable=self.sel_manufacturer_cnpj,
                                                     padding=5)
        self.manufacturer_cnpj_checkbutton.grid(column=0, row=0)

        self.sel_manufacturer_id = tk.BooleanVar()
        self.sel_manufacturer_id.set(False)
        self.manufacturer_id_checkbutton = ttkb.Checkbutton(self.manufacturer_labelframe,
                                                            command=self.__swap_manufacturer)
        self.manufacturer_id_checkbutton.configure(text="Por ID",
                                                   variable=self.sel_manufacturer_id,
                                                   padding=5)
        self.manufacturer_id_checkbutton.grid(column=1, row=0)

        self.manufacturer_id_entry = ttkb.Entry(self.manufacturer_labelframe)
        self.manufacturer_id_entry.configure(justify=tk.CENTER, width=2)
        self.manufacturer_id_entry.grid(column=2, row=0)

        self.manufacturer_id_label = ttkb.Label(self.manufacturer_labelframe)
        self.manufacturer_id_label.configure(text="Id de Destino", padding=5)
        self.manufacturer_id_label.grid(column=3, row=0)

        # SETTINGS[Bottom Separator]
        self.bottom_separator = ttkb.Separator(self.settings_labelframe)
        self.bottom_separator.configure(orient=tk.HORIZONTAL)
        self.bottom_separator.grid(column=0, row=3, sticky=tk.EW)

        # SETTINGS[Bottom Options]
        self.bottom_options_frame = ttkb.Frame(self.settings_labelframe)
        self.bottom_options_frame.configure(padding=20)
        self.bottom_options_frame.grid(column=0, row=4, sticky=tk.SW)
        self.bottom_options_frame.columnconfigure(0, weight=1)
        self.bottom_options_frame.columnconfigure(1, weight=1)
        self.bottom_options_frame.columnconfigure(2, weight=1)
        self.bottom_options_frame.rowconfigure(0, weight=1)
        self.bottom_options_frame.rowconfigure(1, weight=1)

        # SETTINGS[Bottom Options][Options]
        self.sel_productbar = tk.BooleanVar()
        self.sel_productbar.set(False)
        self.productbar_checkbutton = ttkb.Checkbutton(self.bottom_options_frame)
        self.productbar_checkbutton.configure(text="Não importar produtos com barras que iniciam com",
                                              variable=self.sel_productbar)
        self.productbar_checkbutton.grid(column=0, row=0, sticky=tk.W)

        self.value_zeros_spinbox = tk.StringVar(value='1')
        self.zeros_spinbox = ttkb.Spinbox(self.bottom_options_frame)
        self.zeros_spinbox.configure(from_=1,
                                     to=12,
                                     textvariable=self.value_zeros_spinbox,
                                     width=2)
        self.zeros_spinbox.grid(column=1, row=0, sticky=tk.W)

        self.zeros_label = ttkb.Label(self.bottom_options_frame)
        self.zeros_label.configure(text="ou mais zero(s).")
        self.zeros_label.grid(column=2, row=0, sticky=tk.W)

        self.sel_erased = tk.BooleanVar()
        self.sel_erased.set(False)
        self.erased_checkbutton = ttkb.Checkbutton(self.bottom_options_frame)
        self.erased_checkbutton.configure(text="Não importar registros marcados como apagados.",
                                          variable=self.sel_erased)
        self.erased_checkbutton.grid(column=0, row=1, sticky=tk.W)

        # PRODUCT GROUPS
        self.groups_main_frame = ttkb.Frame(self.tabs_notebook)
        self.groups_main_frame.configure(padding=10)
        self.groups_main_frame.grid(sticky=tk.NSEW)
        self.groups_main_frame.rowconfigure(0, weight=1)
        self.groups_main_frame.columnconfigure(0, weight=1)
        self.groups_main_frame.columnconfigure(1, weight=1)

        self.tabs_notebook.add(self.groups_main_frame, text="Grupos de Produtos")

        # PRODUCT GROUPS[Origin Database]
        self.groups_origin_frame = ttkb.Frame(self.groups_main_frame)
        self.groups_origin_frame.configure(padding=5)
        self.groups_origin_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.groups_origin_frame.rowconfigure(0, weight=1)
        self.groups_origin_frame.columnconfigure(0, weight=1)

        self.groups_origin_labelframe = ttkb.Labelframe(self.groups_origin_frame)
        self.groups_origin_labelframe.configure(labelanchor=tk.N,
                                                text="Grupos de Origem",
                                                borderwidth=0,
                                                padding=5)
        self.groups_origin_labelframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.groups_origin_labelframe.columnconfigure(0, weight=1)
        self.groups_origin_labelframe.rowconfigure(0, weight=1)

        self.groups_origin_checkboxtreeview = CheckboxTreeview(self.groups_origin_labelframe)
        self.groups_origin_checkboxtreeview.grid(column=0, row=0, sticky=tk.NSEW)
        self.groups_origin_checkboxtreeview.configure(height=20)
        self.groups_origin_checkboxtreeview['columns'] = ('Novo ID', 'ID', 'Nome')
        self.groups_origin_checkboxtreeview.column('#0', width=30, stretch=False)
        self.groups_origin_checkboxtreeview.column('Novo ID',
                                                   anchor=tk.CENTER,
                                                   width=70,
                                                   stretch=False)
        self.groups_origin_checkboxtreeview.column('ID', anchor=tk.CENTER, width=30, stretch=False)
        self.groups_origin_checkboxtreeview.column('Nome', anchor=tk.W, width=160, stretch=True)
        self.groups_origin_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.groups_origin_checkboxtreeview.heading('Novo ID', text='Novo ID', anchor=tk.CENTER)
        self.groups_origin_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.groups_origin_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_erased_origin_groups = tk.BooleanVar()
        self.sel_erased_origin_groups.set(False)
        self.erased_groups_origin_checkbutton = ttkb.Checkbutton(self.groups_origin_frame,
                                                                 command=self.__origin_groups)
        self.erased_groups_origin_checkbutton.configure(text="Não mostrar grupos apagados",
                                                        variable=self.sel_erased_origin_groups)
        self.erased_groups_origin_checkbutton.grid(column=0, row=1, sticky=tk.NW)

        self.sel_all_origin_groups = tk.BooleanVar()
        self.sel_all_origin_groups.set(False)
        self.all_origin_groups_checkbutton = ttkb.Checkbutton(self.groups_origin_frame,
                                                              command=self.__tag_all_groups)
        self.all_origin_groups_checkbutton.configure(text="Selecionar todos",
                                                     variable=self.sel_all_origin_groups)
        self.all_origin_groups_checkbutton.grid(column=0, row=1, sticky=tk.NE)

        # PRODUCT GROUPS[Destiny Database]
        self.groups_destiny_frame = ttkb.Frame(self.groups_main_frame)
        self.groups_destiny_frame.configure(padding=5)
        self.groups_destiny_frame.grid(column=1, row=0, sticky=tk.NSEW)
        self.groups_destiny_frame.rowconfigure(0, weight=1)
        self.groups_destiny_frame.columnconfigure(0, weight=1)

        self.groups_destiny_labelframe = ttkb.Labelframe(self.groups_destiny_frame)
        self.groups_destiny_labelframe.configure(labelanchor=tk.N,
                                                 text="Grupos de Destino",
                                                 borderwidth=0,
                                                 padding=5)
        self.groups_destiny_labelframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.groups_destiny_labelframe.columnconfigure(0, weight=1)
        self.groups_destiny_labelframe.rowconfigure(0, weight=1)

        self.groups_destiny_checkboxtreeview = CheckboxTreeview(self.groups_destiny_labelframe)
        self.groups_destiny_checkboxtreeview.grid(column=0, row=0, sticky=tk.NSEW)
        self.groups_destiny_checkboxtreeview.configure(height=20)
        self.groups_destiny_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.groups_destiny_checkboxtreeview.column('#0', width=0, stretch=False)
        self.groups_destiny_checkboxtreeview.column('ID', anchor=tk.CENTER, width=50, stretch=False)
        self.groups_destiny_checkboxtreeview.column('Nome', anchor=tk.W, width=160, stretch=True)
        self.groups_destiny_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.groups_destiny_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.groups_destiny_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_erased_destiny_groups = tk.BooleanVar()
        self.sel_erased_destiny_groups.set(False)
        self.erased_groups_destiny_checkbutton = ttkb.Checkbutton(self.groups_destiny_frame,
                                                                  command=self.__destiny_groups)
        self.erased_groups_destiny_checkbutton.configure(text="Não mostrar grupos apagados",
                                                         variable=self.sel_erased_destiny_groups)
        self.erased_groups_destiny_checkbutton.grid(column=0, row=1, sticky=tk.NW)

        # SUPPLIER & BILLS TO PAY
        self.supplier_main_frame = ttkb.Frame(self.tabs_notebook)
        self.supplier_main_frame.configure(padding=15)
        self.supplier_main_frame.grid(sticky=tk.EW)
        self.supplier_main_frame.columnconfigure(0, weight=1)
        self.supplier_main_frame.rowconfigure(0, weight=1)
        self.supplier_main_frame.rowconfigure(1, weight=1)

        self.tabs_notebook.add(self.supplier_main_frame, text="Fornecedores e Pagar")

        self.supplier_options_frame = ttkb.Frame(self.supplier_main_frame)
        self.supplier_options_frame.grid(column=0, row=0, sticky=tk.EW)
        self.supplier_options_frame.columnconfigure(0, weight=1)

        self.supplier_options_labelframe = ttkb.Labelframe(self.supplier_options_frame)
        self.supplier_options_labelframe.configure(labelanchor=tk.N, padding=15, text="Opções")
        self.supplier_options_labelframe.grid(row=0, column=0, sticky=tk.EW)
        self.supplier_options_labelframe.columnconfigure(0, weight=1)
        self.supplier_options_labelframe.columnconfigure(1, weight=1)

        self.sel_suppliers = tk.BooleanVar()
        self.sel_suppliers.set(False)
        self.suppliers_checkbutton = ttkb.Checkbutton(self.supplier_options_labelframe)
        self.suppliers_checkbutton.configure(text="Fornecedores", variable=self.sel_suppliers)
        self.suppliers_checkbutton.grid(row=0, column=0)

        self.sel_bills = tk.BooleanVar()
        self.sel_bills.set(False)
        self.bills_checkbutton = ttkb.Checkbutton(self.supplier_options_labelframe)
        self.bills_checkbutton.configure(text="Pagar", variable=self.sel_bills)
        self.bills_checkbutton.grid(row=0, column=1)

        self.suppliers_checkboxtreeview = CheckboxTreeview(self.supplier_main_frame)
        self.suppliers_checkboxtreeview.grid(row=1, column=0, sticky=tk.NSEW)
        self.suppliers_checkboxtreeview.configure(height=20)
        self.suppliers_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.suppliers_checkboxtreeview.column('#0', width=40, stretch=False)
        self.suppliers_checkboxtreeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.suppliers_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.suppliers_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.suppliers_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.suppliers_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_all_suppliers = tk.BooleanVar()
        self.sel_all_suppliers.set(False)
        self.all_suppliers_checkbutton = ttkb.Checkbutton(self.supplier_main_frame,
                                                          command=self.__tag_all_suppliers)
        self.all_suppliers_checkbutton.configure(text="Selecionar todos",
                                                 variable=self.sel_all_suppliers,
                                                 padding=5)
        self.all_suppliers_checkbutton.grid(row=2, column=0, sticky=tk.NE)

        # COMPANIES/CUSTOMERS & ACCOUNTS RECEIVABLE
        self.company_main_frame = ttkb.Frame(self.tabs_notebook)
        self.company_main_frame.configure(padding=15)
        self.company_main_frame.grid(sticky=tk.EW)
        self.company_main_frame.columnconfigure(0, weight=1)
        self.company_main_frame.rowconfigure(0, weight=1)
        self.company_main_frame.rowconfigure(1, weight=1)

        self.tabs_notebook.add(self.company_main_frame, text="Empresas e Clientes")

        self.company_options_frame = ttkb.Frame(self.company_main_frame)
        self.company_options_frame.grid(column=0, row=0, sticky=tk.EW)
        self.company_options_frame.columnconfigure(0, weight=1)

        self.companies_options_labelframe = ttkb.Labelframe(self.company_options_frame)
        self.companies_options_labelframe.configure(labelanchor=tk.N, padding=15, text="Opções")
        self.companies_options_labelframe.grid(row=0, column=0, sticky=tk.EW)
        self.companies_options_labelframe.columnconfigure(0, weight=1)
        self.companies_options_labelframe.columnconfigure(1, weight=1)

        self.sel_companies = tk.BooleanVar()
        self.sel_companies.set(False)
        self.companies_checkbutton = ttkb.Checkbutton(self.companies_options_labelframe)
        self.companies_checkbutton.configure(text="Empresas e Clientes",
                                             variable=self.sel_companies)
        self.companies_checkbutton.grid(row=0, column=0)

        self.sel_accounts_receivable = tk.BooleanVar()
        self.sel_accounts_receivable.set(False)
        self.accounts_receivable_checkbutton = ttkb.Checkbutton(self.companies_options_labelframe)
        self.accounts_receivable_checkbutton.configure(text="Receber",
                                                       variable=self.sel_accounts_receivable)
        self.accounts_receivable_checkbutton.grid(row=0, column=1)

        self.companies_checkboxtreeview = CheckboxTreeview(self.company_main_frame)
        self.companies_checkboxtreeview.grid(row=1, column=0, sticky=tk.NSEW)
        self.companies_checkboxtreeview.configure(height=20)
        self.companies_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.companies_checkboxtreeview.column('#0', width=40, stretch=False)
        self.companies_checkboxtreeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.companies_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.companies_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.companies_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.companies_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.sel_all_companies = tk.BooleanVar()
        self.sel_all_companies.set(False)
        self.all_companies_checkbutton = ttkb.Checkbutton(self.company_main_frame,
                                                          command=self.__tag_all_companies)
        self.all_companies_checkbutton.configure(text="Selecionar todos",
                                                 variable=self.sel_all_companies,
                                                 padding=5)
        self.all_companies_checkbutton.grid(row=2, column=0, sticky=tk.NE)

        # LOGS
        self.log_main_frame = ttkb.Frame(self.tabs_notebook)
        self.log_main_frame.configure(padding=15)
        self.log_main_frame.grid(sticky=tk.NSEW)
        self.log_main_frame.columnconfigure(0, weight=1)
        self.log_main_frame.rowconfigure(0, weight=1)

        self.tabs_notebook.add(self.log_main_frame, text="Execução e Logs")

        self.logs_scrolledtext = ttkb.ScrolledText(self.log_main_frame)
        self.logs_scrolledtext.configure(font=self.body_font, height=20)
        self.logs_scrolledtext.grid(row=0, column=0, sticky=tk.EW)

        self.log_bottom_frame = ttkb.Frame(self.log_main_frame)
        self.log_bottom_frame.configure(padding=10)
        self.log_bottom_frame.grid(column=0, row=1, sticky=tk.EW)
        self.log_bottom_frame.rowconfigure(0, weight=1)
        self.log_bottom_frame.columnconfigure(0, weight=1)
        self.log_bottom_frame.columnconfigure(1, weight=1)
        self.log_bottom_frame.columnconfigure(2, weight=1)

        self.start_button = ttkb.Button(self.log_bottom_frame, command=self.__start)
        self.start_button.configure(text="Iniciar", width=20)
        self.start_button.grid(row=0, column=0)

        self.progressbar = ttkb.Progressbar(self.log_bottom_frame, mode='determinate')
        self.progressbar.configure(length=450, orient=tk.HORIZONTAL)
        self.progressbar.grid(row=0, column=1)

        self.done_message = tk.Message(self.log_bottom_frame, font=self.body_font)
        self.done_message.configure(text="Não Iniciado",
                                    width=125,
                                    foreground='grey',
                                    relief=tk.FLAT,
                                    borderwidth=1)
        self.done_message.grid(row=0, column=2)

        # DOCUMENTATION
        self.documentation_main_frame = ttkb.Frame(self.tabs_notebook)
        self.documentation_main_frame.configure(padding=15)
        self.documentation_main_frame.grid(sticky=tk.NSEW)
        self.documentation_main_frame.columnconfigure(0, weight=1)
        self.documentation_main_frame.rowconfigure(0, weight=1)

        self.tabs_notebook.add(self.documentation_main_frame, text="Documentação")

        self.documentation_scrolledtext = ttkb.ScrolledText(self.documentation_main_frame)
        self.documentation_scrolledtext.insert(tk.END, doc.INFO_DOC)
        self.documentation_scrolledtext.configure(state=tk.DISABLED,
                                                  borderwidth=5,
                                                  font=self.body_font,
                                                  height=20)
        self.documentation_scrolledtext.grid(sticky=tk.NSEW)

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
    def __origin(self):

        db_origin: dict = {'host': self.ip_origin_entry.get(),
                           'user': self.user_origin_entry.get(),
                           'password': self.pass_origin_entry.get(),
                           'database': self.db_origin_entry.get(),
                           'port': int(self.port_origin_entry.get())}

        log_return = run.connect_origin(db_origin)

        if log_return['return'] == 'Connected':
            self.alert_origin_button.destroy()
            self.origin_message.configure(text="Conectado", foreground='green')

            self.__origin_groups()
            self.__companies()
            self.__suppliers()

        else:
            self.alert_origin_button.destroy()
            self.origin_message.configure(text="Falha", foreground='orange')
            cod_error = log_return['cod']
            desc_error = log_return['description']
            self.__origin_alert(cod_error, desc_error)
            self.alert_origin_button.place(anchor=tk.W, height=22, width=22, x=30, y=323)

    def __destiny(self):

        db_destiny: dict = {'host': self.ip_destiny_entry.get(),
                            'user': self.user_destiny_entry.get(),
                            'password': self.pass_destiny_entry.get(),
                            'database': self.db_destiny_entry.get(),
                            'port': int(self.port_destiny_entry.get())}

        log_return = run.connect_destiny(db_destiny)

        if log_return['return'] == 'Connected':
            self.alert_destiny_button.destroy()
            self.destiny_message.configure(text="Conectado", foreground='green')
            self.__destiny_groups()

        else:
            self.alert_destiny_button.destroy()
            self.destiny_message.configure(text="Falha", foreground='orange')
            cod_error = log_return['cod']
            desc_error = log_return['description']
            self.__destiny_alert(cod_error, desc_error)
            self.alert_destiny_button.place(anchor=tk.W, height=22, width=22, x=30, y=323)

    def __origin_alert(self, cod_error, desc_error):

        alert_image = tk.PhotoImage(file="imgs/info.png")
        self.alert_origin_button = ttkb.Button(self.origin_labelframe, 
                                               image=alert_image, 
                                               command=lambda: self.__return_error(cod_error, desc_error), 
                                               bootstyle=ttkb.WARNING)
        self.alert_origin_button.configure(compound=tk.LEFT, padding=1)

    def __destiny_alert(self, cod_error, desc_error):

        alert_image = tk.PhotoImage(file="imgs/info.png")
        self.alert_destiny_button = ttkb.Button(self.destiny_labelframe,
                                                image=alert_image,
                                                command=lambda: self.__return_error(cod_error, desc_error),
                                                bootstyle="warning")
        self.alert_destiny_button.configure(compound=tk.LEFT, padding=1)

    def __return_error(self, cod_error, desc_error):

        erro = f"Código: {cod_error} | Descrição: {desc_error}"

        error_top = tk.Toplevel()
        error_top.title("Retorno do Erro")

        theme_error = ttkb.Style(error_top)
        theme_error.theme_use('integra_visual')

        error_frame = ttk.Frame(error_top)
        error_frame.configure(height=200, padding=20, width=200)
        error_frame.grid(column=0, row=0)
        error_frame.rowconfigure(1, weight=1)
        error_frame.columnconfigure(1, weight=1)

        error_label = ttk.Label(error_frame)
        error_label.configure(text=erro)
        error_label.grid(column=1, row=1)

    def __log(self, method=None, error_register=None, error_return=None):

        logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s:%(message)s')
        separator = "| ============================================================================= |"
        indentation = "| "

        if method:
            self.logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{indentation}{method}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            logging.warning(separator)
            logging.warning("| %s", method)
            logging.warning(separator)

        if error_register or error_return:
            self.logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{indentation}{error_register}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{indentation}{error_return}\n")
            self.logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            logging.warning(separator)
            logging.warning("| %s", error_register)
            logging.warning("| %s", error_return)
            logging.warning(separator)

    # Métodos de listagem automática e exibição dos dados ao conectar.
    def __origin_groups(self):

        index: int = 0
        option_selected: dict = {'database': 'origin'}

        try:
            if self.sel_erased_origin_groups.get():

                option_selected.update({'option': 'filtered'})
                groups = run.get_groups(option_selected)
                self.__iid_origin_groups: list[int] = []

                for group in groups:
                    self.groups_origin_checkboxtreeview.insert(
                        "",
                        index=tk.END,
                        iid=index,
                        text='',
                        values=('', group['id_grupo'], group['descricao']))
                    self.__iid_origin_groups.append(index)
                    index += 1

            else:

                option_selected.update({'option': 'not_filtered'})
                groups = run.get_groups(option_selected)
                self.__iid_origin_groups: list[int] = []

                for group in groups:
                    self.groups_origin_checkboxtreeview.insert(
                        "",
                        index=tk.END,
                        iid=index,
                        text='',
                        values=('', group['id_grupo'], group['descricao']))
                    self.__iid_origin_groups.append(index)
                    index += 1

        except Exception as error:
            print(f"Exception in method origin_groups_listing: {error}")

    def __destiny_groups(self):

        index: int = 0
        option_selected: dict = {'database': 'destiny'}

        try:
            if self.sel_erased_destiny_groups.get():

                option_selected.update({'option': 'filtered'})
                groups = run.get_groups(option_selected)

                for group in groups:
                    self.groups_destiny_checkboxtreeview.insert(
                        "",
                        index=tk.END,
                        iid=index,
                        text='',
                        values=(group['id_grupo'], group['descricao']))
                    index += 1

            else:

                option_selected.update({'option': 'not_filtered'})
                groups = run.get_groups(option_selected)

                for group in groups:
                    self.groups_destiny_checkboxtreeview.insert(
                        "",
                        index=tk.END,
                        iid=index,
                        text='',
                        values=(group['id_grupo'], group['descricao']))
                    index += 1

        except Exception as error:
            print(f"Exception in method destiny_groups_listing: {error}")

    def __companies(self):

        try:
            companies = run.get_companies()
            index: int = 0
            self.iid_companies: list[int] = []

            for company in companies:
                self.companies_checkboxtreeview.insert(
                    "",
                    index='end',
                    iid=index,
                    text='',
                    values=(company['id_empresa'], company['nome_fantasia']))
                self.iid_companies.append(index)
                index += 1

        except Exception as error:
            print(f"Exception in method companies_listing: {error}")

    def __suppliers(self):

        try:
            suppliers = run.get_suppliers()
            index: int = 0
            self.iid_suppliers: list[int] = []

            for supplier in suppliers:
                self.suppliers_checkboxtreeview.insert(
                    "",
                    index='end',
                    iid=index,
                    text='',
                    values=(supplier['id_fornecedor'], supplier['razao_social']))
                self.iid_suppliers.append(index)
                index += 1

        except Exception as error:
            print(f"Exception in method suppliers_listing: {error}")

    # Métodos de marcação de todos os registros na Interface.
    def __tag_all_companies(self):

        for iid in self.iid_companies:
            self.companies_checkboxtreeview.change_state(item=iid, state='checked')

    def __tag_all_suppliers(self):

        for iid in self.iid_suppliers:
            self.suppliers_checkboxtreeview.change_state(item=iid, state='checked')

    def __tag_all_groups(self):

        for iid in self.__iid_origin_groups:
            self.groups_origin_checkboxtreeview.change_state(item=iid, state='checked')

    # Métodos de coleta dos registros selecionados na Interface.
    def __get_companies(self):

        companies: int = []

        for company in self.companies_checkboxtreeview.get_checked():
            company_id = self.companies_checkboxtreeview.item(item=company, option='values')
            companies.append(company_id[0])
        selected_companies: int = tuple(companies)

        return selected_companies

    def __get_suppliers(self):

        suppliers: int = []

        for supplier in self.suppliers_checkboxtreeview.get_checked():
            supplier_id = self.suppliers_checkboxtreeview.item(item=supplier, option='values')
            suppliers.append(supplier_id[0])
        selected_suppliers = tuple(suppliers)

        return selected_suppliers

    def __get_groups(self):

        selected_groups = []

        for group in self.groups_origin_checkboxtreeview.get_checked():
            values = self.groups_origin_checkboxtreeview.item(item=group, option='values')
            selected_group = {'novo_id': int(values[0]), 'antigo_id': int(values[1])}
            selected_groups.append(selected_group)

        return selected_groups

    # Métodos de retorno de dados da Interface.
    def __return_destiny_communicator(self):

        branch_id: str = str(self.id_destiny_entry.get())
        communicator_table = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
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

        communicator = communicator_table.get(branch_id, 'Not Found')
        if communicator == 'Not Found':
            print("Communicator character not found.")

        return communicator

    def __return_origin_branch_id(self):
        return self.id_origin_entry.get()

    def __return_destiny_branch_id(self):
        return self.id_destiny_entry.get()

    # Métodos de troca automática de estado dos botões.
    def __swap_manufacturer(self):

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

    def __swap_principle(self):

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

    def __swap_product(self):

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
    def __progress_bar(self):
        self.progressbar['value'] += 5

    # Método de execução
    def __start(self):

       # PRE STARTUP
        options = {}
        erased = False
        product_options = {'fabricante_por_cnpj': False,
                           'fabricante_por_id': False,
                           'principio_por_desc': False,
                           'principio_por_id': False,
                           'classe_terapeutica_por_desc': False,
                           'classe_terapeutica_por_padrao': False,
                           'remover_produtos_barras_zerados': False,
                           'quantidade_zeros_barras': int(self.zeros_spinbox.get())}

        module_marker = {'fabricante': False,
                         'principio_ativo': False,
                         'produto': False,
                         'barras': False,
                         'estoque': False,
                         'lote': False,
                         'preco_filial': False,
                         'fornecedor': False,
                         'pagar': False,
                         'empresa': False,
                         'cliente': False,
                         'receber': False}

        self.progressbar['value'] = 0
        self.done_message.configure(text="Em Andamento", width=125, foreground='orange')
        self.__log(method='Integração Iniciada.')

        # MARKERS
        if self.sel_erased.get():
            erased = True

        if self.sel_manufacturer_cnpj.get():
            module_marker.update({'fabricante': True})

        if self.sel_principle_desc.get():
            module_marker.update({'principio_ativo': True})

        if self.sel_product.get():
            module_marker.update({'produto': True})

        if self.sel_bars.get():
            module_marker.update({'barras': True})

        if self.sel_stock.get():
            module_marker.update({'estoque': True})

        if self.sel_partition.get():
            module_marker.update({'lote': True})

        if self.sel_price.get():
            module_marker.update({'preco_filial': True})

        if self.sel_suppliers.get():
            module_marker.update({'fornecedor': True})

        if self.sel_bills.get():
            module_marker.update({'pagar': True})

        if self.sel_companies.get():
            module_marker.update({'empresa': True})
            module_marker.update({'cliente': True})

        if self.sel_accounts_receivable.get():
            module_marker.update({'receber': True})

        if self.sel_productbar.get():
            product_options.update({'remover_produtos_barras_zerados': True})

        if self.sel_manufacturer_cnpj.get():
            product_options.update({'fabricante_por_cnpj': True})

        if self.sel_manufacturer_id.get():
            product_options.update({'fabricante_por_id': True})

        if self.sel_principle_desc.get():
            product_options.update({'principio_por_desc': True})

        if self.sel_principle_id.get():
            product_options.update({'principio_por_id': True})

        options.update({'erased': erased})
        options.update({'module_marker': module_marker})
        options.update({'product_options': product_options})
        options.update({'communicator': self.__return_destiny_communicator()})
        options.update({'origin_branch_id': int(self.__return_origin_branch_id())})
        options.update({'destiny_branch_id': int(self.__return_destiny_branch_id())})
        options.update({'manufacturer_id': self.manufacturer_id_entry.get()})
        options.update({'principle_id': self.principle_id_entry.get()})
        options.update({'selected_companies': self.__get_companies()})
        options.update({'selected_groups': self.__get_groups()})
        options.update({'selected_suppliers': self.__get_suppliers()})

        # START PROCESS
        run.start_process(options)

        # PROCESS LOGS
        all_logs = run.get_log() # pylint: disable=unsubscriptable-object

        if self.sel_manufacturer_cnpj.get():
            self.__log(method='Processamento de Fabricantes Iniciado.')

            if all_logs['manufacturer_logs']:
                manufacturer_log = all_logs['manufacturer_logs']

                for manufacturer in manufacturer_log:
                    self.__log(error_register=manufacturer['error_register'],
                             error_return=manufacturer['error_return'])
            self.__log(method='Processamento de Fabricantes Finalizado.')
        self.__progress_bar()

        # PRINCIPLE
        if self.sel_principle_desc.get():
            self.__log(method='Processamento de Principios Ativos Iniciado.')

            if all_logs['principle_logs']:
                principle_log = all_logs['principle_logs']

                for principle in principle_log:
                    self.__log(error_register=principle['error_register'],
                             error_return=principle['error_return'])
            self.__log(method='Processamento de Principios Ativos Finalizado.')
        self.__progress_bar()

        # PRODUCT
        if self.sel_product.get():
            self.__log(method='Processamento de Produtos Iniciado.')

            if all_logs['product_logs']:
                product_log = all_logs['product_logs']

                for product in product_log:
                    self.__log(error_register=product['error_register'],
                             error_return=product['error_return'])
            self.__log(method='Processamento de Produtos Finalizado.')
        self.__progress_bar()

        # BARS
        if self.sel_bars.get():
            self.__log(method='Processamento de Barras Adicionais Iniciado.')

            if all_logs['bar_logs']:
                bar_logs = all_logs['bar_logs']

                for bars in bar_logs:
                    self.__log(error_register=bars['error_register'],
                             error_return=bars['error_return'])
            self.__log(method='Processamento de Barras Adicionais Finalizado.')
        self.__progress_bar()

        # STOCK
        if self.sel_stock.get():
            self.__log(method='Processamento de Estoque Iniciado.')

            if all_logs['stock_logs']:
                stock_logs = all_logs['stock_logs']

                for stock in stock_logs:
                    self.__log(error_register=stock['error_register'],
                             error_return=stock['error_return'])
            self.__log(method='Processamento de Estoque Finalizado.')
        self.__progress_bar()

        # PARTITION
        if self.sel_partition.get():
            self.__log(method='Processamento de Lotes Iniciado.')

            if all_logs['partition_logs']:
                partition_logs = all_logs['partition_logs']

                for partition in partition_logs:
                    self.__log(error_register=partition['error_register'],
                             error_return=partition['error_return'])
                self.__log(method='Processamento de Lotes Finalizado.')
        self.__progress_bar()

        # PRICE
        if self.sel_price.get():
            self.__log(method='Processamento de Preço Filial Iniciado.')

            if all_logs['price_logs']:
                price_logs = all_logs['price_logs']

                for price in price_logs:
                    self.__log(error_register=price['error_register'],
                             error_return=price['error_return'])
                self.__log(method='Processamento de Preço Filial Finalizado.')
        self.__progress_bar()

        # SUPPLIER
        if self.sel_suppliers.get():
            self.__log(method='Processamento de Fornecedores Iniciado.')

            if all_logs['supplier_logs']:
                supplier_logs = all_logs['supplier_logs']

                for supplier in supplier_logs:
                    self.__log(error_register=supplier['error_register'],
                             error_return=supplier['error_return'])
            self.__log(method='Processamento de Fornecedores Finalizado.')
        self.__progress_bar()

        # BILLS TO PAY
        if self.sel_bills.get():
            self.__log(method='Processamento de Pagar Iniciado.')

            if all_logs['bill_logs']:
                bill_logs = all_logs['bill_logs']

                for bill in bill_logs:
                    self.__log(error_register=bill['error_register'],
                             error_return=bill['error_return'])
            self.__log(method='Processamento de Pagar Finalizado.')
        self.__progress_bar()

        # COMPANY
        if self.sel_companies.get():
            self.__log(method='Processamento de Empresas Iniciado.')

            if all_logs['company_logs']:
                company_logs = all_logs['company_logs']

                for company in company_logs:
                    self.__log(error_register=company['error_register'],
                             error_return=company['error_return'])
            self.__log(method='Processamento de Empresas Finalizado.')

            # CUSTOMER
            self.__log(method='Processamento de Clientes Iniciado.')

            if all_logs['customer_logs']:
                customer_logs = all_logs['customer_logs']

                for customer in customer_logs:
                    self.__log(error_register=customer['error_register'],
                             error_return=customer['error_return'])
            self.__log(method='Processamento de Clientes Finalizado.')

        # ACCOUNT RECEIVABLE
        if self.sel_accounts_receivable.get():
            self.__log(method='Processamento do Receber Iniciado.')

            if all_logs['account_logs']:
                account_logs = all_logs['account_logs']

                for account in account_logs:
                    self.__log(error_register=account['error_register'],
                             error_return=account['error_return'])
            self.__log(method='Processamento do Receber Finalizado.')
        self.__progress_bar()

        self.done_message.configure(text="Concluído", foreground='green')
        self.progressbar['value'] = 100
        self.__log(method='Integração Concluída.')


app = Ui(root)
root.mainloop()
