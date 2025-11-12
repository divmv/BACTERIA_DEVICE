# ModeManager.py
from DAQManager import DAQManager
import time
from datetime import datetime
import os
import threading
import requests
import warnings
from kivy.clock import Clock

<<<<<<< HEAD
warnings.filterwarnings("ignore")

class ModeManager:
    global nebState
    nebState = 0

    def __init__(self, currentService, ui_update_callback=None):
        self.currentService = currentService
        self.logFile = self.currentService.logFileManage
=======
# from first_UI import HeaderFooterLayout

warnings.filterwarnings("ignore")

class ModeManager():

    global nebState
    nebState=0
    
    '''
    def __init__(self,currentService):
        
        self.currentService=currentService
        self.logFile=self.currentService.logFileManage
        self.curDuration = 0
        
        self.stateSet = True
        self.thisState = -1
        self.curDuration = 0
        self.endDuration = 0


        if self.currentService.trialParameters.MODE=="BreathEmulate":
            if self.stateSet:
                print(self.stateSet)
                self.stateSet = False
                self.thisState += 1
                self.SwitchControl(self.nebStates[self.thisState])
            if self.thisState <= len(self.stepDurations):
                self.endDuration = self.stepDurations[self.thisState]
                self.curDuration = 0
            else:
                self.curDuration += 1
            if self.curDuration >= self.endDuration - 1:
                self.stateSet = True
                self.curDuration = 0

            print("entered be if statement")
            self.paraData=self.currentService.trialParameters
            self.nebControl={'NebStatus':True,'StepDurations':list(map(int,self.paraData.SEQUENCE_DURATION.split(','))),'NebStates':list(map(int,self.paraData.SEQUENCE.split(',')))}
            self.currentService.trialParameters.RECORD_DURATION=sum(self.nebControl['StepDurations'])
            
            self.logFile.WriteLog('Step Durations:'+self.paraData.SEQUENCE_DURATION,0)
            self.logFile.WriteLog('Nebulizer States:'+self.paraData.SEQUENCE,0)
            
            self.stepDurations=self.nebControl['StepDurations']
            self.nebStates=self.nebControl['NebStates']
            
            self.thisState=-1
            self.stateSet=True
        self.DAQ=DAQManager(self.currentService)
        self.modeData=self.currentService.deviceFlags
    '''
    
    def __init__(self, currentService, ui_update_callback=None):
        self.currentService = currentService
        self.logFile = self.currentService.logFileManage
        print("name:")
        print(self.logFile)
        # self.ui_update_callback = ui_update_callback 

>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0
        self.stateSet = True
        self.thisState = -1
        self.curDuration = 0
        self.endDuration = 0
        self.nebState = 0
<<<<<<< HEAD
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
=======
        self.DONE = False 

        # self.ui_update_callback = ui_update_callback
        # print(f"ModeManager initialized. ui_update_callback: {self.ui_update_callback}")
    
        
        if self.currentService.trialParameters.MODE == "Static":
            print("entered first static if")
            # write functionality

        if self.currentService.trialParameters.MODE == "BreathEmulate":
            # print("entered be if statement")
            self.paraData = self.currentService.trialParameters
            '''
            if self.stateSet:
                print(self.stateSet)
                self.stateSet = False
                self.thisState += 1
                self.SwitchControl(self.nebStates[self.thisState])
            if self.thisState <= len(self.stepDurations):
                self.endDuration = self.stepDurations[self.thisState]
                self.curDuration = 0
            else:
                self.curDuration += 1
            if self.curDuration >= self.endDuration - 1:
                self.stateSet = True
                self.curDuration = 0


            self.nebControl = {
                'NebStatus': True,
                'StepDurations': list(map(int, self.paraData.SEQUENCE_DURATION.split(','))),
                'NebStates': list(map(int, self.paraData.SEQUENCE.split(',')))
            }

            self.stepDurations = self.nebControl['StepDurations']
            self.nebStates = self.nebControl['NebStates']

            # self.currentService.trialParameters.RECORD_DURATION = sum(self.stepDurations)

            self.logFile.WriteLog('Step Durations: ' + self.paraData.SEQUENCE_DURATION, 0)
            self.logFile.WriteLog('Nebulizer States: ' + self.paraData.SEQUENCE, 0)
            '''
        self.DAQ = DAQManager(self.currentService)
        self.modeData = self.currentService.deviceFlags


    def SwitchControl(self,nebstate1):
        global nebState
        nebState=nebstate1
        print(nebstate1)
        if nebstate1==0:
            requests.post("https://maker.ifttt.com/trigger/off_switch/with/key/bQbEEqB8H2G9oAy3ndl-aK")
            print('Nebulizer Off')
        elif nebstate1==1:    
            requests.post("https://maker.ifttt.com/trigger/on_switch/with/key/bQbEEqB8H2G9oAy3ndl-aK")
            print('Nebulizer On') 
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0

    def current_time_string(self):
        return datetime.now().strftime("%H:%M:%S")

    def RegularModeRun(self):
