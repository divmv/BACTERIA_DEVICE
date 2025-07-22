from datetime import datetime
import os
import pathlib
import pandas as pd
import subprocess
import threading

RCLONE_REMOTE_NAME = 'pranas_pi'
# Replace 'BACTERIA_DEVICE_UPLOADS/Logs' and 'BACTERIA_DEVICE_UPLOADS/Data'
# with the desired paths on your OneDrive
ONEDRIVE_LOG_PATH = 'BACTERIA_DEVICE_UPLOADS/Logs'
ONEDRIVE_DATA_PATH = 'BACTERIA_DEVICE_UPLOADS/RecordedData'



class LogFileManage:
        def __init__(self,currentService):
                #Creating and Initializing Log File to which all the session information is written.
                self.currentService=currentService
                '''
                self.log_file_name='Log_'+str(self.currentService.trialParameters.UID)+\
                                        '_T'+str(self.currentService.trialParameters.TRIAL)+\
                                        '_'+currentService.trialParameters.MODE+\
                                        '_'+currentService.GetCurrentTime(3)+'.log'
                '''
                self.log_file_name='Log_'+str(self.currentService.trialParameters.USER)+\
                                        '_'+currentService.GetCurrentTime(3)+'.log'
                self.logFileFolder = os.path.join(os.path.abspath(os.getcwd()), 'logs')
                os.makedirs(self.logFileFolder, exist_ok=True)
                self.log_file_path = os.path.join(self.logFileFolder, self.log_file_name) # Store the full path
                self.WriteLog('Log started on ' + self.currentService.GetCurrentTime(2), 0)
                self.WriteLog('Initialized local system at ' + self.currentService.GetCurrentTime(1), 0)
                self.currentService=currentService

        def WriteLog(self, writeString, tpe):
                # Writes any string passed as argument to the session's log file opened initially
                if tpe==0:
                        writeString=writeString
                elif tpe==1:
                        writeString=self.currentService.GetCurrentTime(1)+':'+str(writeString)
                
                print(writeString)
                self.logFileFolder=os.path.abspath(os.getcwd())+'//logs'
                # log_file_path = os.path.join(self.logFileFolder, self.log_file_name)
                self.log_file = open(os.path.join(self.logFileFolder,self.log_file_name),"a")
                self.log_file.writelines(writeString+"\n")
                self.log_file.close()

                # self._upload_to_onedrive(log_file_path, ONEDRIVE_LOG_PATH)
                # upload_thread = threading.Thread(target=self._upload_to_onedrive,
                #                          args=(log_file_path, ONEDRIVE_LOG_PATH))
                # upload_thread.daemon = True # Allow the main program to exit even if this thread is running
                # upload_thread.start()

        def _upload_to_onedrive(self, local_file_path, remote_destination_path):
                """Helper method to upload a file using rclone."""
                remote_path = f"{RCLONE_REMOTE_NAME}:{remote_destination_path}"
                command = ['rclone', 'copy', local_file_path, remote_path]
                
                try:
                        # print(f"Uploading {os.path.basename(local_file_path)} to OneDrive: {remote_path}")
                        result = subprocess.run(command, capture_output=True, text=True, check=True)
                        # print(f"Upload successful: {result.stdout}")
                except subprocess.CalledProcessError as e:
                        print(f"Error uploading {os.path.basename(local_file_path)}: {e.stderr}")
                except FileNotFoundError:
                        print("Error: rclone command not found. Is rclone installed and in PATH?")
        
        def upload_log_on_exit(self):
                print(f"Attempting final upload of log file: {self.log_file_name}")
                upload_thread = threading.Thread(target=self._upload_to_onedrive,
                                                args=(self.log_file_path, ONEDRIVE_LOG_PATH))
                upload_thread.daemon = True
                upload_thread.start()
                # You might want to join the thread if you need to ensure the upload finishes
                # before the Python interpreter exits, but that would re-introduce blocking.
                # For daemon threads, Python usually waits briefly or until all non-daemon threads exit.



        
class DataFileManage:
        def __init__(self,currentService):
                self.currentService=currentService
                self.data_file_name='Data_'+str(self.currentService.trialParameters.UID)+\
                                        '_T'+str(self.currentService.trialParameters.TRIAL)+\
                                        '_'+currentService.trialParameters.MODE+\
                                        '_'+currentService.GetCurrentTime(3)+'.csv'
                self.RecordDataFolder=os.path.join(os.getcwd(),'RecordedData')
        def Write2CSV(self,dataFrame):
                data_file_path = os.path.join(self.RecordDataFolder, self.data_file_name)
                dataFrame.to_csv(os.path.join(self.RecordDataFolder,self.data_file_name),index=True,header=True)
                # self._upload_to_onedrive(data_file_path, ONEDRIVE_DATA_PATH)
                upload_thread = threading.Thread(target=self._upload_to_onedrive,
                                         args=(data_file_path, ONEDRIVE_DATA_PATH))
                upload_thread.daemon = True
                upload_thread.start()
        
        def ReadFrmCSV(self,fileName):
                return pd.read_csv(fileName)

        def _upload_to_onedrive(self, local_file_path, remote_destination_path):
                """Helper method to upload a file using rclone."""
                remote_path = f"{RCLONE_REMOTE_NAME}:{remote_destination_path}"
                command = ['rclone', 'copy', local_file_path, remote_path]
                
                try:
                        # print(f"Uploading {os.path.basename(local_file_path)} to OneDrive: {remote_path}")
                        result = subprocess.run(command, capture_output=True, text=True, check=True)
                        # print(f"Upload successful: {result.stdout}")
                except subprocess.CalledProcessError as e:
                        print(f"Error uploading {os.path.basename(local_file_path)}: {e.stderr}")
                except FileNotFoundError:
                        print("Error: rclone command not found. Is rclone installed and in PATH?")


        '''
        def ReadFrmCSV(self):
                path_to_file = os.path.join(self.RecordDataFolder, self.data_file_name)
                return pd.read_csv(path_to_file)

        '''

        # self.data_file_name="Data_"+str(UID)+'_T'+str(TrialNo)+'_'+Mode

class DataTransfer:
    def __init__(self):
        self
