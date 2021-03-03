from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from subprocess import Popen, PIPE
from kivy.graphics import Color, Rectangle
import sqlite3
from kivy.uix.colorpicker import ColorPicker
from kivy.clock import Clock
from kivy.lang import Builder
from pynput.keyboard import Key, Controller
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout
import pandas as pd

from kivy.uix.togglebutton import ToggleButton

# COLORS #

# rgba(42,62,70,1) VERDE ESCURO
# rgba(43,80,83,1) VERDE MENOS ESCURO
# rgba(67,122,112,1) VERDE MÉDIO
# rgba(200,210,197,1) CLARO FUNDO


createTable_materia_prima = """
CREATE TABLE materia_prima(

nome TEXT PRIMARY KEY,
estoque_maximo REAL NOT NULL,
estoque_minimo REAL NOT NULL,
estoque_emergencial REAL NOT NULL,
rgb TEXT NOT NULL,
estoque_atual REAL NOT NULL

)

"""

createTable_formulas = """
CREATE TABLE formulas(

nome TEXT PRIMARY KEY,
formula TEXT NOT NULL
)

"""

createTable_relatorios_fluxo = """
CREATE TABLE relatorios_fluxo(

id INTEGER PRIMARY KEY AUTOINCREMENT,
produto TEXT NOT NULL,
quantidade TEXT NOT NULL,
dia TEXT NOT NULL,

)

"""

conn_kamaleao = sqlite3.connect('kamaleao.db')
cursor_kamaleao = conn_kamaleao.cursor()

conn = sqlite3.connect('pigmentos.db')
cursor = conn.cursor()

conn_forms = sqlite3.connect('forms.db')
cursor_forms = conn_forms.cursor()
# tempo em sqlite
#time_con =cursor_kamaleao.execute("SELECT datetime('now', 'localtime')")
#time_value = cursor_kamaleao.fetchone()[0]
#print(time_value)