<<<<<<< HEAD
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
=======
    
        self.total_samples_read=0
        startTime=time.time()
        totalTime = self.currentService.trialParameters.RECORD_DURATION

        # print(f'Start time: {self.current_time_string()}')
        self.logFile.WriteLog(f": Recording Started", 1)
        # print(current_time_string() + ":Recording Started")
        # print(f'Total Duration: {totalTime}')
        self.logFile.WriteLog(f"Total Duration: {totalTime} seconds", 0)
        elapsed = 0
        # step_durations = self.serviceManager.trialParameters.STEP_DURATIONS
        # nebulizer_states = self.serviceManager.trialParameters.NEBULIZER_STATES

        current_step_index = 0
        step_start_time = time.time()
        self.logFile.WriteLog('Recording Started',1)
        self.DAQ.StartDAQ()

        # previous_elapsed_for_ui = -1

        while (elapsed) < totalTime and (not self.modeData.STOP_FLAG):
            msg,self.total_samples_read, xpos, ypos, pow_data =self.DAQ.ScanDAQ(self.total_samples_read,nebState)
            '''
            if new_data is not None:
                # Do whatever you want with new_data (currentDF)
                print(new_data.head())  # example
            '''

            elapsed = int(time.time() - startTime)
            
            # print(f'Time Elapsed: {elapsed}')
            print(f"{self.current_time_string()}:Time Elapsed (s):{elapsed} of {totalTime}")
            self.logFile.WriteLog(f"{self.current_time_string()}:Time Elapsed (s):{elapsed} of {totalTime}", 0)
            if self.currentService.trialParameters.MODE=="BreathEmulate":
                print("Breath Emulation")
            
            if self.currentService.trialParameters.MODE=="Static":
                print("entered static if statement")
                # WRITE STATIC MODE FUNCTIONALITY
            if msg=='HardwareOvr':
                # self.logFile.WriteLog('Hardware Over Run')
                # break
                self.logFile.WriteLog('Hardware Overrun detected.', 1)
                if self.ui_update_callback:
                    # Schedule error message in red
                    Clock.schedule_once(lambda dt: self.ui_update_callback('Hardware Overrun detected!', color=(1,0,0,1)), 0)
                self.DAQ.ResetDAQ() # Reset the DAQ to clear the error state
                self.modeData.STOP_FLAG = True # Set stop flag to exit the loop gracefully
                break # Exit the while loop
            elif msg=='BuffOvr':
                # self.logFile.WriteLog('Buffer Over Run')
                # break
                self.logFile.WriteLog('Buffer Overrun detected.', 1)
                if self.ui_update_callback:
                    # Schedule error message in red
                    Clock.schedule_once(lambda dt: self.ui_update_callback('Buffer Overrun detected!', color=(1,0,0,1)), 0)
                self.DAQ.ResetDAQ() # Reset the DAQ to clear the error state
                self.modeData.STOP_FLAG = True # Set stop flag to exit the loop gracefully
                break # Exit the while loop
            # time.sleep(0.1)  # sleep
            

        '''
        while not self.modeData.STOP_FLAG and self.modeData.CONNECTION_FLAG:
            currentTime = time.time()
            msg,self.total_samples_read=self.DAQ.ScanDAQ(self.total_samples_read,nebState)
            # COMMENT OUT BELOW
            
            if self.currentService.trialParameters.MODE=="BreathEmulate":
                if self.stateSet:
                    print(self.stateSet)
                    self.stateSet=False
                    self.thisState+=1
                    self.SwitchControl(self.nebStates[self.thisState])
                    if self.thisState<=len(self.stepDurations):
                        endDuration=self.stepDurations[self.thisState]
                        curDuration=0
                else:
                    curDuration+=1
                    if curDuration>=endDuration-1:
                        self.stateSet=True
                        curDuration=0
            #TILL HERE
    
            if self.currentService.trialParameters.MODE=="BreathEmulate":
                
                if self.stateSet:
                    self.stateSet = False
                    self.thisState += 1
                    self.stateStartTime = time.time()

                    if self.thisState < len(self.nebStates):
                        self.SwitchControl(self.nebStates[self.thisState])
                        self.endDuration = self.stepDurations[self.thisState]
                        
                    else:
                        print("Breath Emulation sequence complete.")
                        # break  # or continue without switching

                # else:
                    # elapsed_time = int(currentTime - startTime)
                    # self.logFile.WriteLog(f'(i put)Time Elapsed (s): {elapsed_time}', True)

                    # if elapsed >= self.endDuration:
                        # self.stateSet = True
            
            if self.currentService.trialParameters.MODE=="Static":
                print("entered static if statement")
                # WRITE STATIC MODE FUNCTIONALITY

            elapsed = int(time.time() - startTime)
            if elapsed == totalTime:
                print(f'Elapsed Time: {elapsed}')
                self.logFile.WriteLog(f'(i put)Time Elapsed (s): {elapsed}', True)
            
            # self.logFile.WriteLog('Time Elapsed (s):'+str(int(currentTime-startTime)+1)+' of '+str(self.currentService.trialParameters.RECORD_DURATION),True)
            if msg=='HardwareOvr':
                self.logFile.WriteLog('Hardware Over Run')
                break
            elif msg=='BuffOvr':
                self.logFile.WriteLog('Buffer Over Run')
                break
            else:
                currentTime=time.time()
                timeElapsed=currentTime-startTime
                continue
            time.sleep(0.5)  # sleep for 1 second
        '''
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0

        self.DAQ.ResetDAQ()
        if self.modeData.CONNECTION_FLAG:
            self.currentService.thisConnection.SendData2Server('Recording Complete!')

