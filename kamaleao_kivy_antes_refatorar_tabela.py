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
from kivy.clock import Clock
from kivy.lang import Builder
from pynput.keyboard import Key, Controller
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.togglebutton import ToggleButton

# COLORS #

# rgba(42,62,70,1) VERDE ESCURO
# rgba(43,80,83,1) VERDE MENOS ESCURO
# rgba(67,122,112,1) VERDE MÉDIO
# rgba(200,210,197,1) CLARO FUNDO


conn = sqlite3.connect('pigmentos.db')
cursor = conn.cursor()
conn_forms = sqlite3.connect('forms.db')
cursor_forms = conn_forms.cursor()


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
            def adicionar_estoque(instance):

                def enviar_db(nome):
                    def refresh_tabela():
                        tabela_conteudo.clear_widgets()
                        cursor.execute('''SELECT nome,estoque,estoque_min,estoque_emerg from pigmentos''')
                        refresh_tabela_result = list(cursor.fetchall())
                        for i in refresh_tabela_result:
                            for j in i:
                                lbl = Label(text=str(j),
                                            )
                                tabela_conteudo.add_widget(lbl)

                    def enviar_db_de_vdd(instance):
                        nome_tabela = [nome]
                        cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?", nome_tabela)
                        valor_estoque_antigo_tabela = cursor.fetchone()
                        for i in valor_estoque_antigo_tabela:
                            estoque_antigo = i
                        try:
                            novo_estoque = float(quantidade_adicionar.text) + estoque_antigo
                            incremento_estoque = [novo_estoque, nome]
                            conn.execute("UPDATE pigmentos SET estoque = ? WHERE nome = ?", incremento_estoque)
                            cursor.execute('''SELECT * from pigmentos''')
                            conn.commit()
                        except Exception as e:
                            print("exception 1: ", e)
                        tela_adicionar_estoque_popup.dismiss()
                        refresh_tabela()

                    tela_adicionar_estoque = GridLayout(rows=2)
                    quantidade_adicionar = TextInput(multiline=False, input_filter='float')
                    tela_adicionar_estoque_cima = GridLayout(cols=2)

                    tela_adicionar_estoque_cima.add_widget(Label(text="Quantidade à se adicionar ao estoque: "))
                    tela_adicionar_estoque_cima.add_widget(quantidade_adicionar)

                    tela_adicionar_estoque.add_widget(tela_adicionar_estoque_cima)

                    tela_adicionar_estoque_baixo_btt = Button(text="Enviar")
                    tela_adicionar_estoque_baixo_btt.bind(on_press=enviar_db_de_vdd)
                    tela_adicionar_estoque.add_widget(tela_adicionar_estoque_baixo_btt)

                    tela_adicionar_estoque_popup = Popup(title="Adicionar estoque:" + nome,
                                                         content=tela_adicionar_estoque, size_hint=[1, 0.5])
                    tela_adicionar_estoque_popup.open()

                ## LABELS ##
                adicionar_estoque_layout = GridLayout(cols=4)
                cursor.execute('''SELECT nome from pigmentos''')
                result = list(cursor.fetchall())
                for i in result:
                    for j in i:
                        btn = Button(text=str(j), font_name="fonts/bariol_bold-webfont")
                        btn.bind(on_release=lambda btn: enviar_db(btn.text))
                        adicionar_estoque_layout.add_widget(btn)

                adicionar_estoque_popup = Popup(title="adicioar ao estoque", content=adicionar_estoque_layout)
                adicionar_estoque_popup.open()

            def min_estoque(instance):
                def pesquisa_min_estoque(instance, value):
                    match_min_estoque.clear_widgets()
                    if estoque_min_produto.text != '':
                        cursor.execute(
                            "SELECT nome FROM pigmentos WHERE nome LIKE '{}%'".format(estoque_min_produto.text))
                        nomes = cursor.fetchall()
                        for i in nomes:
                            for z in i:
                                match_min_estoque.add_widget(Label(text=str(z)))

                def alterar_min_estoque(instance):

                    teste_tabela = [estoque_min_produto.text]
                    cursor.execute("SELECT estoque_min FROM pigmentos WHERE nome = ?", teste_tabela)
                    result = cursor.fetchone()
                    try:
                        novo_estoque_min = [float(min_estoque_input.text), estoque_min_produto.text]
                        conn.execute("UPDATE pigmentos SET estoque_min = ? WHERE nome = ?", novo_estoque_min)
                        cursor.execute("SELECT estoque_min FROM pigmentos WHERE nome = ?", teste_tabela)
                        result = cursor.fetchone()
                        conn.commit()
                    except Exception as e:
                        print("exceptionm 2: ", )
                    layout_min_estoque_popup.dismiss()

                layout_min_estoque = GridLayout(cols=2)
                layout_min_estoque.add_widget(Label(text="Produto"))
                estoque_min_produto = TextInput(multiline=False)
                estoque_min_produto.bind(text=pesquisa_min_estoque)
                layout_min_estoque.add_widget(estoque_min_produto)

                layout_min_estoque.add_widget(Label(text="Estoque mínimo"))
                min_estoque_input = TextInput(multiline=False, input_filter='float')
                layout_min_estoque.add_widget(min_estoque_input)

                layout_min_estoque_btt = Button(text="Alterar")
                layout_min_estoque_btt.bind(on_press=alterar_min_estoque)
                layout_min_estoque.add_widget(layout_min_estoque_btt)

                match_min_estoque = GridLayout(cols=2)

                layout_min_estoque.add_widget(match_min_estoque)

                layout_min_estoque_popup = Popup(title="min_extoque", content=layout_min_estoque,
                                                 size_hint=(None, None), size=(600, 600))
                layout_min_estoque_popup.open()

            def emerg_estoque(instance):
                def alterar_estoque_emerg(instance):
                    teste_tabela = [estoque_emerg_produto.text]
                    cursor.execute("SELECT estoque_emerg FROM pigmentos WHERE nome = ?", teste_tabela)
                    result = cursor.fetchone()
                    try:
                        novo_estoque_emerg = [float(emerg_estoque_input.text), estoque_emerg_produto.text]
                        conn.execute("UPDATE pigmentos SET estoque_emerg = ? WHERE nome = ?", novo_estoque_emerg)
                        cursor.execute("SELECT estoque_emerg FROM pigmentos WHERE nome = ?", teste_tabela)
                        result = cursor.fetchone()
                        conn.commit()
                    except Exception as e:
                        print("exception 3: ", e)
                    layout_emerg_estoque_popup.dismiss()

                layout_emerg_estoque = GridLayout(cols=2)
                layout_emerg_estoque.add_widget(Label(text="Produto"))
                estoque_emerg_produto = TextInput(multiline=False)
                layout_emerg_estoque.add_widget(estoque_emerg_produto)

                layout_emerg_estoque.add_widget(Label(text="Estoque Emergencial"))
                emerg_estoque_input = TextInput(multiline=False, input_filter='float')
                layout_emerg_estoque.add_widget(emerg_estoque_input)

                layout_emerg_estoque_btt = Button(text="Alterar")
                layout_emerg_estoque_btt.bind(on_press=alterar_estoque_emerg)
                layout_emerg_estoque.add_widget(layout_emerg_estoque_btt)
                layout_emerg_estoque_popup = Popup(title="Emergencial_estoque", content=layout_emerg_estoque,
                                                   size_hint=(None, None), size=(600, 600))

                layout_emerg_estoque_popup.open()

            layout_ver_tabela = GridLayout(rows=3,size_hint_y=None,height=1500)

            tabela_header = GridLayout(cols=5)
            tabela_header.add_widget(Label(text="Nome", font_name="fonts/bariol_bold-webfont"))
            tabela_header.add_widget(Label(text="Estoque", font_name="fonts/bariol_bold-webfont"))
            tabela_header.add_widget(Label(text="Min", font_name="fonts/bariol_bold-webfont"))
            tabela_header.add_widget(Label(text="EMERG", font_name="fonts/bariol_bold-webfont"))
            layout_ver_tabela.add_widget(tabela_header)

            tabela_conteudo = GridLayout(cols=4, size_hint_y=None, height=500, spacing=[0, 45], padding=10)

            cursor.execute('''SELECT nome,estoque,estoque_min,estoque_emerg from pigmentos''')
            result = list(cursor.fetchall())
            for i in result:
                for j in i:
                    lbl = Label(text=str(j))
                    tabela_conteudo.add_widget(lbl)

            tabela_view = ScrollView(size_hint=(1, None), width=850, height=350)
            tabela_view.add_widget(tabela_conteudo)
            layout_ver_tabela.add_widget(tabela_view)

            tabela_btt = GridLayout(cols=4, size_hint=(1, None),height=75)

            tabela_btt_enviar = Button(text="Adicionar ao estoque", background_color=(1, 0, 0, 1),
                                       font_name="fonts/bariol_bold-webfont", font_size="14", background_normal='')
            tabela_btt_enviar.bind(on_press=adicionar_estoque)

            tabela_btt_min = Button(text="Mínimo", background_color=(1, 0, 1, 1), font_name="fonts/bariol_bold-webfont",
                                    font_size="14")
            tabela_btt_min.bind(on_press=min_estoque)
            tabela_btt.add_widget(tabela_btt_min)

            tabela_btt_emerg = Button(text="Emergencial", background_color=(1, 1, 0, 1),
                                      font_name="fonts/bariol_bold-webfont", font_size="14")
            tabela_btt_emerg.bind(on_press=emerg_estoque)
            tabela_btt.add_widget(tabela_btt_emerg)

            tabela_btt_add = Button(text="Gerenciar Pigmentos", background_color=(0, 1, 1, 1),
                                    font_name="fonts/bariol_bold-webfont", font_size="14")
            tabela_btt_add.bind(on_press=tela_add_or_rmv)
            tabela_btt.add_widget(tabela_btt_add)

            tabela_btt.add_widget(tabela_btt_enviar)

            layout_ver_tabela.add_widget(tabela_btt)

            aba_estoque_pg = Popup(title="ESTOQUE", content=layout_ver_tabela, size_hint=(0.85, 0.85), )
            aba_estoque_pg.open()

        def forms(instance):
            def tela_rmv_form(instance):
                def remover_funcao(instance):
                    nome_remover_funcao = [form_name_rmv.text]
                    try:
                        cursor_forms.execute("DELETE FROM forms WHERE nome = ?", nome_remover_funcao)
                        conn_forms.commit()
                    except sqlite3.Error as error:
                        print("Failed to delete record from sqlite table", error)
                    layout_tela_rmv_form_popup.dismiss()

                layout_tela_rmv_form = GridLayout(cols=2)

                layout_tela_rmv_form.add_widget(Label(text="Nome da Fórmula"))

                form_name_rmv = TextInput(multiline=False)
                layout_tela_rmv_form.add_widget(form_name_rmv)

                layout_tela_rmv_form_btt_rmv = Button(text="Remover")
                layout_tela_rmv_form_btt_rmv.bind(on_press=remover_funcao)

                layout_tela_rmv_form.add_widget(layout_tela_rmv_form_btt_rmv)

                layout_tela_rmv_form_popup = Popup(title="remover fórmula", content=layout_tela_rmv_form,
                                                   size_hint=(0.85, 0.85))

                layout_tela_rmv_form_popup.open()

            def add_form(instance):
                def adicionar_form_db_func(instance):

                    zz = []
                    dicta = {}

                    for i in range(len(vars_name)):
                        for s in nome_pigmentos_para_forms[i]:
                            zz.append(s)
                        if vars_name[i].text == '' or vars_name[i].text == None:
                            vars_name[i].text = "0"
                        zz.append(vars_name[i].text)
                    dicta[form_name.text] = zz
                    para_db = '\n'.join(dicta[form_name.text])
                    list_of_insert = [form_name.text, para_db]
                    try:
                        cursor_forms.execute("""
                        INSERT INTO forms VALUES(?,?)
                        """, list_of_insert)
                        # conn_forms.commit()
                    except Exception as e:
                        print("exception 4: ", e)
                    layout_add_form_popup.dismiss()

                layout_add_form = GridLayout(cols=2)
                layout_add_form.add_widget(Label(text="Nome"))
                form_name = TextInput(multiline=False)
                layout_add_form.add_widget(form_name)
                cursor.execute("SELECT nome FROM pigmentos")
                nome_pigmentos_para_forms = cursor.fetchall()
                vars_name = []
                for i in nome_pigmentos_para_forms:
                    for z in i:
                        layout_add_form.add_widget(Label(text=str(z)))
                        globals()[z] = TextInput(text="0", multiline=False, input_filter='float')
                        layout_add_form.add_widget(globals()[z])
                        vars_name.append(globals()[z])
                adicionar_form_db_btt = Button(text="Enviar")
                adicionar_form_db_btt.bind(on_press=adicionar_form_db_func)
                layout_add_form.add_widget(adicionar_form_db_btt)

                layout_add_form_popup = Popup(title="cansei já", content=layout_add_form, size_hint=(0.85, 0.85))

                layout_add_form_popup.open()
            
            def ver_forms_func(instance):

                tabela = GridLayout(cols=2)

                tabela.add_widget(Label(text="Nome da Fórmula"))
                tabela.add_widget(Label(text="Fórmula"))

                cursor_forms.execute("SELECT nome FROM forms")
                nomes_forms = cursor_forms.fetchall()

                cursor_forms.execute("SELECT pgmts FROM forms")
                formula = cursor_forms.fetchall()

                print(formula)

                for i in nomes_forms:
                    for z in range(len(i)):
                        print(i[z])

                ver_forms_func_popup = Popup(title="Ver forms",content = tabela)
                ver_forms_func_popup.open()


            layout_forms = GridLayout(rows=2)

            layout_forms_btt_add = Button(text="Adicionar")
            layout_forms_btt_add.bind(on_press=add_form)

            layout_forms_btt_rmv = Button(text="Remover")
            layout_forms_btt_rmv.bind(on_press=tela_rmv_form)

            layout_forms_btt_form = Button(text="Ver Forms")
            layout_forms_btt_form.bind(on_press=ver_forms_func)

            layout_forms.add_widget(layout_forms_btt_add)
            layout_forms.add_widget(layout_forms_btt_rmv)
            layout_forms.add_widget(layout_forms_btt_form)


            

            layout_forms_popup = Popup(title="SIMULAÇÃO", content=layout_forms, size_hint=(0.85, 0.85))
            layout_forms_popup.open()

        def simular_tab(instance):

            def pesquisa_forms_func(instance, value):

                pesquisa_forms.clear_widgets()
                if form.text != '':
                    cursor_forms.execute("SELECT nome FROM forms WHERE nome LIKE '{}%'".format(form.text))
                    nomes = cursor_forms.fetchall()
                    for i in nomes:
                        for z in i:
                            pesquisa_forms.add_widget(Label(text=str(z)))

            def enviar_simulacao(instance):
                def comitar(instance):
                    validar = True
                    for i in range(len(valor_quando_abater)):
                        if valor_quando_abater[i] < 0:
                            validar = False
                        if validar:
                            for i in range(len(valor_quando_abater)):
                                lista_pro_db = [valor_quando_abater[i], nomes_pigmentos_lista[i]]
                                conn.execute("UPDATE pigmentos SET estoque = ? WHERE nome = ?", lista_pro_db)
                                conn.commit()

                try:
                    valor_quando_abater = []

                    cursor.execute("SELECT nome FROM pigmentos")
                    nomes_pigmentos = cursor.fetchall()
                    nomes_pigmentos_lista = []
                    for i in nomes_pigmentos:
                        for j in i:
                            nomes_pigmentos_lista.append(j)

                    for i in range(len(nomes_pigmentos_lista)):
                        nome_pro_db = [nomes_pigmentos_lista[i]]
                        cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?", nome_pro_db)
                        valor_antigo = cursor.fetchone()
                        for z in valor_antigo:
                            valor_antigo_fora_do_tuple = z
                        valor_quando_abater.append(valor_antigo_fora_do_tuple - tabela_simulacao_cores[i])
                        # print(float(valor_antigo_fora_do_tuple))
                        # print(float(tabela_simulacao_cores[i]))

                    layout_mostrar_simulacao = GridLayout(cols=2)
                    layout_mostrar_simulacao.add_widget(Label(text="Nome do pigmento"))
                    layout_mostrar_simulacao.add_widget(Label(text="Valor pós simulação"))

                    for i in range(len(valor_quando_abater)):
                        layout_mostrar_simulacao.add_widget(Label(text=str(nomes_pigmentos_lista[i])))
                        if valor_quando_abater[i] >= 0:
                            layout_mostrar_simulacao.add_widget(Label(text=str(valor_quando_abater[i])))
                        else:
                            layout_mostrar_simulacao.add_widget(
                                Label(text=str(valor_quando_abater[i]), color=[1, 0, 0, 1]))

                    layout_mostrar_simulacao_btt_enviar = Button(text="Enivar")
                    layout_mostrar_simulacao_btt_enviar.bind(on_press=comitar)
                    layout_mostrar_simulacao.add_widget(layout_mostrar_simulacao_btt_enviar)
                    layout_mostrar_simulacao_btt_cancelar = Button(text="Cancelar")
                    layout_mostrar_simulacao.add_widget(layout_mostrar_simulacao_btt_cancelar)

                    layout_mostrar_simulacao_popup = Popup(title="Simulação", content=layout_mostrar_simulacao,
                                                           size_hint=(0.85, 0.85))
                    layout_mostrar_simulacao_popup.open()
                except Exception as e:
                    print("exception 5: ", e)

            cursor_forms.execute("SELECT pgmts FROM forms")

            tamanho_lista = cursor_forms.fetchall()
            for i in tamanho_lista:
                for z in i:
                    a = z.split('\n')

            try:
                tabela_simulacao_cores = [0] * (int(len(a) / 2))
            except Exception as e:
                print("exception 6: ", e)

            def adicionar_cor(instance):
                def refresh_simu():
                    layout_mostrar_simulacao.clear_widgets()
                    try:
                        valor_quando_abater = []
                        valor_antes_abater = []

                        cursor.execute("SELECT nome FROM pigmentos")
                        nomes_pigmentos = cursor.fetchall()
                        nomes_pigmentos_lista = []
                        for i in nomes_pigmentos:
                            for j in i:
                                nomes_pigmentos_lista.append(j)

                        for i in range(len(nomes_pigmentos_lista)):
                            nome_pro_db = [nomes_pigmentos_lista[i]]
                            cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?", nome_pro_db)
                            valor_antigo = cursor.fetchone()
                            for z in valor_antigo:
                                valor_antigo_fora_do_tuple = z
                            print(tabela_simulacao_cores)
                            valor_quando_abater.append(valor_antigo_fora_do_tuple - tabela_simulacao_cores[i])
                            valor_antes_abater.append(valor_antigo_fora_do_tuple)
                            # print(float(valor_antigo_fora_do_tuple))
                            # print(float(tabela_simulacao_cores[i]))

                        for i in range(len(valor_quando_abater)):
                            if valor_quando_abater[i] != valor_antes_abater[i]:
                                layout_mostrar_simulacao.add_widget(Label(text=str(nomes_pigmentos_lista[i])))
                                if valor_quando_abater[i] >= 0:
                                    layout_mostrar_simulacao.add_widget(Label(text=str(valor_quando_abater[i])))
                                else:
                                    layout_mostrar_simulacao.add_widget(
                                        Label(text=str(valor_quando_abater[i]), color=[1, 0, 0, 1]))
                            else:
                                print("{} não alterou".format(nomes_pigmentos_lista[i]))
                    except Exception as e:
                        print("exception 7: ", e)

                if form.text == '' or form.text == " ":
                    print("vai dar nao")
                else:
                    formula = [form.text]
                    cursor_forms.execute("SELECT pgmts FROM forms WHERE nome = ?", formula)
                    lista_pgmt = cursor_forms.fetchall()
                    lista_formatada = []

                    for i in lista_pgmt:
                        for z in i:
                            lista_formatada_pre = z.split("\n")

                    try:
                        for xyz in lista_formatada_pre:
                            if xyz.isnumeric():
                                lista_formatada.append(xyz)
                        forms_enviados.add_widget(Label(text=form.text + " X {}".format(qnt.text)))
                    except Exception as e:
                        print("exception 8: ", e)

                    for asd in range(len(lista_formatada)):
                        try:
                            tabela_simulacao_cores[asd] += (float(lista_formatada[asd])) * int(qnt.text)
                        except Exception as e:
                            print("exception 9: ", e)
                    form.text = ""
                    qnt.text = "1"
                    refresh_simu()

            def abater_formula(instance):
                if form.text == "" or form.text == " ":
                    print("vai dar nao tbm")
                else:
                    form_name = [form.text]
                    cursor_forms.execute("SELECT * FROM forms WHERE nome=?", form_name)
                    test = cursor_forms.fetchall()
                    nomes = []
                    valores = []
                    for i in test:
                        for j in test:
                            for z in range(len(j)):
                                s = j[z].split("\n")
                                for zx in range(len(s)):
                                    if zx % 2 == 0:
                                        nomes.append(s[zx])
                                    else:
                                        valores.append("-" + s[zx])
                    try:
                        nomes.remove(nomes[0])
                    except Exception as e:
                        print("exception 10: ", e)

                    for i in range(len(nomes)):

                        nome_tabela = [nomes[i]]
                        cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?", nome_tabela)
                        result = cursor.fetchone()
                        for z in result:
                            estoque_antigo = z
                        novo_estoque = float(valores[i]) + float(estoque_antigo)
                        incremento_estoque = [novo_estoque, nomes[i]]

                        conn.execute("UPDATE pigmentos SET estoque = ? WHERE nome = ?", incremento_estoque)
                        conn.commit()

            def limpar_sim(instance):
                # entendi direito como funciona não
                layout_simular_tab_full_popup.dismiss()

                simular_tab(instance)

            layout_simular_tab_full_mais_full_ainda = GridLayout(cols=2)

            layout_simular_tab_full = GridLayout(rows=2)

            layout_simular_tab = GridLayout(cols=2)
            layout_simular_tab.add_widget(Label(text='Fórmula'))
            form = TextInput(multiline=False)
            form.bind(text=pesquisa_forms_func)
            layout_simular_tab.add_widget(form)

            layout_simular_tab.add_widget(Label(text='Quantidade'))
            qnt = TextInput(multiline=False, input_filter='float', text="1")
            layout_simular_tab.add_widget(qnt)

            pesquisa_forms = GridLayout(cols=2)

            forms_enviados = GridLayout(cols=2)

            layout_simular_tab.add_widget(pesquisa_forms)

            layout_simular_tab.add_widget(forms_enviados)

            layout_simular_tab_full.add_widget(layout_simular_tab)

            simular_tab_btts_bottom = GridLayout(cols=2, size_hint=(1, 0.3))

            simular_tab_btts_bottom_btt_limpar = Button(text="Limpar")
            simular_tab_btts_bottom_btt_limpar.bind(on_press=limpar_sim)
            simular_tab_btts_bottom.add_widget(simular_tab_btts_bottom_btt_limpar)

            simular_tab_btts_bottom_btt_adicionar_cor = Button(text="Adicionar")
            simular_tab_btts_bottom_btt_adicionar_cor.bind(on_press=adicionar_cor)
            simular_tab_btts_bottom.add_widget(simular_tab_btts_bottom_btt_adicionar_cor)

            simular_tab_btts_bottom_btt_abater_estoque = Button(text="Fórmulas")
            simular_tab_btts_bottom_btt_abater_estoque.bind(on_press=forms)
            simular_tab_btts_bottom.add_widget(simular_tab_btts_bottom_btt_abater_estoque)

            simular_tab_btts_bottom_btt_simular = Button(text="Simular")
            simular_tab_btts_bottom_btt_simular.bind(on_press=enviar_simulacao)
            simular_tab_btts_bottom.add_widget(simular_tab_btts_bottom_btt_simular)

            layout_simular_tab_full.add_widget(simular_tab_btts_bottom)

            layout_simular_tab_full_mais_full_ainda.add_widget(layout_simular_tab_full)

            try:
                valor_quando_abater = []

                cursor.execute("SELECT nome FROM pigmentos")
                nomes_pigmentos = cursor.fetchall()
                nomes_pigmentos_lista = []
                for i in nomes_pigmentos:
                    for j in i:
                        nomes_pigmentos_lista.append(j)

                for i in range(len(nomes_pigmentos_lista)):
                    nome_pro_db = [nomes_pigmentos_lista[i]]
                    cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?", nome_pro_db)
                    valor_antigo = cursor.fetchone()
                    for z in valor_antigo:
                        valor_antigo_fora_do_tuple = z
                    valor_quando_abater.append(valor_antigo_fora_do_tuple - tabela_simulacao_cores[i])
                    # print(float(valor_antigo_fora_do_tuple))
                    # print(float(tabela_simulacao_cores[i]))

                layout_mostrar_simulacao = GridLayout(cols=2)
                layout_mostrar_simulacao.add_widget(Label(text="Nome do pigmento"))
                layout_mostrar_simulacao.add_widget(Label(text="Valor pós simulação"))

                for i in range(len(valor_quando_abater)):
                    layout_mostrar_simulacao.add_widget(Label(text=str(nomes_pigmentos_lista[i])))
                    if valor_quando_abater[i] >= 0:
                        layout_mostrar_simulacao.add_widget(Label(text=str(valor_quando_abater[i])))
                    else:
                        layout_mostrar_simulacao.add_widget(
                            Label(text=str(valor_quando_abater[i]), color=[1, 0, 0, 1]))
            except Exception as e:
                print('exception 11: ', e)
            try:
                layout_simular_tab_full_mais_full_ainda.add_widget(layout_mostrar_simulacao)

                layout_simular_tab_full_popup = Popup(title="ABA DE SIMULAÇÃO?",
                                                      content=layout_simular_tab_full_mais_full_ainda,
                                                      size_hint=(0.85, 0.85))

                layout_simular_tab_full_popup.open()
            except Exception as e:
                print("exception 12: ", e)

        def tela_add_or_rmv(instance):
            def add_pigmento(instance):
                def add_pgm_de_vdd(instance):
                    if layout_add_pgm_TI_nome.text == '' or layout_add_pgm_TI_nome.text == ' ':
                        print("Nome vazio")
                    else:
                        if layout_add_pgm_TI_quantidade.text == '' or layout_add_pgm_TI_quantidade.text == None and layout_add_pgm_TI_est_min.text == '' or layout_add_pgm_TI_est_min.text == None and layout_add_pgm_TI_est_emerg.text == '' or layout_add_pgm_TI_est_emerg.text == None:
                            layout_add_pgm_TI_quantidade.text = "0"
                            layout_add_pgm_TI_est_min.text = "1"
                            layout_add_pgm_TI_est_emerg.text = "1"


                        elif layout_add_pgm_TI_est_min.text == '' or layout_add_pgm_TI_est_min.text == None:
                            layout_add_pgm_TI_est_min.text = "1"
                            layout_add_pgm_TI_est_emerg.text = "1"

                        elif layout_add_pgm_TI_est_emerg.text == '' or layout_add_pgm_TI_est_emerg.text == None:
                            layout_add_pgm_TI_est_emerg.text = "1"

                        lista_novo_pgm = [layout_add_pgm_TI_nome.text, layout_add_pgm_TI_quantidade.text,
                                          layout_add_pgm_TI_est_min.text, layout_add_pgm_TI_est_emerg.text]
                        conn.execute("INSERT INTO pigmentos(nome,estoque,estoque_min,estoque_emerg) VALUES(?,?,?,?)",
                                     lista_novo_pgm)
                        cursor.execute('''SELECT * from pigmentos''')
                        conn.commit()
                        layout_add_pgm_popup.dismiss()

                layout_add_pgm_toda = GridLayout(rows=2)
                layout_add_pgm = GridLayout(cols=2)
                layout_add_pgm.add_widget(Label(text="Nome"))
                layout_add_pgm_TI_nome = TextInput(multiline=False)
                layout_add_pgm.add_widget(layout_add_pgm_TI_nome)
                layout_add_pgm.add_widget(Label(text="Quantidade"))
                layout_add_pgm_TI_quantidade = TextInput(multiline=False, input_filter='float')
                layout_add_pgm.add_widget(layout_add_pgm_TI_quantidade)
                layout_add_pgm.add_widget(Label(text="Estoque mínimo"))
                layout_add_pgm_TI_est_min = TextInput(multiline=False, input_filter='float')
                layout_add_pgm.add_widget(layout_add_pgm_TI_est_min)
                layout_add_pgm.add_widget(Label(text="Estoque emergencial"))
                layout_add_pgm_TI_est_emerg = TextInput(multiline=False, input_filter='float')
                layout_add_pgm.add_widget(layout_add_pgm_TI_est_emerg)

                layout_add_pgm_toda.add_widget(layout_add_pgm)
                layout_add_pgm_btt = Button(text="Adicionar novo pigmento no banco de dados")
                layout_add_pgm_btt.bind(on_press=add_pgm_de_vdd)
                layout_add_pgm_toda.add_widget(layout_add_pgm_btt)

                layout_add_pgm_popup = Popup(title="ADD PIGMENTO", content=layout_add_pgm_toda, size_hint=(0.85, 0.85))
                layout_add_pgm_popup.open()

            def rmv_pigmento(instance):
                def remover_pigmento_de_vdd(instance):
                    nome = [nome_pra_remover.text]
                    try:
                        cursor.execute("DELETE FROM pigmentos WHERE nome = ?", nome)
                        conn.commit()
                    except sqlite3.Error as error:
                        print("Failed to delete record from sqlite table", error)

                layout_tela_rmv = GridLayout(cols=2)

                layout_tela_rmv.add_widget(Label(text="Nome"))

                nome_pra_remover = TextInput(multiline=False)
                layout_tela_rmv.add_widget(nome_pra_remover)

                layout_tela_rmv_btt = Button(text="Remover pigmento")
                layout_tela_rmv_btt.bind(on_press=remover_pigmento_de_vdd)
                layout_tela_rmv.add_widget(layout_tela_rmv_btt)

                layout_tela_rmv_popup = Popup(title="remover pigmento", content=layout_tela_rmv, size_hint=(0.85, 0.85))
                layout_tela_rmv_popup.open()

            layout_tela_add_or_tmv = GridLayout(rows=2)
            layout_tela_add_or_tmv_btt_add = Button(text="Adicionar")
            layout_tela_add_or_tmv_btt_add.bind(on_press=add_pigmento)
            layout_tela_add_or_tmv_btt_rmv = Button(text="Remover")
            layout_tela_add_or_tmv_btt_rmv.bind(on_press=rmv_pigmento)
            layout_tela_add_or_tmv.add_widget(layout_tela_add_or_tmv_btt_add)
            layout_tela_add_or_tmv.add_widget(layout_tela_add_or_tmv_btt_rmv)

            layout_tela_add_or_tmv_popup = Popup(title="ADD or RMV", content=layout_tela_add_or_tmv,
                                                 size_hint=(0.85, 0.85))

            layout_tela_add_or_tmv_popup.open()

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
            menu.clear_widgets()
            estoque_menu_layout = GridLayout(cols=2)
            estoque_menu_layout.add_widget(Label(text="Estoque View"))
            menu.add_widget(estoque_menu_layout)

        def relatorios_view(instance):
            menu.clear_widgets()
            relatorios_menu_layout = GridLayout(cols=2)
            relatorios_menu_layout.add_widget(Label(text="Relatŕios View"))
            menu.add_widget(relatorios_menu_layout)

        def settings_view(instance):
            menu.clear_widgets()
            settings_menu_layout = GridLayout(cols=2)
            settings_menu_layout.add_widget(Label(text="Settings View"))
            menu.add_widget(settings_menu_layout)

        side_bar = GridLayout(cols=1)

        side_bar.add_widget(Label(text="Kamaleão", size_hint=(None, None), height=220, width=150))

        Button_produção = ToggleButton(size_hint=(None, None), height=75, width=150, background_normal="img/Produção.png", group='side_menu')
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

        Button_settings = ToggleButton(size_hint=(None, None), height=75, width=150,background_normal="img/settings.png", group='side_menu')
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
