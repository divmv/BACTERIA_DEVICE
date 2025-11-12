# ModeManager.py
from DAQManager import DAQManager
import time
from datetime import datetime
import os
import threading
import requests
import warnings
from kivy.clock import Clock

warnings.filterwarnings("ignore")

class ModeManager:
    global nebState
    nebState = 0

    def __init__(self, currentService, ui_update_callback=None):
        self.currentService = currentService
        self.logFile = self.currentService.logFileManage
        # self.dataFile = self.currentService.dataFileManage
        self.stateSet = True
        self.thisState = -1
        self.curDuration = 0
        self.endDuration = 0
        self.nebState = 0
        self.DONE = False
        self.ui_update_callback = ui_update_callback

        # Create a session folder to store all CSVs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_folder = os.path.join(
            self.currentService.dataFileManage.RecordDataFolder,
            f"{self.currentService.trialParameters.MODE}_{timestamp}"
        )
        os.makedirs(self.session_folder, exist_ok=True)

        if self.currentService.trialParameters.MODE == "BreathEmulate":
            self.paraData = self.currentService.trialParameters
            # BreathEmulate specific setup can go here

        self.DAQ = DAQManager(self.currentService)
        self.modeData = self.currentService.deviceFlags

    def SwitchControl(self, nebstate1):
        global nebState
        nebState = nebstate1
        print(nebstate1)
        if nebstate1 == 0:
            requests.post("https://maker.ifttt.com/trigger/off_switch/with/key/bQbEEqB8H2G9oAy3ndl-aK")
            print('Nebulizer Off')
        elif nebstate1 == 1:
            requests.post("https://maker.ifttt.com/trigger/on_switch/with/key/bQbEEqB8H2G9oAy3ndl-aK")
            print('Nebulizer On')

    def current_time_string(self):
        return datetime.now().strftime("%H:%M:%S")

    def RegularModeRun(self):
        self.total_samples_read = 0
        startTime = time.time()
        totalTime = self.currentService.trialParameters.RECORD_DURATION
        self.logFile.WriteLog(f": Recording Started", 1)
        self.logFile.WriteLog(f"Total Duration: {totalTime} seconds", 0)

        elapsed = 0
        self.DAQ.StartDAQ()

        while elapsed < totalTime and not self.modeData.STOP_FLAG:
            msg, self.total_samples_read, xpos, ypos, pow_data = self.DAQ.ScanDAQ(self.total_samples_read, nebState)
            elapsed = int(time.time() - startTime)
            print(f"{self.current_time_string()}: Time Elapsed (s): {elapsed} of {totalTime}")

            if self.currentService.trialParameters.MODE == "BreathEmulate":
                print("Breath Emulation")

            if self.currentService.trialParameters.MODE == "Static":
                print("Static Mode")

            if msg == 'HardwareOvr':
                self.logFile.WriteLog('Hardware Overrun detected.', 1)
                if self.ui_update_callback:
                    Clock.schedule_once(lambda dt: self.ui_update_callback('Hardware Overrun detected!', color=(1,0,0,1)), 0)
                self.DAQ.ResetDAQ()
                self.modeData.STOP_FLAG = True
                break
            elif msg == 'BuffOvr':
                self.logFile.WriteLog('Buffer Overrun detected.', 1)
                if self.ui_update_callback:
                    Clock.schedule_once(lambda dt: self.ui_update_callback('Buffer Overrun detected!', color=(1,0,0,1)), 0)
                self.DAQ.ResetDAQ()
                self.modeData.STOP_FLAG = True
                break

        self.DAQ.ResetDAQ()
        if self.modeData.CONNECTION_FLAG:
            self.currentService.thisConnection.SendData2Server('Recording Complete!')

        self.logFile.WriteLog('Recording Ended', 1)
        self.logFile.WriteLog(f'Data Recording Complete for a Duration of {elapsed}s', 0)
        self.logFile.WriteLog('Final Data Frame Size:' + str(self.DAQ.recDataFrame.shape), 0)
        self.DAQ.recDataFrame.index.name = 'Samples'
        self.modeData.SEND_FILE = True
        self.modeData.DAQ_SET = True
        self.DONE = True

        # Save CSV in session folder
        iteration_suffix = f"_Iter{self.currentService.currentIteration+1}.csv"
        unique_file_name = (
            f"Data_{self.currentService.trialParameters.UID}_"
            f"T{self.currentService.trialParameters.TRIAL}_"
            f"{self.currentService.trialParameters.MODE}{iteration_suffix}"
        )
        save_path = os.path.join(self.session_folder, unique_file_name)
        self.currentService.dataFileManage.data_file_name = unique_file_name
        self.currentService.dataFileManage.Write2CSV(self.DAQ.recDataFrame)

        if not hasattr(self.currentService, "recorded_files"):
            self.currentService.recorded_files = []
        self.currentService.recorded_files.append(save_path)

        return self.DONE


# ----------------- Mode Classes -----------------
class RecordMode(ModeManager):
    def __init__(self, currentService):
        ModeManager.__init__(self, currentService)

    def Run(self):
        iterations = self.currentService.trialParameters.ITERATIONS
        for i in range(iterations):
            print(f"\nStarting iteration {i + 1} of {iterations}")
            self.currentService.currentIteration = i
            self.RegularModeRun()
            if self.modeData.STOP_FLAG:
                print("Recording stopped early due to STOP_FLAG.")
                break

        # After all iterations: process folder if multiple files exist
        if hasattr(self, 'session_folder'):
            csv_files = [f for f in os.listdir(self.session_folder) if f.endswith('.csv')]
            if len(csv_files) > 1:
                print(f"Multiple CSV files detected in folder: {self.session_folder}")
                try:
                    import Processor
                    Processor.process_folder(self.session_folder)
                except Exception as e:
                    print(f"Error running Processor.py: {e}")

        return self.DONE


class BreathEmulationMode(ModeManager):
    def __init__(self, currentService):
        ModeManager.__init__(self, currentService)

    def Run(self):
        iterations = self.currentService.trialParameters.ITERATIONS
        for i in range(iterations):
            print(f"\nStarting iteration {i + 1} of {iterations}")
            self.currentService.currentIteration = i
            self.RegularModeRun()
            if self.modeData.STOP_FLAG:
                print("Recording stopped early due to STOP_FLAG.")
                break

        if hasattr(self, 'session_folder'):
            csv_files = [f for f in os.listdir(self.session_folder) if f.endswith('.csv')]
            if len(csv_files) > 1:
                print(f"Multiple CSV files detected in folder: {self.session_folder}")
                try:
                    import Processor
                    Processor.process_folder(self.session_folder)
                except Exception as e:
                    print(f"Error running Processor.py: {e}")

        return self.DONE


class StaticMode(ModeManager):
    def __init__(self, currentService):
        ModeManager.__init__(self, currentService)

    def Run(self):
        iterations = self.currentService.trialParameters.ITERATIONS
        for i in range(iterations):
            print(f"\nStarting iteration {i + 1} of {iterations}")
            self.currentService.currentIteration = i
            self.RegularModeRun()
            if self.modeData.STOP_FLAG:
                print("Recording stopped early due to STOP_FLAG.")
                break

        if hasattr(self, 'session_folder'):
            csv_files = [f for f in os.listdir(self.session_folder) if f.endswith('.csv')]
            if len(csv_files) > 1:
                print(f"Multiple CSV files stored in folder: {self.session_folder}")
                try:
                    import Processor
                    Processor.create_and_move_csv(self.session_folder)
                except Exception as e:
                    print(f"Error running Processor.py: {e}")

        return self.DONE
