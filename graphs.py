from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import os
import sys
from kivy.clock import Clock
import time


from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import sqlite3
import numpy as np


class GraphsApp(App):
    def build(self):
        def restart(instance):
            print(f'exec: {sys.executable} {["python"] + sys.argv}')
            os.execvp(sys.executable, ['python'] + sys.argv)
        conn = sqlite3.connect('pigmentos.db')
        cursor = conn.cursor()
        plt.rcParams["figure.figsize"] = (2, 2)



        cursor.execute("SELECT estoque from pigmentos")
        result_estoque = cursor.fetchall()

        cursor.execute("SELECT estoque_min from pigmentos")
        result_min_estoque = cursor.fetchall()

        cursor.execute("SELECT nome from pigmentos")
        result_nome = cursor.fetchall()

        cursor.execute("SELECT estoque_emerg from pigmentos")
        result_emerg = cursor.fetchall()


        estoque = []

        estoque_min = []

        nomes = []

        estoque_emerg = []

        layout = GridLayout(rows=3,padding = 10,spacing=10)


        for i in result_estoque:
            for j in i:
                estoque.append(j)

        for i in result_emerg:
            for j in i:
                estoque_emerg.append(j)

        for i in result_nome:
            for j in i:
                nomes.append(j)

        for i in result_min_estoque:
            for j in i:
                estoque_min.append(j)

        for i in range(len(estoque)):
            estoque_maximo = 3*estoque_min[i]
            print(estoque_maximo)
            porcentagem = estoque[i]/estoque_maximo
            print(porcentagem)
            array_parte2 = (estoque_maximo-porcentagem)/estoque_maximo
            y = np.array([porcentagem,array_parte2])
            fig = plt.figure()

            if estoque[i] <= estoque_emerg[i]:
                fig.set_facecolor((1, 0, 0, 1))
            elif estoque[i] <= estoque_min[i]:
                fig.set_facecolor((1, 1, 0, 1))
            else:
                fig.set_facecolor((0, 0, 0, 1))




            plt.pie(y,colors=["b","r"])






            block = GridLayout(rows=2)
            plt.savefig("mygraph{}.png".format(i))
            plt.close('all')

            block.add_widget(Label(text=nomes[i]))


            block.add_widget(Image(source="mygraph{}.png".format(i)))

            layout.add_widget(block)
        refresh_btt = Button(text="atualizar")
        refresh_btt.bind(on_press=restart)
        layout.add_widget(refresh_btt)










        return layout


if __name__ == '__main__':
    GraphsApp().run()