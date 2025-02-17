# Loads a .mat file that has been saved out by the PhoLabjackCSVHelper MATLAB scripts
# It contains the result of the 'labjackTimeTable' variable

import datetime as dt
import pathlib
import re
from enum import Enum

import h5py as h5py
import numpy as np
import pandas as pd
import scipy.io as sio
from phopyqttimelineplotter.app.filesystem.FilesystemRecordBase import FilesystemLabjackEvent_Record
from PyQt5.QtCore import QEvent, QObject, Qt, pyqtSignal

from phopyqttimelineplotter.GUI.Model.Events.PhoDurationEvent import (
    PhoDurationEvent,
    PhoEvent,
)

# Copied from "phoPythonVideoFileParser" project

# from phopyqttimelineplotter.app.filesystem.LabjackData.LabjackEventsLoader import loadLabjackDataFromPhoServerFormat, loadLabjackDataFromMatlabFormat, labjack_variable_names, labjack_variable_colors_dict, labjack_variable_indicies_dict, labjack_variable_event_type, labjack_variable_port_location, writeLinesToCsvFile
# from phopyqttimelineplotter.app.filesystem.LabjackData.LabjackEventsLoader import LabjackEventsLoader, PhoServerFormatArgs


class PhoServerFormatArgs(QObject):
    """class PhoServerFormatArgs: A simple wrapper class that holds the arguments to filter_invalid_events for phoServerFormat"""

    def __init__(
        self,
        relevantDateTimes,
        relevantFileLines,
        erroneousEventFreeCSVFilePath,
        parsedFileInfoDict,
        parent=None,
    ):
        super(PhoServerFormatArgs, self).__init__(parent=parent)
        # self.usePhoServerFormat = usePhoServerFormat
        self.relevantDateTimes = relevantDateTimes
        self.relevantFileLines = relevantFileLines
        self.erroneousEventFreeCSVFilePath = erroneousEventFreeCSVFilePath
        self.parsedFileInfoDict = parsedFileInfoDict


class LabjackEventType(Enum):
    phoDurationEvent = 1
    filesystemLabjackEvent_Record = 2

    # def get_class(self):
    #     if (self is LabjackEventType.phoDurationEvent):
    #         return PhoDurationEvent.__class__
    #     elif (self is LabjackEventType.filesystemLabjackEvent_Record):
    #         return filesystemLabjackEvent_Record.__class__
    #     else:
    #         print("ERROR: Unknown Type")
    #         return None

    def get_variable_specific_items_key(self):
        if self is LabjackEventType.phoDurationEvent:
            return "variableSpecificEvents"
        elif self is LabjackEventType.filesystemLabjackEvent_Record:
            return "variableSpecificRecords"
        else:
            print("ERROR: Unknown Type")
            raise NotImplementedError
            return None


