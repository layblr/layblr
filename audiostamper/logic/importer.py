import pandas as pd

from logic.analyse import audio_analyse


async def import_predictions(**options):
	# First, load the csv file in memory, this can result in errors (out of memory)!
	df = pd.read_csv(options['prediction_path'], header=0)

	# Load the audio file in memory, detect the total frames
	audio_info = await audio_analyse(options['audio_path'])
	sample_rate = float(int(audio_info['sample_rate']))
	duration = float(audio_info['duration'])

	total_samples = duration * sample_rate
	total_duration = duration * 1000  # in ms
	samples_per_split = total_samples / len(df)
	duration_per_split = samples_per_split / sample_rate
	duration_per_split = round(duration_per_split * 100) / 100

	# Convert the list to frames
	frames = dict()
	last_pred = None
	for idx, row in df.iterrows():
		if last_pred == row['prediction']:
			continue

		current_duration = duration_per_split * idx
		last_pred = row['prediction']
		frames[idx] = dict(
			split=idx,
			category=row['prediction'],
			time=current_duration,
		)

	return dict(
		frames=frames,
		sample_rate=int(sample_rate),
		total_duration=total_duration,
		total_splits=len(df),
		split_duration=duration_per_split * 1000,
		categories=[str(e) for e in df['prediction'].unique()]
	)
