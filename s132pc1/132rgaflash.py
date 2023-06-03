import pyrga
import time
from epics import caget,caput

if __name__ == "__main__":
# initialize client with non-default noise floor setting
	RGA = pyrga.RGAClient("COM9", noise_floor=4)
# check filament status and turn it on if necessary
	RGA.turn_on_filament()
	RGA.set_cdem_voltage(0)	
	print(RGA.get_emission_current(),RGA.get_cdem_voltage())
	time.sleep(7)
	RGA.turn_off_filament()
	print(RGA.get_emission_current(),RGA.get_cdem_voltage())

					