class LabjackEventsLoader(object):

    # Defined constants
    labjack_portNames = ["Water1", "Water2", "Food1", "Food2"]

    labjack_variable_names = [
        "Water1_BeamBreak",
        "Water2_BeamBreak",
        "Food1_BeamBreak",
        "Food2_BeamBreak",
        "Water1_Dispense",
        "Water2_Dispense",
        "Food1_Dispense",
        "Food2_Dispense",
    ]
    labjack_variable_colors = [
        "aqua",
        "aquamarine",
        "coral",
        "magenta",
        "blue",
        "darkblue",
        "crimson",
        "maroon",
    ]
    labjack_variable_indicies = [0, 1, 2, 3, 4, 5, 6, 7]
    labjack_variable_event_type = [
        "BeamBreak",
        "BeamBreak",
        "BeamBreak",
        "BeamBreak",
        "Dispense",
        "Dispense",
        "Dispense",
        "Dispense",
    ]
    labjack_variable_dispense_type = [
        "Water",
        "Water",
        "Food",
        "Food",
        "Water",
        "Water",
        "Food",
        "Food",
    ]
    labjack_variable_port_location = [
        "Water1",
        "Water2",
        "Food1",
        "Food2",
        "Water1",
        "Water2",
        "Food1",
        "Food2",
    ]

    labjack_csv_variable_names = [
        "milliseconds_since_epoch",
        "DIO0",
        "DIO1",
        "DIO2",
        "DIO3",
        "DIO4",
        "DIO5",
        "DIO6",
        "DIO7",
        "MIO0",
    ]

    # Derived Dictionaries
    labjack_variable_colors_dict = dict( zip(labjack_variable_names, labjack_variable_colors) )
    labjack_variable_indicies_dict = dict( zip(labjack_variable_names, labjack_variable_indicies) )

    ## TODO: Generalize to work with analog sensors (like the new 1-9-2020 running wheel absolute rotary encoder)
    rx_stdout_data_line = re.compile(
        r"^(?P<milliseconds_since_epoch>\d{13}): (?P<DIO0>[10]), (?P<DIO1>[10]), (?P<DIO2>[10]), (?P<DIO3>[10]), (?P<DIO4>[10]), (?P<DIO5>[10]), (?P<DIO6>[10]), (?P<DIO7>[10]), (?P<MIO0>[10]),"
    )
    rx_csv_data_line = re.compile(
        r"^(?P<milliseconds_since_epoch>\d{13}),(?P<DIO0>[10]),(?P<DIO1>[10]),(?P<DIO2>[10]),(?P<DIO3>[10]),(?P<DIO4>[10]),(?P<DIO5>[10]),(?P<DIO6>[10]),(?P<DIO7>[10]),(?P<MIO0>[10])"
    )
    rx_stdout_dict = {"data": rx_stdout_data_line}
    rx_csv_dict = {"data": rx_csv_data_line}

    """
    out_file_s470017560_1562601911545.csv

    out_file_s470017560_46Combined.csv
    out_file_s470017560_20190911-20190820_46Combined.csv

    # Combined MATLAB output format:
    out_file_s{LabjackSerialNumber}_{YYYYMMDD_LATEST}-{YYYYMMDD_EARLIEST}_{NumberOfCSVFilesConcatenated}Combined.csv

    "I:\EventData\BB01\Subject_02"

    "I:\EventData\BB01\Subject_02\out_file_s470017560_20190911-20190820_46Combined.csv"


    \d{9}
    BB(?P<bb_id>\d{2})
    (?P<latest_year>\d{4})(?P<latest_month>\d{2})(?P<latest_day>\d{2})
    (?P<earliest_year>\d{4})(?P<earliest_month>\d{2})(?P<earliest_day>\d{2})

    (?P<latest_date>\d{4}\d{2}\d{2})
    (?P<earliest_date>\d{4}\d{2}\d{2})

    (?_(?P<latest_date>\d{4}\d{2}\d{2})-(?P<earliest_date>\d{4}\d{2}\d{2}))?

    """
    # Parses the "out_file_s470017560_20190911-20190820_46Combined" part out of "I:\EventData\BB01\Subject_02\out_file_s470017560_20190911-20190820_46Combined.csv"
    # rx_combined_csv_file_name = re.compile(r'^out_file_s(?P<labjack_serial_number>\d{9})_(?P<latest_year>\d{4})(?P<latest_month>\d{2})(?P<latest_day>\d{2})-(?P<earliest_year>\d{4})(?P<earliest_month>\d{2})(?P<earliest_day>\d{2})_(?P<number_of_CSV_files_concatenated>\d+)Combined$')
    rx_combined_csv_file_name = re.compile(
        r"^out_file_s(?P<labjack_serial_number>\d{9})(?P<date_ranges>_(?P<latest_date>\d{4}\d{2}\d{2})-(?P<earliest_date>\d{4}\d{2}\d{2}))?_(?P<number_of_CSV_files_concatenated>\d+)Combined"
    )

    # Parses the "BB01" part out of the file path "I:\EventData\BB01\Subject_02"
    rx_combined_csv_file_path_name_bb_id = re.compile(r"^BB(?P<bb_id>\d{2})$")

    # Parses the "Subject_02" part out of the file path "I:\EventData\BB01\Subject_02"
    rx_combined_csv_file_path_name_subject_name = re.compile(
        r"^Subject_(?P<subject_id>\d+)$"
    )

    # matPath = 'C:\Users\watsonlab\Documents\code\PhoLabjackCSVHelper\Output\LabjackTimeTable.mat'
    @staticmethod
    def matlab2datetime(matlab_datenum):
        day = dt.datetime.fromordinal(int(matlab_datenum))
        dayfrac = dt.timedelta(days=matlab_datenum % 1) - dt.timedelta(days=366)
        return day + dayfrac

    helper_timenum_to_datetime = np.vectorize(
        lambda x: LabjackEventsLoader.matlab2datetime(x)
    )

    """ find_invalid_events(labjackEvents)
        returns: 1. a dict of invalidDispenseEventTimestamps: {'Water1': list, 'Water2': list, 'Food1': list, 'Food2': list, 'any': list}
                2. valid_labjack_events_mask: a mask of the size of labjackEvents that can be used to filter out the invalid labjack events
    """

    @staticmethod
    def find_invalid_events(labjackEvents, labjackEventType):
        previousFoundDispenseEventTimestamp = {
            "Water1": None,
            "Water2": None,
            "Food1": None,
            "Food2": None,
        }
        previousFoundBeambreakEventTimestamp = {
            "Water1": None,
            "Water2": None,
            "Food1": None,
            "Food2": None,
        }
        invalidDispenseEventTimestamps = {
            "Water1": [],
            "Water2": [],
            "Food1": [],
            "Food2": [],
            "any": [],
        }
        valid_labjack_events_mask = np.ones(len(labjackEvents), dtype=bool)

        for index, anActiveEvent in enumerate(labjackEvents):

            # how the extended data dict is accessed depends on the labjackEventType
            anActiveEvent_ExtendedData = None
            if labjackEventType is LabjackEventType.phoDurationEvent:
                anActiveEvent_ExtendedData = anActiveEvent.extended_data

            elif labjackEventType is LabjackEventType.filesystemLabjackEvent_Record:
                anActiveEvent_ExtendedData = anActiveEvent.get_extended_data()
            else:
                print("ERROR: Unknown Type!")
                return None

            if anActiveEvent_ExtendedData["event_type"] == "BeamBreak":
                currFoundBeambreakEventTimestamp = anActiveEvent.start_date
                previousFoundBeambreakEventTimestamp[
                    anActiveEvent_ExtendedData["port"]
                ] = currFoundBeambreakEventTimestamp

            elif anActiveEvent_ExtendedData["event_type"] == "Dispense":
                currIsInvalidEvent = False
                currFoundDispenseEventTimestamp = anActiveEvent.start_date
                if (
                    previousFoundBeambreakEventTimestamp[
                        anActiveEvent_ExtendedData["port"]
                    ]
                    is None
                ):
                    # If no beambreak preceeds it, it's invalid
                    currIsInvalidEvent = True

                else:
                    if (
                        previousFoundDispenseEventTimestamp[
                            anActiveEvent_ExtendedData["port"]
                        ]
                        is None
                    ):
                        # if no dispense event preceeds it there's no problem
                        pass
                    else:
                        if (
                            previousFoundDispenseEventTimestamp[
                                anActiveEvent_ExtendedData["port"]
                            ]
                            > previousFoundBeambreakEventTimestamp[
                                anActiveEvent_ExtendedData["port"]
                            ]
                        ):
                            # if the most recent dispense event is more recent then the last beambreak, there is a problem!
                            currIsInvalidEvent = True

                previousFoundDispenseEventTimestamp[
                    anActiveEvent_ExtendedData["port"]
                ] = currFoundDispenseEventTimestamp

                if currIsInvalidEvent:
                    valid_labjack_events_mask[index] = False
                    invalidDispenseEventTimestamps[
                        anActiveEvent_ExtendedData["port"]
                    ].append(currFoundDispenseEventTimestamp)
                    invalidDispenseEventTimestamps["any"].append(
                        currFoundDispenseEventTimestamp
                    )

            else:
                pass

        # Produces invalidDispenseEventTimestamps
        return (invalidDispenseEventTimestamps, valid_labjack_events_mask)

    """ filter_invalid_events(dateTimes, onesEventFormatDataArray, variableData, labjackEvents, phoServerFormatArgs):
        Filters invalid events from the loaded data structures
        returns: filtered (dateTimes, onesEventFormatDataArray, variableData,  labjackEvents, phoServerFormatArgs)
    """

    @staticmethod
    def filter_invalid_events(
        dateTimes,
        onesEventFormatDataArray,
        variableData,
        labjackEvents,
        phoServerFormatArgs=None,
    ):
        num_labjack_events = len(labjackEvents)
        if num_labjack_events <= 0:
            # print("WARNING: labjackEvents is empty!")
            return (
                dateTimes,
                onesEventFormatDataArray,
                variableData,
                labjackEvents,
                phoServerFormatArgs,
            )

        active_labjack_event_type = None
        first_labjack_event_obj = labjackEvents[0]
        if type(first_labjack_event_obj) is PhoDurationEvent:
            active_labjack_event_type = LabjackEventType.phoDurationEvent

        elif type(first_labjack_event_obj) is FilesystemLabjackEvent_Record:
            active_labjack_event_type = LabjackEventType.filesystemLabjackEvent_Record
        else:
            print("ERROR: Unknown Type!")
            return None

        # Get the key for the items (either events or records) that belong to a specific variable:
        active_variableData_event_specific_key = (
            active_labjack_event_type.get_variable_specific_items_key()
        )

        # Produces invalidDispenseEventTimestamps
        (
            invalidDispenseEventTimestamps,
            valid_labjack_events_mask,
        ) = LabjackEventsLoader.find_invalid_events(
            labjackEvents, active_labjack_event_type
        )

        # Filter the erroneous events from the individual arrays in each variableData
        for index, aPort in enumerate(LabjackEventsLoader.labjack_portNames):
            # print('Invalid dispense events detected: ', invalidDispenseEventIndicies)
            dispenseVariableIndex = index + 4
            dispenseVariableTimestamps = np.array(
                variableData[dispenseVariableIndex]["timestamps"]
            )
            dispenseVariableInvalidTimestamps = np.array(
                invalidDispenseEventTimestamps[aPort]
            )
            # print(aPort, ": ", len(dispenseVariableInvalidTimestamps), 'invalid dispense events out of', len(dispenseVariableTimestamps), 'events.')
            print(
                aPort,
                ": out of",
                len(dispenseVariableTimestamps),
                "dispense events,",
                len(dispenseVariableInvalidTimestamps),
                "are invalid.",
            )
            print(
                "    Removing ",
                len(dispenseVariableInvalidTimestamps),
                " invalid events...",
            )
            dispenseVariableInvalidIndicies = np.isin(
                dispenseVariableTimestamps, dispenseVariableInvalidTimestamps
            )
            mask = np.ones(len(dispenseVariableTimestamps), dtype=bool)
            mask[dispenseVariableInvalidIndicies] = False
            variableData[dispenseVariableIndex]["timestamps"] = variableData[
                dispenseVariableIndex
            ]["timestamps"][mask]
            variableData[dispenseVariableIndex]["values"] = variableData[
                dispenseVariableIndex
            ]["values"][mask]
            # Issue with this key: variableSpecificEvents
            variableData[dispenseVariableIndex][
                active_variableData_event_specific_key
            ] = np.array(
                variableData[dispenseVariableIndex][
                    active_variableData_event_specific_key
                ]
            )[
                mask
            ]
            variableData[dispenseVariableIndex]["videoIndicies"] = variableData[
                dispenseVariableIndex
            ]["videoIndicies"][mask]
            print(
                "    done.",
                len(variableData[dispenseVariableIndex]["timestamps"]),
                "events remain.",
            )

        # Filter the erroneous events from dateTimes and onesEventFormatDataArray
        num_total_invalid_events = len(invalidDispenseEventTimestamps["any"])
        print(
            "    found {} total invalid labjackEvents... removing...".format(
                str(num_total_invalid_events)
            )
        )

        dispenseVariableAnyInvalidIndicies = np.isin(
            dateTimes, invalidDispenseEventTimestamps["any"]
        )
        dateTimes_mask = np.ones(len(dateTimes), dtype=bool)
        dateTimes_mask[dispenseVariableAnyInvalidIndicies] = False
        print(
            "    done. {} of {} total events remain.".format(
                str(num_labjack_events - num_total_invalid_events),
                str(num_labjack_events),
            )
        )

        # Filter the relevant datetimes to obtain the list of lines that contain invalid events. Save them to a new CSV if desired.
        ## TODO: ensure that non-food 2 events aren't also being removed by removing the entire line at this timestamp.
        if phoServerFormatArgs is not None:
            dispenseVariableAnyInvalidIndicies = np.isin(
                phoServerFormatArgs.relevantDateTimes,
                invalidDispenseEventTimestamps["any"],
            )
            relevantDateTimes_mask = np.ones(
                len(phoServerFormatArgs.relevantDateTimes), dtype=bool
            )
            relevantDateTimes_mask[dispenseVariableAnyInvalidIndicies] = False

            phoServerFormatArgs.relevantDateTimes = (
                phoServerFormatArgs.relevantDateTimes[relevantDateTimes_mask]
            )
            phoServerFormatArgs.relevantFileLines = np.array(
                phoServerFormatArgs.relevantFileLines
            )[relevantDateTimes_mask]
            # r'C:\Users\halechr\repo\phoPythonVideoFileParser'
            # erroneousEventFreeCSVFilePath = r'C:\Users\halechr\repo\phoPythonVideoFileParser\results\erroneousEventsRemoved.csv'
            # erroneousEventFreeCSVFilePath = r'results\erroneousEventsRemoved.csv'
            if phoServerFormatArgs.erroneousEventFreeCSVFilePath is not None:
                print(
                    "Writing to CSV file:",
                    phoServerFormatArgs.erroneousEventFreeCSVFilePath,
                )
                LabjackEventsLoader.writeLinesToCsvFile(
                    phoServerFormatArgs.relevantFileLines,
                    filePath=phoServerFormatArgs.erroneousEventFreeCSVFilePath,
                )
                print("    done.")
            else:
                print(
                    "erroneousEventFreeCSVFilePath is None, so skipping .CSV file output"
                )

        return (
            dateTimes[dateTimes_mask],
            onesEventFormatDataArray[dateTimes_mask],
            variableData,
            labjackEvents[valid_labjack_events_mask],
            phoServerFormatArgs,
        )

    @staticmethod
    def loadLabjackData(matPath):
        mat_dict = sio.loadmat(matPath, squeeze_me=True, struct_as_record=False)
        return mat_dict

    # used by loadLabjackDataFromMatlabFormat(...)
    @staticmethod
    def loadLabjackDataNew(filePath):
        file = h5py.File(filePath, "r")
        return file

    @staticmethod
    def loadLabjackDataFromMatlabFormat(filePath):
        # The exported MATLAB .mat file contains:
        # a single struct named 'labjackDataOutput':
        # 'dateTime': 5388702 x 1 double array - contains timestamps at which the sensor values were sampled
        # 'dataArray': 5388702 x 8 double array - contains sensor values at each sampled timestamp
        # 'ColumnNames': 1 x 8 cell array - contains names of variables
        file = LabjackEventsLoader.loadLabjackDataNew(filePath)
        # Get the 'labjackDataOutput' matlab variable from the loaded file.
        data = file.get("labjackDataOutput")
        # Do try and convert the dateNums to datetimes:
        dateNums = np.squeeze(np.array(data["dateTime"]))
        # dateTimes = [matlab2datetime(tval[0]) for tval in dateNums]
        # dateTimes = np.array(dateTimes)
        dateTimes = np.array(LabjackEventsLoader.helper_timenum_to_datetime(dateNums))
        dataArray = np.array(data["dataArray"]).T
        return (dateNums, dateTimes, dataArray)

    """ def parsePhoServerFormatFilepath(filePathString)
    Tries to determine metadata information from loaded labjack filepath
    """

    @staticmethod
    def parsePhoServerFormatFilepath(filePathString):
        # Expects path in format: "I:\EventData\BB01\Subject_02\out_file_s470017560_20190911-20190820_46Combined.csv"

        parsedResult = dict()

        filePath = pathlib.Path(filePathString)
        filePath = filePath.resolve(strict=True)

        # fileName: "out_file_s470017560_20190911-20190820_46Combined.csv"
        fileName = filePath.name
        fileBaseName = filePath.stem

        # Perform regex parsing:
        did_encounter_issue = False
        labjack_serial_number = None

        date_range_earliest = None
        date_range_latest = None

        # Filename matching:
        filename_matches = LabjackEventsLoader.rx_combined_csv_file_name.search(
            fileBaseName
        )
        if filename_matches is not None:
            # Filename matches:
            if filename_matches.group("labjack_serial_number"):
                labjack_serial_number = filename_matches.group("labjack_serial_number")

            else:
                print(
                    "WARNING: failed to find labjack_serial_number in fileBaseName: {}".format(
                        fileBaseName
                    )
                )

            if filename_matches.group("date_ranges"):
                if filename_matches.group("latest_date"):
                    # latest/earliest date format
                    tempParsableDateString = filename_matches.group("latest_date")
                    date_range_latest = dt.datetime.strptime(
                        tempParsableDateString, "%Y%m%d"
                    )  # YYYYMMDD
                    date_range_latest = date_range_latest.replace(
                        tzinfo=dt.timezone.utc
                    )
                else:
                    print(
                        "found valid date_ranges, but no valid latest_date... fileBaseName: {}".format(
                            fileBaseName
                        )
                    )

                if filename_matches.group("earliest_date"):
                    # earliest_date
                    tempParsableDateString = filename_matches.group("earliest_date")
                    date_range_earliest = dt.datetime.strptime(
                        tempParsableDateString, "%Y%m%d"
                    )  # YYYYMMDD
                    date_range_earliest = date_range_earliest.replace(
                        tzinfo=dt.timezone.utc
                    )
                else:
                    print(
                        "found valid date_ranges, but no valid earliest_date... fileBaseName: {}".format(
                            fileBaseName
                        )
                    )

            else:
                # No date ranges provided...
                print(
                    "couldn't find valid date_ranges: No date ranges provided... fileBaseName: {}".format(
                        fileBaseName
                    )
                )

        else:
            print("Failed to match!!! fileBaseName: {}".format(fileBaseName))

        # remaining_identifier_regexes = [LabjackEventsLoader.rx_combined_csv_file_path_name_subject_name, LabjackEventsLoader.rx_combined_csv_file_path_name_bb_id]
        behavioral_box_id = None
        subject_id = None

        # parentPath: "I:\EventData\BB01\Subject_02\"
        # parentDirName: "Subject_02"
        # parentPath = filePath.parent
        # parentDirName = parentPath.name

        # Should be "Subject_02" part

        # grandparentPath: "I:\EventData\BB01\"
        # grandparentDirName: "BB01"
        # grandparentPath = parentPath.parent
        # grandparentDirName = grandparentPath.name

        # Get all ancestors of filePath
        parentFolderPaths = filePath.parents
        # Iterate through all parents
        for aParentPath in parentFolderPaths:
            # Try to match
            curr_parent_path_name = aParentPath.name

            # Subject ID:
            if subject_id is None:
                subject_id_matches = LabjackEventsLoader.rx_combined_csv_file_path_name_subject_name.search(
                    curr_parent_path_name
                )
                if subject_id_matches is not None:
                    if subject_id_matches.group("subject_id"):
                        subject_id = int(subject_id_matches.group("subject_id"))
                        continue  # found subject_id: Move on to the next part of the path

            # BB ID:
            if behavioral_box_id is None:
                bb_id_matches = (
                    LabjackEventsLoader.rx_combined_csv_file_path_name_bb_id.search(
                        curr_parent_path_name
                    )
                )
                if bb_id_matches is not None:
                    if bb_id_matches.group("bb_id"):
                        behavioral_box_id = int(bb_id_matches.group("bb_id"))
                        continue  # Found bb_id:  Move on to the next part of the path

        did_encounter_issue = (
            (behavioral_box_id is None)
            or (subject_id is None)
            or (labjack_serial_number is None)
            or (date_range_earliest is None)
            or (date_range_latest is None)
        )
        if did_encounter_issue:
            print("encountered issue parsing path: {}".format(filePathString))
        else:
            print("parsed successfully!")
            pass

        # build output dictionary
        parsedResult["filePathString"] = filePathString

        parsedResult["behavioral_box_id"] = behavioral_box_id
        parsedResult["subject_id"] = subject_id
        parsedResult["labjack_serial_number"] = labjack_serial_number
        parsedResult["date_range_earliest"] = date_range_earliest
        parsedResult["date_range_latest"] = date_range_latest

        parsedResult["did_encounter_issue"] = did_encounter_issue

        print("Finished parsing {}. Result: {}".format(filePathString, parsedResult))
        return parsedResult

    ## TODO: Generalize to work with analog sensors (like the new 1-9-2020 running wheel absolute rotary encoder)
    @staticmethod
    def loadLabjackDataFromPhoServerFormat(filePath, shouldUseStdOutFormat=True):
        # Loads from a txt file output by my PhoServer C++ program and returns (relevantFileLines, dateTimes, onesEventFormatOutputData)
        def _parse_line(line):
            """
            Do a regex search against all defined regexes and
            return the key and match result of the first matching regex

            """
            if shouldUseStdOutFormat:
                active_rx_dict = LabjackEventsLoader.rx_stdout_dict
            else:
                active_rx_dict = LabjackEventsLoader.rx_csv_dict

            for key, rx in active_rx_dict.items():
                match = rx.search(line)
                if match:
                    return key, match
            # if there are no matches
            return None, None

        def parse_file(filepath):
            """
            Parse text at given filepath

            Parameters
            ----------
            filepath : str
                Filepath for file_object to be parsed

            Returns
            -------
            data : pd.DataFrame
                Parsed data
            """

            parsedDateTimes = []  # create an empty list to collect the data
            parsedDataArray = []
            relevantFileLines = []
            # open the file and read through it line by line
            with open(filepath, "r") as file_object:
                line = file_object.readline()
                while line:
                    # at each line check for a match with a regex
                    key, match = _parse_line(line)

                    # extract data line elements
                    if key == "data":
                        milliseconds_since_epoch = match.group(
                            "milliseconds_since_epoch"
                        )
                        # DIO0 = match.group('DIO0')
                        # DIO1 = match.group('DIO1')
                        # DIO2 = match.group('DIO2')
                        # DIO3 = match.group('DIO3')
                        # DIO4 = match.group('DIO4')
                        # DIO5 = match.group('DIO5')
                        # DIO6 = match.group('DIO6')
                        # DIO7 = match.group('DIO7')
                        # MIO0 = match.group('MIO0')
                        DIO0 = match.group("DIO0")
                        DIO1 = match.group("DIO1")
                        DIO2 = match.group("DIO2")
                        DIO3 = match.group("DIO3")
                        DIO4 = match.group("DIO4")
                        DIO5 = match.group("DIO5")
                        DIO6 = match.group("DIO6")
                        DIO7 = match.group("DIO7")
                        MIO0 = match.group("MIO0")

                        # local time
                        t = dt.datetime.fromtimestamp(
                            float(milliseconds_since_epoch) / 1000.0
                        )

                        parsedDateTimes.append(t)
                        # rowData = [DIO0, DIO1, DIO2, DIO3, DIO4, DIO5, DIO6, DIO7, MIO0]
                        rowData = [
                            int(DIO0),
                            int(DIO1),
                            int(DIO2),
                            int(DIO3),
                            int(DIO4),
                            int(DIO5),
                            int(DIO6),
                            int(DIO7),
                            int(MIO0),
                        ]
                        # rowData = [DIO0, DIO1, DIO2, DIO3, DIO4, DIO5, DIO6, DIO7, MIO0] == '1'
                        parsedDataArray.append(rowData)
                        # Append the line
                        relevantFileLines.append(line)

                    line = file_object.readline()

            return (
                np.array(relevantFileLines),
                np.array(parsedDateTimes),
                np.array(parsedDataArray),
            )

        parsedFileInfoDict = LabjackEventsLoader.parsePhoServerFormatFilepath(filePath)
        (relevantFileLines, dateTimes, dataArray) = parse_file(filePath)

        # Parse to find the transitions ( "roll" rotates the array to left some step length)
        # A False followed by a True can then be expressed as: https://stackoverflow.com/questions/47750593/finding-false-true-transitions-in-a-numpy-array?rq=1
        # dataArrayTransitions = ~dataArray & np.roll(dataArray, -1)
        numSamples = dataArray.shape[0]
        numVariables = dataArray.shape[1]
        # Look for transitions to negative values (falling edges)
        dataArrayTransitions = np.concatenate(
            (np.zeros((1, numVariables)), np.diff(dataArray, axis=0)), axis=0
        )
        # testTransitions.shape: (7340,9)
        falling_edge_cells_result = np.where(dataArrayTransitions < -0.01)
        # falling_edge_cells_result.shape: ((3995,), (3995,))
        falling_edges_row_indicies = falling_edge_cells_result[0]
        # falling_edges_row_indicies.shape: (3995,)
        # outputDateTimes = dateTimes[falling_edges_row_indicies]
        # outputDateTimes.shape: (3995,)

        # Build output object
        # out_filtered_csv_path = r'C:\Users\halechr\repo\phoPythonVideoFileParser\results\erroneousEventsRemoved.csv'
        out_filtered_csv_path = None
        outputPhoServerFormatArgs = PhoServerFormatArgs(
            dateTimes[falling_edges_row_indicies],
            relevantFileLines[falling_edges_row_indicies],
            out_filtered_csv_path,
            parsedFileInfoDict,
        )

        # "onesEventFormat" has a '1' value anywhere an event occurred, and zeros elsewhere. These are computed by checking falling edges to find transitions. Has same dimensionality as inputEventFormat.
        onesEventFormatOutputData = np.zeros((numSamples, numVariables))
        onesEventFormatOutputData[falling_edge_cells_result] = 1.0
        return (outputPhoServerFormatArgs, dateTimes, onesEventFormatOutputData)

    """ loadLabjackEventsFile_loadFromFile(...): Just loads the file
    Called by loadLabjackEventsFile(...)
        Calls the static LabjackEventsLoader functions for the appropriate file format (phoServer format or Matlab format).
        Returns a onesEventFormatDataArray.
    """

    @staticmethod
    def loadLabjackEventsFile_loadFromFile(
        labjackFilePath, usePhoServerFormat=False, phoServerFormatIsStdOut=True
    ):
        ## Load the Labjack events data from an exported MATLAB file
        # Used only for PhoServerFormat:
        phoServerFormatArgs = None

        if usePhoServerFormat:
            (
                phoServerFormatArgs,
                dateTimes,
                onesEventFormatDataArray,
            ) = LabjackEventsLoader.loadLabjackDataFromPhoServerFormat(
                labjackFilePath, shouldUseStdOutFormat=phoServerFormatIsStdOut
            )

        else:
            (
                dateNums,
                dateTimes,
                onesEventFormatDataArray,
            ) = LabjackEventsLoader.loadLabjackDataFromMatlabFormat(labjackFilePath)

        return (dateTimes, onesEventFormatDataArray, phoServerFormatArgs)

    ## Data Export:
    @staticmethod
    def writeLinesToCsvFile(lines, filePath="data/output/LabjackDataExport/output.csv"):
        # Open a text file to write the lines out to
        with open(filePath, "w", newline="") as csvfile:
            csvfile.write(
                ", ".join(LabjackEventsLoader.labjack_csv_variable_names) + "\n"
            )
            for aLine in lines:
                csvfile.write(aLine.replace(":", ","))
            csvfile.close()

    @staticmethod
    def loadAndConcatenateLabjackDataFromPhoServerFormat(filePaths):
        combinedFileLines = []
        for (fileIndex, aFilePath) in enumerate(filePaths):
            (
                relevantFileLines,
                relevantDateTimes,
                dateTimes,
                onesEventFormatDataArray,
            ) = LabjackEventsLoader.loadLabjackDataFromPhoServerFormat(aFilePath)
            combinedFileLines = np.append(combinedFileLines, relevantFileLines)
        combinedFileLines = np.unique(combinedFileLines)
        numRelevantLines = len(combinedFileLines)
        print(numRelevantLines)
        return combinedFileLines

    @staticmethod
    def writeRecordsDataframeToCsvFile(
        records_dataframe, filePath="results/export.csv"
    ):
        records_dataframe.to_csv(filePath)

    """
        Builds a records dataframe out of the list of labjackEventRecords
    """

    @staticmethod
    def build_records_dataframe(labjackEventRecords):
        # Build the records dataframe from the labjackEventRecords
        records_dataframe = pd.DataFrame.from_records(
            [s.to_dict() for s in labjackEventRecords]
        )

        # Filters the records_dataframe to only the relevant fields that we'd want to export.
        ## Choose just the columns we care about. See https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
        # https://stackoverflow.com/questions/38231591/splitting-dictionary-list-inside-a-pandas-column-into-separate-columns
        # https://stackoverflow.com/questions/34997174/how-to-convert-list-of-model-objects-to-pandas-dataframe/41762270

        # pd.concat([in_records_df.drop(['b'], axis=1), in_records_df['b'].apply(pd.Series)], axis=1)
        # final_out_df = pd.concat([in_records_df[['start_date', 'end_date', 'variable_name']], in_records_df.extended_info_dict.apply(pd.Series)[['event_type', 'dispense_type', 'port']]], axis=1)
        return pd.concat(
            [
                records_dataframe[["start_date", "variable_name"]],
                records_dataframe.extended_info_dict.apply(pd.Series)[
                    ["event_type", "port"]
                ],
            ],
            axis=1,
        )
