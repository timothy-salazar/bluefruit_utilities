import pigpio
import time
import sys

def main(msg, mode='UART'):
     # MODE = grey, GPIO 27
     MODE = 27
     ###########################################
     # TRANSMIT OUT OF BLUEFRUIT
     # TXO = green, GPIO 09
     TXO = 9
     #    - UART Transmit pin out of the breakout
     # CTS = purple, GPIO 26
     CTS = 26
     #   - Clear to Send hardware flow control pin
     #     into the the breakout. Set low for data
     #     transfer out.
     ############################################
     # TRANSMIT INTO BLUEFRUIT
     # RXI = white, GPIO 04
     RXI = 4
     #    -  UART Receive pin into the breakout
     # RTS = blue, GPIO 17
     RTS = 17
     #    - this is an output pin, it will be low
     #      when it's ok to send data to the bluefruit


     pi = pigpio.pi()
     # CTS SETUP
     ##########################################
     pi.set_mode(CTS, pigpio.OUTPUT)
     pi.write(CTS, 0)
     # MODE SETUP
     #########################################
     pi.set_mode(MODE, pigpio.OUTPUT)
     if mode == "command": pi.write(MODE,1)
     else: pi.write(MODE,0)

     # SERIAL INPUT SETUP
     ########################################
     pi.set_mode(RXI, pigpio.OUTPUT)
     pi.wave_clear()
     pi.wave_add_serial(RXI, 9600, msg)
     serial_wave = pi.wave_create()

     # SERIAL OUTPUT SETUP
     ########################################
     pi.set_mode(TXO, pigpio.INPUT)
     status = pi.bb_serial_read_open(TXO, 9600)

     # SEND SERIAL DATA
     ########################################
     pi.wave_send_once(serial_wave)
     time.sleep(.1)
     # READ SERIAL DATA
     ########################################
     (count, data) = pi.bb_serial_read(TXO)
     status = pi.bb_serial_read_close(TXO)
     pi.wave_tx_stop()
     pi.wave_clear()

if __name__ == '__main__':
     msg = sys.argv[1]
     if len(sys.argv) > 2: 
          main(msg+'\r\n', sys.argv[2])
     else: main(msg)
