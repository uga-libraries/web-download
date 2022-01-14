import os
import PySimpleGUI as sg
import sys

# For threading. Used to prevent the GUI from saying it is unresponsive when a process is taking a while.
import threading
import gc
SCRIPT_THREAD = '-SCRIPT_THREAD-'

# For threading. Disables garbage collecting, which is restarted with gc.collect() once the GUI starts.
gc.disable()

# Defines a GUI for users to provide the input needed for this script and
# to receive messages about errors to their inputs and the script progress.
sg.theme("DarkTeal6")

labels = [[sg.Text('Folder with CSVs', font=("roboto", 13))],
          [sg.Text('Archive-It Collection Number', font=("roboto", 13))],
          [sg.Text(font=("roboto", 1))],
          [sg.Submit(key="submit", disabled=False), sg.Cancel()]]

boxes = [[sg.Input(key="input_folder"), sg.FolderBrowse()],
         [sg.Input(key="ait_collection")],
         [sg.Text(font=("roboto", 1))],
         [sg.Text(font=("roboto", 13))]]

layout = [[sg.Column(labels), sg.Column(boxes)],
          [sg.Output(size=(90, 10))]]

window = sg.Window("Download PDFs from Archive-It", layout)

# Keeps the GUI open until the user quits the program. Receives user input, verifies the input,
# and when all input is correct runs the program.
while True:

    # For threading: start garbage collecting.
    gc.collect()

    # Gets the user input data and saves the input values to their own variables for easier referencing in the script.
    event, values = window.read()

    # For threading: let the user submit new information now that the script thread is over.
    if event == SCRIPT_THREAD:
        window[f'{"submit"}'].update(disabled=False)

    # If the user submitted values, tests they are correct. If not, errors are displayed. If yes, the script is run.
    if event == "submit":

        # Communicate that the script is starting to the user in the GUI dialogue box.
        print("\nPlease wait while the PDFs you requested are generated...")
        window.Refresh()

        # Error testing on all of the user inputs. Both fields are required and the path must be valid.
        # Errors are saved to a list so all values can be tested prior to notifying the user.
        errors = []
        if values["input_folder"] == "":
            errors.append("Folder with CSV can't be blank.")
        if not os.path.exists(values["input_folder"]):
            errors.append("Folder with CSV path is not correct.")
        if values["ait_collection"] == "":
            errors.append("Archive-It Collection Number cannot be blank.")

        # If the user inputs are correct, runs the script.
        if len(errors) == 0:

            print("Can run!")
            # For threading: run make_csv() in a thread.
            # TODO: adapt from parser code to download files code.
            #processing_thread = threading.Thread(target=make_csv, args=(values["input_file"], output_csv,
            #                                                                    values["mapping_csv"],
            #                                                                    values["output_folder"], window))
            #processing_thread.start()

            # Disable the submit button while make_csv() is running so users can't overwhelm computing resources
            # by requesting new CSVs before the first is done being created.
            #window[f'{"submit"}'].update(disabled=True)

        # If some of the user inputs were not correct, creates a pop up box alerting the user to the problem
        # and prints the errors in the GUI dialogue box.
        # The user may then edit the provided input and resubmit.
        else:
            sg.Popup("There is a problem with the provided information. See the program window for details.")
            print("\nThe app could not run. Please correct the following information and submit again.")
            print("\n".join(errors))
            window.Refresh()

    # If the user clicked cancel or the X on the GUI, quites the script.
    if event in ("Cancel", None):
        sys.exit()
