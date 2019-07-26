import csv
import pandas as pd


def export_classified_features(**options):
	# First, load the csv file in memory, this can result in errors (out of memory)!
	df = pd.read_csv(options['features_path'], header=None)

	# Create list from frames
	last_frame = None
	split_categories = list()
	for split_nr in range(0, options['total_splits']):
		if str(split_nr) in options['frames']:
			last_frame = options['frames'][str(split_nr)]
		if last_frame:
			split_categories.append(last_frame['category'] if last_frame and 'category' in last_frame else None)

	# Append to dataframe.
	sc_df = pd.DataFrame({'category': split_categories})
	df = df.join(sc_df)

	# Write to csv file.
	df.to_csv(options['export_path'], header=None, index=False)


def export_separate_classes_per_split(**options):
	last_frame = None
	with open(options['export_path'], 'w', newline='') as handler:
		# Fields: Split Number, Category
		writer = csv.writer(handler)
		for split_nr in range(0, options['total_splits']):
			if str(split_nr) in options['frames']:
				last_frame = options['frames'][str(split_nr)]
			writer.writerow([split_nr, last_frame['category'] if last_frame and 'category' in last_frame else None])


def export_separate_classes_per_frame(**options):
	# Export frames
	with open(options['export_path'], 'w', newline='') as handler:
		fieldnames = ['split', 'time', 'category']
		writer = csv.DictWriter(handler, fieldnames=fieldnames)
		writer.writerows(options['frames'].values())
