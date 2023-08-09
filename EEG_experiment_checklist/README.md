# EEG experiment checklist
## Before the Experiment
- [] Tell your participants to wash their hair, best on the day of the experiment, and to not use any other hair products (i.e. conditioner; oil etc.).
- [] Remember to explain the process to the participants, including that they will need to wash their hair afterwards (and that we have everything).
- [] Arrive at least 15 minutes prior to meeting a participant at the lab. (Keep an eye on incoming calls/messages if e.g. a participant can't find the lab.)
### Preparation for ...
#### ... subject:
- [] Lay out 'data privacy policy', 'informed consent', 'participant information', and 'remuneration' forms together with a pen.
- [] Center chair for subject in front of the screen.
- [] Position screen correctly.
- [] Clean sink in bathroom.
- [] EEG Caps, cape (gel protection), paper towels.
- [] 'EEG measurement' box in lab with: EEG gel, syringes + orange tips, measuring tape, ear clip holder for ground electrode, alcohol pads, adhesive tape, attachment rings for EOG electrodes.
#### ... acquiring EEG data
**EEGL: Impedance measurement**
- [] Power on amplifier and connect to EEGL.
- [] Switch off power strip (for EEGL, Amp, and desk → on left side of table on floor) and
disconnect the power cable from the amplifier and EEGL! (otherwise there's a lot of 50 Hz
noise).
- [] Start 'eego LSL App' (=ANT recorder):
    Windows:
        - Desktop folder: recorder > ANT-recorder
        - Record 64 channel EEG: double click 'ANT_RecordData.exe' and select 'waveguard64.txt.' (Hint for gel application: in this case the white and green electrodes are used.)
        - [Record bipolar channels only (e.g. for test purposes with photoresistor): double click 'ANT_BIPonly.exe' and select 'bip1_only.txt']
        - Screen for impedance measurement should be up.
    or Ubuntu:
        - "$ cd build-eegosport-Desktop-Release" ($ means that this is a terminal command!)
        - "$ sudo ./eegosport"
        - select 'waveguard64_Imp.txt'
        - Screen for impedance measurement should be up.
**RecL: Recording and supervision**
- [] Open: LSL Viewer, LSL Recorder, "$ lsl_status"
- [] Open 'gucview' for webcam - here: go to 'video controls', select 'general webcam' (1st option) as device, and click 'restart' in pop-up.
**StimPC: Matlab**
- [] Open "$ matlab"
- [] Set parameters for small example run with participant.
- [] Check if parameters for experiment are correct (or can be quickly changed to if you do an example run).
- [] Check if button box works.
## Pick up subject from building entrance
- [] [Ask participant if they did a Covid test, otherwise provide them with a self-test and let them do it upstairs.]
- [] Explain 'data privacy policy' and 'informed consent' and let them sign the forms. (→ Move signed forms to dedicated folder in lab for storage.)
- [] Fill out 'participant information' form.
## Perform eyesight test with subject
*Website*: http://www.openoptometry.com/OTC.html
- [] Settings:
    - [] Chart type: Snellen
    - [] Optotype: [6] Landolt C's
    - [] Viewing Preference: [w] Line
    - [] Measure calibration line on bottom left and set the corresponding value.
    - [] Measure monitor distance and set the corresponding value.
    - [] Visual acuity (right side of screen): 6/6 (0.0)
- [] Let participants determine opening of Landolt C's. Should have at least 4/5 correct (it's better to repeat the test in this case).
## Prepare subject for EEG measurement
- [] Let subject put on cape (to protect clothes from gel), get seated comfortably on chair, and adjust chair height.
- [] Measure head circumference → S, M or L cap?
- [] Put on EEG cap in correct size and align it following the 10-20 International System:
    - Place Cz electrode on intersection between craniometric reference points using a measuring tape:
        - left-right: left (PAL) and right (PAR) preauricular points
        - front-back: nasion (NS) and insion (IN)
- [] Attach GRD + EOG electrodes:
    - [] Clean skin at electrode position(s) with alcohol pad.
    - [] Attach GRD electrode to left ear with ear clip holder.
    - [] Attach EOG electrodes above (VEOGU) and below (VEOGL) the left eye, left of left eye (HEOGL) and right of eye (HEOGR), on corresponding midlines of the eyes with attachment rings.
- [] Apply EEG gel with syringe (10 ml + orange tip) and wiggle until impedance is <10 Ohm (green) at every electrode in 'eego LSL App'.
    - Tips: Start with reference (CPz) and GRD electrodes. Apply gel to all electrodes first, then start wiggling.
*During preparation don't forget to talk to the participant! It can be incredibly boring/ annoying to sit there while someone is scrubbing your head.*

*If the participant is not really social it's always a good idea to talk to your prep-partner.*

*And always remember: A happy participant is a good participant!*
## Explain experiment to subject in detail
(Explanation of the experiment can of course be done during the previous step.)
- [] Set up small portion of experiment (e.g. 2 blocks of 20 trials) as an example to run through with subject and make sure the task is clearly understood:
- [] Present experiment instructions on screen via Matlab on StimPC.
- [] Run example.
- [] Answer all questions of subject throughout and after example run.

