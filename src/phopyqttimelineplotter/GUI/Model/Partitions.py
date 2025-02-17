import sys
from datetime import datetime, timedelta, timezone

import numpy as np
from phopyqttimelineplotter.app.database.entry_models.db_model import (
    CategoricalDurationLabel,
    Context,
    Subcontext,
)
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
    QVBoxLayout,
)

from phopyqttimelineplotter.GUI.Model.Events.PhoDurationEvent import PhoDurationEvent
from phopyqttimelineplotter.GUI.Model.Events.PhoDurationEvent_Partition import (
    PhoDurationEvent_Partition,
)
from phopyqttimelineplotter.GUI.Model.Events.PhoEvent import PhoEvent
from phopyqttimelineplotter.GUI.Model.ModelViewContainer import ModelViewContainer
from phopyqttimelineplotter.GUI.UI.AbstractDatabaseAccessingWidgets import (
    AbstractDatabaseAccessingQObject,
)

# """
# Represents a partition
# """
# class PartitionInfo(QObject):
#     def __init__(self, name='', start_pos=0.0, end_pos=1.0, extended_data=dict()):
#         super(PartitionInfo, self).__init__(None)
#         self.name = name
#         self.start_pos = start_pos
#         self.end_pos = end_pos
#         self.extended_data = extended_data

#     def __eq__(self, otherEvent):
#         return self.name == otherEvent.name and self.start_pos == otherEvent.start_pos and self.end_pos == otherEvent.end_pos

#     # Less Than (<) operator
#     def __lt__(self, otherEvent):
#         return self.start_pos < otherEvent.start_pos

#     def __str__(self):
#         return 'Event {0}: start_pos: {1}, end_pos: {2}, extended_data: {3}'.format(self.name, self.start_pos, self.end_pos, str(self.extended_data))


"""
Each Partition Track has a Partitioner that manages its partitions.
There's a "partitions" list which represents the model layer and consists of SQLAlchemy database records
The "partitions" track consists of GUI objects.


When a partition timeline is created/loaded:
    Any existing partitions are loaded from the database
    *?- Maybe Start or end times should be None for "open interval" partitions.
        - The partition automatically created is determined by the global start and end times of the timeline that loads. It doesn't contain meaningful information to start.
        - The user should start by partitioning at the start and end of the global data region. The ends will be "non-data regions" or "no-mouse regions"
            - These end partitions can be discarded?
            -best-> ? Perhaps all non-user-labeled regions shouldn't be saved to the database, and should be reconstructed on load.
                - This would mean when there's no data partitions within the timeline (a new database) it would create the a single un-labled partition (as desired).


# If an existing data partition (with an id) is changed to type_id = None or subtype_id = None, the version in the database should be updated too.

New partition objects are created when a timeline



When the user cuts a partition.

    The original partition:
        - It's modified time and modified user are changed

    The new partition:
        - A new database record object is created and added to the database
            - Its creation time and user are set to now


When the user modifies an existing partition:
    The directly modified partition:
        - Both the model and view partition objects are updated. The modifications of the data objects are propigated to the database via .commit()

    Any other adjacent partitions that need to be modified as a result:
        - Adjacent partitions may need to be modified as a result of changing the start or end times of a partition.
        - Only their start or end times will need to be updated


"""


"""
A 0.0 to 1.0 timeline
"""


