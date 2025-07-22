# SignalColumn.py

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
import time
from kivy.uix.popup import Popup

from tab1 import Tab1Content
from tab2 import Tab2Content
from tab3 import Tab3Content
from ServiceManager import ServiceManager
from DAQManager import DAQManager
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import os
import glob
import csv
import subprocess
import threading

from kivy.uix.behaviors import ButtonBehavior

RCLONE_REMOTE_NAME = 'pranas_pi'
# Define the desired path on your OneDrive for plot images
ONEDRIVE_PLOTS_PATH = 'BACTERIA_DEVICE_UPLOADS/PlotData/Signals'

class ClickableImage(ButtonBehavior, Image):
    pass


class SignalColumn(BoxLayout):
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

    def _upload_plot_to_onedrive(self, local_plot_path):
        """Helper method to upload a plot file using rclone."""
        # Ensure the remote destination path exists on OneDrive.
        # rclone will create it if it doesn't, but explicitly creating it
        # makes the intent clearer.
        remote_destination_path = ONEDRIVE_PLOTS_PATH
        remote_path = f"{RCLONE_REMOTE_NAME}:{remote_destination_path}"
        
        # Command to copy the specific plot file
        command = ['rclone', 'copy', local_plot_path, remote_path]
        
        try:
            # print(f"Uploading plot {os.path.basename(local_plot_path)} to OneDrive: {remote_path}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            # print(f"Plot upload successful: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error uploading plot {os.path.basename(local_plot_path)}: {e.stderr}")
            # Optionally log this to your log file as well
            # self.service_manager.logFileManage.WriteLog(f"ERROR: Failed to upload plot {os.path.basename(local_plot_path)}: {e.stderr}", 1)
        except FileNotFoundError:
            print("Error: rclone command not found. Is rclone installed and in PATH?")
            # self.service_manager.logFileManage.WriteLog("ERROR: rclone command not found for plot upload.", 1)

    
    def create_header(self):
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)

        signal = Label(text='SIGNAL', font_size=20, size_hint=(1, 0.5),color=(1,1,0,1), bold=True)
        header.add_widget(signal)

        return header


    def create_body(self):
        self.graph_column = BoxLayout(orientation='vertical', size_hint_x=0.9, spacing=10)

        # 2. Middle: Graph area (initially empty)
        # padding = [padding_left, padding_top, padding_right, padding_bottom]
        self.graph_container = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.graph_column.add_widget(self.graph_container)

        self.button_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, spacing=10, padding=10)

        
        self.load_button = Button(
            text='Xpos',
            size_hint=(None,None),
            # background_color=(0.2, 0.2, 0.2, 1),
            # color=(1, 1, 0, 1),
            font_size=14,
            size=(150, 20),
            # pos_hint={'center_x': 0.6},
            disabled = False
        )

        self.load_button.bind(on_press=self.on_xpos_press)
        self.button_row.add_widget(self.load_button)
        '''
        self.load_button2 = Button(
            text='Ypos',
            size_hint=(None,None),
            # background_color=(0.2, 0.2, 0.2, 1),
            # color=(1, 1, 0, 1),
            font_size=14,
            size=(90, 20),
            # pos_hint={'center_x': 0.6},
            disabled = False
        )

        self.load_button2.bind(on_press=self.on_ypos_press)
        self.button_row.add_widget(self.load_button2)
        '''
        self.load_button3 = Button(
            text='Pow',
            size_hint=(None,None),
            # background_color=(0.2, 0.2, 0.2, 1),
            # color=(1, 1, 0, 1),
            font_size=14,
            size=(150, 20),
            # pos_hint={'center_x': 0.6},
            disabled = False
        )

        self.load_button3.bind(on_press=self.on_pow_press)
        self.button_row.add_widget(self.load_button3)

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

    def get_latest_plot_path(self, directory):
        list_of_files = os.listdir(directory)

        image_files = [os.path.join(directory, f) for f in list_of_files if f.endswith('.png')]
        
        if not image_files:
            return None
        
        # Sort by modification time (most recent first)
        latest_file = max(image_files, key=os.path.getmtime)
        return latest_file



    def on_xpos_press(self, instance):
        file_path = 'PlotData/Signals'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            print(f"Created directory: {file_path}")

        if os.path.exists('xplot.png'):
            os.remove('xplot.png')
        self.graph_container.clear_widgets()
        self.DAQ.StartDAQ()
        msg, self.total_samples_read, xpos_data, ypos_data, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)
        record_dur = self.service_manager.trialParameters.RECORD_DURATION
        num_samples = len(xpos_data)
        time_array = np.linspace(0, self.service_manager.trialParameters.RECORD_DURATION, num_samples)
        print(record_dur)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        plot_filename_base = f"xplot_{timestamp}"


        # Make the plot and save
        fig = plt.figure(figsize=(12,6))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xpos_data, ypos_data, pow_data, c='blue', marker='o', s=10, alpha=0.6)

        # Set labels for the axes
        ax.set_xlabel('X Pos')
        ax.set_ylabel('Y Pos')
        ax.set_zlabel('Pow')
        ax.set_title('3D Plot: Xpos, Ypos, and Power')

        plt.tight_layout() # Adjust layout to prevent labels/titles from overlapping
        
        # Save the 3D plot
        plot_path = os.path.join(file_path, f"{plot_filename_base}.png")
        plt.savefig(plot_path, dpi=200)
        plt.close(fig) # Close the figure to free up memory
        print(f"Saved 3D plot: {plot_path}")

        self._upload_plot_to_onedrive(plot_path)

        '''
        plt.scatter(time_array, xpos_data, s=10, c='black')
        plt.xlabel('Time (s)')
        plt.ylabel('Xpos')
        plt.title('Xpos vs Time')
        plt.tight_layout()
        # plt.savefig('xplot.png', dpi=200)
        xplot_path = os.path.join(file_path, f"{plot_filename_base}.png")
        plt.savefig(xplot_path, dpi=200)
        plt.close()
        '''
        latest_plot_path = self.get_latest_plot_path(file_path)

        # timestamp = time.time()
        graph_image = ClickableImage(source=f'{latest_plot_path}', allow_stretch=True, keep_ratio=True)
        # graph_image = ClickableImage(source='xplot.png', allow_stretch=True, keep_ratio=True)
        graph_image.size_hint = (0.9, 0.9)
        graph_image.pos_hint = {'center_x': 0.6, 'center_y': 0.5}
        graph_image.bind(on_press=self.show_large_image)
        graph_image.reload()
        self.graph_container.add_widget(graph_image)

    '''
    def on_ypos_press(self, instance):
        if os.path.exists('yplot.png'):
            os.remove('yplot.png')

        self.graph_container.clear_widgets()
        self.DAQ.StartDAQ()
        msg, self.total_samples_read, xpos_data, ypos_data, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)
        time = self.service_manager.trialParameters.RECORD_DURATION
        num_samples = len(xpos_data)
        time_array = np.linspace(0, self.service_manager.trialParameters.RECORD_DURATION, num_samples)
        print(time)

        # Make the plot and save
        plt.figure(figsize=(10,5))
        plt.scatter(time_array, ypos_data, s=10, c='black')
        plt.xlabel('Time (s)')
        plt.ylabel('Ypos')
        plt.title('Ypos vs Time')
        plt.tight_layout()
        plt.savefig('yplot.png')
        plt.close()

        graph_image = ClickableImage(source='yplot.png', allow_stretch=True, keep_ratio=True)
        graph_image.size_hint = (0.9, 0.9)
        graph_image.pos_hint = {'center_x': 0.6, 'center_y': 0.5}
        graph_image.bind(on_press=self.show_large_image)
        graph_image.reload()
        self.graph_container.add_widget(graph_image)
    '''

    def on_pow_press(self, instance):
        file_path = 'PlotData/Signals'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            print(f"Created directory: {file_path}")

        if os.path.exists('powplot.png'):
            os.remove('powplot.png')
        self.graph_container.clear_widgets()
        self.DAQ.StartDAQ()
        msg, self.total_samples_read, xpos_data, ypos_data, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)
        record_dur = self.service_manager.trialParameters.RECORD_DURATION
        num_samples = len(xpos_data)
        time_array = np.linspace(0, self.service_manager.trialParameters.RECORD_DURATION, num_samples)
        print(record_dur)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        plot_filename_base = f"powplot_{timestamp}"


        # Make the plot and save
        plt.figure(figsize=(12,6))
        plt.scatter(time_array, pow_data, s=10, c='blue')
        plt.xlabel('Time (s)')
        plt.ylabel('Pow')
        plt.title('Pow vs Time')
        plt.tight_layout()
        # plt.savefig('xplot.png', dpi=200)
        powplot_path = os.path.join(file_path, f"{plot_filename_base}.png")
        plt.savefig(powplot_path, dpi=200)
        plt.close()

        self._upload_plot_to_onedrive(powplot_path)

        latest_plot_path = self.get_latest_plot_path(file_path)

        # timestamp = time.time()
        graph_image = ClickableImage(source=f'{latest_plot_path}', allow_stretch=True, keep_ratio=True)
        # graph_image = ClickableImage(source='xplot.png', allow_stretch=True, keep_ratio=True)
        graph_image.size_hint = (0.9, 0.9)
        graph_image.pos_hint = {'center_x': 0.6, 'center_y': 0.5}
        graph_image.bind(on_press=self.show_large_image)
        graph_image.reload()
        self.graph_container.add_widget(graph_image)

    '''
    def on_pow_press(self, instance):
        file_path = 'PlotData'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            print(f"Created directory: {file_path}")
        if os.path.exists('powplot.png'):
            os.remove('powplot.png')
        
        self.graph_container.clear_widgets()
        self.DAQ.StartDAQ()
        msg, self.total_samples_read, xpos_data, ypos_data, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)
        time = self.service_manager.trialParameters.RECORD_DURATION
        num_samples = len(xpos_data)
        time_array = np.linspace(0, self.service_manager.trialParameters.RECORD_DURATION, num_samples)
        print(time)

        # Make the plot and save
        plt.figure(figsize=(10,5))
        plt.scatter(time_array, pow_data, s=10, c='black')
        plt.xlabel('Time (s)')
        plt.ylabel('Pow')
        plt.title('Pow vs Time')
        plt.tight_layout()
        plt.savefig('powplot.png')
        plt.close()

        graph_image = ClickableImage(source='powplot.png', allow_stretch=True, keep_ratio=True)
        graph_image.size_hint = (0.9, 0.9)
        graph_image.pos_hint = {'center_x': 0.6, 'center_y': 0.5}
        graph_image.bind(on_press=self.show_large_image)
        graph_image.reload()
        self.graph_container.add_widget(graph_image)

        
        graph_image = Image(source='powplot.png', allow_stretch=True, keep_ratio=True)
        graph_image.size_hint = (0.9, 0.9)
        graph_image.size = (self.graph_container.width * 0.9, self.graph_container.height * 0.9)
        # graph_image.size = (500, 50)
        graph_image.pos_hint = {'center_x': 0.6, 'center_y': 0.5}
        self.graph_container.add_widget(graph_image)
        
    '''

    
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


 