If subject is ready to start the experiment, go to the next step.
## Run experiment
- [] Turn on the 'Versuch läuft' sign outside the lab.
- [] Set room lighting with 'Osram BT control' App.

**EEGL: Start sending data (in 'eego LSL App')**
- [] Select sampling rate. (We used 1000 Hz.)
- [] Click 'Stream EEG to LSL'.
- [] Click 'Ok' in pop-up window (!)
- [] Check if recording works in 'Brainvision LSL Viewer' (Windows) or 'LSL viewer' (Linux):
    - [] Connect amplifier (only in 'Brainvision LSL Viewer').
    - [] Demonstrate to subject how artefacts are produced (e.g. muscle artefacts through jaw clenching or head rotation, eye movement, blinks, maybe heart rate artefacts are visible in some channels, ...
- [] Close the door between the two rooms.

→ Start recording on RecL.

**RecL: Receive data via LSL and save together with triggers**
- [] Check if data (EEGL) & triggers (EEGL+StimPC) are received:
    - [] "$ lsl_status" and 'LSL Viewer'
- [] Start 'LSL Recorder' from desktop. Here:
    - [] Set Study Root to '/home/recorder/projects/2022-projectName'
    - [] Set Run, Participant, and Session.
    - [] Are 'LSL_Markers_matlab(StimPC)', 'eegoSports-EE225_markerMarkers(CCSEEGLaptop), and 'EEGStream EE225(CCS-EEGLaptop)' green?
    - [] Click 'Start' and Confirm.

→ Start experiment in Matlab (StimPC).

**StimPC: Present experiment**
- [] Run main experimental script with correct parameters after everything else is set up and recording is started on RecL.

**During experiment**
- Check LSL stream (EEG data, trigger) and responses regularly.
- Communication with subject via interphone system or written (Matlab).
## End recording
1. StimPC: 
    - [] Matlab script terminates by itself or terminate manually (e.g. press 'q' to quit, Ctrl+C, ...).
2. RecL:
    - [] Click 'Stop' in 'LSL Recorder' to stop recording data.
3. EEGL:
    - [] Click 'Stop EEG Stream' in 'eego LSL App' to stop streaming data.
    - [] Click 'Done' (green button, bottom right) before you exit the software.
## Finish experiment
- [] Take off EEG cap.
- [] Guide subject to the bathroom, bring keys and black chair.
- [] Give subject a towel and show where to find shampoo and hair dryer. Show functions of water tap.
- [] Hang 'In Benutzung für Studie' sign outside the bathroom door.
- [] Let lab door open so subject easily finds room again.
- [] (Participants responded very well to going through behavioral results of the experiment together.)
- [] Let participant fill out feedback form.
- [] Give participant payment for study and let them sign 'remuneration' form, that they received it.
- [] If everything is completed, guide the subject back to the building entrance and thank them for participating.
- [] Tidy up the lab. Put everything back where it belongs.
- [] Thoroughly wash EEG Cap with oral irrigator and syringes. Keep cable connectors dry at all time!
- [] Disinfect table and button box 'Bacillol AF' (no need for dilution).
- [] Disinfect participant's chair with 'Cosimed' (no need for dilution).
- [] Disinfect EEG Cap with 'pursept AF'. Dilute:
    - [] Wear protective gloves.
    - [] Adapt the concentration to the time between participants: 0.5% for 1h, 1% for 30 min, 2% for 15 min of contact time.
    - [] 0.5% (1%, 2%) solution: Measure 5 ml (10ml, 20ml) of disinfectant in small measuring beak. Add it to big measuring beak and fill up to 2 l with water. Keep the cap submerged for 15 min.
    - [] Rinse the cap again.

- The caps take around 4 hours to dry. If participants are scheduled with less pause, use the ventilator to dry the cap (takes around 15-20 min). Otherwise let it dry on styrofoam head.
- Charge Amplifier and EEGL.
- Wash towels in regular intervals.
## Troubleshoot
EEGL:
- Is amplifier connected to EEGL and running? Sometimes the connection breaks when slightly touching the cable - try to unplug and replug.
- If there is a lot of noise in the signal in 'LSL viewer': Is amplifier power cable disconnected?
- Is Wifi working? May use ethernet.
- Forgot to press 'Done' in 'eego LSL App'? Go to task manager and end process 'ANT_recordData.exe', then you can open the software and record again.
RecL:
- No data is received:
    - Forgot to click 'Ok' in pop-up window on EEGL (6.1.3)?
    - Check all internet connections! If USB Ethernet isn't working reattach USB-Hub.
StimPC:
- Check stimulus monitor refresh rate: "$ DISPLAY=:0.1 xrandr &"
    - Change to 390 Hz: "$ DISPLAY=:0.1 xrandr --output DisplayPort-3 --mode 1920 x 1080 --rate 390.30"
If nothing works - reboot :)
## In case of emergency
Phone numbers for all cases are on a note next to the phone.