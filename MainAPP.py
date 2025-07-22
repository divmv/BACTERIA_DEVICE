# MainAPP.py

from kivy.app import App
from ServiceManager import ServiceManager
from first_UI import HeaderFooterLayout
from tab1 import Tab1Content
import time

class PranasApp(App):
    def __init__(self, **kwargs):
        """
        Initialize attributes here to ensure they always exist on the instance
        before build() or on_stop() are called.
        """
        super().__init__(**kwargs)
        self.service_manager = None
        self.layout = None

    def build(self):
        # Create the Tab1Content UI and ServiceManager
        self.service_manager = ServiceManager(gui=None)  # Initialize ServiceManager
        self.layout = HeaderFooterLayout(self.service_manager)  # Pass ServiceManager to Tab1Content
        
        # Update the ServiceManager with the Tab1Content as the GUI
        self.service_manager.gui = self.layout

        return self.layout

    '''    
    
    def on_stop(self):
        """
        This method is called when the Kivy application is stopping.
        Use it to trigger the final log file upload.
        """
        print("Kivy application is stopping. Initiating final log upload...")

        # Access the LogFileManage instance through the service_manager
        # Assuming ServiceManager creates and holds an instance of LogFileManage
        # e.g., self.service_manager.logFileManage
        if hasattr(self.service_manager, 'logFileManage') and \
           self.service_manager.logFileManage is not None:
            self.service_manager.logFileManage.upload_log_on_exit()
            print("Log upload initiated in background.")
            # Give the upload thread a moment to start, especially for small files.
            # For critical uploads, you might need a more robust shutdown sequence
            # that waits for the thread to complete, but that would block app exit.
            time.sleep(1) # Small delay to allow thread to kick off

        # Also, ensure DAQ is stopped gracefully if it's still running
        # You'll need to trace how DAQManager is instantiated and accessed.
        # Assuming HeaderFooterLayout -> SignalColumn -> DAQManager
        if hasattr(self.layout, 'signal_column') and \
           hasattr(self.layout.signal_column, 'DAQ') and \
           self.layout.signal_column.DAQ is not None:
            print("Attempting to stop and reset DAQ...")
            self.layout.signal_column.DAQ.StopDAQ()
            self.layout.signal_column.DAQ.ResetDAQ()
            print("DAQ stopped and reset.")
        else:
            print("DAQ instance not found or not initialized in on_stop.")

        print("Application shutdown complete.")
    '''
    def on_stop(self):
        """
        This method is called when the Kivy application is stopping.
        Use it to trigger the final log file upload.
        """
        print("Kivy application is stopping. Initiating final log upload...")

        # Access the LogFileManage instance through the service_manager
        # Now, self.service_manager is guaranteed to exist (might be None if build failed early)
        if self.service_manager and \
           hasattr(self.service_manager, 'logFileManage') and \
           self.service_manager.logFileManage is not None:
            print(f"LogFileManage instance exists: {self.service_manager.logFileManage}")
            print(f"Attempting to upload log file: {self.service_manager.logFileManage.log_file_name}")
            self.service_manager.logFileManage.upload_log_on_exit()
            print("Log upload initiated in background.")
            # Give the upload thread a moment to start, especially for small files.
            # For critical uploads, you might need a more robust shutdown sequence
            # that waits for the thread to complete, but that would block app exit.
            time.sleep(1) # Small delay to allow thread to kick off
        else:
            print("Warning: service_manager or logFileManage not available for final log upload.")

        # Also, ensure DAQ is stopped gracefully if it's still running
        # Now, self.layout is guaranteed to exist (might be None if build failed early)
        if self.layout and \
           hasattr(self.layout, 'signal_column') and \
           hasattr(self.layout.signal_column, 'DAQ') and \
           self.layout.signal_column.DAQ is not None:
            print("Attempting to stop and reset DAQ...")
            self.layout.signal_column.DAQ.StopDAQ()
            self.layout.signal_column.DAQ.ResetDAQ()
            print("DAQ stopped and reset.")
        else:
            print("DAQ instance not found or not initialized in on_stop.")

        print("Application shutdown complete.")


if __name__ == '__main__':
    PranasApp().run()
