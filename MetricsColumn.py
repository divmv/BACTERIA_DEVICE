# MetricsColumn.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Line, Color
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.config import Config
import numpy as np
from kivy.uix.popup import Popup

from tab1 import Tab1Content
from tab2 import Tab2Content
from tab3 import Tab3Content
from ServiceManager import ServiceManager
from DAQManager import DAQManager
import matplotlib.pyplot as plt
# from DataClasses import DeviceFlags
# from ModeManager import ModeManager

import os
import glob
import csv

from kivy.uix.behaviors import ButtonBehavior

class ClickableImage(ButtonBehavior, Image):
    pass


class MetricsColumn(BoxLayout):
    def __init__(self, service_manager, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager
        self.modeData = self.service_manager.deviceFlags
        # self.mode_manager = ModeManager(self.service_manager)
        # self.currentService = currentService
        self.total_samples_read = 0
        self.nebState = 0
        self.DAQ = DAQManager(self.service_manager)
        self.orientation = 'vertical'
        self.DAQ.ResetDAQ()
        self.DAQ.StartDAQ()

        # Create and add the header
        header = self.create_header()
        self.add_widget(header)

        # self.tab1_content = Tab1Content(service_manager)
        # self.add_widget(self.tab1_content)
        # Create and add the body with tabs and the reset button
        body = self.create_body()
        self.add_widget(body)

        # Create and add the footer
        '''
        footer = self.create_footer()
        self.add_widget(footer)
        '''

    
    def create_header(self):
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)

        signal = Label(text='METRICS', font_size=20, size_hint=(1, 0.5),color=(1,1,0,1), bold=True)
        header.add_widget(signal)

        return header


    def create_body(self):
        self.graph_column = BoxLayout(orientation='vertical', size_hint_x=0.9, spacing=10)

        # 2. Middle: Graph area (initially empty)
        # padding = [padding_left, padding_top, padding_right, padding_bottom]
        self.graph_container = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.graph_column.add_widget(self.graph_container)

        self.button_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, spacing=10, padding=10)

        # self.DAQ.StartDAQ()
        # msg, self.total_samples_read, xpos_data, ypos_data, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)

        
        self.load_button = Button(
            text='BDE vs DIR',
            size_hint=(None,None),
            # background_color=(0.2, 0.2, 0.2, 1),
            # color=(1, 1, 0, 1),
            font_size=14,
            size=(150, 20),
            # pos_hint={'center_x': 0.6},
            disabled = False
        )

        self.load_button.bind(on_press=self.on_bde_press)
        self.button_row.add_widget(self.load_button)

        self.load_button2 = Button(
            text='MAG vs DIR',
            size_hint=(None,None),
            # background_color=(0.2, 0.2, 0.2, 1),
            # color=(1, 1, 0, 1),
            font_size=14,
            size=(150, 20),
            # pos_hint={'center_x': 0.6},
            disabled = False
        )

        self.load_button2.bind(on_press=self.on_siv_press)
        self.button_row.add_widget(self.load_button2)

        self.graph_column.add_widget(self.button_row)
        
        return self.graph_column
    

    def show_large_image(self, instance):
        source = instance.source
        box = BoxLayout()
        big_image = Image(source=source, allow_stretch=True, keep_ratio=True)
        box.add_widget(big_image)
        popup = Popup(title='Graph',
                    content=box,
                    size_hint=(0.9, 0.9))
        popup.open()



    def on_bde_press(self, instance):
        if os.path.exists('bdeplot.png'):
            os.remove('bdeplot.png')
        self.graph_container.clear_widgets()
        self.DAQ.StartDAQ()
        msg, self.total_samples_read, xpos_data, ypos_data, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)

        xpos_data = np.array(xpos_data)
        ypos_data = np.array(ypos_data)
        pow_data  = np.array(pow_data)


        magnitude = np.sqrt(xpos_data**2 + ypos_data**2)
        direction = np.arctan2(ypos_data, xpos_data)

        bde = magnitude/pow_data

        # Make the plot and save
        plt.figure(figsize=(12,6))
        plt.scatter(bde, direction, s=10, c='black')
        plt.xlabel('BDE')
        plt.ylabel('DIR')
        plt.title('BDE vs DIR')
        plt.tight_layout()
        plt.savefig('bdeplot.png', dpi=200)
        plt.close()

        graph_image = ClickableImage(source='bdeplot.png', allow_stretch=True, keep_ratio=True)
        graph_image.size_hint = (0.9, 0.9)
        graph_image.pos_hint = {'center_x': 0.6, 'center_y': 0.5}
        graph_image.bind(on_press=self.show_large_image)
        graph_image.reload()
        self.graph_container.add_widget(graph_image)

    def on_siv_press(self, instance):
        if os.path.exists('sivplot.png'):
            os.remove('sivplot.png')
        self.graph_container.clear_widgets()
        self.DAQ.StartDAQ()
        msg, self.total_samples_read, xpos_data, ypos_data, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)

        xpos_data = np.array(xpos_data)
        ypos_data = np.array(ypos_data)
        pow_data  = np.array(pow_data)


        magnitude = np.sqrt(xpos_data**2 + ypos_data**2)
        direction = np.arctan2(ypos_data, xpos_data)

        bde = magnitude/pow_data

        mean_power = np.mean(pow_data)
        std_power = np.std(pow_data)

        if mean_power != 0:
            siv = std_power / mean_power
        else:
            siv = 0  # or np.nan, depending on how you want to handle it


        # Make the plot and save
        plt.figure(figsize=(10,5))
        plt.scatter(magnitude, direction, s=10, c='black')
        # plt.hist(bde, bins=30, color='red')
        plt.xlabel('MAG')
        plt.ylabel('DIR')
        plt.title('MAG vs DIR')
        plt.tight_layout()
        plt.savefig('sivplot.png')
        plt.close()

        graph_image = ClickableImage(source='sivplot.png', allow_stretch=True, keep_ratio=True)
        graph_image.size_hint = (0.9, 0.9)
        graph_image.pos_hint = {'center_x': 0.6, 'center_y': 0.5}
        graph_image.bind(on_press=self.show_large_image)
        graph_image.reload()
        self.graph_container.add_widget(graph_image)

    
    def create_footer(self):
        footer = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)
        self.load_button = Button(
            text='Load Graph',
            # size_hint=(1, 0.1),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 0, 1),
            font_size=16,
            # disabled = False
        )


        self.load_button.bind(on_press=self.on_load_button_press)
        footer.add_widget(self.load_button)
        print("Load button size:", self.load_button.size)

        # self.graph_column.add_widget(self.load_button)
        return footer


 
