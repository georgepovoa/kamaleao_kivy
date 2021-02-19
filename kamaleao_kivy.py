from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

import sqlite3


class KamaleaoApp(App):
    def build(self):
        conn = sqlite3.connect('pigmentos.db')
        cursor = conn.cursor()
        conn_forms = sqlite3.connect('forms.db')
        cursor_forms = conn_forms.cursor()
        pigmentos_table = """ 
        CREATE TABLE pigmentos(
        nome CHAR(20) NOT NULL,
        estoque FLOAT NOT NULL,
        misturas INT ,
        estoque_min float,
        estoque_emerg float
        
        )
        """

        def aba_estoque(instance):
            def ver_tabela(instance):
                def adicionar_estoque(instance):

                    def enviar_db(nome):
                        def enviar_db_de_vdd(instance):
                            nome_tabela = [nome]
                            cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?", nome_tabela)
                            result = cursor.fetchone()
                            print(result)
                            for i in result:
                                estoque_antigo = i
                            novo_estoque = float(quantidade_adicionar.text) + estoque_antigo
                            print(novo_estoque)
                            incremento_estoque = [novo_estoque, nome]
                            conn.execute("UPDATE pigmentos SET estoque = ? WHERE nome = ?", incremento_estoque)
                            cursor.execute('''SELECT * from pigmentos''')
                            #conn.commit()
                            result = cursor.fetchall()
                            print(result)

                        tela_adicionar_estoque = GridLayout(rows=2)
                        quantidade_adicionar = TextInput()
                        tela_adicionar_estoque_cima = GridLayout(cols=2)

                        tela_adicionar_estoque_cima.add_widget(Label(text="quantidade à se adicionar ao estoque: "))
                        tela_adicionar_estoque_cima.add_widget(quantidade_adicionar)

                        tela_adicionar_estoque.add_widget(tela_adicionar_estoque_cima)

                        tela_adicionar_estoque_baixo_btt = Button(text="enviar")
                        tela_adicionar_estoque_baixo_btt.bind(on_press=enviar_db_de_vdd)
                        tela_adicionar_estoque.add_widget(tela_adicionar_estoque_baixo_btt)

                        tela_adicionar_estoque_popup = Popup(title="adicionar estoque" + nome,
                                                             content=tela_adicionar_estoque)
                        tela_adicionar_estoque_popup.open()

                    ## LABELS ##
                    adicionar_estoque = GridLayout(cols=4)
                    cursor.execute('''SELECT nome from pigmentos''')
                    result = list(cursor.fetchall())
                    for i in result:
                        for j in i:
                            print(j)
                            btn = Button(text=str(j))
                            btn.bind(on_release=lambda btn: enviar_db(btn.text))
                            adicionar_estoque.add_widget(btn)

                    adicionar_estoque_popup = Popup(title="adicioar ao estoque", content=adicionar_estoque)
                    adicionar_estoque_popup.open()

                layout_ver_tabela = GridLayout(rows=3)

                tabela_header = GridLayout(cols=5)
                tabela_header.add_widget(Label(text="Nome"))
                tabela_header.add_widget(Label(text="estoque"))
                tabela_header.add_widget(Label(text="Min"))
                tabela_header.add_widget(Label(text="EMERG"))
                layout_ver_tabela.add_widget(tabela_header)

                tabela_conteudo = GridLayout(cols=4, size_hint_y=None, height=5000, spacing=[0, 45], padding=25)

                cursor.execute('''SELECT nome,estoque,estoque_min,estoque_emerg from pigmentos''')
                result = list(cursor.fetchall())
                for i in result:
                    for j in i:
                        print(j)
                        lbl = Label(text=str(j))
                        tabela_conteudo.add_widget(lbl)

                tabela_view = ScrollView(size_hint=(1, None), width=850, height=300)
                tabela_view.add_widget(tabela_conteudo)
                layout_ver_tabela.add_widget(tabela_view)

                tabela_btt = GridLayout(cols=2)

                tabela_btt_enviar = Button(text="Adicionar")
                tabela_btt_enviar.bind(on_press=adicionar_estoque)
                tabela_btt.add_widget(tabela_btt_enviar)

                tabela_btt_enviar = Button(text="Remover")
                tabela_btt.add_widget(tabela_btt_enviar)

                layout_ver_tabela.add_widget(tabela_btt)

                ver_tabela_popup = Popup(title="Estoque", content=layout_ver_tabela)
                ver_tabela_popup.open()

            def min_estoque(instance):
                def alterar_min_estoque(instance):
                    teste_tabela = [estoque_min_produto.text]
                    cursor.execute("SELECT estoque_min FROM pigmentos WHERE nome = ?", teste_tabela)
                    result = cursor.fetchone()
                    print(result)
                    novo_estoque_min = [float(min_estoque_input.text), estoque_min_produto.text]
                    print(novo_estoque_min)
                    conn.execute("UPDATE pigmentos SET estoque_min = ? WHERE nome = ?", novo_estoque_min)
                    cursor.execute("SELECT estoque_min FROM pigmentos WHERE nome = ?", teste_tabela)
                    result = cursor.fetchone()
                    #conn.commit()
                    print(result)

                layout_min_estoque = GridLayout(cols=4)
                layout_min_estoque.add_widget(Label(text="produto"))
                estoque_min_produto = TextInput()
                layout_min_estoque.add_widget(estoque_min_produto)

                layout_min_estoque.add_widget(Label(text="Min estoque"))
                min_estoque_input = TextInput()
                layout_min_estoque.add_widget(min_estoque_input)

                layout_min_estoque_btt = Button(text="alterar")
                layout_min_estoque_btt.bind(on_press=alterar_min_estoque)
                layout_min_estoque.add_widget(layout_min_estoque_btt)

                layout_min_estoque_popup = Popup(title="min_extoque", content=layout_min_estoque,
                                                 size_hint=(None, None), size=(600, 120))
                layout_min_estoque_popup.open()

            def emerg_estoque(instance):
                def alterar_estoque_emerg(instance):
                    teste_tabela = [estoque_emerg_produto.text]
                    cursor.execute("SELECT estoque_emerg FROM pigmentos WHERE nome = ?", teste_tabela)
                    result = cursor.fetchone()
                    print(result)
                    novo_estoque_emerg = [float(emerg_estoque_input.text), estoque_emerg_produto.text]
                    print(novo_estoque_emerg)
                    conn.execute("UPDATE pigmentos SET estoque_emerg = ? WHERE nome = ?", novo_estoque_emerg)
                    cursor.execute("SELECT estoque_emerg FROM pigmentos WHERE nome = ?", teste_tabela)
                    result = cursor.fetchone()
                    #conn.commit()
                    print(result)

                layout_emerg_estoque = GridLayout(cols=4)
                layout_emerg_estoque.add_widget(Label(text="produto"))
                estoque_emerg_produto = TextInput()
                layout_emerg_estoque.add_widget(estoque_emerg_produto)

                layout_emerg_estoque.add_widget(Label(text="Estoque Emergencial"))
                emerg_estoque_input = TextInput()
                layout_emerg_estoque.add_widget(emerg_estoque_input)

                layout_emerg_estoque_btt = Button(text="alterar")
                layout_emerg_estoque_btt.bind(on_press=alterar_estoque_emerg)
                layout_emerg_estoque.add_widget(layout_emerg_estoque_btt)
                layout_emerg_estoque_popup = Popup(title="Emergencial_estoque", content=layout_emerg_estoque,
                                                   size_hint=(None, None), size=(600, 120))
                layout_emerg_estoque_popup.open()

            layout_estoque = GridLayout(rows=3)

            layout_estoque_btt_ver_tabela = Button(text="Tabela")
            layout_estoque_btt_ver_tabela.bind(on_press=ver_tabela)
            layout_estoque.add_widget(layout_estoque_btt_ver_tabela)

            layout_estoque_min_btt = Button(text="Estoque Min.")
            layout_estoque_min_btt.bind(on_press=min_estoque)
            layout_estoque.add_widget(layout_estoque_min_btt)

            layout_estoque_emerg_btt = Button(text="Estoque Emergencial")
            layout_estoque_emerg_btt.bind(on_press=emerg_estoque)
            layout_estoque.add_widget(layout_estoque_emerg_btt)

            layout_estoque_add_novo_pgm = Button(text="Gerenciar pigmentos")
            layout_estoque_add_novo_pgm.bind(on_press=add_pigmento)
            layout_estoque.add_widget(layout_estoque_add_novo_pgm)

            aba_estoque_pg = Popup(title="popup", content=layout_estoque, size_hint=(None, None), size=(400, 400))
            aba_estoque_pg.open()

        def forms(instance):
            def add_form(instance):
                def asjdklsa(instance):
                    zz = []
                    dicta = {}

                    for i in range(len(vars_name)):
                        for s in sei_do_q_chamar_n[i]:
                            zz.append(s)
                        zz.append(vars_name[i].text)
                    dicta[form_name.text] = zz
                    para_db = '\n'.join(dicta[form_name.text])
                    list_of_insert = [form_name.text, para_db]
                    try:
                        cursor_forms.execute("""
                        INSERT INTO forms VALUES(?,?)
                        """, list_of_insert)
                    except:
                        print("deu nao")
                    cursor_forms.execute("SELECT * FROM forms")
                    print_db_forms = cursor_forms.fetchall()
                    for i in print_db_forms:
                        for j in i:
                            print(j)

                layout_add_form = GridLayout(rows=30)
                layout_add_form.add_widget(Label(text="nome"))
                form_name = TextInput()
                layout_add_form.add_widget(form_name)
                cursor.execute("SELECT nome FROM pigmentos")
                sei_do_q_chamar_n = cursor.fetchall()
                vars_name = []
                for i in sei_do_q_chamar_n:
                    for z in i:
                        layout_add_form.add_widget(Label(text=str(z)))
                        globals()[z] = TextInput(text="0")
                        layout_add_form.add_widget(globals()[z])
                        vars_name.append(globals()[z])
                asdasdsa = Button(text="enviar")
                asdasdsa.bind(on_press=asjdklsa)
                layout_add_form.add_widget(asdasdsa)

                layout_add_form_popup = Popup(title="cansei já", content=layout_add_form)

                layout_add_form_popup.open()

            layout_forms = GridLayout(rows=2)

            layout_forms_btt_add = Button(text="add")
            layout_forms_btt_add.bind(on_press=add_form)

            layout_forms_btt_rmv = Button(text="rmv")
            layout_forms.add_widget(layout_forms_btt_add)
            layout_forms.add_widget(layout_forms_btt_rmv)

            layout_forms_popup = Popup(title="SIMULAÇÃO", content=layout_forms)
            layout_forms_popup.open()

        def aba_producao(instance):

            def simular_tab(instance):
                def enviar_simulacao(instance):
                    valor_quando_abater = []

                    cursor.execute("SELECT nome FROM pigmentos")
                    nomes_pigmentos = cursor.fetchall()
                    nomes_pigmentos_lista=[]
                    for i in nomes_pigmentos:
                        for j in i:
                            nomes_pigmentos_lista.append(j)

                    for i in range(len(nomes_pigmentos_lista)):
                        nome_pro_db = [nomes_pigmentos_lista[i]]
                        cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?",nome_pro_db)
                        valor_antigo = cursor.fetchone()
                        for z in valor_antigo:
                            valor_antigo_fora_do_tuple = z
                        print(valor_antigo_fora_do_tuple)
                        valor_quando_abater.append(valor_antigo_fora_do_tuple-tabela_simulacao_cores[i])
                        print(valor_quando_abater)

                    layout_mostrar_simulacao = GridLayout(cols=2)
                    layout_mostrar_simulacao.add_widget(Label(text="NOME PGMENTO"))
                    layout_mostrar_simulacao.add_widget(Label(text="VALOR DEPOIS DA SIMULAÇÃO"))

                    for i in range(len(valor_quando_abater)):
                        layout_mostrar_simulacao.add_widget(Label(text=str(nomes_pigmentos_lista[i])))
                        layout_mostrar_simulacao.add_widget(Label(text=str(valor_quando_abater[i])))
                    layout_mostrar_simulacao_btt_enviar = Button(text="enivar")
                    layout_mostrar_simulacao.add_widget(layout_mostrar_simulacao_btt_enviar)
                    layout_mostrar_simulacao_btt_cancelar = Button(text="cancelar")
                    layout_mostrar_simulacao.add_widget(layout_mostrar_simulacao_btt_cancelar)


                    layout_mostrar_simulacao_popup = Popup(title="SIMULAÇÃO",content =layout_mostrar_simulacao )
                    layout_mostrar_simulacao_popup.open()






                cursor_forms.execute("SELECT pgmts FROM forms")

                tamanho_lista = cursor_forms.fetchall()
                for i in tamanho_lista:
                    for z in i:
                        a = z.split('\n')
                tabela_simulacao_cores = [0] * (int(len(a) / 2))
                print(len(tabela_simulacao_cores))

                def adicionar_cor(instance):
                    add_pgmts = []
                    formula = [form.text]
                    cursor_forms.execute("SELECT pgmts FROM forms WHERE nome = ?", formula)
                    lista_pgmt = cursor_forms.fetchall()
                    lista_formatada =[]

                    for i in lista_pgmt:
                        for z in i:
                            lista_formatada_pre = z.split("\n")
                            print("LISTA FORMATADA:",lista_formatada_pre)

                    for xyz in lista_formatada_pre:
                        if xyz.isnumeric():
                            lista_formatada.append(xyz)



                    print("LISTA FORMATADA:", lista_formatada)
                    for asd in range(len(lista_formatada)):
                        print(lista_formatada[asd])
                        try:
                            print("foi o try", lista_formatada[asd])
                            tabela_simulacao_cores[asd] += int(lista_formatada[asd])
                        except:
                            pass

                    print(tabela_simulacao_cores)
                    print("len: ", len(tabela_simulacao_cores))




                    form.text = ""
                    qnt.text = ""

                def abater_formula(instance):


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
                    nomes.remove(nomes[0])
                    print(nomes)
                    print(valores)

                    for i in range(len(nomes)):

                        nome_tabela = [nomes[i]]
                        cursor.execute("SELECT estoque FROM pigmentos WHERE nome = ?", nome_tabela)
                        result = cursor.fetchone()
                        print(result)
                        for z in result:
                            estoque_antigo = z
                        novo_estoque = float(valores[i]) + float(estoque_antigo)
                        incremento_estoque = [novo_estoque, nomes[i]]

                        conn.execute("UPDATE pigmentos SET estoque = ? WHERE nome = ?", incremento_estoque)
                        cursor.execute('''SELECT * from pigmentos''')
                        result = cursor.fetchall()
                    print(result)

                layout_simular_tab_full = GridLayout(rows=2)

                layout_simular_tab = GridLayout(cols=2)
                layout_simular_tab.add_widget(Label(text='formula'))
                form = TextInput()
                layout_simular_tab.add_widget(form)

                layout_simular_tab.add_widget(Label(text='Quantidade'))
                qnt = TextInput()
                layout_simular_tab.add_widget(qnt)

                layout_simular_tab_full.add_widget(layout_simular_tab)

                simular_tab_btts_bottom = GridLayout(cols=3)
                simular_tab_btts_bottom_btt_simular = Button(text="simular")
                simular_tab_btts_bottom_btt_simular.bind(on_press = enviar_simulacao)

                simular_tab_btts_bottom.add_widget(simular_tab_btts_bottom_btt_simular)

                simular_tab_btts_bottom_btt_adicionar_cor = Button(text="adicionar cor")
                simular_tab_btts_bottom_btt_adicionar_cor.bind(on_press=adicionar_cor)
                simular_tab_btts_bottom.add_widget(simular_tab_btts_bottom_btt_adicionar_cor)

                simular_tab_btts_bottom_btt_abater_estoque = Button(text="abater no estoque")
                simular_tab_btts_bottom_btt_abater_estoque.bind(on_press=abater_formula)
                simular_tab_btts_bottom.add_widget(simular_tab_btts_bottom_btt_abater_estoque)

                layout_simular_tab_full.add_widget(simular_tab_btts_bottom)

                layout_simular_tab_full_popup = Popup(title="q?", content=layout_simular_tab_full)

                layout_simular_tab_full_popup.open()

            layout_prod = GridLayout(rows=3)

            layout_prod_simulacao_btt = Button(text="simular")
            layout_prod_simulacao_btt.bind(on_press=simular_tab)
            layout_prod.add_widget(layout_prod_simulacao_btt)

            layout_prod_baixa_btt = Button(text="dar baixa em estoque")
            layout_prod.add_widget(layout_prod_baixa_btt)

            layout_prod_forms_btt = Button(text="gerenciar Fórmulas")
            layout_prod_forms_btt.bind(on_press=forms)
            layout_prod.add_widget(layout_prod_forms_btt)

            layout_prod_popup = Popup(title="PROD", content=layout_prod)
            layout_prod_popup.open()

        layout = GridLayout(cols=1)

        def aba_rel(instance):
            cursor.execute("SELECT * FROM pigmentos")
            a = cursor.fetchall()
            for i in a:
                print(i)
            layout_fin = GridLayout(cols=2)
            layout_fin.add_widget(Label(text="ainda nao sei o que colocar"))

            layout_fin_popup = Popup(title="fin", content=layout_fin)
            layout_fin_popup.open()

        def add_pigmento(instance):
            def add_pgm_de_vdd(instance):
                lista_novo_pgm = [layout_add_pgm_TI_nome.text, layout_add_pgm_TI_quantidade.text,
                                  layout_add_pgm_TI_est_min.text, layout_add_pgm_TI_est_emerg.text]
                conn.execute("INSERT INTO pigmentos(nome,estoque,estoque_min,estoque_emerg) VALUES(?,?,?,?)",
                             lista_novo_pgm)
                cursor.execute('''SELECT * from pigmentos''')
                #conn.commit()
                result = cursor.fetchall()
                print(result)

            layout_add_pgm_toda = GridLayout(rows=2)
            layout_add_pgm = GridLayout(cols=2)
            layout_add_pgm.add_widget(Label(text="nome"))
            layout_add_pgm_TI_nome = TextInput()
            layout_add_pgm.add_widget(layout_add_pgm_TI_nome)
            layout_add_pgm.add_widget(Label(text="quantidade"))
            layout_add_pgm_TI_quantidade = TextInput()
            layout_add_pgm.add_widget(layout_add_pgm_TI_quantidade)
            layout_add_pgm.add_widget(Label(text="estoque minimo"))
            layout_add_pgm_TI_est_min = TextInput()
            layout_add_pgm.add_widget(layout_add_pgm_TI_est_min)
            layout_add_pgm.add_widget(Label(text="estoque emergencial"))
            layout_add_pgm_TI_est_emerg = TextInput()
            layout_add_pgm.add_widget(layout_add_pgm_TI_est_emerg)

            layout_add_pgm_toda.add_widget(layout_add_pgm)
            layout_add_pgm_btt = Button(text="adicionar novo pigmento no banco de dados")
            layout_add_pgm_btt.bind(on_press=add_pgm_de_vdd)
            layout_add_pgm_toda.add_widget(layout_add_pgm_btt)

            layout_add_pgm_popup = Popup(title="ADD PIGMENTO", content=layout_add_pgm_toda)
            layout_add_pgm_popup.open()

        ###### menu #######
        menu = GridLayout(rows=3, padding=[10, 10, 10, 10], spacing=50)

        menu_estoque_btt = Button(text="ESTOQUE")
        menu_estoque_btt.bind(on_press=aba_estoque)
        menu.add_widget(menu_estoque_btt)

        menu_prod_btt = Button(text="PRODUÇÃO")
        menu_prod_btt.bind(on_press=aba_producao)
        menu.add_widget(menu_prod_btt)

        menu_fin_btt = Button(text="Relatórios")
        menu_fin_btt.bind(on_press=aba_rel)

        menu.add_widget(menu_fin_btt)

        ###### menu #######

        layout.add_widget(menu)

        return layout


if __name__ == '__main__':
    KamaleaoApp().run()
