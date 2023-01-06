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

        self.__body_font = font.Font(family='Roboto', size=10)
        self.__iid_companies = None
        self.__iid_suppliers = None
        self.__iid_origin_groups = None

        # MAIN FRAME
        self.__main_frame = ttkb.Frame(master)
        self.__main_frame.configure(padding=10)
        self.__main_frame.grid(sticky=tk.NSEW)

        self.__tabs_notebook = ttkb.Notebook(self.__main_frame)
        self.__tabs_notebook.configure(padding=5)
        self.__tabs_notebook.grid(column=1, row=0, sticky=tk.NSEW)

        # LOGO BANNER
        self.__logo_main_frame = ttkb.Frame(self.__main_frame)
        self.__logo_main_frame.grid(column=0, row=0)

        self.__logo_image = ImageTk.PhotoImage(Image.open('imgs/banner.png'))
        self.__logo_image_label = ttkb.Label(self.__logo_main_frame, image=self.__logo_image)
        self.__logo_image_label.grid(sticky=tk.NSEW)

        # CONNECTIONS
        self.__connection_main_frame = ttkb.Frame(self.__tabs_notebook)
        self.__connection_main_frame.configure(padding=25)
        self.__connection_main_frame.grid(sticky=tk.NSEW)
        self.__connection_main_frame.grid_anchor(tk.CENTER)
        self.__connection_main_frame.columnconfigure(0, weight=1)
        self.__connection_main_frame.columnconfigure(1, weight=1)
        self.__connection_main_frame.columnconfigure(2, weight=1)

        self.__tabs_notebook.add(
            self.__connection_main_frame, text="Conexões")

        # CONNECTIONS[Origin Database]
        self.__origin_labelframe = ttkb.Labelframe(self.__connection_main_frame)
        self.__origin_labelframe.configure(labelanchor=tk.N, padding=15, text="Banco de Origem")
        self.__origin_labelframe.grid(column=0, row=0, sticky=tk.E)
        self.__origin_labelframe.columnconfigure(0, weight=1)

        self.__ip_origin_label = ttkb.Label(self.__origin_labelframe)
        self.__ip_origin_label.configure(text="Ip do Servidor", font=self.__body_font)
        self.__ip_origin_label.grid(column=0, row=0)

        self.__ip_origin_entry = ttkb.Entry(self.__origin_labelframe)
        self.__ip_origin_entry.configure(justify=tk.CENTER)
        self.__ip_origin_entry.grid(column=0, row=1)

        self.__db_origin_label = ttkb.Label(self.__origin_labelframe)
        self.__db_origin_label.configure(text="Nome do Banco", font=self.__body_font)
        self.__db_origin_label.grid(column=0, row=2)

        self.__db_origin_entry = ttkb.Entry(self.__origin_labelframe)
        self.__db_origin_entry.configure(justify=tk.CENTER)
        self.__db_origin_entry.grid(column=0, row=3)

        self.__user_origin_label = ttkb.Label(self.__origin_labelframe)
        self.__user_origin_label.configure(text="Usuário", font=self.__body_font)
        self.__user_origin_label.grid(column=0, row=4)

        self.__user_origin_entry = ttkb.Entry(self.__origin_labelframe)
        self.__user_origin_entry.configure(justify=tk.CENTER)
        self.__user_origin_entry.grid(column=0, row=5)

        self.__pass_origin_label = ttkb.Label(self.__origin_labelframe)
        self.__pass_origin_label.configure(text="Senha", font=self.__body_font)
        self.__pass_origin_label.grid(column=0, row=6)

        self.__pass_origin_entry = ttkb.Entry(self.__origin_labelframe)
        self.__pass_origin_entry.configure(justify=tk.CENTER, show='*')
        self.__pass_origin_entry.grid(column=0, row=7)

        self.__port_origin_label = ttkb.Label(self.__origin_labelframe)
        self.__port_origin_label.configure(text="Porta", font=self.__body_font)
        self.__port_origin_label.grid(column=0, padx=17, row=8, sticky=tk.W)

        self.__port_origin_entry = ttkb.Entry(self.__origin_labelframe)
        self.__port_origin_entry.configure(justify=tk.CENTER, width=8)
        self.__port_origin_entry.grid(column=0, row=9, sticky=tk.W)

        self.__id_origin_label = ttkb.Label(self.__origin_labelframe)
        self.__id_origin_label.configure(text="ID Filial", font=self.__body_font)
        self.__id_origin_label.grid(column=0, row=8, sticky=tk.E, ipadx=5)

        self.__id_origin_entry = ttkb.Entry(self.__origin_labelframe)
        self.__id_origin_entry.configure(justify=tk.CENTER, width=8)
        self.__id_origin_entry.grid(column=0, row=9, sticky=tk.E)

        self.__conn_origin_button = ttkb.Button(self.__origin_labelframe, command=self.__origin)
        self.__conn_origin_button.configure(text="Conectar", width=15)
        self.__conn_origin_button.grid(column=0, pady=10, row=11)

        self.__alert_origin_button = ttkb.Button()

        self.__origin_message = tk.Message(self.__origin_labelframe)
        self.__origin_message.configure(
            font=self.__body_font,
            text="Desconectado",
            width=100,
            foreground='red')
        self.__origin_message.grid(column=0, row=12)

        # CONNECTIONS[Separator]
        self.__database_separator = ttkb.Separator(self.__connection_main_frame)
        self.__database_separator.configure(orient=tk.HORIZONTAL)
        self.__database_separator.grid(column=1, row=0)

        # CONNECTIONS[Destiny Database]
        self.__destiny_labelframe = ttkb.Labelframe(self.__connection_main_frame)
        self.__destiny_labelframe.configure(labelanchor=tk.N, padding=15, text="Banco de Destino")
        self.__destiny_labelframe.grid(column=2, row=0, sticky=tk.W)
        self.__destiny_labelframe.columnconfigure(0, weight=1)

        self.__ip_destiny_label = ttkb.Label(self.__destiny_labelframe)
        self.__ip_destiny_label.configure(text="Ip do Servidor", font=self.__body_font)
        self.__ip_destiny_label.grid(column=0, row=0)

        self.__ip_destiny_entry = ttkb.Entry(self.__destiny_labelframe)
        self.__ip_destiny_entry.configure(justify=tk.CENTER)
        self.__ip_destiny_entry.grid(column=0, row=1)

        self.__db_destiny_label = ttkb.Label(self.__destiny_labelframe)
        self.__db_destiny_label.configure(text="Nome do Banco", font=self.__body_font)
        self.__db_destiny_label.grid(column=0, row=2)

        self.__db_destiny_entry = ttkb.Entry(self.__destiny_labelframe)
        self.__db_destiny_entry.configure(justify=tk.CENTER)
        self.__db_destiny_entry.grid(column=0, row=3)

        self.__user_destiny_label = ttkb.Label(self.__destiny_labelframe)
        self.__user_destiny_label.configure(text="Usuário", font=self.__body_font)
        self.__user_destiny_label.grid(column=0, row=4)

        self.__user_destiny_entry = ttkb.Entry(self.__destiny_labelframe)
        self.__user_destiny_entry.configure(justify=tk.CENTER)
        self.__user_destiny_entry.grid(column=0, row=5)

        self.__pass_destiny_label = ttkb.Label(self.__destiny_labelframe)
        self.__pass_destiny_label.configure(text="Senha", font=self.__body_font)
        self.__pass_destiny_label.grid(column=0, row=6)

        self.__pass_destiny_entry = ttkb.Entry(self.__destiny_labelframe)
        self.__pass_destiny_entry.configure(justify=tk.CENTER, show='*')
        self.__pass_destiny_entry.grid(column=0, row=7)

        self.__port_destiny_label = ttkb.Label(self.__destiny_labelframe)
        self.__port_destiny_label.configure(text="Porta", font=self.__body_font)
        self.__port_destiny_label.grid(column=0, padx=17, row=8, sticky=tk.W)

        self.__port_destiny_entry = ttkb.Entry(self.__destiny_labelframe)
        self.__port_destiny_entry.configure(justify=tk.CENTER, width=8)
        self.__port_destiny_entry.grid(column=0, row=9, sticky=tk.W)

        self.__id_destiny_label = ttkb.Label(self.__destiny_labelframe)
        self.__id_destiny_label.configure(text="ID Filial", font=self.__body_font)
        self.__id_destiny_label.grid(column=0, row=8, sticky=tk.E, ipadx=5)

        self.__id_destiny_entry = ttkb.Entry(self.__destiny_labelframe)
        self.__id_destiny_entry.configure(justify=tk.CENTER, width=8)
        self.__id_destiny_entry.grid(column=0, row=9, sticky=tk.E)

        self.__conn_destiny_button = ttkb.Button(self.__destiny_labelframe, command=self.__destiny)
        self.__conn_destiny_button.configure(text="Conectar", width=15)
        self.__conn_destiny_button.grid(column=0, pady=10, row=11)

        self.__alert_destiny_button = ttkb.Button()

        self.__destiny_message = tk.Message(self.__destiny_labelframe)
        self.__destiny_message.configure(
            font=self.__body_font,
            text="Desconectado",
            width=100,
            foreground='red')
        self.__destiny_message.grid(column=0, row=12)

        # SETTINGS
        self.__settings_main_frame = ttkb.Frame(self.__tabs_notebook)
        self.__settings_main_frame.configure(padding=15)
        self.__settings_main_frame.grid(sticky=tk.NSEW)
        self.__settings_main_frame.columnconfigure(0, weight=1)
        self.__settings_main_frame.rowconfigure(0, weight=1)

        self.__tabs_notebook.add(self.__settings_main_frame, text="Configurações Gerais")

        self.__settings_labelframe = ttkb.Labelframe(self.__settings_main_frame)
        self.__settings_labelframe.configure(labelanchor=tk.N, padding=20, text="Opções")
        self.__settings_labelframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.__settings_labelframe.columnconfigure(0, weight=1)
        self.__settings_labelframe.rowconfigure(2, weight=1)

        # SETTINGS[Top Options]
        self.__top_options_frame = ttkb.Frame(self.__settings_labelframe)
        self.__top_options_frame.configure(padding=25)
        self.__top_options_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.__top_options_frame.columnconfigure(0, weight=1)
        self.__top_options_frame.columnconfigure(1, weight=1)
        self.__top_options_frame.columnconfigure(2, weight=1)
        self.__top_options_frame.columnconfigure(3, weight=1)
        self.__top_options_frame.columnconfigure(4, weight=1)

        self.__sel_product = tk.BooleanVar()
        self.__sel_product.set(False)
        self.__product_checkbutton = ttkb.Checkbutton(
            self.__top_options_frame,
            command=self.__swap_product)
        self.__product_checkbutton.configure(text="Produto", variable=self.__sel_product)
        self.__product_checkbutton.grid(column=0, row=0)

        self.__sel_bars = tk.BooleanVar()
        self.__sel_bars.set(False)
        self.__bars_checkbutton = ttkb.Checkbutton(self.__top_options_frame)
        self.__bars_checkbutton.configure(
            text="Barras Adicional",
            state=tk.DISABLED,
            variable=self.__sel_bars)
        self.__bars_checkbutton.grid(column=1, row=0)

        self.__sel_stock = tk.BooleanVar()
        self.__sel_stock.set(False)
        self.__stock_checkbutton = ttkb.Checkbutton(self.__top_options_frame)
        self.__stock_checkbutton.configure(
            text="Estoque",
            state=tk.DISABLED,
            variable=self.__sel_stock)
        self.__stock_checkbutton.grid(column=2, row=0)

        self.__sel_partition = tk.BooleanVar()
        self.__sel_partition.set(False)
        self.__partition_checkbutton = ttkb.Checkbutton(self.__top_options_frame)
        self.__partition_checkbutton.configure(
            text="Lote",
            state=tk.DISABLED,
            variable=self.__sel_partition)
        self.__partition_checkbutton.grid(column=3, row=0)

        self.__sel_price = tk.BooleanVar()
        self.__sel_price.set(False)
        self.__price_checkbutton = ttkb.Checkbutton(self.__top_options_frame)
        self.__price_checkbutton.configure(
            text="Preço Filial",
            state=tk.DISABLED,
            variable=self.__sel_price)
        self.__price_checkbutton.grid(column=4, row=0)

        # SETTINGS[Top Separator]
        self.__top_separator = ttkb.Separator(self.__settings_labelframe)
        self.__top_separator.configure(orient=tk.HORIZONTAL)
        self.__top_separator.grid(column=0, row=1, sticky=tk.EW)

        # SETTINGS[Mid Options]
        self.__mid_options_frame = ttkb.Frame(self.__settings_labelframe)
        self.__mid_options_frame.configure(padding=25)
        self.__mid_options_frame.grid(column=0, row=2, sticky=tk.EW)
        self.__mid_options_frame.columnconfigure(0, weight=1)
        self.__mid_options_frame.columnconfigure(1, weight=1)
        self.__mid_options_frame.rowconfigure(0, weight=1)

        # SETTINGS[Mid Options][Principle]
        self.__principle_labelframe = ttkb.Labelframe(self.__mid_options_frame)
        self.__principle_labelframe.configure(
            text="Principio Ativo",
            labelanchor=tk.N,
            padding=10,
            borderwidth=0)
        self.__principle_labelframe.grid(column=0, row=0, sticky=tk.NW)

        self.__sel_principle_desc = tk.BooleanVar()
        self.__sel_principle_desc.set(False)
        self.__principle_desc_checkbutton = ttkb.Checkbutton(
            self.__principle_labelframe,
            command=self.__swap_principle)
        self.__principle_desc_checkbutton.configure(
            text="Por Descrição",
            variable=self.__sel_principle_desc,
            padding=5)
        self.__principle_desc_checkbutton.grid(column=0, row=0)

        self.__sel_principle_id = tk.BooleanVar()
        self.__sel_principle_id.set(False)
        self.__principle_id_checkbutton = ttkb.Checkbutton(
            self.__principle_labelframe,
            command=self.__swap_principle)
        self.__principle_id_checkbutton.configure(
            text="Por ID",
            variable=self.__sel_principle_id,
            padding=5)
        self.__principle_id_checkbutton.grid(column=1, row=0)

        self.__principle_id_entry = ttkb.Entry(self.__principle_labelframe)
        self.__principle_id_entry.configure(justify=tk.CENTER, width=2)
        self.__principle_id_entry.grid(column=2, row=0)

        self.__principle_id_label = ttkb.Label(self.__principle_labelframe)
        self.__principle_id_label.configure(text="Id de Destino", padding=5)
        self.__principle_id_label.grid(column=3, row=0)

        # SETTINGS[Middle Options][Manufacturer]
        self.__manufacturer_labelframe = ttkb.Labelframe(self.__mid_options_frame)
        self.__manufacturer_labelframe.configure(
            text="Fabricante",
            labelanchor=tk.N,
            padding=10,
            borderwidth=0)
        self.__manufacturer_labelframe.grid(column=1, row=0, sticky=tk.NE)

        self.__sel_manufacturer_cnpj = tk.BooleanVar()
        self.__sel_manufacturer_cnpj.set(False)
        self.__manufacturer_cnpj_checkbutton = ttkb.Checkbutton(
            self.__manufacturer_labelframe,
            command=self.__swap_manufacturer)
        self.__manufacturer_cnpj_checkbutton.configure(
            text="Por CNPJ",
            variable=self.__sel_manufacturer_cnpj,
            padding=5)
        self.__manufacturer_cnpj_checkbutton.grid(column=0, row=0)

        self.__sel_manufacturer_id = tk.BooleanVar()
        self.__sel_manufacturer_id.set(False)
        self.__manufacturer_id_checkbutton = ttkb.Checkbutton(
            self.__manufacturer_labelframe,
            command=self.__swap_manufacturer)
        self.__manufacturer_id_checkbutton.configure(
            text="Por ID",
            variable=self.__sel_manufacturer_id,
            padding=5)
        self.__manufacturer_id_checkbutton.grid(column=1, row=0)

        self.__manufacturer_id_entry = ttkb.Entry(self.__manufacturer_labelframe)
        self.__manufacturer_id_entry.configure(justify=tk.CENTER, width=2)
        self.__manufacturer_id_entry.grid(column=2, row=0)

        self.__manufacturer_id_label = ttkb.Label(self.__manufacturer_labelframe)
        self.__manufacturer_id_label.configure(text="Id de Destino", padding=5)
        self.__manufacturer_id_label.grid(column=3, row=0)

        # SETTINGS[Bottom Separator]
        self.__bottom_separator = ttkb.Separator(self.__settings_labelframe)
        self.__bottom_separator.configure(orient=tk.HORIZONTAL)
        self.__bottom_separator.grid(column=0, row=3, sticky=tk.EW)

        # SETTINGS[Bottom Options]
        self.__bottom_options_frame = ttkb.Frame(self.__settings_labelframe)
        self.__bottom_options_frame.configure(padding=20)
        self.__bottom_options_frame.grid(column=0, row=4, sticky=tk.SW)
        self.__bottom_options_frame.columnconfigure(0, weight=1)
        self.__bottom_options_frame.columnconfigure(1, weight=1)
        self.__bottom_options_frame.columnconfigure(2, weight=1)
        self.__bottom_options_frame.rowconfigure(0, weight=1)
        self.__bottom_options_frame.rowconfigure(1, weight=1)

        # SETTINGS[Bottom Options][Options]
        self.__sel_productbar = tk.BooleanVar()
        self.__sel_productbar.set(False)
        self.__productbar_checkbutton = ttkb.Checkbutton(self.__bottom_options_frame)
        self.__productbar_checkbutton.configure(
            text="Não importar produtos com barras que iniciam com",
            variable=self.__sel_productbar)
        self.__productbar_checkbutton.grid(column=0, row=0, sticky=tk.W)

        self.__value_zeros_spinbox = tk.StringVar(value='1')
        self.__zeros_spinbox = ttkb.Spinbox(self.__bottom_options_frame)
        self.__zeros_spinbox.configure(
            from_=1,
            to=12,
            textvariable=self.__value_zeros_spinbox,
            width=2)
        self.__zeros_spinbox.grid(column=1, row=0, sticky=tk.W)

        self.__zeros_label = ttkb.Label(self.__bottom_options_frame)
        self.__zeros_label.configure(text="ou mais zero(s).")
        self.__zeros_label.grid(column=2, row=0, sticky=tk.W)

        self.__sel_erased = tk.BooleanVar()
        self.__sel_erased.set(False)
        self.__erased_checkbutton = ttkb.Checkbutton(self.__bottom_options_frame)
        self.__erased_checkbutton.configure(
            text="Não importar registros marcados como apagados.",
            variable=self.__sel_erased)
        self.__erased_checkbutton.grid(column=0, row=1, sticky=tk.W)

        # PRODUCT GROUPS
        self.__groups_main_frame = ttkb.Frame(self.__tabs_notebook)
        self.__groups_main_frame.configure(padding=10)
        self.__groups_main_frame.grid(sticky=tk.NSEW)
        self.__groups_main_frame.rowconfigure(0, weight=1)
        self.__groups_main_frame.columnconfigure(0, weight=1)
        self.__groups_main_frame.columnconfigure(1, weight=1)

        self.__tabs_notebook.add(self.__groups_main_frame, text="Grupos de Produtos")

        # PRODUCT GROUPS[Origin Database]
        self.__groups_origin_frame = ttkb.Frame(self.__groups_main_frame)
        self.__groups_origin_frame.configure(padding=5)
        self.__groups_origin_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.__groups_origin_frame.rowconfigure(0, weight=1)
        self.__groups_origin_frame.columnconfigure(0, weight=1)

        self.__groups_origin_labelframe = ttkb.Labelframe(self.__groups_origin_frame)
        self.__groups_origin_labelframe.configure(
            labelanchor=tk.N,
            text="Grupos de Origem",
            borderwidth=0,
            padding=5)
        self.__groups_origin_labelframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.__groups_origin_labelframe.columnconfigure(0, weight=1)
        self.__groups_origin_labelframe.rowconfigure(0, weight=1)

        self.__groups_origin_checkboxtreeview = CheckboxTreeview(self.__groups_origin_labelframe)
        self.__groups_origin_checkboxtreeview.grid(column=0, row=0, sticky=tk.NSEW)
        self.__groups_origin_checkboxtreeview.configure(height=20)
        self.__groups_origin_checkboxtreeview['columns'] = ('Novo ID', 'ID', 'Nome')
        self.__groups_origin_checkboxtreeview.column('#0', width=30, stretch=False)
        self.__groups_origin_checkboxtreeview.column('Novo ID', anchor=tk.CENTER, width=70, stretch=False)
        self.__groups_origin_checkboxtreeview.column('ID', anchor=tk.CENTER, width=30, stretch=False)
        self.__groups_origin_checkboxtreeview.column('Nome', anchor=tk.W, width=160, stretch=True)
        self.__groups_origin_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.__groups_origin_checkboxtreeview.heading('Novo ID', text='Novo ID', anchor=tk.CENTER)
        self.__groups_origin_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.__groups_origin_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.__sel_erased_origin_groups = tk.BooleanVar()
        self.__sel_erased_origin_groups.set(False)
        self.__erased_groups_origin_checkbutton = ttkb.Checkbutton(
            self.__groups_origin_frame,
            command=self.__origin_groups)
        self.__erased_groups_origin_checkbutton.configure(
            text="Não mostrar grupos apagados",
            variable=self.__sel_erased_origin_groups)
        self.__erased_groups_origin_checkbutton.grid(column=0, row=1, sticky=tk.NW)

        self.__sel_all_origin_groups = tk.BooleanVar()
        self.__sel_all_origin_groups.set(False)
        self.__all_origin_groups_checkbutton = ttkb.Checkbutton(
            self.__groups_origin_frame,
            command=self.__tag_all_groups)
        self.__all_origin_groups_checkbutton.configure(
            text="Selecionar todos",
            variable=self.__sel_all_origin_groups)
        self.__all_origin_groups_checkbutton.grid(column=0, row=1, sticky=tk.NE)

        # PRODUCT GROUPS[Destiny Database]
        self.__groups_destiny_frame = ttkb.Frame(self.__groups_main_frame)
        self.__groups_destiny_frame.configure(padding=5)
        self.__groups_destiny_frame.grid(column=1, row=0, sticky=tk.NSEW)
        self.__groups_destiny_frame.rowconfigure(0, weight=1)
        self.__groups_destiny_frame.columnconfigure(0, weight=1)

        self.__groups_destiny_labelframe = ttkb.Labelframe(self.__groups_destiny_frame)
        self.__groups_destiny_labelframe.configure(
            labelanchor=tk.N,
            text="Grupos de Destino",
            borderwidth=0,
            padding=5)
        self.__groups_destiny_labelframe.grid(column=0, row=0, sticky=tk.NSEW)
        self.__groups_destiny_labelframe.columnconfigure(0, weight=1)
        self.__groups_destiny_labelframe.rowconfigure(0, weight=1)

        self.__groups_destiny_checkboxtreeview = CheckboxTreeview(self.__groups_destiny_labelframe)
        self.__groups_destiny_checkboxtreeview.grid(column=0, row=0, sticky=tk.NSEW)
        self.__groups_destiny_checkboxtreeview.configure(height=20)
        self.__groups_destiny_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.__groups_destiny_checkboxtreeview.column('#0', width=0, stretch=False)
        self.__groups_destiny_checkboxtreeview.column('ID', anchor=tk.CENTER, width=50, stretch=False)
        self.__groups_destiny_checkboxtreeview.column('Nome', anchor=tk.W, width=160, stretch=True)
        self.__groups_destiny_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.__groups_destiny_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.__groups_destiny_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.__sel_erased_destiny_groups = tk.BooleanVar()
        self.__sel_erased_destiny_groups.set(False)
        self.__erased_groups_destiny_checkbutton = ttkb.Checkbutton(
            self.__groups_destiny_frame,
            command=self.__destiny_groups)
        self.__erased_groups_destiny_checkbutton.configure(
            text="Não mostrar grupos apagados",
            variable=self.__sel_erased_destiny_groups)
        self.__erased_groups_destiny_checkbutton.grid(column=0, row=1, sticky=tk.NW)

        # SUPPLIER|BILLS
        self.__supplier_main_frame = ttkb.Frame(self.__tabs_notebook)
        self.__supplier_main_frame.configure(padding=15)
        self.__supplier_main_frame.grid(sticky=tk.EW)
        self.__supplier_main_frame.columnconfigure(0, weight=1)
        self.__supplier_main_frame.rowconfigure(0, weight=1)
        self.__supplier_main_frame.rowconfigure(1, weight=1)

        self.__tabs_notebook.add(self.__supplier_main_frame, text="Fornecedores e Pagar")

        # SUPPLIER|BILLS[Top Options]
        self.__supplier_options_frame = ttkb.Frame(self.__supplier_main_frame)
        self.__supplier_options_frame.grid(column=0, row=0, sticky=tk.EW)
        self.__supplier_options_frame.columnconfigure(0, weight=1)

        self.__supplier_options_labelframe = ttkb.Labelframe(self.__supplier_options_frame)
        self.__supplier_options_labelframe.configure(labelanchor=tk.N, padding=15, text="Opções")
        self.__supplier_options_labelframe.grid(row=0, column=0, sticky=tk.EW)
        self.__supplier_options_labelframe.columnconfigure(0, weight=1)
        self.__supplier_options_labelframe.columnconfigure(1, weight=1)

        self.__sel_suppliers = tk.BooleanVar()
        self.__sel_suppliers.set(False)
        self.__suppliers_checkbutton = ttkb.Checkbutton(self.__supplier_options_labelframe)
        self.__suppliers_checkbutton.configure(text="Fornecedores", variable=self.__sel_suppliers)
        self.__suppliers_checkbutton.grid(row=0, column=0)

        self.__sel_bills = tk.BooleanVar()
        self.__sel_bills.set(False)
        self.__bills_checkbutton = ttkb.Checkbutton(self.__supplier_options_labelframe)
        self.__bills_checkbutton.configure(text="Pagar", variable=self.__sel_bills)
        self.__bills_checkbutton.grid(row=0, column=1)

        # SUPPLIER|BILLS[Mid & Bottom Options]
        self.__suppliers_checkboxtreeview = CheckboxTreeview(self.__supplier_main_frame)
        self.__suppliers_checkboxtreeview.grid(row=1, column=0, sticky=tk.NSEW)
        self.__suppliers_checkboxtreeview.configure(height=20)
        self.__suppliers_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.__suppliers_checkboxtreeview.column('#0', width=40, stretch=False)
        self.__suppliers_checkboxtreeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.__suppliers_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.__suppliers_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.__suppliers_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.__suppliers_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.__sel_all_suppliers = tk.BooleanVar()
        self.__sel_all_suppliers.set(False)
        self.__all_suppliers_checkbutton = ttkb.Checkbutton(
            self.__supplier_main_frame,
            command=self.__tag_all_suppliers)
        self.__all_suppliers_checkbutton.configure(
            text="Selecionar todos",
            variable=self.__sel_all_suppliers,
            padding=5)
        self.__all_suppliers_checkbutton.grid(row=2, column=0, sticky=tk.NE)

        # COMPANIES|CUSTOMERS|ACCOUNTS
        self.__company_main_frame = ttkb.Frame(self.__tabs_notebook)
        self.__company_main_frame.configure(padding=15)
        self.__company_main_frame.grid(sticky=tk.EW)
        self.__company_main_frame.columnconfigure(0, weight=1)
        self.__company_main_frame.rowconfigure(0, weight=1)
        self.__company_main_frame.rowconfigure(1, weight=1)

        self.__tabs_notebook.add(self.__company_main_frame, text="Empresas e Clientes")

        # COMPANIES|CUSTOMERS|ACCOUNTS[Top Options]
        self.__company_options_frame = ttkb.Frame(self.__company_main_frame)
        self.__company_options_frame.grid(column=0, row=0, sticky=tk.EW)
        self.__company_options_frame.columnconfigure(0, weight=1)

        self.__companies_options_labelframe = ttkb.Labelframe(self.__company_options_frame)
        self.__companies_options_labelframe.configure(labelanchor=tk.N, padding=15, text="Opções")
        self.__companies_options_labelframe.grid(row=0, column=0, sticky=tk.EW)
        self.__companies_options_labelframe.columnconfigure(0, weight=1)
        self.__companies_options_labelframe.columnconfigure(1, weight=1)

        self.__sel_companies = tk.BooleanVar()
        self.__sel_companies.set(False)
        self.__companies_checkbutton = ttkb.Checkbutton(self.__companies_options_labelframe)
        self.__companies_checkbutton.configure(
            text="Empresas e Clientes",
            variable=self.__sel_companies)
        self.__companies_checkbutton.grid(row=0, column=0)

        self.__sel_accounts_receivable = tk.BooleanVar()
        self.__sel_accounts_receivable.set(False)
        self.__accounts_receivable_checkbutton = ttkb.Checkbutton(
            self.__companies_options_labelframe)
        self.__accounts_receivable_checkbutton.configure(
            text="Receber",
            variable=self.__sel_accounts_receivable)
        self.__accounts_receivable_checkbutton.grid(row=0, column=1)

        # COMPANIES|CUSTOMERS|ACCOUNTS[Mid & Bottom Options]
        self.__companies_checkboxtreeview = CheckboxTreeview(self.__company_main_frame)
        self.__companies_checkboxtreeview.grid(row=1, column=0, sticky=tk.NSEW)
        self.__companies_checkboxtreeview.configure(height=20)
        self.__companies_checkboxtreeview['columns'] = ('ID', 'Nome')
        self.__companies_checkboxtreeview.column('#0', width=40, stretch=False)
        self.__companies_checkboxtreeview.column('ID', anchor=tk.CENTER, width=120, stretch=False)
        self.__companies_checkboxtreeview.column('Nome', anchor=tk.W, width=120, stretch=True)
        self.__companies_checkboxtreeview.heading('#0', text='', anchor=tk.CENTER)
        self.__companies_checkboxtreeview.heading('ID', text='ID', anchor=tk.CENTER)
        self.__companies_checkboxtreeview.heading('Nome', text='Nome', anchor=tk.W)

        self.__sel_all_companies = tk.BooleanVar()
        self.__sel_all_companies.set(False)
        self.__all_companies_checkbutton = ttkb.Checkbutton(
            self.__company_main_frame,
            command=self.__tag_all_companies)
        self.__all_companies_checkbutton.configure(
            text="Selecionar todos",
            variable=self.__sel_all_companies,
            padding=5)
        self.__all_companies_checkbutton.grid(row=2, column=0, sticky=tk.NE)

        # LOGS
        self.__log_main_frame = ttkb.Frame(self.__tabs_notebook)
        self.__log_main_frame.configure(padding=15)
        self.__log_main_frame.grid(sticky=tk.NSEW)
        self.__log_main_frame.columnconfigure(0, weight=1)
        self.__log_main_frame.rowconfigure(0, weight=1)

        self.__tabs_notebook.add(self.__log_main_frame, text="Execução e Logs")

        self.__logs_scrolledtext = ttkb.ScrolledText(self.__log_main_frame)
        self.__logs_scrolledtext.configure(font=self.__body_font, height=20)
        self.__logs_scrolledtext.grid(row=0, column=0, sticky=tk.EW)

        self.__log_bottom_frame = ttkb.Frame(self.__log_main_frame)
        self.__log_bottom_frame.configure(padding=10)
        self.__log_bottom_frame.grid(column=0, row=1, sticky=tk.EW)
        self.__log_bottom_frame.rowconfigure(0, weight=1)
        self.__log_bottom_frame.columnconfigure(0, weight=1)
        self.__log_bottom_frame.columnconfigure(1, weight=1)
        self.__log_bottom_frame.columnconfigure(2, weight=1)

        self.__start_button = ttkb.Button(self.__log_bottom_frame, command=self.__start)
        self.__start_button.configure(text="Iniciar", width=20)
        self.__start_button.grid(row=0, column=0)

        self.__progressbar = ttkb.Progressbar(self.__log_bottom_frame, mode='determinate')
        self.__progressbar.configure(length=450, orient=tk.HORIZONTAL)
        self.__progressbar.grid(row=0, column=1)

        self.__done_message = tk.Message(self.__log_bottom_frame, font=self.__body_font)
        self.__done_message.configure(
            text="Não Iniciado",
            width=125,
            foreground='grey',
            relief=tk.FLAT,
            borderwidth=1)
        self.__done_message.grid(row=0, column=2)

        # DOCS
        self.__documentation_main_frame = ttkb.Frame(self.__tabs_notebook)
        self.__documentation_main_frame.configure(padding=15)
        self.__documentation_main_frame.grid(sticky=tk.NSEW)
        self.__documentation_main_frame.columnconfigure(0, weight=1)
        self.__documentation_main_frame.rowconfigure(0, weight=1)

        self.__tabs_notebook.add(self.__documentation_main_frame, text="Documentação")

        self.__documentation_scrolledtext = ttkb.ScrolledText(self.__documentation_main_frame)
        self.__documentation_scrolledtext.insert(tk.END, doc.INFO_DOC)
        self.__documentation_scrolledtext.configure(
            state=tk.DISABLED,
            borderwidth=5,
            font=self.__body_font,
            height=20)
        self.__documentation_scrolledtext.grid(sticky=tk.NSEW)

        # BIND
        self.__groups_origin_checkboxtreeview.bind("<Double-1>", self.__double_click)

    # BIND METHODS

    @staticmethod
    def __focus_out(event):
        event.widget.destroy()

    def __double_click(self, event):

        click_region = self.__groups_origin_checkboxtreeview.identify_region(event.x, event.y)

        if click_region not in ("tree", "cell"):
            return None

        column = self.__groups_origin_checkboxtreeview.identify_column(event.x)
        column_index = int(column[1:]) - 1

        selected_iid = self.__groups_origin_checkboxtreeview.focus()
        selected_values = self.__groups_origin_checkboxtreeview.item(selected_iid)
        selected_line = None

        if column != '#1':
            print("Invalid column")
        else:
            selected_line = selected_values.get('values')[column_index]

        column_box = self.__groups_origin_checkboxtreeview.bbox(selected_iid, column)

        temp_entry = ttk.Entry(self.__groups_origin_checkboxtreeview)
        temp_entry.column_identifier = column_index
        temp_entry.iid_identifier = selected_iid
        temp_entry.insert(0, selected_line)
        temp_entry.select_range(0, tk.END)

        temp_entry.focus()
        temp_entry.bind("<FocusOut>", self.__focus_out)
        temp_entry.bind("<Return>", self.__press_enter)

        temp_entry.place(x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3])

    def __press_enter(self, event):

        new_text = event.widget.get()
        selected_iid = event.widget.iid_identifier
        column_index = event.widget.column_identifier

        if column_index == 0:
            current_value = self.__groups_origin_checkboxtreeview.item(selected_iid).get('values')
            current_value[column_index] = new_text
            self.__groups_origin_checkboxtreeview.item(selected_iid, values=current_value)

        event.widget.destroy()

    # CONNECTION METHODS

    def __origin(self):

        db_origin: dict = {'host': self.__ip_origin_entry.get(),
                           'user': self.__user_origin_entry.get(),
                           'password': self.__pass_origin_entry.get(),
                           'database': self.__db_origin_entry.get(),
                           'port': int(self.__port_origin_entry.get())}

        log_return = run.connect_origin(db_origin)

        if log_return['return'] == 'Connected':
            self.__alert_origin_button.destroy()
            self.__origin_message.configure(text="Conectado", foreground='green')

            self.__origin_groups()
            self.__companies()
            self.__suppliers()

        else:
            self.__alert_origin_button.destroy()
            self.__origin_message.configure(text="Falha", foreground='orange')
            self.__origin_alert(log_return['cod'], log_return['description'])
            self.__alert_origin_button.place(anchor=tk.W, height=22, width=22, x=30, y=323)

    def __destiny(self):

        db_destiny: dict = {'host': self.__ip_destiny_entry.get(),
                            'user': self.__user_destiny_entry.get(),
                            'password': self.__pass_destiny_entry.get(),
                            'database': self.__db_destiny_entry.get(),
                            'port': int(self.__port_destiny_entry.get())}

        log_return = run.connect_destiny(db_destiny)

        if log_return['return'] == 'Connected':
            self.__alert_destiny_button.destroy()
            self.__destiny_message.configure(text="Conectado", foreground='green')
            self.__destiny_groups()

        else:
            self.__alert_destiny_button.destroy()
            self.__destiny_message.configure(text="Falha", foreground='orange')
            self.__destiny_alert(log_return['cod'], log_return['description'])
            self.__alert_destiny_button.place(anchor=tk.W, height=22, width=22, x=30, y=323)

    def __origin_alert(self, cod_error, desc_error):

        alert_image = tk.PhotoImage(file="imgs/info.png")
        self.__alert_origin_button = ttkb.Button(
            self.__origin_labelframe,
            image=alert_image,
            command=lambda: self.__return_error(cod_error, desc_error),
            bootstyle=ttkb.WARNING)
        self.__alert_origin_button.configure(compound=tk.LEFT, padding=1)

    def __destiny_alert(self, cod_error, desc_error):

        alert_image = tk.PhotoImage(file="imgs/info.png")
        self.__alert_destiny_button = ttkb.Button(
            self.__destiny_labelframe,
            image=alert_image,
            command=lambda: self.__return_error(cod_error, desc_error),
            bootstyle=ttkb.WARNING)
        self.__alert_destiny_button.configure(compound=tk.LEFT, padding=1)

    def __return_error(self, cod_error, desc_error):

        error = f"Código: {cod_error} | Descrição: {desc_error}"

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
        error_label.configure(text=error)
        error_label.grid(column=1, row=1)

    def __log(self, method=None, error_register=None, error_return=None):

        logging.basicConfig(filename='log.txt',
                            level=logging.DEBUG,
                            format='%(asctime)s:%(message)s')
        separator = "| ========================================================================== |"
        indentation = "| "

        if method:
            self.__logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            self.__logs_scrolledtext.insert(tk.INSERT, f"{indentation}{method}\n")
            self.__logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            logging.warning(separator)
            logging.warning("| %s", method)
            logging.warning(separator)

        if error_register or error_return:
            self.__logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            self.__logs_scrolledtext.insert(tk.INSERT, f"{indentation}{error_register}\n")
            self.__logs_scrolledtext.insert(tk.INSERT, f"{indentation}{error_return}\n")
            self.__logs_scrolledtext.insert(tk.INSERT, f"{separator}\n")
            logging.warning(separator)
            logging.warning("| %s", error_register)
            logging.warning("| %s", error_return)
            logging.warning(separator)

    # LISTING METHODS

    def __origin_groups(self):

        index: int = 0
        option_selected: dict = {'database': 'origin'}

        try:
            if self.__sel_erased_origin_groups.get():

                option_selected.update({'option': 'filtered'})
                groups = run.get_groups(option_selected)
                self.__iid_origin_groups: list[int] = []

                for group in groups:
                    self.__groups_origin_checkboxtreeview.insert(
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
                    self.__groups_origin_checkboxtreeview.insert(
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
            if self.__sel_erased_destiny_groups.get():

                option_selected.update({'option': 'filtered'})
                groups = run.get_groups(option_selected)

                for group in groups:
                    self.__groups_destiny_checkboxtreeview.insert(
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
                    self.__groups_destiny_checkboxtreeview.insert(
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
            self.__iid_companies: list[int] = []

            for company in companies:
                self.__companies_checkboxtreeview.insert(
                    "",
                    index='end',
                    iid=index,
                    text='',
                    values=(company['id_empresa'], company['nome_fantasia']))
                self.__iid_companies.append(index)
                index += 1

        except Exception as error:
            print(f"Exception in method companies_listing: {error}")

    def __suppliers(self):

        try:
            suppliers = run.get_suppliers()
            index: int = 0
            self.__iid_suppliers: list[int] = []

            for supplier in suppliers:
                self.__suppliers_checkboxtreeview.insert(
                    "",
                    index='end',
                    iid=index,
                    text='',
                    values=(supplier['id_fornecedor'], supplier['razao_social']))
                self.__iid_suppliers.append(index)
                index += 1

        except Exception as error:
            print(f"Exception in method suppliers_listing: {error}")

    # TAG METHODS

    def __tag_all_companies(self):

        for iid in self.__iid_companies:
            self.__companies_checkboxtreeview.change_state(item=iid, state='checked')

    def __tag_all_suppliers(self):

        for iid in self.__iid_suppliers:
            self.__suppliers_checkboxtreeview.change_state(item=iid, state='checked')

    def __tag_all_groups(self):

        for iid in self.__iid_origin_groups:
            self.__groups_origin_checkboxtreeview.change_state(item=iid, state='checked')

    # COLLECT METHODS

    def __get_companies(self):

        companies: int = []

        for company in self.__companies_checkboxtreeview.get_checked():
            company_id = self.__companies_checkboxtreeview.item(item=company, option='values')
            companies.append(company_id[0])
        selected_companies: int = tuple(companies)

        return selected_companies

    def __get_suppliers(self):

        suppliers: int = []

        for supplier in self.__suppliers_checkboxtreeview.get_checked():
            supplier_id = self.__suppliers_checkboxtreeview.item(item=supplier, option='values')
            suppliers.append(supplier_id[0])
        selected_suppliers = tuple(suppliers)

        return selected_suppliers

    def __get_groups(self):

        selected_groups = []

        for group in self.__groups_origin_checkboxtreeview.get_checked():
            values = self.__groups_origin_checkboxtreeview.item(item=group, option='values')
            selected_group = {'novo_id': int(values[0]), 'antigo_id': int(values[1])}
            selected_groups.append(selected_group)

        return selected_groups

    def __return_destiny_communicator(self):

        branch_id: str = str(self.__id_destiny_entry.get())
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
        return self.__id_origin_entry.get()

    def __return_destiny_branch_id(self):
        return self.__id_destiny_entry.get()

    # SWAP BUTTONS METHODS

    def __swap_manufacturer(self):

        if self.__sel_manufacturer_cnpj.get():
            self.__manufacturer_id_checkbutton.configure(state=tk.DISABLED)
            self.__manufacturer_id_entry.configure(state=tk.DISABLED)
        else:
            self.__manufacturer_id_checkbutton.configure(state=tk.NORMAL)
            self.__manufacturer_id_entry.configure(state=tk.NORMAL)

        if self.__sel_manufacturer_id.get():
            self.__manufacturer_cnpj_checkbutton.configure(state=tk.DISABLED)
        else:
            self.__manufacturer_cnpj_checkbutton.configure(state=tk.NORMAL)

    def __swap_principle(self):

        if self.__sel_principle_desc.get():
            self.__principle_id_checkbutton.configure(state=tk.DISABLED)
            self.__principle_id_entry.configure(state=tk.DISABLED)
        else:
            self.__principle_id_checkbutton.configure(state=tk.NORMAL)
            self.__principle_id_entry.configure(state=tk.NORMAL)

        if self.__sel_principle_id.get():
            self.__principle_desc_checkbutton.configure(state=tk.DISABLED)
        else:
            self.__principle_desc_checkbutton.configure(state=tk.NORMAL)

    def __swap_product(self):

        if self.__sel_product.get():
            self.__bars_checkbutton.configure(state=tk.NORMAL)
            self.__stock_checkbutton.configure(state=tk.NORMAL)
            self.__partition_checkbutton.configure(state=tk.NORMAL)
            self.__price_checkbutton.configure(state=tk.NORMAL)

        else:
            self.__bars_checkbutton.configure(state=tk.DISABLED)
            self.__stock_checkbutton.configure(state=tk.DISABLED)
            self.__partition_checkbutton.configure(state=tk.DISABLED)
            self.__price_checkbutton.configure(state=tk.DISABLED)

    def __progress_bar(self):
        self.__progressbar['value'] += 5

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
                           'quantidade_zeros_barras': int(self.__zeros_spinbox.get())}

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

        self.__progressbar['value'] = 0
        self.__done_message.configure(text="Em Andamento", width=125, foreground='orange')
        self.__log(method='Integração Iniciada.')

        # MARKERS
        if self.__sel_erased.get():
            erased = True

        if self.__sel_manufacturer_cnpj.get():
            module_marker.update({'fabricante': True})

        if self.__sel_principle_desc.get():
            module_marker.update({'principio_ativo': True})

        if self.__sel_product.get():
            module_marker.update({'produto': True})

        if self.__sel_bars.get():
            module_marker.update({'barras': True})

        if self.__sel_stock.get():
            module_marker.update({'estoque': True})

        if self.__sel_partition.get():
            module_marker.update({'lote': True})

        if self.__sel_price.get():
            module_marker.update({'preco_filial': True})

        if self.__sel_suppliers.get():
            module_marker.update({'fornecedor': True})

        if self.__sel_bills.get():
            module_marker.update({'pagar': True})

        if self.__sel_companies.get():
            module_marker.update({'empresa': True})
            module_marker.update({'cliente': True})

        if self.__sel_accounts_receivable.get():
            module_marker.update({'receber': True})

        if self.__sel_productbar.get():
            product_options.update({'remover_produtos_barras_zerados': True})

        if self.__sel_manufacturer_cnpj.get():
            product_options.update({'fabricante_por_cnpj': True})

        if self.__sel_manufacturer_id.get():
            product_options.update({'fabricante_por_id': True})

        if self.__sel_principle_desc.get():
            product_options.update({'principio_por_desc': True})

        if self.__sel_principle_id.get():
            product_options.update({'principio_por_id': True})

        options.update({'erased': erased})
        options.update({'module_marker': module_marker})
        options.update({'product_options': product_options})
        options.update({'communicator': self.__return_destiny_communicator()})
        options.update({'origin_branch_id': int(self.__return_origin_branch_id())})
        options.update({'destiny_branch_id': int(self.__return_destiny_branch_id())})
        options.update({'manufacturer_id': self.__manufacturer_id_entry.get()})
        options.update({'principle_id': self.__principle_id_entry.get()})
        options.update({'selected_companies': self.__get_companies()})
        options.update({'selected_groups': self.__get_groups()})
        options.update({'selected_suppliers': self.__get_suppliers()})

        # START PROCESS
        run.start_process(**options)

        # PROCESS LOGS
        all_logs = run.get_log()

        if self.__sel_manufacturer_cnpj.get():
            self.__log(method='Processamento de Fabricantes Iniciado.')

            if all_logs['manufacturer_logs']:
                manufacturer_log = all_logs['manufacturer_logs']

                for manufacturer in manufacturer_log:
                    self.__log(error_register=manufacturer['error_register'],
                             error_return=manufacturer['error_return'])
            self.__log(method='Processamento de Fabricantes Finalizado.')
        self.__progress_bar()

        # PRINCIPLE
        if self.__sel_principle_desc.get():
            self.__log(method='Processamento de Principios Ativos Iniciado.')

            if all_logs['principle_logs']:
                principle_log = all_logs['principle_logs']

                for principle in principle_log:
                    self.__log(error_register=principle['error_register'],
                             error_return=principle['error_return'])
            self.__log(method='Processamento de Principios Ativos Finalizado.')
        self.__progress_bar()

        # PRODUCT
        if self.__sel_product.get():
            self.__log(method='Processamento de Produtos Iniciado.')

            if all_logs['product_logs']:
                product_log = all_logs['product_logs']

                for product in product_log:
                    self.__log(error_register=product['error_register'],
                             error_return=product['error_return'])
            self.__log(method='Processamento de Produtos Finalizado.')
        self.__progress_bar()

        # BARS
        if self.__sel_bars.get():
            self.__log(method='Processamento de Barras Adicionais Iniciado.')

            if all_logs['bar_logs']:
                bar_logs = all_logs['bar_logs']

                for bars in bar_logs:
                    self.__log(error_register=bars['error_register'],
                             error_return=bars['error_return'])
            self.__log(method='Processamento de Barras Adicionais Finalizado.')
        self.__progress_bar()

        # STOCK
        if self.__sel_stock.get():
            self.__log(method='Processamento de Estoque Iniciado.')

            if all_logs['stock_logs']:
                stock_logs = all_logs['stock_logs']

                for stock in stock_logs:
                    self.__log(error_register=stock['error_register'],
                             error_return=stock['error_return'])
            self.__log(method='Processamento de Estoque Finalizado.')
        self.__progress_bar()

        # PARTITION
        if self.__sel_partition.get():
            self.__log(method='Processamento de Lotes Iniciado.')

            if all_logs['partition_logs']:
                partition_logs = all_logs['partition_logs']

                for partition in partition_logs:
                    self.__log(error_register=partition['error_register'],
                             error_return=partition['error_return'])
                self.__log(method='Processamento de Lotes Finalizado.')
        self.__progress_bar()

        # PRICE
        if self.__sel_price.get():
            self.__log(method='Processamento de Preço Filial Iniciado.')

            if all_logs['price_logs']:
                price_logs = all_logs['price_logs']

                for price in price_logs:
                    self.__log(error_register=price['error_register'],
                             error_return=price['error_return'])
                self.__log(method='Processamento de Preço Filial Finalizado.')
        self.__progress_bar()

        # SUPPLIER
        if self.__sel_suppliers.get():
            self.__log(method='Processamento de Fornecedores Iniciado.')

            if all_logs['supplier_logs']:
                supplier_logs = all_logs['supplier_logs']

                for supplier in supplier_logs:
                    self.__log(error_register=supplier['error_register'],
                             error_return=supplier['error_return'])
            self.__log(method='Processamento de Fornecedores Finalizado.')
        self.__progress_bar()

        # BILLS TO PAY
        if self.__sel_bills.get():
            self.__log(method='Processamento de Pagar Iniciado.')

            if all_logs['bill_logs']:
                bill_logs = all_logs['bill_logs']

                for bill in bill_logs:
                    self.__log(error_register=bill['error_register'],
                             error_return=bill['error_return'])
            self.__log(method='Processamento de Pagar Finalizado.')
        self.__progress_bar()

        # COMPANY
        if self.__sel_companies.get():
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
        if self.__sel_accounts_receivable.get():
            self.__log(method='Processamento do Receber Iniciado.')

            if all_logs['account_logs']:
                account_logs = all_logs['account_logs']

                for account in account_logs:
                    self.__log(error_register=account['error_register'],
                             error_return=account['error_return'])
            self.__log(method='Processamento do Receber Finalizado.')
        self.__progress_bar()

        self.__done_message.configure(text="Concluído", foreground='green')
        self.__progressbar['value'] = 100
        self.__log(method='Integração Concluída.')


app = Ui(root)
root.mainloop()
