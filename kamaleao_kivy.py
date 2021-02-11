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
        def aba_estoque(instance):
            def ver_tabela(instance):
                layout_ver_tabela = GridLayout(rows=3)

                tabela_header = GridLayout(cols=3)
                tabela_header.add_widget(Label(text="Nome"))
                tabela_header.add_widget(Label(text="quantidade"))
                tabela_header.add_widget(Label(text="obs"))
                layout_ver_tabela.add_widget(tabela_header)

                tabela_conteudo = GridLayout(cols=3, size_hint_y=None, height=5000, spacing=[0, 45], padding=25)
                pgmts = ['pigmento0', 'pigmento1', 'pigmento2', 'pigmento3', 'pigmento4', 'pigmento5', 'pigmento6',
                         'pigmento7', 'pigmento8', 'pigmento9', 'pigmento10', 'pigmento11', 'pigmento12', 'pigmento13',
                         'pigmento14', 'pigmento15', 'pigmento16', 'pigmento17', 'pigmento18', 'pigmento19',
                         'pigmento20', 'pigmento21', 'pigmento22', 'pigmento23', 'pigmento24', 'pigmento25',
                         'pigmento26', 'pigmento27', 'pigmento28', 'pigmento29', 'pigmento30', 'pigmento31',
                         'pigmento32', 'pigmento33', 'pigmento34', 'pigmento35', 'pigmento36', 'pigmento37',
                         'pigmento38', 'pigmento39', 'pigmento40', 'pigmento41', 'pigmento42', 'pigmento43',
                         'pigmento44', 'pigmento45', 'pigmento46', 'pigmento47', 'pigmento48', 'pigmento49']
                qnt = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                       27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

                obs = ['OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES', 'OBSERVAÇÕES',
                       'OBSERVAÇÕES', 'OBSERVAÇÕES']
                for i in range(len(pgmts)):
                    tabela_conteudo.add_widget(Label(text=str(pgmts[i])))
                    tabela_conteudo.add_widget(Label(text=str(qnt[i])))
                    tabela_conteudo.add_widget(Label(text=str(obs[i])))


                tabela_view = ScrollView(size_hint=(1, None), width=850,height=300)
                tabela_view.add_widget(tabela_conteudo)
                layout_ver_tabela.add_widget(tabela_view)

                tabela_btt = GridLayout(cols=2)

                tabela_btt_enviar = Button(text="Adicionar")
                tabela_btt.add_widget(tabela_btt_enviar)

                tabela_btt_enviar = Button(text="Remover")
                tabela_btt.add_widget(tabela_btt_enviar)

                layout_ver_tabela.add_widget(tabela_btt)

                ver_tabela_popup = Popup(title="Estoque", content=layout_ver_tabela)
                ver_tabela_popup.open()

            def min_estoque(instance):

                layout_min_estoque = GridLayout(cols = 4)
                layout_min_estoque.add_widget(Label(text="produto"))
                layout_min_estoque.add_widget(TextInput())


                layout_min_estoque.add_widget(Label(text="Min estoque"))
                layout_min_estoque.add_widget(TextInput())
                layout_min_estoque_btt = Button(text="alterar")
                layout_min_estoque.add_widget(layout_min_estoque_btt)


                layout_min_estoque_popup = Popup(title="min_extoque",content=layout_min_estoque,size_hint=(None,None),size=(600,120))
                layout_min_estoque_popup.open()

            def emerg_estoque(instance):
                layout_emerg_estoque = GridLayout(cols=4)
                layout_emerg_estoque.add_widget(Label(text="produto"))
                layout_emerg_estoque.add_widget(TextInput())

                layout_emerg_estoque.add_widget(Label(text="Estoque Emergencial"))
                layout_emerg_estoque.add_widget(TextInput())
                layout_emerg_estoque_btt = Button(text="alterar")
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


            layout_estoque_emerg_btt=Button(text="Estoque Emergencial")
            layout_estoque_emerg_btt.bind(on_press=emerg_estoque)
            layout_estoque.add_widget(layout_estoque_emerg_btt)

            aba_estoque_pg = Popup(title="popup", content=layout_estoque, size_hint=(None, None), size=(400, 400))
            aba_estoque_pg.open()

        def simular_popup(instance):

            layout_simular = GridLayout(rows=3)

            layout_simular.add_widget(Label(text="Custo: "))
            layout_simular.add_widget(Label(text=" xxx "))

            layout_simular.add_widget(Label(text="Lucro: "))

            layout_simular.add_widget(Label(text=" xxx "))

            layout_simular.add_widget(Label(text="Possui em estoque: "))
            layout_simular.add_widget(Label(text=" xxx "))





            layout_simular_popup = Popup(title="SIMULAÇÃO",content = layout_simular)
            layout_simular_popup.open()







        def aba_producao(instance):
            layout_producao = GridLayout(rows=2)

            layout_producao_text = GridLayout(cols=2)

            layout_producao_text_cor = Label(text='cor')

            layout_producao_text.add_widget(layout_producao_text_cor)
            layout_producao_text.add_widget(TextInput())


            layout_producao_text_qnt = Label(text='qnt')
            layout_producao_text.add_widget(layout_producao_text_qnt)
            layout_producao_text.add_widget(TextInput())


            layout_producao_btt = GridLayout(cols=2,spacing=150,padding=100)

            layout_producao_btt_simulacao = Button(text="simular")
            layout_producao_btt_simulacao.bind(on_press=simular_popup)
            layout_producao_btt.add_widget(layout_producao_btt_simulacao)

            layout_producao_btt_enviar = Button(text="enviar")
            layout_producao_btt.add_widget(layout_producao_btt_enviar)

            layout_producao.add_widget(layout_producao_text)
            layout_producao.add_widget(layout_producao_btt)

            layout_producao_pop = Popup(title="produçao", content=layout_producao, )
            layout_producao_pop.open()

        layout = GridLayout(cols=1)

        def aba_fin(instance):
            layout_fin = GridLayout(cols=2)
            layout_fin.add_widget(Label(text="ainda nao sei o que colocar"))

            layout_fin_popup = Popup(title="fin", content=layout_fin)
            layout_fin_popup.open()

        ###### menu #######
        menu = GridLayout(rows=3,padding =[10,10,10,10],spacing=50)

        menu_estoque_btt = Button(text="ESTOQUE")
        menu_estoque_btt.bind(on_press=aba_estoque)
        menu.add_widget(menu_estoque_btt)

        menu_prod_btt = Button(text="PRODUÇÃO")
        menu_prod_btt.bind(on_press=aba_producao)
        menu.add_widget(menu_prod_btt)

        menu_fin_btt = Button(text="FINANCEIRO")
        menu_fin_btt.bind(on_press=aba_fin)

        menu.add_widget(menu_fin_btt)

        ###### menu #######

        layout.add_widget(menu)

        return layout


if __name__ == '__main__':
    KamaleaoApp().run()
