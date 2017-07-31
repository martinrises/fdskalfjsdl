target_file = open("labeled_daily_price.csv", 'w')
with open("daily_price.csv", "r") as src_file:
	lines = src_file.readlines()
	# ,open,close,high,low,total_turnover,volume
	keys = lines[0].strip().split(',')
	date_ix = keys.index("date")
	open_ix = keys.index("open")
	close_ix = keys.index("close")
	high_ix = keys.index("high")
	low_ix = keys.index("low")
	turnover_ix = keys.index("total_turnover")
	volume_ix = keys.index("volume")
	print("date = {}, open = {}, close = {}, high = {}, low = {}, turnover = {}, volume = {}".format(date_ix, open_ix, close_ix, high_ix, low_ix, turnover_ix, volume_ix))