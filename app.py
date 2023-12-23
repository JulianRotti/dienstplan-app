import os
import pandas as pd
import kivy
from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from scripts.create_dienstplan import find_maximal_matching

kivy.require('2.2.1')  # Replace with your current Kivy version



class LoadDialog(BoxLayout):
    def __init__(self, load, cancel, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.filechooser = FileChooserIconView()
        self.add_widget(self.filechooser)

        button_layout = BoxLayout(size_hint_y=None, height=30)
        load_button = Button(text='Load')
        load_button.bind(on_release=lambda x: load(self.filechooser.path, self.filechooser.selection))
        button_layout.add_widget(load_button)

        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_release=lambda x: cancel())
        button_layout.add_widget(cancel_button)

        self.add_widget(button_layout)

class SaveDialog(BoxLayout):
    def __init__(self, save, cancel, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.filechooser = FileChooserIconView()
        self.add_widget(self.filechooser)

        button_layout = BoxLayout(size_hint_y=None, height=30)
        save_button = Button(text='Save')
        save_button.bind(on_release=lambda x: save(self.filechooser.path))
        button_layout.add_widget(save_button)

        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_release=lambda x: cancel())
        button_layout.add_widget(cancel_button)

        self.add_widget(button_layout)

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.dienstplan = None

        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        button_layout.pos_hint = {'center_x': .5}

        # Upload Button (regular Button instead of HoverButton)
        self.upload_button = Button(text='Upload Excel File')
        self.upload_button.bind(on_release=lambda x: self.show_load())
        button_layout.add_widget(self.upload_button)

        # Save Button (regular Button instead of HoverButton)
        self.save_button = Button(text='Save Dienstplan')
        self.save_button.bind(on_release=lambda x: self.show_save())
        self.save_button.disabled = True  # Initially disabled
        button_layout.add_widget(self.save_button)

        self.add_widget(button_layout)

        # Label for displaying messages
        self.label = Label(text='No file selected')
        self.add_widget(self.label)

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.dismiss_popup()
        if filename:
            self.label.text = f'Selected file: {filename[0]}'
            try:
                df1 = pd.read_excel(filename[0], sheet_name='Qualifikationen')
                df2 = pd.read_excel(filename[0], sheet_name='Arbeitstage')
                df3 = pd.read_excel(filename[0], sheet_name='Benötigtes Personal')
                self.dienstplan = find_maximal_matching(df1, df2, df3)
                self.save_button.disabled = False  # Enable save button
                self.label.text = f'Dienstplan successfully created. Download it by clicking "Save Dienstplan"'
            except Exception as e: 
                self.dienstplan = None
                self.save_button.disabled = True
                self.label.text = f'Error processing file: {e}'

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path):
        self.dismiss_popup()
        if self.dienstplan is not None:
            save_path = os.path.join(path, 'Dienstplan.csv')
            self.dienstplan.to_csv(save_path, index=False)
            self.label.text = f'Dienstplan saved to: {save_path}'

    def dismiss_popup(self):
        self._popup.dismiss()

class ExcelApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    ExcelApp().run()
