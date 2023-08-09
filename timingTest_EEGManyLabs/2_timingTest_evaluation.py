# Config

USE_XDF = True # True if LSL is used for recording
PHOTOSENSOR = 'Bipolar0' # set channel name for photosensor

filepath = './'
filename = 'sub-005_ses-001_task-Default_run-003_eeg.xdf'

##### Change only if USE_XDF is true!
LSL_MARKERS = True
LPT_MARKERS = False
# You have to decide whether you want LSL or LPT makers?
assert not (LSL_MARKERS and LPT_MARKERS)
# Define only if XDF is used
# Use None for a marker stream you did not record
XDF_eegstreamname = "EEGstream EE225"
XDF_LPTmarkerstreamname = "eegoSports-EE225_markersMarkers" # None
XDF_LSLmarkerstreamname = "LSL_Markers" # None

#%% Import
import os
import matplotlib.pyplot as plt
import numpy as np
import mne
from mnelab.io.xdf import read_raw_xdf
from pyxdf import match_streaminfos, resolve_streams

#%% Functions
def import_eeg(filename,filepath="."):
    fullfile = os.path.join(filepath,filename)
    print("Trying to import file: "+fullfile)
    raw = mne.io.read_raw(fullfile)
    
    return raw

def import_eeg_xdf(filename,filepath=".", eegstreamname = None):
    fullfile = os.path.join(filepath,filename)
    # Get streams
    streams = resolve_streams(fullfile)
    ix_eeg = match_streaminfos(streams, [{"name": eegstreamname}])[0]
    nominal_eeg_srate = [s["nominal_srate"] for s in streams if s["stream_id"]==ix_eeg][0]
    # Create raw object
    raw = read_raw_xdf(fullfile, stream_ids=[ix_eeg], prefix_markers=True,fs_new=nominal_eeg_srate)

    return raw

def extract_triggers(raw):
    return mne.events_from_annotations(raw)[0]

def extract_triggers_XDF(raw,XDF_LPTmarkerstreamname = None, XDF_LSLmarkerstreamname=None):
    streams = resolve_streams(raw.filenames[0])

    if XDF_LPTmarkerstreamname:
        ix_lpt_markers = match_streaminfos(streams, [{"name": XDF_LPTmarkerstreamname}])[0]
    if XDF_LSLmarkerstreamname:
        ix_lsl_markers = match_streaminfos(streams, [{"name": XDF_LSLmarkerstreamname}])
    
    # Events
    events_lpt, _ = mne.events_from_annotations(raw, regexp='^'+str(ix_lpt_markers),event_id=lambda x:int(x.split("@")[0].split("-")[1]))
        
    # Dejitter markers - old code, not working!
    #ix = np.arange(0, raw.n_times, 1)[:, None]
    #X = np.concatenate((np.ones_like(ix), ix), axis=1)
    #y = raw.times[ix]
    #coef = np.linalg.lstsq(X, y)[0]
    ##raw.times[ix] = mapping[0] + mapping[1] * ix 
    
    if XDF_LSLmarkerstreamname:
        if len(ix_lsl_markers)!=1:
            # It can happen that we have multiple LSL streams in our XDF - this tries to find the one that actually has data in it
            for i in ix_lsl_markers[0:-1]:
                try:
                    events_lsl, _ = mne.events_from_annotations(raw, regexp='^'+str(ix_lsl_markers))
                    ix_lsl_markers = ix_lsl_markers[i]
                    break
                except ValueError:
                    pass
        else:
            events_lsl, _ = mne.events_from_annotations(raw, regexp='^'+str(ix_lsl_markers[0]))
        
        events_lsl[:,2] = events_lsl[:,2] + 10000
        events_lpt = np.append(events_lpt,events_lsl,axis=0)
        
    return events_lpt

#%% Get streams
if USE_XDF:
    raw = import_eeg_xdf(filename,filepath,XDF_eegstreamname)
    events = extract_triggers_XDF(raw,XDF_LPTmarkerstreamname,XDF_LSLmarkerstreamname)
else:
    raw = import_eeg(filename,filepath)
    events = extract_triggers(raw)

#%% Plot first 60 seconds of photosensor data
sfreq = raw.info['sfreq']
start_stop_seconds = np.array([0, 60])
start_sample, stop_sample = (start_stop_seconds * sfreq).astype(int)

# Extract photosensor channel by name
raw_selection = raw[PHOTOSENSOR, start_sample:stop_sample]

# Plot raw data
t = raw_selection[1]
signal = raw_selection[0].T
plt.figure(1)
plt.plot(t, signal)
plt.title("raw photosensor data")
plt.xlabel("time [s]")
plt.ylabel("signal")

#%% Events
mne.viz.plot_events(events, raw.info['sfreq'])

# Assert that 1000 on & 1000 off triggers are in each marker stream
if USE_XDF:
    assert len(events[:,2]) == 4000
else:
    assert len(events[:,2]) == 2000

