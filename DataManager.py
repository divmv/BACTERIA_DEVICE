from datetime import datetime
import os
import pathlib
import pandas as pd
import subprocess
import threading

RCLONE_REMOTE_NAME = 'pranas_pi'
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
                # self.log_file = None
                self.log_file_name='Log_'+str(self.currentService.trialParameters.USER)+\
                                        '_'+currentService.GetCurrentTime(3)+'.log'
                self.logFileFolder = os.path.join(os.path.abspath(os.getcwd()), 'logs')
                print("Folder")
                print(self.logFileFolder)
                os.makedirs(self.logFileFolder, exist_ok=True)
                self.log_file_path = os.path.join(self.logFileFolder, self.log_file_name) # Store the full path
                print("path:")
                print(self.log_file_path)
                self.WriteLog('Log started on ' + self.currentService.GetCurrentTime(2), 0)
                self.WriteLog('Initialized local system at ' + self.currentService.GetCurrentTime(1), 0)
                self.currentService=currentService

        def WriteLog(self, writeString, tpe):
                # Writes any string passed as argument to the session's log file opened initially
                # if self.log_file is None:
                #         print(f"WARNING: Log file not open. Cannot write: {writeString}")
                #         return
                if tpe==0:
                        writeString=writeString
                elif tpe==1:
                        writeString=self.currentService.GetCurrentTime(1)+':'+str(writeString)
                
                print(writeString)
                self.logFileFolder=os.path.abspath(os.getcwd())+'/logs'
                # log_file_path = os.path.join(self.logFileFolder, self.log_file_name)
                self.log_file = open(os.path.join(self.logFileFolder,self.log_file_name),"a")
                print("logfile")
                # print(self.log_file)
                self.log_file.writelines(writeString+"\n")
                # self.log_file.close()

                # self._upload_to_onedrive(log_file_path, ONEDRIVE_LOG_PATH)
                # upload_thread = threading.Thread(target=self._upload_to_onedrive,
                #                          args=(log_file_path, ONEDRIVE_LOG_PATH))
                # upload_thread.daemon = True # Allow the main program to exit even if this thread is running
                # upload_thread.start()

        def _upload_to_onedrive(self, local_file_path, remote_destination_path):
                """Helper method to upload a file using rclone."""
                remote_path = f"{RCLONE_REMOTE_NAME}:{remote_destination_path}"
                command = ['rclone', 'copy', '-vv', local_file_path, remote_path]
                
                try:
                        # print(f"Uploading {os.path.basename(local_file_path)} to OneDrive: {remote_path}")
                        result = subprocess.run(command, capture_output=True, text=True, check=True)
                        # print(f"Upload successful: {result.stdout}")
                        # print(f"Upload successful. Rclone stdout:\n{result.stdout.strip()}")
                        
                except subprocess.CalledProcessError as e:
                        print(f"Error uploading {os.path.basename(local_file_path)}: {e.stderr}")
                except FileNotFoundError:
                        print("Error: rclone command not found. Is rclone installed and in PATH?")
        
        def upload_log_file(self):
                print(f"Attempting final upload of log file: {self.log_file_name}")
                self._close_log_file()
                upload_thread = threading.Thread(target=self._upload_to_onedrive,
                                                args=(self.log_file_path, ONEDRIVE_LOG_PATH))
                upload_thread.daemon = False
                upload_thread.start()
                print("Waiting for log file upload to complete...")
                upload_thread.join(timeout=60) # Try 120 seconds (2 minutes)
                if upload_thread.is_alive():
                        print(f"WARNING: Log file upload thread for {self.log_file_name} did not finish within timeout.")
                else:
                        print(f"Log file '{self.log_file_name}' upload process finished.")
        
        def _close_log_file(self):
                """Internal method to ensure the log file is closed."""
                if self.log_file:
                        try:
                                self.log_file.flush() # Flush any remaining buffered data
                                self.log_file.close()
                                print(f"DEBUG: LogFileManage: Log file '{self.log_file_name}' closed successfully.")
                        except Exception as e:
                                print(f"ERROR: LogFileManage: Failed to close log file: {e}")
                        self.log_file = None # Clear the file handle after closing




        
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
