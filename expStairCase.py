from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioLib'] = 'ptb'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import pdb
from pylsl import StreamInfo, StreamOutlet
import json
import time
import matplotlib.pyplot as plt

from psychopy.hardware import keyboard

# Outlets
trialInfo = StreamInfo('Trial_Marker', 'Markers', 1, 0, 'string', 'peiPCtrial')
trialOutlet = StreamOutlet(trialInfo)

stimInfo = StreamInfo('HD-SC_Markers_out', 'Markers', 1, 0, 'string','HD-SC_Markers_out')
stimOutlet = StreamOutlet(stimInfo)

jStart = json.dumps({'Action': 4})
jStop  = json.dumps({'Action': 5})

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Prompt for subject info
subID = str(input('Subject ID: '))
blockNum = int(input('Block Number: '))

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'expStairCase'  # from the Builder filename that created this script
expInfo = {'participant': str(subID), 'session': '001'}

expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\Alex\\Documents\\MATLAB\\cmu\\stim_v2\\expStairCase.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Printing stuff
StimSide = ['Left', 'Right']
TargSide = ['Left', 'Right']
SideFrst = ['Left', 'Right']
Stim     = ['Sham', 'True']
Gen      = ['Male', 'Female']
sylList   = ['ba', 'da', 'ga']

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1200, 600], fullscr=False, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "expStart"
expStartClock = core.Clock()
expStartText = visual.TextStim(win=win, name='expStartText',
    text='Press space to begin',
    font='Open Sans',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
expStartKey = keyboard.Keyboard()

# Initialize components for Routine "blockStart"
blockStartClock = core.Clock()
blockStartText = visual.TextStim(win=win, name='blockStartText',
    text='Block 1 of 1\nPress space to begin',
    font='Open Sans',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
blockStartKey = keyboard.Keyboard()

# Initialize components for Routine "trial"
trialClock = core.Clock()
visCueText = visual.TextStim(win=win, name='visCueText',
    text='Test',
    font='Open Sans',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
fixDot = visual.ShapeStim(
    win=win, name='fixDot',
    size=(0.015, 0.015), vertices='circle',
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='white',
    opacity=None, depth=-1.0, interpolate=True)
fixDotBlue = visual.ShapeStim(
    win=win, name='fixDotBlue',
    size=(0.015, 0.015), vertices='circle',
    ori=0.0, pos=(0, 0),
    lineWidth=1.0,     colorSpace='rgb',  lineColor='blue', fillColor='blue',
    opacity=None, depth=-2.0, interpolate=True)
soundStim = sound.Sound('A', secs=-1, stereo=True, hamming=True,
    name='soundStim')
soundStim.setVolume(0)
trialKey = keyboard.Keyboard()

# Initialize components for Routine "blockEnd"
blockEndClock = core.Clock()
blockEndText = visual.TextStim(win=win, name='blockEndText',
    text='End of Block 1\nPress space to begin next block',
    font='Open Sans',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
blockEndKey = keyboard.Keyboard()

# Initialize components for Routine "expEnd"
expEndClock = core.Clock()
expEndText = visual.TextStim(win=win, name='expEndText',
    text='End of experiment! \nPlease stay seated.',
    font='Open Sans',
    pos=(0, 0), height=0.025, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);
expEndKey = keyboard.Keyboard()

# Function to load the stimulus to LSL
def loadStim(iStimSide, iStim, amp, stimOutlet):

    allChan = ['CP2', 'P4', 'PO4', 'P2', 'CP1', 'P3', 'PO3', 'P1']
    chanNum = [1, 2, 3, 4, 9, 10, 11, 12]
    chanR   = ['CP2', 'P4', 'PO4', 'P2']
    chanL   = ['CP1', 'P3', 'PO3', 'P1']

    if iStimSide == 0:
        stimChan = chanL
    elif iStimSide == 1:
        stimChan = chanR 

    if iStim == 0:
        stimSuf = 'sham'
    elif iStim == 1:
        stimSuf = 'true'

    for iChan, chan in enumerate(allChan):
        if chan in stimChan:
            pathWave = os.path.join('C:\\','Users','MxN-33', 'waveforms_steps', str(amp), chan + '_' + stimSuf + '.txt')
            jWaveform = json.dumps({'ChannelNumber': chanNum[iChan], 'Action': 1, 'PathToFile': pathWave})
        else:
            jWaveform = json.dumps({'Action': 2, 'ChannelNumber': chanNum[iChan]})
        stimOutlet.push_sample([jWaveform])

    jDuration = json.dumps({'Action': 7, 'Duration': 10})
    stimOutlet.push_sample([jDuration])

    jFreq = json.dumps({'Action': 7, 'Frequency': 0.1})
    stimOutlet.push_sample([jFreq])

    jRamp = json.dumps({'Action': 7, 'RampUp': 0})
    stimOutlet.push_sample([jRamp])

    jLoad = json.dumps({'Action': 3})
    stimOutlet.push_sample([jLoad])

    return

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "expStart"-------
continueRoutine = True
# update component parameters for each repeat
expStartKey.keys = []
expStartKey.rt = []
_expStartKey_allKeys = []
# keep track of which components have finished
expStartComponents = [expStartText, expStartKey]
for thisComponent in expStartComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
expStartClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "expStart"-------
while continueRoutine:
    # get current time
    t = expStartClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=expStartClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *expStartText* updates
    if expStartText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        expStartText.frameNStart = frameN  # exact frame index
        expStartText.tStart = t  # local t and not account for scr refresh
        expStartText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(expStartText, 'tStartRefresh')  # time at next scr refresh
        expStartText.setAutoDraw(True)
    
    # *expStartKey* updates
    waitOnFlip = False
    if expStartKey.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
        # keep track of start time/frame for later
        expStartKey.frameNStart = frameN  # exact frame index
        expStartKey.tStart = t  # local t and not account for scr refresh
        expStartKey.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(expStartKey, 'tStartRefresh')  # time at next scr refresh
        expStartKey.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(expStartKey.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(expStartKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if expStartKey.status == STARTED and not waitOnFlip:
        theseKeys = expStartKey.getKeys(keyList=['space'], waitRelease=False)
        _expStartKey_allKeys.extend(theseKeys)
        if len(_expStartKey_allKeys):
            expStartKey.keys = _expStartKey_allKeys[-1].name  # just the last key pressed
            expStartKey.rt = _expStartKey_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in expStartComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "expStart"-------
for thisComponent in expStartComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('expStartText.started', expStartText.tStartRefresh)
thisExp.addData('expStartText.stopped', expStartText.tStopRefresh)
# check responses
if expStartKey.keys in ['', [], None]:  # No response was made
    expStartKey.keys = None
thisExp.addData('expStartKey.keys',expStartKey.keys)
if expStartKey.keys != None:  # we had a response
    thisExp.addData('expStartKey.rt', expStartKey.rt)
thisExp.addData('expStartKey.started', expStartKey.tStartRefresh)
thisExp.addData('expStartKey.stopped', expStartKey.tStopRefresh)
thisExp.nextEntry()
# the Routine "expStart" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
block = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='block')
thisExp.addLoop(block)  # add the loop to the experiment
thisBlock = block.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

for thisBlock in block:
    # Skip to a certain block number
    if block.thisRepN + 1 == blockNum:

        trialOutlet.push_sample(['Block : {}'.format(blockNum)])

        blockNum += 1
        currentLoop = block
        # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
        if thisBlock != None:
            for paramName in thisBlock:
                exec('{} = thisBlock[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "blockStart"-------
        continueRoutine = True
        # update component parameters for each repeat
        blockStartKey.keys = []
        blockStartKey.rt = []
        _blockStartKey_allKeys = []
        # keep track of which components have finished
        blockStartComponents = [blockStartText, blockStartKey]
        for thisComponent in blockStartComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        blockStartClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "blockStart"-------
        while continueRoutine:
            # get current time
            t = blockStartClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=blockStartClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # Must pre load the first trial
            pathTrialInfo = os.path.join(os.getcwd(), 'trialInfo', 'StairCase', str(block.thisRepN + 1) + '.csv')

            if frameN == 0:

                trials = data.TrialHandler(nReps=1, method='sequential', 
                    extraInfo=expInfo, originPath=-1,
                    trialList=data.importConditions(pathTrialInfo),
                    seed=None, name='trials')

                thisTrial = trials.trialList[0]

                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))

                loadStim(iStimSide, iStim, 1000, stimOutlet)

            # *blockStartText* updates
            if blockStartText.status == NOT_STARTED and tThisFlip >= 10.0-frameTolerance:
                # keep track of start time/frame for later
                blockStartText.frameNStart = frameN  # exact frame index
                blockStartText.tStart = t  # local t and not account for scr refresh
                blockStartText.tStartRefresh = tThisFlipGlobal  # on global time
                blockStartText.text = 'Block {} of {}\n Press space to continue'.format(block.thisRepN+1, block.nTotal)
                win.timeOnFlip(blockStartText, 'tStartRefresh')  # time at next scr refresh
                blockStartText.setAutoDraw(True)
            
            # *blockStartKey* updates
            waitOnFlip = False
            if blockStartKey.status == NOT_STARTED and tThisFlip >= 10.0-frameTolerance:
                # keep track of start time/frame for later
                blockStartKey.frameNStart = frameN  # exact frame index
                blockStartKey.tStart = t  # local t and not account for scr refresh
                blockStartKey.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blockStartKey, 'tStartRefresh')  # time at next scr refresh
                blockStartKey.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(blockStartKey.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(blockStartKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if blockStartKey.status == STARTED and not waitOnFlip:
                theseKeys = blockStartKey.getKeys(keyList=['space'], waitRelease=False)
                _blockStartKey_allKeys.extend(theseKeys)
                if len(_blockStartKey_allKeys):
                    blockStartKey.keys = _blockStartKey_allKeys[-1].name  # just the last key pressed
                    blockStartKey.rt = _blockStartKey_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in blockStartComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "blockStart"-------
        for thisComponent in blockStartComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        block.addData('blockStartText.started', blockStartText.tStartRefresh)
        block.addData('blockStartText.stopped', blockStartText.tStopRefresh)
        # check responses
        if blockStartKey.keys in ['', [], None]:  # No response was made
            blockStartKey.keys = None
        block.addData('blockStartKey.keys',blockStartKey.keys)
        if blockStartKey.keys != None:  # we had a response
            block.addData('blockStartKey.rt', blockStartKey.rt)
        block.addData('blockStartKey.started', blockStartKey.tStartRefresh)
        block.addData('blockStartKey.stopped', blockStartKey.tStopRefresh)
        # the Routine "blockStart" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        pathTrialInfo = os.path.join(os.getcwd(), 'trialInfo', 'StairCase', str(block.thisRepN + 1) + '.csv')

        trials = data.TrialHandler(nReps=1, method='sequential', 
            extraInfo=expInfo, originPath=-1,
            trialList=data.importConditions(pathTrialInfo),
            seed=None, name='trials')

        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))

        nCorrect = 0
        # firstReversal = False
        currentStim = 300
        allResponse = []
        nReversal = 0
        allReversal = []
        allCurrent = []
        wait = -10
        for thisTrial in trials:

            trialOutlet.push_sample(['Trial : {}'.format(trials.thisTrialN+1)])

            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "trial"-------
            continueRoutine = True
            routineTimer.add(14.800000)
            # update component parameters for each repeat
            soundStim.setSound('A', secs=2.8, hamming=True)
            soundStim.setVolume(0, log=False)
            trialKey.keys = []
            trialKey.rt = []
            _trialKey_allKeys = []
            # keep track of which components have finished
            trialComponents = [visCueText, fixDot, fixDotBlue, soundStim, trialKey]
            for thisComponent in trialComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1
            loadTime = 8
            # -------Run Routine "trial"-------
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = trialClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=trialClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # Print trial info stuff
                if frameN == 0:

                    stimOutlet.push_sample([jStart])
                    stimLoaded = False

                    print('Block: {} | Trial: {}'.format(block.thisRepN + 1, trials.thisTrialN + 1))
                    print('iStimSide: {} | iTargSide: {} | iSideFirst: {} | iStim: {}'.format(iStimSide, iTargSide, iSideFirst, iStim))
                    print('iGen: {} | sylTarg: {} | sylDist: {} | sylCent: {}'.format(iGen, sylTarg, sylDist, sylCent))

                # Load the stimulation for the next trial
                if tThisFlip >= 10.5-frameTolerance and stimLoaded == False:

                    if trials.nRemaining > 0:
                        nextTrial = trials.trialList[trials.thisTrialN+1]

                        for paramName in nextTrial:
                            exec('{}_next = nextTrial[paramName]'.format(paramName))

                        # print('Next')
                        # print('iStimSide: {} | iTargSide: {} | iSideFirst: {} | iStim: {}'.format(iStimSide_next, iTargSide_next, iSideFirst_next, iStim_next))
                        # print('iGen: {} | sylTarg: {} | sylDist: {} | sylCent: {}'.format(iGen_next, sylTarg_next, sylDist_next, sylCent_next))

                        if displayKey == False:
                            # Display response
                            tempStr = ''
                            if len(trialKey.keys) >= 1:
                                nKey = 1
                            else:
                                nKey = 0

                            for i in range(nKey):
                                tempStr = tempStr + trialKey.keys[i]

                            if tempStr == 'down' and iStim == 0:
                                nCorrect += 1
                                allResponse.append('Right') 
                            elif tempStr == 'up' and iStim == 1:
                                nCorrect += 1
                                allResponse.append('Right')
                            elif len(tempStr) == 0:
                                allResponse.append('None')
                            else:
                                allResponse.append('Wrong')


                            print('Response: {} | {} | {}/{}'.format(tempStr, iStimSide, nCorrect, len(trials.trialList)))
                            print(allResponse)

                            displayKey = True

                        if iStim == 1:

                            if allResponse[-1] == 'Wrong':
                                currentStim += 100
                            elif allResponse[-1] == 'Right':
                                currentStim -= 100
                            else:
                                currentStim += 0


                        # if len(allResponse) > 0:

                        #     # No reversal occured yet, single up/down
                        #     if firstReversal == False:

                        #         if allResponse[-1] == False:
                        #             currentStim += 100
                        #         else:
                        #             currentStim -= 100

                        #         # Check for reversal
                        #         if len(allResponse) >= 2:
                        #             if allResponse[-1] != allResponse[-2]:
                        #                 firstReversal = True
                        #                 nReversal += 1
                        #                 allReversal.append(trials.thisTrialN)
                        #                 print('First Reversal')

                        #     # First reversal occured, 2 down 1 up
                        #     elif firstReversal == True:

                        #         # 1 up
                        #         if allResponse[-1] == False:
                        #             currentStim += 100
                        #             # Was reversal?
                        #             if allResponse[-2] == True:
                        #                 nReversal += 1
                        #                 allReversal.append(trials.thisTrialN)
                        #                 print('Reversal: {}'.format(nReversal))

                        #         # 2 down
                        #         elif allResponse[-1] == True and allResponse[-2] == True:
                        #             if wait != trials.thisTrialN - 1:
                        #                 currentStim -= 100
                        #                 wait = trials.thisTrialN

                        #             # Was reversal? 
                        #             if allResponse[-3] == False:
                        #                 nReversal += 1
                        #                 allReversal.append(trials.thisTrialN)
                        #                 print('Reversal: {}'.format(nReversal))

                        allCurrent.append(currentStim)

                        print('Current Stim: {}'.format(currentStim))
                        print()


                        loadStim(iStimSide_next, iStim_next, currentStim, stimOutlet)
                        stimLoaded = True

                # *visCueText* updates
                if visCueText.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                    # keep track of start time/frame for later
                    visCueText.frameNStart = frameN  # exact frame index
                    visCueText.tStart = t  # local t and not account for scr refresh
                    visCueText.tStartRefresh = tThisFlipGlobal  # on global time
                    visCueText.text = TargSide[iTargSide]
                    win.timeOnFlip(visCueText, 'tStartRefresh')  # time at next scr refresh
                    visCueText.setAutoDraw(True)
                if visCueText.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > visCueText.tStartRefresh + 1.0-frameTolerance:
                        # keep track of stop time/frame for later
                        visCueText.tStop = t  # not accounting for scr refresh
                        visCueText.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(visCueText, 'tStopRefresh')  # time at next scr refresh
                        visCueText.setAutoDraw(False)
                
                # *fixDot* updates
                if fixDot.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                    # keep track of start time/frame for later
                    fixDot.frameNStart = frameN  # exact frame index
                    fixDot.tStart = t  # local t and not account for scr refresh
                    fixDot.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixDot, 'tStartRefresh')  # time at next scr refresh
                    fixDot.setAutoDraw(True)
                if fixDot.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > fixDot.tStartRefresh + 4.8-frameTolerance:
                        # keep track of stop time/frame for later
                        fixDot.tStop = t  # not accounting for scr refresh
                        fixDot.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(fixDot, 'tStopRefresh')  # time at next scr refresh
                        fixDot.setAutoDraw(False)
                
                # *fixDotBlue* updates
                if fixDotBlue.status == NOT_STARTED and tThisFlip >= 6.8-frameTolerance:
                    # keep track of start time/frame for later
                    fixDotBlue.frameNStart = frameN  # exact frame index
                    fixDotBlue.tStart = t  # local t and not account for scr refresh
                    fixDotBlue.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(fixDotBlue, 'tStartRefresh')  # time at next scr refresh
                    fixDotBlue.setAutoDraw(True)
                if fixDotBlue.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > fixDotBlue.tStartRefresh + loadTime-frameTolerance:
                        # keep track of stop time/frame for later
                        fixDotBlue.tStop = t  # not accounting for scr refresh
                        fixDotBlue.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(fixDotBlue, 'tStopRefresh')  # time at next scr refresh
                        fixDotBlue.setAutoDraw(False)
                # start/stop soundStim
                if soundStim.status == NOT_STARTED and tThisFlip >= 3-frameTolerance:
                    # keep track of start time/frame for later
                    soundStim.frameNStart = frameN  # exact frame index
                    soundStim.tStart = t  # local t and not account for scr refresh
                    soundStim.tStartRefresh = tThisFlipGlobal  # on global time
                    soundStim.play(when=win)  # sync with win flip
                    trialOutlet.push_sample(['StartSound'])

                if soundStim.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > soundStim.tStartRefresh + 2.8-frameTolerance:
                        # keep track of stop time/frame for later
                        soundStim.tStop = t  # not accounting for scr refresh
                        soundStim.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(soundStim, 'tStopRefresh')  # time at next scr refresh
                        soundStim.stop()
                
                # *trialKey* updates
                waitOnFlip = False
                if trialKey.status == NOT_STARTED and tThisFlip >= 6.8-frameTolerance:
                    # keep track of start time/frame for later
                    trialKey.frameNStart = frameN  # exact frame index
                    trialKey.tStart = t  # local t and not account for scr refresh
                    trialKey.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(trialKey, 'tStartRefresh')  # time at next scr refresh
                    trialKey.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(trialKey.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(trialKey.clearEvents, eventType='keyboard')  # clear events on next screen flip

                    displayKey = False

                if trialKey.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > trialKey.tStartRefresh + loadTime-frameTolerance:
                        # keep track of stop time/frame for later
                        trialKey.tStop = t  # not accounting for scr refresh
                        trialKey.frameNStop = frameN  # exact frame index
                        win.timeOnFlip(trialKey, 'tStopRefresh')  # time at next scr refresh
                        trialKey.status = FINISHED

                if trialKey.status == STARTED and not waitOnFlip:
                    theseKeys = trialKey.getKeys(keyList=['up', 'down'], waitRelease=False)
                    _trialKey_allKeys.extend(theseKeys)
                    if len(_trialKey_allKeys):
                        trialKey.keys = [key.name for key in _trialKey_allKeys]  # storing all keys
                        trialKey.rt = [key.rt for key in _trialKey_allKeys]


                # check for quit (typically the Esc key)
                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # -------Ending Routine "trial"-------
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            trials.addData('visCueText.started', visCueText.tStartRefresh)
            trials.addData('visCueText.stopped', visCueText.tStopRefresh)
            trials.addData('fixDot.started', fixDot.tStartRefresh)
            trials.addData('fixDot.stopped', fixDot.tStopRefresh)
            trials.addData('fixDotBlue.started', fixDotBlue.tStartRefresh)
            trials.addData('fixDotBlue.stopped', fixDotBlue.tStopRefresh)
            soundStim.stop()  # ensure sound has stopped at end of routine
            trials.addData('soundStim.started', soundStim.tStartRefresh)
            trials.addData('soundStim.stopped', soundStim.tStopRefresh)
            # check responses
            if trialKey.keys in ['', [], None]:  # No response was made
                trialKey.keys = None
            trials.addData('trialKey.keys',trialKey.keys)
            if trialKey.keys != None:  # we had a response
                trials.addData('trialKey.rt', trialKey.rt)
            trials.addData('trialKey.started', trialKey.tStartRefresh)
            trials.addData('trialKey.stopped', trialKey.tStopRefresh)
            thisExp.nextEntry()



        # completed 32.0 repeats of 'trials'
        
        
        # ------Prepare to start Routine "blockEnd"-------
        continueRoutine = True
        # update component parameters for each repeat
        blockEndKey.keys = []
        blockEndKey.rt = []
        _blockEndKey_allKeys = []
        # keep track of which components have finished
        blockEndComponents = [blockEndText, blockEndKey]
        for thisComponent in blockEndComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        blockEndClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "blockEnd"-------
        while continueRoutine:
            # get current time
            t = blockEndClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=blockEndClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blockEndText* updates
            if blockEndText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blockEndText.frameNStart = frameN  # exact frame index
                blockEndText.tStart = t  # local t and not account for scr refresh
                blockEndText.tStartRefresh = tThisFlipGlobal  # on global time
                blockEndText.text = 'End of Block {}\nYour accuracy: {:.2f}\nPress space to begin next block'.format(block.thisRepN+1, nCorrect/len(trials.trialList)*100)
                win.timeOnFlip(blockEndText, 'tStartRefresh')  # time at next scr refresh
                blockEndText.setAutoDraw(True)
            
            # *blockEndKey* updates
            waitOnFlip = False
            if blockEndKey.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blockEndKey.frameNStart = frameN  # exact frame index
                blockEndKey.tStart = t  # local t and not account for scr refresh
                blockEndKey.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blockEndKey, 'tStartRefresh')  # time at next scr refresh
                blockEndKey.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(blockEndKey.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(blockEndKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if blockEndKey.status == STARTED and not waitOnFlip:
                theseKeys = blockEndKey.getKeys(keyList=['space'], waitRelease=False)
                _blockEndKey_allKeys.extend(theseKeys)
                if len(_blockEndKey_allKeys):
                    blockEndKey.keys = _blockEndKey_allKeys[-1].name  # just the last key pressed
                    blockEndKey.rt = _blockEndKey_allKeys[-1].rt
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in blockEndComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "blockEnd"-------
        for thisComponent in blockEndComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        block.addData('blockEndText.started', blockEndText.tStartRefresh)
        block.addData('blockEndText.stopped', blockEndText.tStopRefresh)
        # check responses
        if blockEndKey.keys in ['', [], None]:  # No response was made
            blockEndKey.keys = None
        block.addData('blockEndKey.keys',blockEndKey.keys)
        if blockEndKey.keys != None:  # we had a response
            block.addData('blockEndKey.rt', blockEndKey.rt)
        block.addData('blockEndKey.started', blockEndKey.tStartRefresh)
        block.addData('blockEndKey.stopped', blockEndKey.tStopRefresh)
        # the Routine "blockEnd" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 6.0 repeats of 'block'


# ------Prepare to start Routine "expEnd"-------
continueRoutine = True
# update component parameters for each repeat
expEndKey.keys = []
expEndKey.rt = []
_expEndKey_allKeys = []
# keep track of which components have finished
expEndComponents = [expEndText, expEndKey]
for thisComponent in expEndComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
expEndClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "expEnd"-------
while continueRoutine:
    # get current time
    t = expEndClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=expEndClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *expEndText* updates
    if expEndText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        expEndText.frameNStart = frameN  # exact frame index
        expEndText.tStart = t  # local t and not account for scr refresh
        expEndText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(expEndText, 'tStartRefresh')  # time at next scr refresh
        expEndText.setAutoDraw(True)
    
    # *expEndKey* updates
    waitOnFlip = False
    if expEndKey.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        expEndKey.frameNStart = frameN  # exact frame index
        expEndKey.tStart = t  # local t and not account for scr refresh
        expEndKey.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(expEndKey, 'tStartRefresh')  # time at next scr refresh
        expEndKey.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(expEndKey.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(expEndKey.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if expEndKey.status == STARTED and not waitOnFlip:
        theseKeys = expEndKey.getKeys(keyList=['space'], waitRelease=False)
        _expEndKey_allKeys.extend(theseKeys)
        if len(_expEndKey_allKeys):
            expEndKey.keys = _expEndKey_allKeys[-1].name  # just the last key pressed
            expEndKey.rt = _expEndKey_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in expEndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "expEnd"-------
for thisComponent in expEndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('expEndText.started', expEndText.tStartRefresh)
thisExp.addData('expEndText.stopped', expEndText.tStopRefresh)
# check responses
if expEndKey.keys in ['', [], None]:  # No response was made
    expEndKey.keys = None
thisExp.addData('expEndKey.keys',expEndKey.keys)
if expEndKey.keys != None:  # we had a response
    thisExp.addData('expEndKey.rt', expEndKey.rt)
thisExp.addData('expEndKey.started', expEndKey.tStartRefresh)
thisExp.addData('expEndKey.stopped', expEndKey.tStopRefresh)
thisExp.nextEntry()
# the Routine "expEnd" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# Print the current stimulation
allCurrent = np.asarray(allCurrent)
temp = np.diff(allCurrent, 2)
iReversal = np.where(temp != 0)[0] + 1
mean = np.mean(allCurrent[iReversal])

print('Current Stim Mean: {}'.format(mean))

plt.plot(allCurrent)
plt.show()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