#%% Check drift
if USE_XDF and XDF_LPTmarkerstreamname and XDF_LSLmarkerstreamname:
    lpt_markers = events[events[:,2] < 10000]
    lsl_markers = events[events[:,2] > 10000]
    # Plot the two trigger channels against each other
    plt.figure(2)
    diff = np.subtract(lpt_markers[:,0],lsl_markers[:,0])
    plt.plot(diff)
    plt.title("check drift")
    plt.xlabel("marker")
    plt.ylabel("diff signal")

#%% Epoch
epochs = mne.Epochs(
    raw,
    events,
    event_id = 1 if LPT_MARKERS else 10001,#[1,10001],
    tmin = -0.005,
    tmax = 0.05,
    baseline=None,
    preload=True)

epochs.plot_image()

epochs_df = epochs.to_data_frame()

#%% Analyse timings
# Restrict data to 5-95 % of range between max and min for robustness against outliers
data_max = max(epochs_df['Bipolar0']) * 0.95
data_min =  min(epochs_df['Bipolar0']) + abs(max(epochs_df['Bipolar0']) - min(epochs_df['Bipolar0'])) * 0.05
range_minmax = abs(data_max-data_min)

# Thresholds at 10% and 75%
threshold10 = data_min + range_minmax * 0.1
threshold75 = data_min + range_minmax * 0.75

# Function to find supra-threshold indices
def supraThresh(epochs_df,threshold):
    supraThresh = [ix for ix, val in enumerate(epochs_df['Bipolar0']) if val > threshold]
    return supraThresh

# RTs -------------------------------------------------
# Reaction time (= monitor input lag)
reactionTimes = [supraThresh(epochs_grouped,threshold10)[0] for ix, epochs_grouped in epochs_df.groupby(['epoch'])]
valsInEpochBeforeZero = epochs_df[epochs_df.time == 0].index[0]
reactionTime = np.subtract(np.mean(reactionTimes),valsInEpochBeforeZero)/sfreq

# Reponse time
responseTimes = [supraThresh(epochs_grouped,threshold75)[0] for ix, epochs_grouped in epochs_df.groupby(['epoch'])]
responseTime = np.subtract(np.mean(responseTimes),valsInEpochBeforeZero)/sfreq

# Raise time
raiseTime = responseTime - reactionTime

# Stimulus duration --------------------------------------
# = first to last value above 75 % threshold
stimDurSamples = [supraThresh(epochs_grouped,threshold75) for ix, epochs_grouped in epochs_df.groupby(['epoch'])]
stimDur = [len(col) for col in stimDurSamples]
stimStart = np.mean(np.subtract([col[0] for col in stimDurSamples],valsInEpochBeforeZero))/sfreq
meanDuration = np.mean([len(col) for col in stimDurSamples])
medianDuration = np.median([len(col) for col in stimDurSamples])

# Plot
plt.figure(3,dpi=250)
epochs_df.set_index('time').groupby('epoch')['Bipolar0'].plot(color="gray", linewidth=0.1)
epochs_df.set_index('epoch').groupby('time')['Bipolar0'].agg(lambda x: np.mean(x.values.tolist(), axis=0)).plot(color="black", linewidth=2)
h_thresh10 = plt.axhline(threshold10, color="palegreen", linewidth=1.5, label='threshold 10%')
h_thresh75 = plt.axhline(threshold75, color="forestgreen", linewidth=1.5, label='threshold 75%')
plt.axvline(0, color="black", linewidth=1, label='trigger')
plt.axvline(reactionTime, color="black", linewidth=1)
plt.axvline(responseTime, color="black", linewidth=1)
h_reactiontime = plt.hlines(y=data_max, xmin=0, xmax=reactionTime, color="skyblue", label='reaction time: '+str(round(reactionTime*sfreq,2))+' ms')
h_raiseTime = plt.hlines(y=data_max-range_minmax*0.1, xmin=reactionTime, xmax=responseTime, color="aqua", label='raise time: '+str(round(raiseTime*sfreq,2))+' ms')
h_responsetime = plt.hlines(y=data_max-range_minmax*0.2, xmin=0, xmax=responseTime, color="blue", label='response time: '+str(round(responseTime*sfreq,2))+' ms')
h_stimDur = plt.hlines(y=data_max-range_minmax*0.235, xmin=stimStart, xmax=stimStart+meanDuration/sfreq, color="crimson", label='stimulus duration: '+str(round(meanDuration,2))+' ms')
plt.title("switch black2white")
plt.xlabel("time [s]")
plt.ylabel("signal")
plt.legend(handles = [h_reactiontime, h_raiseTime, h_responsetime, h_stimDur, h_thresh75, h_thresh10], bbox_to_anchor=(1,1))

# Plot stimulus duration histogram
plt.figure(4,dpi=250)
plt.hist(stimDur, bins=10)
plt.axvline(meanDuration, color="red", linewidth=0.8)
plt.axvline(medianDuration, color="yellow", linewidth=0.8)
plt.title("histogram of stimulus durations")
plt.xlabel("duration [ms]")
plt.ylabel("number of stimuli")
plt.legend(["mean: "+str(round(meanDuration,2)),"median: "+str(round(medianDuration,2))], loc="upper left")
