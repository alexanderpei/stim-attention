from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
import json

stimInfo = StreamInfo('HD-SC_Markers', 'Markers', 1, 0, 'string','HD-SC_Markers')
stimOutlet = StreamOutlet(stimInfo)

print("Looking for stream...")
streams = resolve_stream('name','HD-SC_Markers_out')

inlet = StreamInlet(streams[0])

while True:
	sample, timestamp = inlet.pull_sample()

	if sample:
		stimOutlet.push_shample([sample])