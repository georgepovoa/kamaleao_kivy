import math
import os
import sqlite3
import subprocess
import sys
from subprocess import PIPE, Popen

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.utils import get_color_from_hex

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
estoque_atual REAL NOT NULL,
porcento REAL

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

createTable_relatorios_sales_rate= """

CREATE TABLE relatorio_saida_materia_prima(

id INTEGER PRIMARY KEY AUTOINCREMENT,
nome_mp TEXT NOT NULL,
quantidade_saida REAL NOT NULL,
sales_rate REAL NOT NULL,
data TEXT NOT NULL
)


"""



conn_kamaleao = sqlite3.connect('kamaleao.db')
cursor_kamaleao = conn_kamaleao.cursor()

conn = sqlite3.connect('pigmentos.db')
cursor = conn.cursor()

conn_forms = sqlite3.connect('forms.db')
cursor_forms = conn_forms.cursor()



# tempo em sqlite
# time_con =cursor_kamaleao.execute("SELECT datetime('now', 'localtime')")
# time_value = cursor_kamaleao.fetchone()[0]
# print(time_value)


class KamaleãoApp(App):

    def build(self):

        float_layout = FloatLayout(size=(Window.size[0], Window.size[1]))

        Window.clearcolor = (200 / 255, 210 / 255, 197 / 255, 1)

        layout = GridLayout(cols=2)

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
            # ########## VER TABELA É O LAYOUT DOS BTTS ######### #

            def enviar_db(nome):
                # ########## ENVIAR_DB É O LAYOUT APÓS ABRIR UM BTT ######### #

                def enviar_db_de_vdd(instance):
                    # ########## É A ACÃO DO BOTAO DE ENVIAR(adiciona no banco de dados o valor) ######### #

                    def refresh_tabela_estoque():
                        tela_adicionar_estoque_popup.dismiss()
                        aba_estoque_pg.dismiss()
                        ver_tabela(instance)

                    # ########## COMEÇO ENVIAR_DB_DE_VDD ######### #

                    # separar o % do nome #
                    tabela = [nome.split("\n")[0]]
                    nome_do_produto = nome.split("\n")[0]
                    # separar o % do nome #

                    # verificação de input vazio e enviar 0 quando vazio #
                    if quantidade_adicionar.text == "." or quantidade_adicionar.text == "":
                        quantidade_adicionar.text = "0"
                    # verificação de input vazio e enviar 0 quando vazio #

                    # lógica de do db estoque_atual#
                    cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?", tabela)
                    estoque_antigo = cursor_kamaleao.fetchone()[0]
                    estoque_novo = estoque_antigo + float(quantidade_adicionar.text)
                    tabela_db = [estoque_novo, nome_do_produto]
                    conn_kamaleao.execute("UPDATE materia_prima set estoque_atual = ? WHERE nome = ?", tabela_db)
                    # lógica de do db estoque_atual#

                    # lógica db porcento #
                    cursor_kamaleao.execute("SELECT estoque_atual, estoque_maximo FROM materia_prima WHERE nome = ?",
                                            tabela)
                    result = cursor_kamaleao.fetchone()
                    maxim = result[1]
                    atual = result[0]
                    tabela_update_porcento = [(atual / maxim) * 100, tabela[0]]
                    print(tabela_update_porcento)
                    conn_kamaleao.execute("UPDATE materia_prima set porcento = ? WHERE nome = ?",
                                          tabela_update_porcento)

                    # lógica db porcento #

                    refresh_tabela_estoque()

                    # lógica db fluxo_db #
                    cursor_kamaleao.execute("SELECT datetime('now', 'localtime')")
                    time_value = cursor_kamaleao.fetchone()[0]
                    relatorios_tabela = [nome_do_produto, float(quantidade_adicionar.text), time_value]
                    conn_kamaleao.execute("INSERT INTO relatorios_fluxo(produto,quantidade,dia) VALUES (?,?,?)",
                                          relatorios_tabela)

                    # lógica db fluxo_db #

                # ########## COMEÇO ENVIAR_DB ######### #
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

            # ########## COMEÇO VER TABELA ######### #

            layout_tabela = GridLayout(rows=2)
            blocks = GridLayout(rows=5, spacing=20)

            # GERADOR DE BTT DINAMICO##
            cursor_kamaleao.execute('''SELECT * from materia_prima''')
            result = cursor_kamaleao.fetchall()
            for i in result:
                nome = i[0]
                percent = i[6]
                cor = i[4].replace("[", '')
                cor = cor.replace(']', '')
                cor = cor.split(",")
                for z in range(len(cor)):
                    cor[z] = round(float(cor[z]), 2)
                cor = tuple(cor)

                btn = Button(text="{}\n{}%".format(nome, percent),
                             font_name="fonts/bariol_bold-webfont", background_color=cor, size_hint=(0.3, 0.3))
                btn.bind(on_release=lambda btn: enviar_db(btn.text))
                blocks.add_widget(btn)
            layout_tabela.add_widget(blocks)
            # GERADOR DE BTT DINAMICO##

            aba_estoque_pg = Popup(title="Estoque", content=layout_tabela)
            aba_estoque_pg.open()

        def forms(instance):
            # TELA PARA ADICIONAR UMA NOVA FÓRMULA #

            def enviar_forms(instance):

                # LÓGICA PARA ADICIONAR AO BD #
                formula = {}

                # validação de input #

                for i in range(len(nome_das_materias_primas_iterate)):
                    if nome_das_materias_primas_iterate[i].text == "" or nome_das_materias_primas_iterate[
                        i].text == '.':
                        nome_das_materias_primas_iterate[i].text = '0'

                    # validação de input #

                    # meu amigo... isso aqui é pra adicionar uma fórmula no formato de DICT#
                    formula[nomes_mas_materias_primas_string[i]] = nome_das_materias_primas_iterate[i].text

                # pra depois tranformar o dict em string pra adicionar no banco de dados
                formula_inteira = str(formula)
                formula_db = [nome_da_formula.text, formula_inteira]
                try:
                    conn_kamaleao.execute("INSERT INTO formulas VALUES(?,?)", formula_db)
                    result = cursor_kamaleao.execute("SELECT * FROM formulas")
                    for f in result:
                        print(f)
                except:
                    print("fórmula já existente")

            # COMEÇO DA TELA PARA ADICIONAR UMA NOVA FÓRMULA #

            formulas_layout = GridLayout(cols=2)
            formulas_layout.add_widget(Label(text="Nome"))
            nome_da_formula = TextInput(multiline=False)
            formulas_layout.add_widget(nome_da_formula)
            cursor_kamaleao.execute("SELECT nome FROM materia_prima")
            result = cursor_kamaleao.fetchall()
            nome_das_materias_primas_iterate = []
            nomes_mas_materias_primas_string = []
            # velho, isso aqui foi pra salvar cada TextInput em uma variável diferente
            # esse globlas ai cria um nome de variável dinamicamente
            # depois eu adicionei essas variáveis em uma lista
            # que é essa aqui nome_das_materias_primas_iterate

            for i in result:
                for z in i:
                    formulas_layout.add_widget(Label(text=str(z)))
                    nomes_mas_materias_primas_string.append(z)
                    globals()[str(z)] = TextInput(multiline=False, input_filter='float')
                    nome_das_materias_primas_iterate.append(globals()[str(z)])
                    formulas_layout.add_widget(globals()[z])
            #
            #
            #
            #
            formulas_layout_btt = Button(text="enviar")

            formulas_layout_btt.bind(on_press=enviar_forms)
            formulas_layout.add_widget(formulas_layout_btt)

            formulas_popup = Popup(title="forms", content=formulas_layout, size_hint=(1, 1))
            formulas_popup.open()

        def simular_tab(instance):

            # SIMULAR TAB É A TELA DE PRODUÇÃO

            def on_text(instance, value):

                # on_text é pra sempre pegar o valor do text input quando existe mudança

                def print_it(instance, value_label):
                    # esse print_it é pra quando o label que é resultado de pesquisa for clickado
                    # tranformar o texto do TextInput nele
                    nome_da_formula.text = value_label

                # Lógica de pesquisa, quando digitar algo no  TextInput
                # Vão aparecer 5 valores que podem ser o q você quer

                esqueda_baixo_area_esquerda.clear_widgets()
                cursor_kamaleao.execute("SELECT nome FROM formulas WHERE nome LIKE '{}%'".format(value))
                result = cursor_kamaleao.fetchmany(5)
                for i in result:
                    for f in i:
                        label = Label(text="[ref={}][color=0000ff]{}[/color][/ref]".format(str(f), str(f)), markup=True)
                        label.bind(on_ref_press=print_it)
                        esqueda_baixo_area_esquerda.add_widget(label)

            # precisam ser declarados antes do botão pq se nao toda vez reseta
            # e não pode pois a ideia é somar
            formula_formatada = {}
            esqueda_baixo_area_direita_tabela = []

            def adicionar_cor(instance):
                # mano, isso aqui foi dificil

                # validar input, não pode ser 0, é isso.
                # em alguma hora eu multiplico, divido, aí 0 da mt ruim

                if quantidade.text == "" or quantidade.text == "." or quantidade.text == "0":
                    quantidade.text = "1"

                ######## pegar informações #########

                nome = [nome_da_formula.text]
                # limpar resultado para não ficar adicionando um atrás do outro
                direita_tab_content.clear_widgets()

                # esse aqui é a tabela de fórmulas já adicionadas
                esqueda_baixo_area_direita.clear_widgets()

                # float pq vai que ele quer fazer sla um número quebrado
                quantidade_que_multiplica_formula = float(quantidade.text)

                ######## pegar informações #########

                cursor_kamaleao.execute("SELECT * FROM formulas WHERE nome = ?", nome)
                try:
                    ###### aqui a gente limpa o dict que foi transformado em str #####
                    formula_completa = cursor_kamaleao.fetchone()[1]
                    print("aqui a gente limpa o dict que foi transformado em str ", formula_completa)
                    formula_completa = formula_completa.replace("{", '')
                    formula_completa = formula_completa.replace("}", '')
                    formula_completa = formula_completa.translate({ord("'"): None})
                    ###### e transforma ele em uma lista no formato nome da cor : valor #####
                    formula_completa = formula_completa.split(',')

                    ## Agora separa essas listas, para pegar o Nome e o valor de cada matéria prima ##
                    for i in formula_completa:
                        i = i.strip()
                        i = i.split(":")

                    ## aqui, soma no dict um valor se a matéria prima já estiver dentro do dict ##
                    ## ou adiciona no dict uma nova matéria prima com seu valor a ser descontado  ##

                        if i[0] in formula_formatada:
                            formula_formatada[i[0]] += float(i[1]) * quantidade_que_multiplica_formula
                        else:
                            formula_formatada[i[0]] = float(i[1]) * quantidade_que_multiplica_formula

                    # agora cria outro loop para mostrar como os valores ficariam após a adição de tal formula #

                    for i in formula_formatada:
                        nome = [i]


                        cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?", nome)
                        novo_valor = cursor_kamaleao.fetchone()[0] - formula_formatada.get(i)
                        direita_tab_content.add_widget(Label(text=str(i)))
                        direita_tab_content.add_widget(Label(text=str(novo_valor)))
                    # aqui adiciona na tela o nome da fórmula e a quantidade de vezes que ela foi adicionada #
                    esqueda_baixo_area_direita_tabela.append([nome_da_formula.text, quantidade_que_multiplica_formula])
                    for i in esqueda_baixo_area_direita_tabela:
                        esqueda_baixo_area_direita.add_widget(Label(text="{}   x   {}".format(i[0], i[1])))
                except:
                    # aqui se deu ruim ainda tem que Criar uma tela pra avisar que deu.
                    print("NOME NÃO EXISTE NO BANCO DE DADOS")

            def produzir_func(instance):
                print(formula_formatada)
                # essa é a função do botão de produzir#
                # primeira coisa que tem que fazer é declarar uma variável booleana#
                # pra só produzir se todos os requirements forem satisfeitos

                valido = True

                # Verifica se algum valor é menor que 0

                for i in formula_formatada:
                    nome = [i]
                    cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?", nome)
                    novo_valor = cursor_kamaleao.fetchone()[0] - formula_formatada.get(i)
                    if novo_valor < 0:
                        # se existir, o valido fica falso e não permite a produção #
                        valido = False
                if valido:

                    # Se válido, update o estoque atual de matéria prima #
                    for i in formula_formatada:
                        nome = [i]
                        cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?", nome)
                        novo_valor = cursor_kamaleao.fetchone()[0] - formula_formatada.get(i)
                        atualizar_tabela = [novo_valor, i]
                        conn_kamaleao.execute("UPDATE materia_prima SET estoque_atual = ? WHERE nome = ?",
                                              atualizar_tabela)

                        # e atualiza a porcentagem #

                        cursor_kamaleao.execute("SELECT estoque_atual,estoque_maximo FROM materia_prima where nome = ?",
                                                nome)
                        result = cursor_kamaleao.fetchone()
                        maxim = result[1]
                        atual = result[0]
                        tabela_update_porcento = [(atual / maxim) * 100, nome[0]]
                        conn_kamaleao.execute("UPDATE materia_prima set porcento = ? WHERE nome = ?",
                                              tabela_update_porcento)

                        # e aqui atualiza o relatório #

                        ####### RELATORIO_fluxo ########
                        cursor_kamaleao.execute("SELECT datetime('now', 'localtime')")
                        time_value = cursor_kamaleao.fetchone()[0]
                        for z in range(len(esqueda_baixo_area_direita_tabela)):
                            valores_relatorios_producao = [esqueda_baixo_area_direita_tabela[z][0],
                                                           esqueda_baixo_area_direita_tabela[z][1], time_value]
                            conn_kamaleao.execute("INSERT INTO relatorios_fluxo(produto,quantidade,dia) VALUES (?,?,?)",
                                                  valores_relatorios_producao)
                        ## e aqui relatório sales_rate ##

                        try:
                            cursor_kamaleao.execute("SELECT date('now', 'localtime')")

                            date = cursor_kamaleao.fetchone()[0]
                            verificar_se_ja_existe = [i,date]
                            cursor_kamaleao.execute("SELECT * FROM relatorio_saida_materia_prima WHERE nome_mp = ? AND data = ?",verificar_se_ja_existe)
                            achou = cursor_kamaleao.fetchone()[0]
                            cursor_kamaleao.execute("SELECT * FROM relatorio_saida_materia_prima WHERE nome_mp = ? AND data = ?",verificar_se_ja_existe)
                            todas_infos = cursor_kamaleao.fetchall()
                            print(todas_infos)
                            nome_mp = todas_infos[0][1]
                            quantidade = todas_infos[0][2]
                            print("Quantidade antes: ",quantidade)
                            quantidade = todas_infos[0][2]+ formula_formatada.get(i)
                            print("Quantidade depois: ", quantidade)
                            sales_rate = todas_infos[0][3]

                            # ta dando erroa qui
                            try:
                                conn_kamaleao.execute("""
                                UPDATE relatorio_saida_materia_prima SET quantidade_saida = {}  WHERE nome_mp = ? AND data = ?
                                """.format(quantidade,achou),verificar_se_ja_existe)
                            except Exception as e:
                                print(e)

                            print("achou",achou)


                        except:

                            print(date)
                            tabela_pra_saleRate = [i,formula_formatada.get(i),date]
                            print(tabela_pra_saleRate)
                            conn_kamaleao.execute("""
                            INSERT INTO relatorio_saida_materia_prima(
                            nome_mp,quantidade_saida,sales_rate,data)
                            VALUES(?,?,0,?)
                            """,tabela_pra_saleRate)
                            cursor_kamaleao.execute("SELECT * FROM relatorio_saida_materia_prima")
                            print(cursor_kamaleao.fetchall())



                        esqueda_baixo_area_direita_tabela.clear()
                else:
                    # aqui se o válido for falso, a gente pega os valores falsos e transforma#
                    #  ou tenta trasnformar em um Pedido de compra #
                    valores_negativos = []

                    for i in formula_formatada:
                        nome = [i]
                        cursor_kamaleao.execute("SELECT estoque_atual FROM materia_prima WHERE nome = ?", nome)
                        novo_valor = cursor_kamaleao.fetchone()[0] - formula_formatada.get(i)
                        if novo_valor < 0:
                            valores_negativos.append("{} : {}".format(i, novo_valor))
                    print(valores_negativos)

            # COMEÇO DA TELA DE SIMULAÇÃO

            layout_simular_tab = GridLayout(cols=2)

            esquerda_tab = GridLayout(cols=2)

            esquerda_tab.add_widget(Label(text="Nome da fórmula", size_hint=(1, 0.2)))
            nome_da_formula = TextInput(size_hint=(1, 0.2), multiline=False)
            nome_da_formula.bind(text=on_text)
            esquerda_tab.add_widget(nome_da_formula)

            esquerda_tab.add_widget(Label(text="quantidade desejada", size_hint=(1, 0.3)))
            quantidade = TextInput(size_hint=(1, 0.2), multiline=False, input_filter='float')
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

            simular_tab_popup = Popup(title="PRODUZIR", content=layout_simular_tab, size_hint=(0.8, 0.8),
                                      background_color=(0, 0, 1, 1))
            simular_tab_popup.open()

        ##############side bar###############
        def producao_view(instance):

            menu.clear_widgets()
            print(menu.size)
            print(layout.size)
            width_calc = (layout.size[0] - 150) / 3.8
            heigt_calc = layout.size[1] / 1.73
            print(width_calc, heigt_calc)

            menu_producao_layout = GridLayout(cols=3)

            menu_estoque_btt = Button(background_normal='img/Botao_estoque.png', color=(0, 0, 0, 0),
                                      pos_hint={"x": 1, "y": 1}, size_hint=(None, None), width=width_calc,
                                      height=heigt_calc,
                                      background_down='img/Botao_estoque.png', border=(0, 0, 0, 0))
            menu_estoque_btt.bind(on_press=ver_tabela)
            menu_producao_layout.add_widget(menu_estoque_btt)

            menu_prod_btt = Button(background_normal='img/Simular.png', color=(0, 0, 0, 0), pos_hint={"x": 1, "y": 1},
                                   size_hint=(None, None), width=width_calc, height=heigt_calc,
                                   background_down='img/Simular.png',
                                   border=(0, 0, 0, 0))
            menu_prod_btt.bind(on_press=simular_tab)
            menu_producao_layout.add_widget(menu_prod_btt)

            menu_forms_btt = Button(background_normal='img/Gerenciar.png', color=(0, 0, 0, 0),
                                    pos_hint={"x": 1, "y": 1},
                                    size_hint=(None, None), width=width_calc, height=heigt_calc,
                                    background_down='img/Gerenciar.png',
                                    border=(0, 0, 0, 0))
            menu_forms_btt.bind(on_press=forms)

            menu_producao_layout.add_widget(menu_forms_btt)

            menu.add_widget(menu_producao_layout)

            ###### menu #######

        def estoque_view(instance):

            # ESSA AQUI É A TELA DE ESTOQUE #

            def gerenciar_materiaPrima_func(instance):
                # ESSA AQUI É A DE GERENCIAR, EXISTEM 3 TELAS DENTRO DELA #
                # ADICIONAR, REMOVER E MODIFICAR, BASICAMENTE O CRUDE #


                def adicionar_materiaPrima_func(instance):
                    # essa daqui perceptivelmente, adiciona #

                    # isso aqui é pro roda de cores funcionar #
                    def on_color(instance, value):
                        pass  # or instance.color


                    def adicionar_no_database(instance):
                        if estoque_atual.text == '0' or estoque_atual.text == "." or estoque_atual.text=="":
                            estoque_atual.text="1"

                        if estoque_maximo.text == '0' or estoque_maximo.text == "." or estoque_maximo.text == "":
                            estoque_maximo.text = "1"
                        # função do botao adicionar ao banco de dados#

                        # e aqui é a lógica para adicionar no banco de dados#

                        lista_adicionar_materiaPrima_btt = [nome.text, estoque_maximo.text, estoque_minimo.text,
                                                            estoque_emergencial.text, str(clr_picker.color),
                                                            estoque_atual.text, float(estoque_atual.text) / float(
                                estoque_maximo.text) * 100]
                        # validador de input #

                        for i in range(len(lista_adicionar_materiaPrima_btt)):
                            if lista_adicionar_materiaPrima_btt[i] == "" or lista_adicionar_materiaPrima_btt[i] == ".":
                                lista_adicionar_materiaPrima_btt[i] = "1"
                        try:
                            # adicionar no materias primas db#
                            cursor_kamaleao.execute("INSERT INTO materia_prima VALUES(?,?,?,?,?,?,?)",
                                                    lista_adicionar_materiaPrima_btt)
                            # conn_kamaleao.commit()
                        except:
                            print("Nome já está no db")

                    clr_picker = ColorPicker()

                    # começo do layout para adicionar matérios primas #
                    layout_adicionar_materiaPrima = GridLayout(cols=2)
                    layout_adicionar_materiaPrima.add_widget(Label(text="Nome", size_hint=(1, 0.2)))
                    nome = TextInput(multiline=False, size_hint=(1, 0.2))
                    layout_adicionar_materiaPrima.add_widget(nome)
                    layout_adicionar_materiaPrima.add_widget(
                        Label(text="Estoque máximo\n            (g)", size_hint=(1, 0.3)))
                    estoque_maximo = TextInput(multiline=False, input_filter='float', size_hint=(1, 0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_maximo)
                    layout_adicionar_materiaPrima.add_widget(
                        Label(text="Estoque mínimo\n            (%)", size_hint=(1, 0.2)))
                    estoque_minimo = TextInput(multiline=False, input_filter='float', size_hint=(1, 0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_minimo)
                    layout_adicionar_materiaPrima.add_widget(
                        Label(text="Estoque Emergencial\n                (%)", size_hint=(1, 0.2)))
                    estoque_emergencial = TextInput(multiline=False, input_filter='float', size_hint=(1, 0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_emergencial)

                    layout_adicionar_materiaPrima.add_widget(
                        (Label(text="Estoque Atual\n          (g)", size_hint=(1, 0.2))))
                    estoque_atual = TextInput(multiline=False, input_filter='float', size_hint=(1, 0.2))
                    layout_adicionar_materiaPrima.add_widget(estoque_atual)

                    layout_adicionar_materiaPrima.add_widget(Label(text="COR"))
                    layout_adicionar_materiaPrima.add_widget(clr_picker)
                    clr_picker.bind(color=on_color)

                    layout_adicionar_materiaPrima.add_widget(Label(text="", size_hint=(1, 0.2)))

                    layout_adicionar_materiaPrima_btt = Button(text="Adicionar no DataBase", size_hint=(1, 0.2))
                    layout_adicionar_materiaPrima_btt.bind(on_press=adicionar_no_database)
                    layout_adicionar_materiaPrima.add_widget(layout_adicionar_materiaPrima_btt)

                    layout_adicionar_materiaPrima_popup = Popup(title="Adicionar matéria prima",
                                                                content=layout_adicionar_materiaPrima,
                                                                size_hint=(0.9, 0.9))
                    layout_adicionar_materiaPrima_popup.open()

                def modificar_valores_materiaPrima_func(instance):
                    # tela modificar valores
                    def modificar_valores_de_um(nome_botao, estoque_maximo, estoque_minimo, estoque_emergencial,
                                                estoque_atual):
                        # aqui é a tela dentro de um botão

                        #isso aqui é pra cor funcionar
                        def on_color(instance, value):
                            pass  # or instance.color

                        def modificar_valores_materiaprima_db(instance):
                            # essa é função para efetivamente modificar valores
                            def refresh_mudar_valores():

                                layout_modificar_valores_popup.dismiss()
                                aba_modificar_valores.dismiss()
                                modificar_valores_materiaPrima_func(instance)

                            tabela_pro_execute = [estoque_maximo.text, estoque_minimo.text,
                                                  estoque_emergencial.text, str(clr_picker.color),
                                                  estoque_atual.text, nome_botao]

                            # validar TextInput
                            for n in range(len(tabela_pro_execute)):
                                if tabela_pro_execute[n] == "" or tabela_pro_execute[n] == ".":
                                    tabela_pro_execute[n] = "0.1"

                            # modificar materia prima
                            print(tabela_pro_execute)
                            nome_pra_teste = [nome_botao]
                            cursor_kamaleao.execute("SELECT * from materia_prima WHERE nome =? ", nome_pra_teste)
                            a = cursor_kamaleao.fetchone()
                            print(a)
                            conn_kamaleao.execute(
                                "UPDATE materia_prima SET estoque_maximo = ?,estoque_minimo =?,estoque_emergencial=?,"
                                "rgb=?,estoque_atual=? WHERE nome = ?",
                                tabela_pro_execute)

                            # modificar porcento

                            cursor_kamaleao.execute(
                                "SELECT estoque_atual,estoque_maximo FROM materia_prima where nome = ?", nome_pra_teste)
                            result = cursor_kamaleao.fetchone()
                            maxim = result[1]
                            atual = result[0]
                            tabela_update_porcento = [(atual / maxim) * 100, nome_pra_teste[0]]
                            conn_kamaleao.execute("UPDATE materia_prima set porcento = ? WHERE nome = ?",
                                                  tabela_update_porcento)

                            cursor_kamaleao.execute("SELECT * from materia_prima WHERE nome =? ", nome_pra_teste)
                            c = cursor_kamaleao.fetchone()
                            print(c)
                            refresh_mudar_valores()

                        clr_picker = ColorPicker()
                        #  COMEÇO aqui é a tela dentro de um botão
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
                            content=layout_modificar_valores, size_hint=(1, 1))
                        layout_modificar_valores_popup.open()

                    # COMEÇO tela modificar valores
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
                    # segue o mesmo padrão dos outros só que com delete
                    def remover_materiaPrima_db(nome_btt):
                        def refresh_delete_tabela():
                            aba_remover_materiaPrima.dismiss()
                            layout_gerenciar_materiaPrima_popup.dismiss()

                            remover_materiaPrima_func(instance)

                        tabela_btt = [nome_btt]
                        conn_kamaleao.execute("DELETE FROM materia_prima WHERE Nome = ?", tabela_btt)
                        # conn_kamaleao.commit()
                        refresh_delete_tabela()

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
                                                            content=layout_gerenciar_materiaPrima, size_hint=(0.8, 0.8))
                layout_gerenciar_materiaPrima_popup.open()

            def adicionar_ao_estoque_func(instance):
                print(instance.text)

            # COMEÇO DA TELA DE ESTOQUE #

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
            df = pd.read_sql_query("SELECT * from relatorios_fluxo", conn_kamaleao)

            relatorios_menu_layout = GridLayout(cols=2)

            df.to_excel(r'teste_relatorios_fluxo.xlsx', index=False)
            # if sys.platform == "win32":
            #    os.startfile('teste_relatorios_fluxo.xlsx')
            # else:
            #    opener = "open" if sys.platform == "darwin" else "xdg-open"
            #    subprocess.call([opener, 'teste_relatorios_fluxo.xlsx'])

            cursor_kamaleao.execute("SELECT * FROM materia_prima")
            cores = cursor_kamaleao.fetchall()

            # ############ GRÁFICO 1 ############### #

            cursor_kamaleao.execute("SELECT * FROM materia_prima")
            tamanho = math.ceil(len(cursor_kamaleao.fetchall()) / 2)

            print(tamanho)
            df = pd.read_sql_query("SELECT nome,porcento,rgb from materia_prima LIMIT {}".format(tamanho),
                                   conn_kamaleao)
            df.reset_index(drop=True, inplace=True)
            nomes = df["nome"]
            porcento = df["porcento"]
            cursor_kamaleao.execute('''SELECT rgb from materia_prima''')
            result = cursor_kamaleao.fetchall()

            ax = df.plot.bar(x='nome', y='porcento', rot=0, figsize=(18, 1.8))

            childrenLS = ax.get_children()
            barlist = filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), childrenLS)
            n = 0
            cursor_kamaleao.execute("SELECT * from materia_prima LIMIT {}".format(tamanho))
            result = cursor_kamaleao.fetchall()
            cores_pro_grafico = []

            for i in result:
                cor = i[4].replace("[", '')
                cor = cor.replace(']', '')
                cor = cor.split(",")
                for z in range(len(cor)):
                    cor[z] = round(float(cor[z]), 2)
                cor = tuple(cor)
                cores_pro_grafico.append(cor)

            n = 0
            for i in barlist:
                try:
                    cor = cores_pro_grafico[n]
                    i.set_color(cor)
                    print("try:")


                except Exception as e:
                    print(e)
                n += 1

            for i, v in enumerate(porcento):
                ax.text(i - .25,
                        v / porcento[i] + 50,
                        round(porcento[i], 1),
                        fontsize=11,
                        color="gray",
                        fontweight='bold'
                        )
            ax.get_legend().remove()
            plt.xticks(rotation=45, ha="right")

            plt.ylim(0, 100)
            ax.set(xlabel='')
            ax.plot()
            plt.savefig("testando_plot", bbox_inches='tight')

            plt.close()
            menu.add_widget(Image(source="testando_plot.png", size_hint=(None, None), size=(Window.size[0] - 150, 250)))
            # ############ GRÁFICO 1 ############### #

            # ############ GRÁFICO 2 ############### #

            df_2 = pd.read_sql_query(
                "SELECT nome,porcento,rgb from materia_prima LIMIT {} OFFSET {}".format(tamanho, tamanho),
                conn_kamaleao)
            df_2.reset_index(drop=True, inplace=True)
            cursor_kamaleao.execute('''SELECT rgb from materia_prima''')
            result = cursor_kamaleao.fetchall()

            ax = df_2.plot.bar(x='nome', y='porcento', rot=0, figsize=(18, 1.8))
            porcento_2 = df_2["porcento"]

            childrenLS = ax.get_children()
            barlist = filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), childrenLS)
            n = 0
            cursor_kamaleao.execute("SELECT * from materia_prima LIMIT {} OFFSET {}".format(tamanho, tamanho))
            result = cursor_kamaleao.fetchall()
            cores_pro_grafico = []

            for i in result:
                cor = i[4].replace("[", '')
                cor = cor.replace(']', '')
                cor = cor.split(",")
                for z in range(len(cor)):
                    cor[z] = round(float(cor[z]), 2)
                cor = tuple(cor)
                cores_pro_grafico.append(cor)

            n = 0
            for i in barlist:
                try:
                    cor = cores_pro_grafico[n]
                    i.set_color(cor)
                    print("try:")


                except Exception as e:
                    print(e)
                n += 1

            for i, v in enumerate(porcento_2):
                ax.text(i - .25,
                        v / porcento_2[i] + 10,
                        round(porcento_2[i], 1),
                        fontsize=11,
                        color="gray",
                        fontweight='bold'
                        )
            ax.get_legend().remove()
            plt.xticks(rotation=45, ha="right")

            plt.ylim(0, 100)

            ax.set(xlabel='')
            # plt.setp(ax1.get_xticklabels(), visible=False)
            # plt.setp(ax1.get_yticklabels(), visible=False)
            ax.tick_params(axis='both', which='both', length=0)
            ax.plot()

            plt.savefig("testando_plot_2", bbox_inches='tight')

            plt.close()
            menu.add_widget(
                Image(source="testando_plot_2.png", size_hint=(None, None), size=(Window.size[0] - 150, 250)))

            menu.add_widget(relatorios_menu_layout)
            # ############ GRÁFICO 2 ############### #

        def settings_view(instance):
            menu.clear_widgets()

            settings_menu_layout = GridLayout(cols=2)
            settings_menu_layout.add_widget(Label(text="Settings View"))
            menu.add_widget(settings_menu_layout)

        side_bar = GridLayout(cols=1, size_hint_x=None, width=150)

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
        menu = GridLayout(cols=1, size_hint_x=None, width=Window.size[0] - 150)

        layout.add_widget(menu)

        with side_bar.canvas.before:
            Color(42 / 255, 62 / 255, 70 / 255, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=[150, 1500],
                                  pos=side_bar.pos)
        # process = Popen(['python3', 'graphs.py'], stdout=PIPE, stderr=PIPE)

        float_layout.add_widget(layout)
        return float_layout


if __name__ == '__main__':
    Window.maximize()
    KamaleãoApp().run()
conn.close()
conn_forms.close()
conn_kamaleao.close()
