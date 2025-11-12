from datetime import datetime
import os
import pathlib
import pandas as pd
<<<<<<< HEAD
import Clustering
import Processor
=======
import subprocess
import threading

import DataProcessor as dp


RCLONE_REMOTE_NAME = 'pranas_pi'
ONEDRIVE_LOG_PATH = 'BACTERIA_DEVICE_UPLOADS/Logs'
ONEDRIVE_DATA_PATH = 'BACTERIA_DEVICE_UPLOADS/RecordedData'
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0



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
<<<<<<< HEAD
                self.log_file_name='Log_'+str(self.currentService.trialParameters.USER)+\
                                        '_'+currentService.GetCurrentTime(3)+'.log'
=======
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
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0
                self.WriteLog('Log started on ' + self.currentService.GetCurrentTime(2), 0)
                self.WriteLog('Initialized local system at ' + self.currentService.GetCurrentTime(1), 0)
                self.currentService=currentService

        def WriteLog(self, writeString, tpe):
                # Writes any string passed as argument to the session's log file opened initially
<<<<<<< HEAD
=======
                # if self.log_file is None:
                #         print(f"WARNING: Log file not open. Cannot write: {writeString}")
                #         return
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0
                if tpe==0:
                        writeString=writeString
                elif tpe==1:
                        writeString=self.currentService.GetCurrentTime(1)+':'+str(writeString)
                
                print(writeString)
<<<<<<< HEAD
                self.logFileFolder=os.path.abspath(os.getcwd())+'//logs'
                self.log_file = open(os.path.join(self.logFileFolder,self.log_file_name),"a")
                self.log_file.writelines(writeString+"\n")
                self.log_file.close()
=======
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

                if self.log_file:
                        try:
                                self.log_file.flush() # Flush any remaining buffered data
                                self.log_file.close()
                                print(f"DEBUG: LogFileManage: Log file '{self.log_file_name}' closed successfully.")
                        except Exception as e:
                                print(f"ERROR: LogFileManage: Failed to close log file: {e}")
                        self.log_file = None # Clear the file handle after closing




>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0
        
class DataFileManage:
        def __init__(self,currentService):
                self.currentService=currentService
                self.data_file_name='Data_'+str(self.currentService.trialParameters.UID)+\
                                        '_T'+str(self.currentService.trialParameters.TRIAL)+\
                                        '_'+currentService.trialParameters.MODE+\
                                        '_'+currentService.GetCurrentTime(3)+'.csv'
                self.RecordDataFolder=os.path.join(os.getcwd(),'RecordedData')
        def Write2CSV(self,dataFrame):
<<<<<<< HEAD
                dataFrame.to_csv(os.path.join(self.RecordDataFolder,self.data_file_name),index=True,header=True)
        
        def ReadFrmCSV(self,fileName):
                return pd.read_csv(fileName)
=======
                data_file_path = os.path.join(self.RecordDataFolder, self.data_file_name)
                dataFrame.to_csv(os.path.join(self.RecordDataFolder,self.data_file_name),index=True,header=True)
                # self._upload_to_onedrive(data_file_path, ONEDRIVE_DATA_PATH)
                upload_thread = threading.Thread(target=self._upload_to_onedrive,
                                         args=(data_file_path, ONEDRIVE_DATA_PATH))
                upload_thread.daemon = True
                upload_thread.start()

                self.DataProcess()
        
        def ReadFrmCSV(self,fileName):
                return pd.read_csv(fileName)

        def _upload_to_onedrive(self, local_file_path, remote_destination_path):

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

        def DataProcess(self):
                #----- INCLUDE DATA PROCESSING HERE -----#

                input_folder = self.RecordDataFolder  
                result = dp.create_and_move_csv(input_folder)
                print("Data processing finished:", result)
                return result


                #----- DATA PROCESSING ENDS HEREEEEE -----#

>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0
        '''
        def ReadFrmCSV(self):
                path_to_file = os.path.join(self.RecordDataFolder, self.data_file_name)
                return pd.read_csv(path_to_file)

        '''
<<<<<<< HEAD
        # def dataprocessor():
        #         folder_path = request.form.get('folder')
        #         #folder_path = folder_path.split('/')
        #         folder_path = 'ProcessedData/'+folder_path
        #         result = dp1.create_and_move_csv(folder_path)
        
class DataFileManage:
        def __init__(self,currentService):
                self.currentService=currentService
                self.data_file_name='Data_'+str(self.currentService.trialParameters.UID)+\
                                        '_T'+str(self.currentService.trialParameters.TRIAL)+\
                                        '_'+currentService.trialParameters.MODE+\
                                        '_'+currentService.GetCurrentTime(3)+'.csv'
                self.RecordDataFolder=os.path.join(os.getcwd(),'RecordedData')

        def Write2CSV(self,dataFrame):
                dataFrame.to_csv(os.path.join(self.RecordDataFolder,self.data_file_name),index=True,header=True)

        def ReadFrmCSV(self,fileName):
                return pd.read_csv(fileName)

        def clustering(self, master_file_path, algorithm='KMS', bacts='["B1","B2","B3"]', conc=0.1, vol=50, slide='S1'):
                """
                Run clustering on the master CSV file.
                
                Parameters:
                master_file_path: Path to the master CSV from Processor.py
                algorithm: 'KMS' | 'dbs' | 'OPS'
                bacts: List of bacteria names to include (stringified list)
                conc: concentration filter
                vol: volume filter
                slide: slide identifier
                """
                if not os.path.isfile(master_file_path):
                        print(f"Master file not found: {master_file_path}")
                        return

                # Load master CSV
                df = pd.read_csv(master_file_path)
                print(f"Master CSV loaded: {df.shape}")

                # Call your Clustering.Clustered_data function
                import Clustering
                try:
                        result = Clustering.Clustered_data(df, algorithm, bacts, conc, vol, slide)
                        print(result)
                except Exception as e:
                        print(f"Error during clustering: {e}")


                # self.data_file_name="Data_"+str(UID)+'_T'+str(TrialNo)+'_'+Mode
=======

        # self.data_file_name="Data_"+str(UID)+'_T'+str(TrialNo)+'_'+Mode
>>>>>>> 21cb90037cb0d71038ca9daaf58431e6daec4ee0

class DataTransfer:
    def __init__(self):
        self
