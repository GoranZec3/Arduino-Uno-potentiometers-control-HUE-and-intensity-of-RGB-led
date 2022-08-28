from numpy import interp
import time
from pyfirmata import Arduino, util

'''
Python 3.1 verion
If you use older verions of Python, code shouldn't work because of 'match - case' syntax
'''
# value for colors range
value_min = 0
value_max = 255

# value for led input
val_write_min = 0
val_write_max = 1

#defining board
board = Arduino('COM3')

#defining pins for RGB
blue_col = board.get_pin('d:3:p')
green_col = board.get_pin('d:5:p')
red_col = board.get_pin('d:6:p')

#defining pins for potentiometers
potentiometer_one = board.get_pin('a:0:i')
potentiometer_two = board.get_pin('a:1:i')

#iteration board
iterator = util.Iterator(board)
iterator.start()
time.sleep(0.1)

try:
    while True:

        pot_one_value = potentiometer_one.read() #read value from potentiometer one
        pot_two_value = potentiometer_two.read()
        #print(pot_one_value)
        round_value_pot_one = round(pot_one_value, 3)  # setting input to 3 decimals
        round_value_pot_two = round(pot_two_value, 2)

        pot_one_float = float(round_value_pot_one)  # converting round_value to float
        pot_two_float = float(round_value_pot_two)  # value which is using to control intensity with second potentiometer
        #print(pot_two_float)


        range_set = interp(pot_one_float, [0,1], [0,255]) #mapping potentiometer value from 0-1 to 0-255
        rgb_range = interp(range_set, [value_min,value_max], [0, 6]) # split range_set values in order to use match func with 6 cases


        gUp = interp(range_set, [0,42], [val_write_min, val_write_max])          # case 0
        rDown = interp(range_set, [43, 84], [val_write_max, val_write_min])      # case 1
        bUp = interp(range_set, [85, 128], [val_write_min, val_write_max])       # case 2
        gDown = interp(range_set, [128, 169], [val_write_max, val_write_min])    # case 3
        rUp = interp(range_set, [170, 212], [val_write_min, val_write_max])      # case 4
        bDown = interp(range_set, [213, 255], [val_write_max, val_write_min])    # case 5


        print('case ' + str(int(rgb_range)))

        #interpolate between cases
        match int(rgb_range):
            case (0):
                green_col.write(round(gUp,2) * pot_two_float) #setting green
                print('gUp value: '+ str(round(gUp,2)))
                red_col.write(1 * pot_two_float)
                blue_col.write(0)
                time.sleep(0.1)
            case(1):
                green_col.write(1 * pot_two_value)
                red_col.write(round(rDown,2) * pot_two_float)
                print('rDown value:' + str(round(rDown,2)))
                blue_col.write(0)
                time.sleep(0.1)
            case(2):
                green_col.write(1 * pot_two_value)
                red_col.write(0)
                blue_col.write(round(bUp,2) * pot_two_float)
                print('bUp value:' + str(round(bUp,2)))
                time.sleep(0.1)
            case(3):
                green_col.write(round(gDown,2) * pot_two_float)
                print('gDown value:' + str(round(gDown,2)))
                red_col.write(0)
                blue_col.write(1 * pot_two_value)
                time.sleep(0.1)
            case(4):
                green_col.write(0)
                red_col.write(round(rUp,2) * pot_two_float)
                print('rUp value: '+ str(round(rUp,2)))
                blue_col.write(1 * pot_two_value)
                time.sleep(0.1)
            case(5):
                green_col.write(0)
                red_col.write(1 * pot_two_value)
                blue_col.write(round(bDown,2) * pot_two_float)
                print('bDown value: '+ str(round(bDown,2)))
                time.sleep(0.1)

except KeyboardInterrupt:
    green_col.write(0)
    red_col.write(0)
    blue_col.write(0)
    board.exit()
