# Config:
# 1) Set monitor refresh rate to 60 Hz
# 2) Set up your marker streams
# 3) At which corner of the screen is the photosensor placed? If lower left corner, continue, else change 'pos' argument for rect1+2
# 4) Run script

#%% Import
from psychopy import core, event
from psychopy.visual import Window, Rect
from pylsl import StreamInfo, StreamOutlet
import serial
import random as rand
#import pyglet

#%% 2) Set up your marker streams

def send_triggers(value):
    """Send value as hardware trigger and LSL marker."""
    outlet.push_sample(value)
    port.write('WRITE {}\n'.format(str(value)[1]).encode())

# Setup LSL
# Create stream info
info = StreamInfo(name="LSL_Markers", type="Markers", channel_count=1,
                  channel_format="int32", source_id="LSL_Markers_00{}".format(rand.randint(1,9)))
# Make an outlet
outlet = StreamOutlet(info)

# Setup ParallelPort
port = serial.Serial("/dev/ttyACM0", baudrate=128000, bytesize=8)

#%% OpenGL

# In the s-ccs setup we have to create our own OpenGL context, otherwise Psychopy doesn't work on the desired screen.
# Uncomment this if you're also running into the ‘pyglet.gl.ContextException: Could not create GL context’

# display = pyglet.canvas.Display(x_screen=1)
# screen = display.get_default_screen()
# template = pyglet.gl.Config()
# config = screen.get_best_config(template)
# context = config.create_context(None)
# window = pyglet.window.Window(context=context)

#%% Settings

BLACK, WHITE = (-1, -1, -1), (1, 1, 1) # stimulus colors

n_trials = 1000 # number of trials
win_size = 1920, 1080  # window size
stim_size = 100, 100  # stimulus size
n_frames = 1  # number of frames: 1 frame at 60 Hz refresh rate is 16 ms

win = Window(size=win_size, fullscr=True, allowGUI = False, color=BLACK,
             units="pix", winType='pyglet', screen=0)

#%% Stimulus position

# Options for stimulus position
LOWER_LEFT = (stim_size[0]/2 - win_size[0]/2, stim_size[1]/2 - win_size[1]/2)
UPPER_LEFT = (stim_size[0]/2 - win_size[0]/2, win_size[1]/2 - stim_size[1]/2)
LOWER_RIGHT = (win_size[0]/2 - stim_size[0]/2, stim_size[1]/2 - win_size[1]/2)
Upper_RIGHT = (win_size[0]/2 - stim_size[0]/2, win_size[1]/2 - stim_size[1]/2)

# 3) Choose where to display the stimulus, i.e. the corner of the monitor where the photosensor is placed
rect1 = Rect(win=win, width=stim_size[0], height=stim_size[1], fillColor=WHITE, pos=LOWER_LEFT)
rect2 = Rect(win=win, width=stim_size[0], height=stim_size[1], fillColor=BLACK, pos=LOWER_LEFT)

#%% Monitor refresh rate

refreshRate = win.getMsPerFrame(nFrames=240) # Get monitor refresh rate

# Stop script if monitor refresh rate is not set to 60 Hz
if refreshRate[2] <  16 or refreshRate[2] >  17:
    print("Refresh rate has to be 60 Hz!")
    win.close()
    core.quit()

#%% Main loop

core.wait(10) # Wait before paradigm starts (has to be that long for us because we loose lsl triggers otherwise)
    
# Send triggers every time an image changes
for i in range(n_trials):
    if event.getKeys(keyList=["escape"]):
        break
    win.callOnFlip(send_triggers, [1])
    for n in range(n_frames):
        rect1.draw()
        win.flip()
    win.callOnFlip(send_triggers, [2])
    for n in range(n_frames):
        rect2.draw()
        win.flip()
    core.wait(0.08+rand.random()/1000*40) # jitter onsets uniform 80-120 ms 

# Close & quit
port.close()
win.close()
core.quit()