class KamaleãoApp(App):

    def build(self):

        Window.clearcolor = (200 / 255, 210 / 255, 197 / 255, 1)

        layout = GridLayout(cols=2, col_force_default=True, col_default_width=150)

        # pigmentos_table = """

        # CREATE TABLE pigmentos(
        # nome CHAR(20) NOT NULL,
        # estoque FLOAT NOT NULL,
        # misturas INT ,
        # estoque_min float,
        # estoque_emerg float
        # )
        # """

        def ver_tabela(instance):
            def enviar_db(nome):
                def enviar_db_de_vdd(instance):
                    tabela = [nome.split("\n")[0]]
                    nome_do_produto = nome.split("\n")[0]

                    cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?", tabela)
                    estoque_antigo = cursor_kamaleao.fetchone()[0]
                    estoque_novo = estoque_antigo + float(quantidade_adicionar.text)
                    tabela_db = [estoque_novo, nome_do_produto]
                    conn_kamaleao.execute("UPDATE materia_prima set estoque_atual = ? WHERE nome = ?", tabela_db)
                    time_con =cursor_kamaleao.execute("SELECT datetime('now', 'localtime')")
                    time_value = cursor_kamaleao.fetchone()[0]
                    relatorios_tabela = [nome_do_produto,float(quantidade_adicionar.text),time_value]
                    conn_kamaleao.execute("INSERT INTO relatorios_fluxo(produto,quantidade,dia) VALUES (?,?,?)",relatorios_tabela)

                tela_adicionar_estoque = GridLayout(rows=2)
                quantidade_adicionar = TextInput(multiline=False, input_filter='float')
                tela_adicionar_estoque_cima = GridLayout(cols=2)

                tela_adicionar_estoque_cima.add_widget(Label(text="Quantidade à se adicionar ao estoque: "))
                tela_adicionar_estoque_cima.add_widget(quantidade_adicionar)

                tela_adicionar_estoque.add_widget(tela_adicionar_estoque_cima)

                tela_adicionar_estoque_baixo_btt = Button(text="Enviar")
                tela_adicionar_estoque_baixo_btt.bind(on_press=enviar_db_de_vdd)
                tela_adicionar_estoque.add_widget(tela_adicionar_estoque_baixo_btt)

                tela_adicionar_estoque_popup = Popup(title="Adicionar estoque: " + nome,
                                                     content=tela_adicionar_estoque, size_hint=[1, 0.5])
                tela_adicionar_estoque_popup.open()

            layout_tabela = GridLayout(rows=2)
            blocks = GridLayout(rows=7,spacing=20)

            cursor_kamaleao.execute('''SELECT * from materia_prima''')
            result = cursor_kamaleao.fetchall()
            for i in result:
                nome = i[0]
                estoque_maximo=i[1]
                estoque_atual = i[5]
                percent = round((estoque_atual/estoque_maximo)*100,1)
                cor = i[4].replace("[", '')
                cor = cor.replace(']', '')
                cor = cor.split(",")
                for z in range(len(cor)):
                    cor[z] = round(float(cor[z]), 2)
                cor = tuple(cor)

                btn = Button(text="{}\n{}%".format(nome,percent),
                             font_name="fonts/bariol_bold-webfont", background_color=cor,size_hint=(0.3,0.3))
                btn.bind(on_release=lambda btn: enviar_db(btn.text))
                blocks.add_widget(btn)
            layout_tabela.add_widget(blocks)

            aba_estoque_pg = Popup(title="ESTOQUE", content=layout_tabela,)
            aba_estoque_pg.open()


        def forms(instance):
            def enviar_forms(instance):
                formula = {}
                for i in range(len(nome_das_materias_primas_iterate)):
                    if nome_das_materias_primas_iterate[i].text == "" or nome_das_materias_primas_iterate[i].text == ' ':
                        nome_das_materias_primas_iterate[i].text ='0'

                    formula[nomes_mas_materias_primas_string[i]] = nome_das_materias_primas_iterate[i].text

                formula_inteira = str(formula)
                formula_db = [nome_da_formula.text, formula_inteira]
                try:
                    conn_kamaleao.execute("INSERT INTO formulas VALUES(?,?)", formula_db)
                    result = cursor_kamaleao.execute("SELECT * FROM formulas")
                    for f in result:
                        print(f)
                except:
                    print("fórmula já existente")

            formulas_layout = GridLayout(cols=2)
            formulas_layout.add_widget(Label(text="Nome"))
            nome_da_formula = TextInput(multiline=False)
            formulas_layout.add_widget(nome_da_formula)
            cursor_kamaleao.execute("SELECT nome FROM materia_prima")
            result = cursor_kamaleao.fetchall()
            nome_das_materias_primas_iterate = []
            nomes_mas_materias_primas_string = []
            # pegar todos os nomes
            for i in result:
                for z in i:
                    formulas_layout.add_widget(Label(text=str(z)))
                    nomes_mas_materias_primas_string.append(z)
                    globals()[str(z)] = TextInput(multiline=False,input_filter='float')
                    nome_das_materias_primas_iterate.append(globals()[str(z)])
                    formulas_layout.add_widget(globals()[z])

            formulas_layout_btt = Button(text="enviar")


            formulas_layout_btt.bind(on_press=enviar_forms)
            formulas_layout.add_widget(formulas_layout_btt)

            formulas_popup = Popup(title="forms", content=formulas_layout,size_hint=(0.8,0.8))
            formulas_popup.open()

        def simular_tab(instance):
            def on_text(instance, value):
                esqueda_baixo_area_esquerda.clear_widgets()
                texto_atual = [value]
                cursor_kamaleao.execute("SELECT nome FROM formulas WHERE nome LIKE '{}%'".format(value))
                result = cursor_kamaleao.fetchmany(5)
                for i in result:
                    for f in i:
                        esqueda_baixo_area_esquerda.add_widget(Label(text=str(f)))
            # precisa ser declarado antes do botão pq se nao toda vez reseta
            formula_formatada = {}
            esqueda_baixo_area_direita_tabela = []
            def adicionar_cor(instance):
                # insert relatŕoios
                #conn_kamaleao.execute("INSERT INTO relatorios_fluxo(produto,quantidade,dia) VALUES (?,?,?)",relatorios_tabela)

                nome = [nome_da_formula.text]
                direita_tab_content.clear_widgets()
                esqueda_baixo_area_direita.clear_widgets()
                quantidade_que_multiplica_formula = int(quantidade.text)

                cursor_kamaleao.execute("SELECT * FROM formulas WHERE nome = ?",nome)
                try:
                    formula_completa = cursor_kamaleao.fetchone()[1]
                    formula_completa = formula_completa.replace("{",'')
                    formula_completa = formula_completa.replace("}",'')
                    formula_completa = formula_completa.translate({ord("'"):None})
                    formula_completa =formula_completa.split(',')
                    for i in formula_completa:
                        i = i.strip()
                        i = i.split(":")
                        if i[0] in formula_formatada:
                            formula_formatada[i[0]] += float(i[1])*quantidade_que_multiplica_formula
                        else :
                            formula_formatada[i[0]] = float(i[1])*quantidade_que_multiplica_formula
                    for i in formula_formatada:
                        nome = [i]

                        cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?",nome)
                        novo_valor = cursor_kamaleao.fetchone()[0]-formula_formatada.get(i)
                        direita_tab_content.add_widget(Label(text=str(i)))
                        direita_tab_content.add_widget(Label(text=str(novo_valor)))


                        print(novo_valor)
                    esqueda_baixo_area_direita_tabela.append([nome_da_formula.text,quantidade_que_multiplica_formula])
                    for i in esqueda_baixo_area_direita_tabela:
                        esqueda_baixo_area_direita.add_widget(Label(text="{}   x   {}".format(i[0],i[1])))
                except:
                    print("NOME NÃO EXISTE NO BANCO DE DADOS")
                    #('teste', 789.0)
                    #('teste 1', 380.0)
                    #('teste 2', 1500.0)


            def produzir_func(instance):
                for i in formula_formatada:
                    nome = [i]
                    cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?", nome)
                    novo_valor = cursor_kamaleao.fetchone()[0] - formula_formatada.get(i)
                    atualizar_tabela = [novo_valor,i]
                    conn_kamaleao.execute("UPDATE materia_prima SET estoque_atual = ? WHERE nome = ?", atualizar_tabela)
                #RESOLVER RELATORIO DE FORMULAS !
                cursor_kamaleao.execute("SELECT datetime('now', 'localtime')")
                time_value = cursor_kamaleao.fetchone()[0]
                valores_relatorios_producao = [esqueda_baixo_area_direita_tabela[0],esqueda_baixo_area_direita_tabela[1],time_value]
                print("a",valores_relatorios_producao)
                    #funcionar quantidade primeiro antes de gerar relatório
                    #conn_kamaleao.execute("INSERT INTO relatorios_fluxo(produto,quantidade,dia) VALUES (?,?,?)",esqueda_baixo_area_direita_tabela)





            layout_simular_tab = GridLayout(cols=2)

            esquerda_tab = GridLayout(cols=2)

            esquerda_tab.add_widget(Label(text="Nome da fórmula",size_hint=(1,0.2)))
            nome_da_formula = TextInput(size_hint=(1,0.2), multiline=False)
            nome_da_formula.bind(text=on_text)
            esquerda_tab.add_widget(nome_da_formula)

            esquerda_tab.add_widget(Label(text="quantidade desejada",size_hint=(1,0.3)))
            quantidade = TextInput(size_hint=(1,0.2), multiline=False,input_filter='float')
            esquerda_tab.add_widget(quantidade)

            produzir_btt = Button(text="produzir")
            produzir_btt.bind(on_press=produzir_func)

            esquerda_tab.add_widget(produzir_btt)

            adicionar_cor_btt = Button(text="adicionar cor")
            adicionar_cor_btt.bind(on_press=adicionar_cor)
            esquerda_tab.add_widget(adicionar_cor_btt)



            esqueda_baixo_area_esquerda = GridLayout(cols=3)

            esqueda_baixo_area_direita = GridLayout(cols=2)


            esquerda_tab.add_widget(esqueda_baixo_area_esquerda)
            esquerda_tab.add_widget(esqueda_baixo_area_direita)






            limpar_btt = Button(text="limpar")
            esquerda_tab.add_widget(limpar_btt)






            layout_simular_tab.add_widget(esquerda_tab)


            direita_tab = GridLayout(rows=2)
            direita_tab_header = GridLayout(cols=2)

            direita_tab_header.add_widget(Label(text="Nome da matéria prima"))

            direita_tab_header.add_widget(Label(text="quantidade restante em estoque"))
            direita_tab.add_widget(direita_tab_header)

            direita_tab_content = GridLayout(cols=2)

            direita_tab.add_widget(direita_tab_content)

            layout_simular_tab.add_widget(direita_tab)

            simular_tab_popup= Popup(title="PRODUZIR",content=layout_simular_tab,size_hint=(0.8,0.8))
            simular_tab_popup.open()


        ##############side bar###############
        def producao_view(instance):
            menu.clear_widgets()

            menu_estoque_btt = Button(background_normal='img/Botao_estoque.png', color=(0, 0, 0, 0),
                                      pos_hint={"x": 1, "y": 1}, size_hint=(None, None), width=300, height=410,
                                      background_down='img/Botao_estoque.png', border=(0, 0, 0, 0))
            menu_estoque_btt.bind(on_press=ver_tabela)
            menu.add_widget(menu_estoque_btt)

            menu_prod_btt = Button(background_normal='img/Simular.png', color=(0, 0, 0, 0), pos_hint={"x": 1, "y": 1},
                                   size_hint=(None, None), width=300, height=410, background_down='img/Simular.png',
                                   border=(0, 0, 0, 0))
            menu_prod_btt.bind(on_press=simular_tab)
            menu.add_widget(menu_prod_btt)

            menu_forms_btt = Button(background_normal='img/Gerenciar.png', color=(0, 0, 0, 0),
                                    pos_hint={"x": 1, "y": 1},
                                    size_hint=(None, None), width=300, height=410, background_down='img/Gerenciar.png',
                                    border=(0, 0, 0, 0))
            menu_forms_btt.bind(on_press=forms)

            menu.add_widget(menu_forms_btt)

            ###### menu #######

        def estoque_view(instance):
            def gerenciar_materiaPrima_func(instance):
                def adicionar_materiaPrima_func(instance):
                    def on_color(instance, value):
                        pass  # or instance.color

                    def adicionar_no_database(instance):
                        lista_adicionar_materiaPrima_btt = [nome.text, estoque_maximo.text, estoque_minimo.text,
                                                            estoque_emergencial.text, str(clr_picker.color),
                                                            estoque_atual.text]
                        cursor_kamaleao.execute("INSERT INTO materia_prima VALUES(?,?,?,?,?,?)",
                                                lista_adicionar_materiaPrima_btt)
                        #conn_kamaleao.commit()
                        cursor_kamaleao.execute("SELECT * FROM materia_prima")
                        materias_primas_bd = cursor_kamaleao.fetchall()
                        for i in materias_primas_bd:
                            print("i[1]= " + str(i[1]))
                            print("i 0= " + str(i[0]))

                    clr_picker = ColorPicker()
                    layout_adicionar_materiaPrima = GridLayout(cols=2)
                    layout_adicionar_materiaPrima.add_widget(Label(text="Nome",size_hint=(1,0.2)))
                    nome = TextInput(multiline=False,size_hint=(1,0.2))
                    layout_adicionar_materiaPrima.add_widget(nome)
                    layout_adicionar_materiaPrima.add_widget(Label(text="Estoque máximo\n            (g)",size_hint=(1,0.3)))
                    estoque_maximo = TextInput(multiline=False, input_filter='float',size_hint=(1,0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_maximo)
                    layout_adicionar_materiaPrima.add_widget(Label(text="Estoque mínimo\n            (%)",size_hint=(1,0.2)))
                    estoque_minimo = TextInput(multiline=False, input_filter='float',size_hint=(1,0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_minimo)
                    layout_adicionar_materiaPrima.add_widget(Label(text="Estoque Emergencial\n                (%)",size_hint=(1,0.2)))
                    estoque_emergencial = TextInput(multiline=False, input_filter='float',size_hint=(1,0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_emergencial)

                    layout_adicionar_materiaPrima.add_widget((Label(text="Estoque Atual\n          (g)",size_hint=(1,0.2))))
                    estoque_atual = TextInput(multiline=False, input_filter='float',size_hint=(1,0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_atual)

                    layout_adicionar_materiaPrima.add_widget(Label(text="COR"))
                    layout_adicionar_materiaPrima.add_widget(clr_picker)
                    clr_picker.bind(color=on_color)

                    layout_adicionar_materiaPrima.add_widget(Label(text="",size_hint=(1,0.2)))

                    layout_adicionar_materiaPrima_btt = Button(text="Adicionar no DataBase",size_hint=(1,0.2))
                    layout_adicionar_materiaPrima_btt.bind(on_press=adicionar_no_database)
                    layout_adicionar_materiaPrima.add_widget(layout_adicionar_materiaPrima_btt)

                    layout_adicionar_materiaPrima_popup = Popup(title="Adicionar matéria prima",
                                                                content=layout_adicionar_materiaPrima,size_hint=(0.9,0.9))
                    layout_adicionar_materiaPrima_popup.open()

                def modificar_valores_materiaPrima_func(instance):
                    def modificar_valores_de_um(nome_botao, estoque_maximo, estoque_minimo, estoque_emergencial,
                                                estoque_atual):
                        def on_color(instance, value):
                            pass  # or instance.color

                        def modificar_valores_materiaprima_db(instance):
                            tabela_pro_execute = [estoque_maximo.text, estoque_minimo.text,
                                                  estoque_emergencial.text, str(clr_picker.color),
                                                  estoque_atual.text, nome_botao]
                            print(tabela_pro_execute)
                            nome_pra_teste = [nome_botao]
                            cursor_kamaleao.execute("SELECT * from materia_prima WHERE nome =? ", nome_pra_teste)
                            a = cursor_kamaleao.fetchone()
                            print(a)
                            conn_kamaleao.execute(
                                "UPDATE materia_prima SET estoque_maximo = ?,estoque_minimo =?,estoque_emergencial=?,rgb=?,estoque_atual=? WHERE nome = ?",
                                tabela_pro_execute)
                            cursor_kamaleao.execute("SELECT * from materia_prima WHERE nome =? ", nome_pra_teste)
                            c = cursor_kamaleao.fetchone()
                            print(c)

                        clr_picker = ColorPicker()

                        nome_pra_teste = [nome_botao]
                        cursor_kamaleao.execute("SELECT * from materia_prima WHERE nome =? ", nome_pra_teste)
                        a = cursor_kamaleao.fetchone()

                        estoque_maximo = a[1]
                        estoque_minimo = a[2]
                        estoque_emergencial = a[3]
                        estoque_atual = a[5]

                        layout_modificar_valores = GridLayout(cols=2)
                        layout_modificar_valores.add_widget(Label(text="Nome"))
                        nome = TextInput(multiline=False, text=str(nome_botao))

                        layout_modificar_valores.add_widget(nome)
                        layout_modificar_valores.add_widget(Label(text="Estoque máximo\n            (g)"))
                        estoque_maximo = TextInput(multiline=False, input_filter='float', text=str(estoque_maximo))

                        layout_modificar_valores.add_widget(estoque_maximo)
                        layout_modificar_valores.add_widget(Label(text="Estoque mínimo\n            (%)"))
                        estoque_minimo = TextInput(multiline=False, input_filter='float', text=str(estoque_minimo))
                        layout_modificar_valores.add_widget(estoque_minimo)

                        layout_modificar_valores.add_widget(Label(text="Estoque Emergencial\n               (%)"))
                        estoque_emergencial = TextInput(multiline=False, input_filter='float',
                                                        text=str(estoque_emergencial))
                        layout_modificar_valores.add_widget(estoque_emergencial)

                        layout_modificar_valores.add_widget((Label(text="Estoque Atual\n           (g)")))
                        estoque_atual = TextInput(multiline=False, input_filter='float', text=str(estoque_atual))
                        layout_modificar_valores.add_widget(estoque_atual)

                        layout_modificar_valores.add_widget(Label(text="COR"))
                        layout_modificar_valores.add_widget(clr_picker)
                        clr_picker.bind(color=on_color)

                        layout_modificar_valores_btt = Button(text="Adicionar no DataBase")
                        layout_modificar_valores_btt.bind(on_press=modificar_valores_materiaprima_db)
                        layout_modificar_valores.add_widget(layout_modificar_valores_btt)

                        layout_modificar_valores_popup = Popup(
                            title="MODIFICAR VALORES DA MATÉRIA PRIMA : " + nome_botao,
                            content=layout_modificar_valores,size_hint=(0.8,0.8))
                        layout_modificar_valores_popup.open()

                    layou_modificar_valores_materiaPrima = GridLayout(cols=4)

                    cursor_kamaleao.execute('''SELECT * from materia_prima''')
                    result = cursor_kamaleao.fetchall()
                    for i in result:
                        nome = i[0]
                        estoque_maximo = i[1]
                        estoque_minimo = i[2]
                        estoque_emergencial = i[3]
                        cor = i[4].replace("[", '')
                        cor = cor.replace(']', '')
                        cor = cor.split(",")
                        for z in range(len(cor)):
                            cor[z] = round(float(cor[z]), 2)
                        cor = tuple(cor)

                        estoque_atual = i[5]

                        btn = Button(text="{}".format(str(nome)),
                                     font_name="fonts/bariol_bold-webfont", background_color=cor)
                        btn.bind(
                            on_release=lambda btn: modificar_valores_de_um(btn.text, estoque_maximo, estoque_minimo,
                                                                           estoque_emergencial, estoque_atual))
                        layou_modificar_valores_materiaPrima.add_widget(btn)

                    aba_modificar_valores = Popup(title="MODIFICAR VALORES DA MATÉRIA PRIMA",
                                                  content=layou_modificar_valores_materiaPrima,
                                                  size_hint=(0.85, 0.85), )
                    aba_modificar_valores.open()

                def remover_materiaPrima_func(instance):
                    def remover_materiaPrima_db(nome_btt):
                        tabela_btt = [nome_btt]
                        conn_kamaleao.execute("DELETE FROM materia_prima WHERE Nome = ?", tabela_btt)

                    layout_remover_valores_materiaPrima = GridLayout(cols=4)

                    cursor_kamaleao.execute('''SELECT * from materia_prima''')
                    result = cursor_kamaleao.fetchall()
                    for i in result:
                        nome = i[0]
                        cor = i[4].replace("[", '')
                        cor = cor.replace(']', '')
                        cor = cor.split(",")
                        for z in range(len(cor)):
                            cor[z] = round(float(cor[z]), 2)
                        cor = tuple(cor)

                        btn = Button(text="{}".format(str(nome)),
                                     font_name="fonts/bariol_bold-webfont", background_color=cor)
                        btn.bind(on_release=lambda btn: remover_materiaPrima_db(btn.text))
                        layout_remover_valores_materiaPrima.add_widget(btn)

                    aba_remover_materiaPrima = Popup(title="REMOVER MATÉRIA PRIMA",
                                                     content=layout_remover_valores_materiaPrima,
                                                     size_hint=(0.85, 0.85), )
                    aba_remover_materiaPrima.open()

                layout_gerenciar_materiaPrima = GridLayout(cols=3)

                adicionar_materiaPrima_btt = Button(text="Adicionar matéria prima")
                adicionar_materiaPrima_btt.bind(on_press=adicionar_materiaPrima_func)

                remover_materiaPrima_btt = Button(text="Remover matéria prima")
                remover_materiaPrima_btt.bind(on_press=remover_materiaPrima_func)

                modificar_valores_materiaPrima_btt = Button(text="Modificar valores")
                modificar_valores_materiaPrima_btt.bind(on_press=modificar_valores_materiaPrima_func)

                layout_gerenciar_materiaPrima.add_widget(adicionar_materiaPrima_btt)
                layout_gerenciar_materiaPrima.add_widget(remover_materiaPrima_btt)
                layout_gerenciar_materiaPrima.add_widget(modificar_valores_materiaPrima_btt)

                layout_gerenciar_materiaPrima_popup = Popup(title="Gerenciar matéria prima",
                                                            content=layout_gerenciar_materiaPrima,size_hint=(0.8,0.8))
                layout_gerenciar_materiaPrima_popup.open()

            def adicionar_ao_estoque_func(instance):
                print(instance.text)

            menu.clear_widgets()
            estoque_menu_layout = GridLayout(cols=2)
            gerenciar_materiaPrima_btt = Button(text="Gerenciar matéra prima",
                                                size_hint=(None, None), width=300, height=410,
                                                )
            gerenciar_materiaPrima_btt.bind(on_press=gerenciar_materiaPrima_func)

            adicionar_ao_estoque_btt = Button(text="Adicionar ao estoque",
                                              size_hint=(None, None), width=300, height=410,
                                              )

            adicionar_ao_estoque_btt.bind(on_press=adicionar_ao_estoque_func)

            estoque_menu_layout.add_widget(gerenciar_materiaPrima_btt)
            estoque_menu_layout.add_widget(adicionar_ao_estoque_btt)
            menu.add_widget(estoque_menu_layout)

        def relatorios_view(instance):
            menu.clear_widgets()
            relatorios_menu_layout = GridLayout(cols=2)
            relatorios_menu_layout.add_widget(Label(text="Relatŕios View"))
            menu.add_widget(relatorios_menu_layout)
            df = pd.read_sql_query("SELECT * from relatorios_fluxo", conn_kamaleao)
            df.to_excel(r'teste_relatorios_fluxo.xlsx', index=False)

        def settings_view(instance):
            menu.clear_widgets()
            settings_menu_layout = GridLayout(cols=2)
            settings_menu_layout.add_widget(Label(text="Settings View"))
            menu.add_widget(settings_menu_layout)

        side_bar = GridLayout(cols=1)

        side_bar.add_widget(Label(text="Kamaleão", size_hint=(None, None), height=220, width=150))

        Button_produção = ToggleButton(size_hint=(None, None), height=75, width=150,
                                       background_normal="img/Produção.png", group='side_menu')
        Button_produção.bind(on_press=producao_view)

        side_bar.add_widget(Button_produção)

        Button_estoque = ToggleButton(size_hint=(None, None), height=75, width=150,
                                      background_normal="img/estoque.png", group='side_menu')

        Button_estoque.bind(on_press=estoque_view)

        side_bar.add_widget(Button_estoque)

        Button_relatorios = ToggleButton(size_hint=(None, None), height=75, width=150,
                                         background_normal="img/relatórios.png", group='side_menu')

        Button_relatorios.bind(on_press=relatorios_view)

        side_bar.add_widget(Button_relatorios)

        Button_settings = ToggleButton(size_hint=(None, None), height=75, width=150,
                                       background_normal="img/settings.png", group='side_menu')
        Button_settings.bind(on_press=settings_view)
        side_bar.add_widget(Button_settings)

        layout.add_widget(side_bar)

        ##############side bar #####################

        ###### menu #######
        menu = GridLayout(cols=3, padding=[85, 150, 10, 30], spacing=50)

        layout.add_widget(menu)

        with side_bar.canvas.before:
            Color(42 / 255, 62 / 255, 70 / 255, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=[150, 1500],
                                  pos=side_bar.pos)
        # process = Popen(['python3', 'graphs.py'], stdout=PIPE, stderr=PIPE)
        return layout


if __name__ == '__main__':
    Window.size = (1366, 768)
    KamaleãoApp().run()
conn.close()
conn_forms.close()
conn_kamaleao.close()