class Partitioner(AbstractDatabaseAccessingQObject):
    # TODO: Could just use its owning_parent_track's database_connection?
    def __init__(
        self,
        totalStartTime,
        totalEndTime,
        owning_parent_track,
        database_connection,
        name="",
        partitionViews=None,
        partitionDataObjects=None,
        extended_data=dict(),
    ):
        super(Partitioner, self).__init__(database_connection)
        self.totalStartTime = totalStartTime
        self.totalEndTime = totalEndTime
        self.totalDuration = self.totalEndTime - self.totalStartTime
        self.owning_parent_track = owning_parent_track
        self.name = name
        self.partitions = []

        # needs_initialize_partitions = False
        if not (partitionViews is None):
            print(
                "WARNING: Initializing Partitioner from partitionViews is no longer supported!!!!"
            )

        if partitionDataObjects is None:
            partitionDataObjects = []

        # call on_reload_partition_records(...) to build any additional appropriate records (spanning the current timeline) needed and the GUI views
        self.on_reload_partition_records(partitionDataObjects)
        self.extended_data = extended_data

    # Returns a new Partition object (both data and view)
    def create_new_partition(self, startTime, endTime, title, parentContextPair=None):
        # Requires both parent context and parent config to create a new partition. Changing context or config requires a reload
        if parentContextPair is None:
            parentContextPair = self.get_parent_contexts()
            # If parentContextPair is still none even after trying to create it
            if parentContextPair is None:
                print(
                    "Error: Couldn't get parent context pair to create partition!! Aborting"
                )
                return

        parentConfig = self.get_parent_config()
        # If parentContextPair is still none even after trying to create it
        if parentConfig is None:
            print("Error: Couldn't get parent config to create partition!! Aborting")
            return

        # View Object:
        new_partition_view = PhoDurationEvent_Partition(
            startTime, endTime, title, parent=self.owning_parent_track
        )
        new_partition_view.on_edit.connect(
            self.owning_parent_track.on_partition_modify_event
        )

        ## Record Object:
        new_partition_record = CategoricalDurationLabel()
        new_partition_record.start_date = startTime
        new_partition_record.end_date = endTime

        new_partition_record.label_created_date = datetime.now()
        new_partition_record.label_created_user = "Unknown User"
        # Set the last updated properties to the creation properties (since we just created it)
        new_partition_record.last_updated_user = new_partition_record.label_created_user
        new_partition_record.last_updated_date = new_partition_record.label_created_date

        new_partition_record.Context = parentContextPair[0]
        new_partition_record.Subcontext = parentContextPair[1]
        # Since it's not user-labeled, the type and subtype will all be "None"
        new_partition_record.type_id = None
        new_partition_record.subtype_id = None
        new_partition_record.tertiarytype_id = None

        new_partition_record.primary_text = title
        new_partition_record.secondary_text = ""
        new_partition_record.tertiary_text = ""
        new_partition_record.notes = "auto"

        parentFilter = parentConfig.get_filter()

        # Set the id values
        sel_behavioral_box_id, sel_experiment_id, sel_cohort_id, sel_animal_id = (
            None,
            None,
            None,
            None,
        )
        (
            sel_behavioral_box_ids,
            sel_experiment_ids,
            sel_cohort_ids,
            sel_animal_ids,
        ) = parentFilter.get_ids()
        if sel_behavioral_box_ids is not None:
            sel_behavioral_box_id = sel_behavioral_box_ids[0]
        if sel_experiment_ids is not None:
            sel_experiment_id = sel_experiment_ids[0]
        if sel_cohort_ids is not None:
            sel_cohort_id = sel_cohort_ids[0]
        if sel_animal_ids is not None:
            sel_animal_id = sel_animal_ids[0]

        new_partition_record.set_id_values(
            sel_behavioral_box_id, sel_experiment_id, sel_cohort_id, sel_animal_id
        )

        new_partition_obj = ModelViewContainer(
            new_partition_record, new_partition_view, self.owning_parent_track
        )
        return new_partition_obj

    # Builds "Partition" objects containing a reference to both a record and a view
    # Note that setAccessibleName(...) isn't called on objects created by a cut event
    def construct_spanning_unlabeled_partition_records(self, loadedDataPartitions):
        ##TODO: from the loaded partitions records (which only contain the user labeled regions) build the intermediate non-user-labeled partitions (with type and subtype None)
        # print("Partitioner.construct_spanning_unlabeled_partition_records(...)")
        spanning_partition_records = []
        # Construct a partition to span to the start of the first data partition

        if len(loadedDataPartitions) > 0:
            prevPartitionObj = None
            for aDataPartition in loadedDataPartitions:
                # for first partition only
                if prevPartitionObj is None:
                    # It's only None for the first partition in the list
                    if aDataPartition.start_date > self.totalStartTime:
                        # if the first data partition starts later than the first partition, create a partition to fill the gap
                        newPartitionIndex = len(spanning_partition_records)
                        new_partition_obj = self.create_new_partition(
                            self.totalStartTime,
                            aDataPartition.start_date,
                            str(newPartitionIndex),
                        )
                        new_partition_obj.get_view().setAccessibleName(
                            str(newPartitionIndex)
                        )
                        spanning_partition_records.append(new_partition_obj)
                else:
                    # Otherwise we have a valid previous partition
                    if aDataPartition.start_date > prevPartitionObj.end_date:
                        # the current partition starts later than the end of the previous partition, this is unacceptable, and we need to create a partition to fill the gap
                        newPartitionIndex = len(spanning_partition_records)
                        new_partition_obj = self.create_new_partition(
                            prevPartitionObj.end_date,
                            aDataPartition.start_date,
                            str(newPartitionIndex),
                        )
                        new_partition_obj.get_view().setAccessibleName(
                            str(newPartitionIndex)
                        )
                        spanning_partition_records.append(new_partition_obj)
                    elif aDataPartition.start_date == prevPartitionObj.end_date:
                        # This is the expected case
                        pass
                    else:
                        print(
                            "FATAL: the loadedDataPartitions aren't monotonically sorted"
                        )
                        return

                # Add the current record
                # Get the partition object from the record partition object
                newPartitionIndex = len(spanning_partition_records)
                newGuiObject = Partitioner.get_gui_partition(
                    aDataPartition, self.owning_parent_track
                )
                # newGuiObject.on_edit.connect(self.owning_parent_track.on_partition_modify_event)
                # Get new color associated with the modified subtype_id
                # TODO: maybe more dynamic getting of color from parent track?
                # theColor = self.owning_parent_track.behaviors[from_database_partition_record.subtype_id-1].primaryColor.get_QColor()
                newGuiObject.setAccessibleName(str(newPartitionIndex))
                # build the combined partition object
                new_partition_obj = ModelViewContainer(
                    aDataPartition, newGuiObject, parent=self.owning_parent_track
                )
                # Add it to the output array
                spanning_partition_records.append(new_partition_obj)
                # Set the prevPartitionObj reference to the data partition
                prevPartitionObj = aDataPartition

            # Span to the end if needed (we know this list is non-empty)
            lastDataPartition = loadedDataPartitions[len(loadedDataPartitions) - 1]
            if self.totalEndTime > lastDataPartition.end_date:
                # if the last data partition ends sooner than the end of the timeline, create a partition to fill the gap
                newPartitionIndex = len(spanning_partition_records)
                new_partition_obj = self.create_new_partition(
                    lastDataPartition.end_date,
                    self.totalEndTime,
                    str(newPartitionIndex),
                )
                new_partition_obj.get_view().setAccessibleName(str(newPartitionIndex))
                spanning_partition_records.append(new_partition_obj)

        else:
            # create a partition to fill the empty timeline
            newPartitionIndex = len(spanning_partition_records)
            new_partition_obj = self.create_new_partition(
                self.totalStartTime, self.totalEndTime, str(newPartitionIndex)
            )
            if new_partition_obj is None:
                print(
                    "Couldn't create a new default partition, most likely due to invalid parent context!"
                )
                return []

            new_partition_obj.get_view().setAccessibleName(str(newPartitionIndex))
            spanning_partition_records = [new_partition_obj]

        numRecordsAddedToSpan = len(spanning_partition_records) - len(
            loadedDataPartitions
        )
        print(
            "Partitioner.construct_spanning_unlabeled_partition_records(...): {0} records added to span for a total of {1} records".format(
                numRecordsAddedToSpan, len(spanning_partition_records)
            )
        )
        return spanning_partition_records

    # Called by the parent when the partition record objects have be loaded from the database. updates self.partitions
    def on_reload_partition_records(self, loadedDataPartitions):
        print(
            "on_reload_partition_records(loadedDataPartitions: {0})".format(
                len(loadedDataPartitions)
            )
        )
        self.partitions = self.construct_spanning_unlabeled_partition_records(
            loadedDataPartitions
        )
        print(
            "on_reload_partition_records(...): {0} new partitions".format(
                len(self.partitions)
            )
        )

    # Tries to get the context from the owning parent
    def get_parent_contexts(self):
        if self.owning_parent_track is None:
            print("ERROR: owning_parent_track isn't valid!")
            return None

        if not (self.owning_parent_track.trackContextConfig.get_is_valid()):
            print("owning_parent_track context is invalid!")
            return None
        else:
            newContext, newSubcontext = (
                self.owning_parent_track.trackContextConfig.get_context(),
                self.owning_parent_track.trackContextConfig.get_subcontext(),
            )
            return (newContext, newSubcontext)

    # Tries to get the config from the owning parent
    def get_parent_config(self):
        if self.owning_parent_track is None:
            print("ERROR: owning_parent_track isn't valid!")
            return None

        if not (self.owning_parent_track.trackConfig):
            print("owning_parent_track config is invalid!")
            return None
        else:
            return self.owning_parent_track.trackConfig

    def __eq__(self, otherEvent):
        return (
            self.name == otherEvent.name
            and self.totalDuration == otherEvent.totalDuration
        )

    # Less Than (<) operator
    def __lt__(self, otherEvent):
        return self.startTime < otherEvent.startTime

    def __str__(self):
        return "Event {0}: startTime: {1}, partitions: {2}, extended_data: {3}".format(
            self.name, self.partitions, self.color, str(self.extended_data)
        )

    ## TODO: efficiency. Shouldn't use these functions except to replace legacy references to property objects
    ## TODO: self.partitions: should refer to the partition wrapper objects, need to get the views for each of them.
    def get_partition_views(self):
        return [(aPartition.get_view()) for aPartition in self.partitions]

    def get_partition_records(self):
        return [(aPartition.get_record()) for aPartition in self.partitions]

    def get_partitions(self):
        return self.partitions

    ## DONE 11-22-2019 11am: modified to use new dual view/record scheme
    def cut_partition(self, cut_partition_index, cut_datetime):
        # Creates a cut at a given datetime
        partition_to_cut = self.partitions[cut_partition_index]

        parentContextPair = self.get_parent_contexts()
        if parentContextPair is None:
            print("Error: parent context pair is None! Aborting cut!")
            return

        if (
            partition_to_cut.get_view().startTime
            < cut_datetime
            < partition_to_cut.get_view().endTime
        ):
            # only can cut if it's in the appropriate partition.
            # Create a new partition and insert it after the partition to cut. It should span from [cut_datetime, to the end of the cut partition]
            new_partition_index = cut_partition_index + 1
            # Create the new partition object
            new_partition_obj = self.create_new_partition(
                cut_datetime,
                partition_to_cut.get_view().endTime,
                str(new_partition_index),
                parentContextPair,
            )
            self.partitions.insert(new_partition_index, new_partition_obj)

            self.partitions[
                cut_partition_index
            ].get_record().end_date = (
                cut_datetime  # Truncate the partition to cut to the cut_datetime
            )
            self.partitions[
                cut_partition_index
            ].get_view().endTime = (
                cut_datetime  # Truncate the partition to cut to the cut_datetime
            )

            self.save_partitions_to_database()

            return True
        else:
            print(
                "Error! Tried to cut invalid partition! parition[{0}]: (start: {1}, attemptted_cut: {2}, end: {3})".format(
                    cut_partition_index,
                    partition_to_cut.get_view().startTime,
                    cut_datetime,
                    partition_to_cut.get_view().endTime,
                )
            )
            return False

        # The first partition keeps the metadata/info, while the second is initialized to a blank partition

    ## DONE 11-22-2019 11am: modified to use new dual view/record scheme
    # Called when the Partition Edit Dialog returns with an accept message. Called from TimelineTrackDrawingWidget_Partition's try_update_partition(...) function
    def modify_partition(
        self,
        modify_partition_index,
        start_date,
        end_date,
        title,
        subtitle,
        body,
        type_id,
        subtype_id,
        color,
    ):
        partition_to_modify = self.partitions[modify_partition_index]
        if not partition_to_modify:
            print("invalid partition to modify!")
            return
        if not (partition_to_modify.get_view().startTime == start_date):
            # Start time changed
            if modify_partition_index > 0:
                # Get the preceding partition, as it will need to be changed too
                prec_partition_index = modify_partition_index - 1
                prec_partition = self.partitions[prec_partition_index]
                # TODO: Update its end time
                prec_partition.get_view().endTime = start_date
                prec_partition.get_record().end_date = start_date

                prec_partition.get_view().totalDuration = (
                    prec_partition.get_view().endTime
                    - prec_partition.get_view().startTime
                )
                # Note: record object doesn't store duration, doesn't need to be updated

                self.partitions[prec_partition_index] = prec_partition

            partition_to_modify.get_view().startTime = start_date
            partition_to_modify.get_record().start_date = start_date

        if not (partition_to_modify.get_view().endTime == end_date):
            # End time changed
            if modify_partition_index < (len(self.partitions) - 1):
                # Get the following partition, as it will need to be changed too
                foll_partition_index = modify_partition_index + 1
                foll_partition = self.partitions[foll_partition_index]
                foll_partition.get_view().startTime = end_date
                foll_partition.get_record().start_date = end_date
                foll_partition.get_view().totalDuration = (
                    foll_partition.get_view().endTime
                    - foll_partition.get_view().startTime
                )
                # Note: record object doesn't store duration, doesn't need to be updated
                self.partitions[foll_partition_index] = foll_partition
                # TODO: Update its end time

            partition_to_modify.get_view().endTime = end_date
            partition_to_modify.get_record().end_date = end_date

        partition_to_modify.get_view().totalDuration = (
            partition_to_modify.get_view().endTime
            - partition_to_modify.get_view().startTime
        )
        # Note: record object doesn't store duration, doesn't need to be updated

        # Rename it if needed
        if not (partition_to_modify.get_view().name == title):
            partition_to_modify.get_view().name = title

        if not (partition_to_modify.get_record().primary_text == title):
            partition_to_modify.get_record().primary_text = title

        partition_to_modify.get_view().subtitle = subtitle
        partition_to_modify.get_record().secondary_text = subtitle

        partition_to_modify.get_view().body = body
        partition_to_modify.get_record().tertiary_text = body

        if not (partition_to_modify.get_view().type_id == type_id):
            partition_to_modify.get_view().type_id = type_id
        if not (partition_to_modify.get_record().type_id == type_id):
            partition_to_modify.get_record().type_id = type_id

        if not (partition_to_modify.get_view().subtype_id == subtype_id):
            partition_to_modify.get_view().subtype_id = subtype_id
            partition_to_modify.get_view().color = color

        if not (partition_to_modify.get_record().subtype_id == subtype_id):
            partition_to_modify.get_record().subtype_id = subtype_id

        # Update in the array
        self.partitions[modify_partition_index] = partition_to_modify

    @staticmethod
    def create_data_partition(from_gui_partition, contextObj, subcontextObj):
        newPartRecord = CategoricalDurationLabel()
        newPartRecord.start_date = from_gui_partition.startTime
        newPartRecord.end_date = from_gui_partition.endTime

        newPartRecord.label_created_date = datetime.now()
        newPartRecord.label_created_user = "Unknown User"
        # Set the last updated properties to the creation properties (since we just created it)
        newPartRecord.last_updated_user = newPartRecord.label_created_user
        newPartRecord.last_updated_date = newPartRecord.label_created_date

        newPartRecord.Context = contextObj
        newPartRecord.Subcontext = subcontextObj

        newPartRecord.type_id = from_gui_partition.type_id
        newPartRecord.subtype_id = from_gui_partition.subtype_id
        newPartRecord.tertiarytype_id = None

        newPartRecord.primary_text = from_gui_partition.name
        newPartRecord.secondary_text = from_gui_partition.subtitle
        newPartRecord.tertiary_text = from_gui_partition.body
        newPartRecord.notes = "auto"

        return newPartRecord

    @staticmethod
    def get_gui_partition(from_database_partition_record, parent):
        # Get new color associated with the modified subtype_id
        # TODO: maybe more dynamic getting of color from parent track?
        # theColor = parent.behaviors[from_database_partition_record.subtype_id-1].primaryColor.get_QColor()
        # Get new color associated with the modified subtype_id
        # if ((from_database_partition_record.type_id is None) or (from_database_partition_record.subtype_id is None)):
        #     theColor = PhoDurationEvent_Partition.ColorBase
        # else:
        #     theColor = parent.behaviors[from_database_partition_record.subtype_id-1].primaryColor.get_QColor()
        # # theColor = Qt.black
        # outPartitionGuiObj = PhoDurationEvent_Partition(from_database_partition_record.start_date, from_database_partition_record.end_date, \
        #     from_database_partition_record.primary_text, from_database_partition_record.secondary_text, from_database_partition_record.tertiary_text, \
        #         theColor, from_database_partition_record.type_id, from_database_partition_record.subtype_id, {'notes':from_database_partition_record.notes}, parent=parent)
        # outPartitionGuiObj.on_edit.connect(parent.on_partition_modify_event)
        # return outPartitionGuiObj
        return CategoricalDurationLabel.get_gui_view(
            from_database_partition_record, parent
        )

    # # rebuilds the GUI partitions from the set of data partitions. Could be more efficient by reusing existing partitions
    # def rebuild_gui_partitions(self, from_data_partitions):
    #     newPartitionViews = []
    #     for (anIndex, aDataObj) in enumerate(from_data_partitions):
    #         # Create the graphical annotation object
    #         newGuiObject = Partitioner.get_gui_partition(aDataObj, self.owning_parent_track)
    #         # newGuiObject.on_edit.connect(self.owning_parent_track.on_partition_modify_event)

    #         # Get new color associated with the modified subtype_id
    #         # TODO: maybe more dynamic getting of color from parent track?
    #         # theColor = self.owning_parent_track.behaviors[from_database_partition_record.subtype_id-1].primaryColor.get_QColor()

    #         newPartitionIndex = len(self.partitions)
    #         newGuiObject.setAccessibleName(str(newPartitionIndex))

    #         newPartitionViews.append(newGuiObject)

    #     return newPartitionViews

    # Only saves user-labled partitions
    def save_partitions_to_database(self):
        shouldDisableNoneTypeSaves = False
        contextObj, subcontextObj = self.get_parent_contexts()
        print(
            "partitions manager: save_partitions_to_database({0}, {1})".format(
                str(contextObj), str(subcontextObj)
            )
        )
        print("trying to save {0} partition objects".format(len(self.partitions)))

        # Tries to save the active partitions out to the database
        outDataPartitions = []
        for (index, aPartitionObj) in enumerate(self.partitions):
            aDataPartition = aPartitionObj.get_record()
            if aDataPartition.id is None:
                # Never been saved to the database before
                if shouldDisableNoneTypeSaves and (
                    (aDataPartition.type_id is None)
                    or (aDataPartition.subtype_id is None)
                ):
                    # It's not user labled. It shouldn't be added to the database
                    print("skipping item because it's None-type")
                    continue
                else:
                    # It is user labeled and hasn't ever been saved to the database. Add it to the database now
                    outDataPartitions.append(aDataPartition)

            else:
                # Otherwise it's already been saved to the database before (because it was loaded from the database). A .commit() is sufficient to update the changes.
                print(
                    "skipping save because data partition has already been saved to the database!"
                )
                pass

        self.database_connection.save_to_database(
            outDataPartitions, "CategoricalDurationLabel"
        )

        # After saving to the database, we should reload from the database. The parent does this.
        self.owning_parent_track.reloadModelFromDatabase()
        # Should the parent actually do this as opposed to this track?
        self.owning_parent_track.setWindowModified(False)

        ## TODO: this doesn't update the owner's objects (doesn't call owner.reinitialize_from_partition_manager() or owner.update())
        print("done.")