<<<<<<< HEAD
        self.logFile.WriteLog('Recording Ended', 1)
        self.logFile.WriteLog(f'Data Recording Complete for a Duration of {elapsed}s', 0)
        self.logFile.WriteLog('Final Data Frame Size:' + str(self.DAQ.recDataFrame.shape), 0)
        self.DAQ.recDataFrame.index.name = 'Samples'
=======
        self.logFile.WriteLog('Recording Ended ',1)
        # self.logFile.WriteLog('Data Recording Complete for a Duration of '+str(int(timeElapsed))+'s',0)
        self.logFile.WriteLog(f'Data Recording Complete for a Duration of {elapsed}s', 0)
        self.logFile.WriteLog('Final Data Frame Size:'+str(self.DAQ.recDataFrame.shape),0)
        self.DAQ.recDataFrame.index.name='Samples'
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0
        self.modeData.SEND_FILE = True
        self.modeData.DAQ_SET = True
        self.DONE = True

<<<<<<< HEAD
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
=======
        # Clock.schedule_once(lambda dt: self.ui_update_callback('Analysis Complete!', (0, 1, 0, 1)), 0)


        self.currentService.dataFileManage.Write2CSV(self.DAQ.recDataFrame)
        '''
        if self.ui_update_callback:
            if not self.modeData.STOP_FLAG: # Loop completed naturally
                Clock.schedule_once(lambda dt: self.ui_update_callback('Analysis Complete!', (0, 1, 0, 1)), 0)
            else: # Loop stopped by user or error
                 Clock.schedule_once(lambda dt: self.ui_update_callback('Analysis Stopped or Error Occurred.', (1, 0.65, 0, 1)), 0)
        '''
        return self.DONE

        



class RecordMode(ModeManager):
    def __init__(self,currentService):
        ModeManager.__init__(self,currentService)
    # def Run(self):
    #     print("entered record/combined mode")
    #     self.RegularModeRun()
    #     return self.DONE
    def Run(self):
        print("entered BE mode")
        # iterations = getattr(self.currentService.trialParameters, 'ITERATIONS', 1)
        iterations = int(self.currentService.trialParameters.ITERATIONS)
        for i in range(iterations):
            print(f"Starting iteration {i+1} of {iterations}")
            done = self.RegularModeRun()  # Run the analysis once
            if self.modeData.STOP_FLAG:  # Stop early if user presses STOP
                print("Analysis stopped by user.")
                break
        return self.DONE

class BreathEmulationMode(ModeManager):
    def __init__(self,currentService):
        ModeManager.__init__(self,currentService)
        #self.Nebulizer_Thread=threading.Thread(target=self.NebulizerControl,args=())
    def Run(self):
        print("entered be mode")
        self.RegularModeRun()
        return self.DONE

class StaticMode(ModeManager):
    def __init__(self,currentService):
        ModeManager.__init__(self,currentService)
    def Run(self):
        print("entered static mode")
        self.RegularModeRun()
        return self.DONE
        
    
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0
