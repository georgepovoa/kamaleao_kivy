from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

import sqlite3

class GraphsApp(App):
    def build(self):

        layout = GridLayout(cols=2)

        layout.add_widget(Button(text="q?"))

        return layout


if __name__ == '__main__':
    GraphsApp().run()