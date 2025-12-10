
## Requirements:
VLC 3.0.8 Vetinari (64-bit)

The application uses a portable VLC installation located at `external/vlc-portable/`. This ensures version compatibility and prevents conflicts with system-installed VLC.

### Installing VLC Portable:

**Automatic Installation (Recommended):**
```bash
python scripts/download_vlc.py
```

This script will:
- Download VLC 3.0.8 64-bit portable from VideoLAN's official repository
- Extract it to `external/vlc-portable/`
- Verify the installation

**Manual Installation:**
If automatic download fails, you can manually download VLC 3.0.8 64-bit portable from:
https://download.videolan.org/pub/videolan/vlc/3.0.8/win64/vlc-3.0.8-win64.zip

Extract the ZIP file and place the contents in `external/vlc-portable/` such that `external/vlc-portable/libvlc.dll` exists.

**Note:** The portable VLC installation is automatically detected and used by the application. No system-wide VLC installation is required.

(Py3PyQt5)

# Creating an Environment:
conda create -n PyQt6
conda activate PyQt6

mamba install orange-canvas-core PyQt configparser QtAwesome orange-canvas-core pillow av ffmpeg pyqtgraph qtmodern matplotlib numpy scipy pandas opencv ffmpeg sqlalchemy h5py pip -c conda-forge

## --OR-- (If mamba isn't installed, much slower):
conda install -c conda-forge orange-canvas-core PyQt configparser QtAwesome orange-canvas-core pillow av ffmpeg pyqtgraph qtmodern matplotlib numpy scipy pandas opencv ffmpeg sqlalchemy h5py pip

# pip requirements:
pip install opencv-python



# Old:
## Installing from Environment:
1. Open up Admin CMD Prompt
2. cd C:\Users\Administrator\repo\PhoPyQtTimelinePlotter
3. ? conda config --set ssl_verify no
3. ? conda config --show channels
3. ? conda config --append channels conda-forge
4. conda update conda
5. conda update anaconda
6. conda env create -f "EXTERNAL\Requirements\06-01-2020\environment_no_builds.yml"
7. conda activate Py3PyQt5
### Spec-File:
conda list --explicit > EXTERNAL\Requirements\06-01-2020\spec-file.txt
### Installing from Spec-file:
conda create --name Py3PyQt5New --file EXTERNAL\Requirements\06-01-2020\spec-file.txt
C:\Users\Administrator\repo\PhoPyQtTimelinePlotter\EXTERNAL\Requirements\06-01-2020\environment_no_builds.yml

###  Making a clone:
conda create --name Py3PyQt5_Testing --clone Py3PyQt5


## Hierarchy:

## app/filesystem/FilesystemRecordBase.py
# FilesystemRecordBase: an attempt to make a "record" like object for events loaded from filesystem files analagous to the records loaded from the database
# FilesystemLabjackEvent_Record: for labjack events loaded from a labjack data file

## app/filesystem/LabjackEventsLoader.py
# LabjackEventType
# LabjackEventsLoader
#   from phopyqttimelineplotter.app.filesystem.FilesystemRecordBase import FilesystemRecordBase, FilesystemLabjackEvent_Record

## app/filesystem/LabjackFilesystemLoadingMixin.py
# LabjackFilesystemLoader: this object tries to find Labjack-exported data files in the filesystem and make them accessible in memory
    # load_labjack_data_files(...): this is the main function that searches the listed paths for labjack data files, and then loads them into memory.
# LabjackEventFile: a single imported data file containing one or more labjack events.
#   from phopyqttimelineplotter.app.filesystem.LabjackData.LabjackEventsLoader import LabjackEventsLoader, PhoServerFormatArgs
#   from phopyqttimelineplotter.app.filesystem.FilesystemRecordBase import FilesystemRecordBase, FilesystemLabjackEvent_Record





## GUI/TimelineTrackWidgets/TimelineTrackDrawingWidget_DataFile.py


## GUI/Model/TrackConfigs/DataFileTrackConfig.py


## Loading Videos:
