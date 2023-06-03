import pyrga
if __name__ == "__main__":
# initialize client with non-default noise floor setting
	RGA = pyrga.RGAClient("COM9", noise_floor=4)
	RGA.turn_off_filament()