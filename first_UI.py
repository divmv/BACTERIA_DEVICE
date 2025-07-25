# first_UI.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.core.window import Window

from tab1 import Tab1Content
from tab2 import Tab2Content
from tab3 import Tab3Content
from ServiceManager import ServiceManager
from DAQManager import DAQManager
from SignalColumn import SignalColumn
from MetricsColumn import MetricsColumn
# from DataClasses import DeviceFlags
from ModeManager import ModeManager, BreathEmulationMode, StaticMode, RecordMode

import os
import glob
import csv

Window.show_cursor = False
# Config.set('input', 'mouse', 'mouse,disable')
Window.fullscreen = True
# Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class HeaderFooterLayout(BoxLayout):
    def __init__(self, service_manager, **kwargs):
        super().__init__(**kwargs)
        self.service_manager = service_manager
        self.modeData = self.service_manager.deviceFlags
        self.mode_manager = ModeManager(self.service_manager)
        # self.currentService = currentService
        self.SignalColumn = SignalColumn(self.service_manager)
        self.MetricsColumn = MetricsColumn(self.service_manager)
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
        footer = self.create_footer()
        self.add_widget(footer)

    def create_header(self):
        """Create the header layout with an image and text."""
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)

        with header.canvas.after:
            Color(1, 0, 0, 1)  # Red color
            self.header_line = Line(points=[0, 0, header.width, 0], width=2)

        header.bind(size=self.update_header_line, pos=self.update_header_line)

        header.add_widget(Image(source='Images/icon.ico', size_hint=(0.1, 1)))

        header.add_widget(Label(
            text='Personal Respiratory Analyzing System',
            font_size=40, bold=True, halign='left', color=(0, 1, 0, 1)
        ))

        return header

    def create_body(self):
        """Create the body layout with a reset button and tabs."""
        body = BoxLayout(orientation='horizontal', size_hint=(1, 0.8), padding=10, spacing=10)

        # Create the left column with the reset button and tabs
        left_column = BoxLayout(orientation='vertical', size_hint_x=0.6)

        # Add the reset button at the top of the left column
        reset_button = Button(
            text='Reset Tabs',
            size_hint=(1, 0.1),
            background_color=(1, 0, 0, 1)  # Red color
        )
        reset_button.bind(on_press=self.reset_tabs)

        # Add the reset button to the left column
        left_column.add_widget(reset_button)

        # Add the TabbedPanel below the reset button
        self.tab_panel = self.create_tabs()
        left_column.add_widget(self.tab_panel)

        # Create the right column content split into two rows with a separator
        right_column = self.create_right_column()

        # Add the left and right columns to the body
        body.add_widget(left_column)

        with body.canvas.after:
            Color(1, 1, 1, 1)  # White color
            self.separator_line = Line(width=2)

        body.add_widget(right_column)

        body.bind(size=self.update_body_separator, pos=self.update_body_separator)

        return body

    def create_tabs(self):
        """Create a TabbedPanel with three tabs."""
        tab_panel = TabbedPanel(do_default_tab=False)  # Disable default tab

        # Create Tab 1
        self.tab1 = TabbedPanelItem(text='Tab 1')
        self.tab1.content = Tab1Content(self.service_manager)
        tab_panel.add_widget(self.tab1)

        # Create Tab 2
        self.tab2 = TabbedPanelItem(text='Tab 2')
        self.tab2.content = Tab2Content()
        tab_panel.add_widget(self.tab2)

        # Create Tab 3
        self.tab3 = TabbedPanelItem(text='Tab 3')
        self.tab3.content = Tab3Content()
        tab_panel.add_widget(self.tab3)

        return tab_panel

    def create_right_column(self):
        """Create the right column split into two rows with a separator widget."""
        right_column = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=10)
        self.DAQ.StartDAQ()

        # Top half = SIGNAL (with Load button and graph)
        right_column.add_widget(self.SignalColumn)
        self.SignalColumn.size_hint_y = 1

        # Add a real separator (could just be a colored box)
        separator = Widget(size_hint_y=None, height=2)
        with separator.canvas:
            Color(1, 1, 1, 1)
            Rectangle(size=(separator.width, 2), pos=separator.pos)
        separator.bind(size=self.update_separator_rect, pos=self.update_separator_rect)
        right_column.add_widget(separator)


        # row2.size_hint_y = 1
        right_column.add_widget(self.MetricsColumn)
        self.MetricsColumn.size_hint_y = 1

        return right_column

    def update_separator_rect(self, instance, value):
        instance.canvas.clear()
        with instance.canvas:
            Color(1, 1, 1, 1)
            Rectangle(size=(instance.width, 2), pos=instance.pos)


    '''
    def update_signal_label(self, pow_data):
        if not pow_data:
            self.row1.text = "Pow: No Data"
            return

        cols = 3
        lines = []
        for i in range(0, len(pow_data), cols):
            line = '\t'.join(f"{x:.6f}" for x in pow_data[i:i+cols])
            # line = '\t'.join(str(x) for x in pow_data[i:i+cols]) cols=1
            lines.append(line)
        self.row1.text = "\n".join(lines)
        self.row1.scroll_y = 1

    def on_load_button_press(self, instance):
        # Get pow_data from your DataManager or wherever it lives
        self.DAQ.StartDAQ()
        msg, self.total_samples_read, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)
        
        # Update the label
        self.update_signal_label(pow_data)
    


    def create_right_column(self):
        """Create the right column split into two rows with a line separator."""
        right_column = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=10)
        # self.DAQ.ResetDAQ()
        self.DAQ.StartDAQ()

        # Create two rows
        # self.row1 = Label(text='SIGNAL', font_size=24, size_hint=(1, 0.5),color=(1,1,0,1))
        self.row1 = TextInput(
            text='SIGNAL',
            readonly=True,
            font_size=15,
            size_hint=(1, 0.5),
            foreground_color=(1,1,0,1),
            background_color=(0,0,0,1),
            multiline=True
        )
        
        row2 = Label(text='METRICS', font_size=24, size_hint=(1, 0.5),color=(1,1,0,1))

        # Add the first row
        right_column.add_widget(self.row1)


        print("printing signals")
        # msg, self.total_samples_read, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, self.nebState)
        # self.update_signal_label(pow_data)

        # Draw a separator line between the two rows
        with right_column.canvas.after:
            Color(1, 1, 1, 1)  # Red color for the line
            self.row_separator = Line(points=[0, right_column.height / 2, right_column.width, right_column.height / 2], width=2)

        # Bind size and position to update the separator dynamically
        right_column.bind(size=self.update_row_separator, pos=self.update_row_separator)

        # Add the second row
        right_column.add_widget(row2)

         # Load CSV Button
        self.load_button = Button(
            text='Load CSV Data',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 0, 1),
            font_size=16,
            disabled = False
        )
        print(self.modeData.SEND_FILE)
        if self.modeData.SEND_FILE:
            self.load_button.disabled = False
        self.load_button.bind(on_press=self.on_load_button_press)
        right_column.add_widget(self.load_button)

        return right_column
    '''
    '''
    def update_padding(self, instance, value):
        instance.padding = [ (instance.width - instance._get_text_width(instance.text, instance.tab_width, instance._label_cached)) / 2, 0 ]
    '''
    '''
    def load_pow_data_from_csv(self, filepath):
        """Reads numerical POW data from the CSV file, returns list of floats."""
        pow_data = []
        try:
            with open(filepath, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    for item in row:
                        try:
                            pow_data.append(float(item.strip()))
                        except ValueError:
                            pass  # skip non-numeric
            print(f"Loaded {len(pow_data)} data points from CSV.")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        return pow_data


    def load_latest_pow_data(self, instance=None):
        latest_csv = self.find_latest_csv_file()
        if not latest_csv:
            self.row1.text = "No CSV found."
            return
        pow_data = self.load_pow_data_from_csv(latest_csv)
        self.update_signal_label(pow_data)

        
    def find_latest_csv_file(self):
        """Find the most recent Data_*.csv file in RecordedData folder."""
        recorded_data_path = os.path.join(os.getcwd(), 'RecordedData')
        pattern = os.path.join(recorded_data_path, 'Data_*.csv')
        files = glob.glob(pattern)
        if not files:
            print("No CSV files found in RecordedData.")
            return None
        latest_file = max(files, key=os.path.getmtime)
        print(f"Found latest CSV file: {latest_file}")
        return latest_file
    '''

    '''  
    def update_row_separator(self, instance, value):
        """Update the separator line between the rows."""
        self.row_separator.points = [
            instance.x, instance.center_y,  # Start at the center
            instance.right, instance.center_y  # End at the center
        ]
    '''

    def reset_tabs(self, instance):
        """Reset the content of all tabs to their initial state."""
        current_tab = self.tab_panel.current_tab
        self.tab1.content = Tab1Content(self.service_manager)
        self.tab2.content = Tab2Content()
        self.tab3.content = Tab3Content()

    def create_footer(self):
        """Create the footer layout with images and text."""
        footer = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)

        with footer.canvas.before:
            Color(1, 0, 0, 1)  # Red color
            self.footer_line = Line(points=[0, footer.height, footer.width, footer.height], width=2)

        footer.bind(size=self.update_footer_line, pos=self.update_footer_line)

        footer.add_widget(Image(source='Images/ugalogo.png', size_hint=(0.1, 1)))

        footer.add_widget(Label(
            text='Developed at Design Informatics and Computational Engineering Lab,\n'
                 'University of Georgia, Athens, GA, USA',
            font_size=16, halign='center'
        ))

        footer.add_widget(Image(source='Images/dicelogo.jpg', size_hint=(0.1, 1)))

        return footer

    def update_header_line(self, instance, value):
        """Update the header line dynamically."""
        self.header_line.points = [instance.x, instance.y, instance.right, instance.y]

    def update_footer_line(self, instance, value):
        """Update the footer line dynamically."""
        self.footer_line.points = [instance.x, instance.top, instance.right, instance.top]

    def update_body_separator(self, instance, value):
        """Update the separator line dynamically between columns."""
        separator_x = instance.width * 0.6  # 60% of the body's width
        self.separator_line.points = [separator_x, instance.y, separator_x, instance.top]

service_manager = ServiceManager(gui=None)

class PranasApp(App):
        def build(self):
                return HeaderFooterLayout(service_manager)

if __name__ == '__main__':
    PranasApp().run()
