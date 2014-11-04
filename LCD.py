#!/usr/bin/python
#
# HD44780 LCD Script for
# Raspberry Pi

# Adapted from Matt Hawkins (http://www.raspberrypi-spy.co.uk)
# 26/07/2012 code (http://www.raspberrypi-spy.co.uk/2012/08/20x4-lcd-module-control-using-python/)
#
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
LED_ON = 15

# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def main():
  # Main program block

  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable

  # Initialise display
  lcd_init()

  # Toggle backlight off-on
  GPIO.output(LED_ON, False)
  time.sleep(1)
  GPIO.output(LED_ON, True)
  time.sleep(1)

  # Send some centred test
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("--------------------",2)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("Rasbperry Pi",2)
  lcd_byte(LCD_LINE_3, LCD_CMD)
  lcd_string("Model B",2)
  lcd_byte(LCD_LINE_4, LCD_CMD)
  lcd_string("--------------------",2)

  time.sleep(3) # 3 second delay

  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Raspberrypi-spy",3)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string(".co.uk",3)
  lcd_byte(LCD_LINE_3, LCD_CMD)
  lcd_string("",2)
  lcd_byte(LCD_LINE_4, LCD_CMD)
  lcd_string("20x4 LCD Module Test",2)

  time.sleep(20) # 20 second delay

  # Blank display
  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("",3)
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("",3)
  lcd_byte(LCD_LINE_3, LCD_CMD)
  lcd_string("",2)
  lcd_byte(LCD_LINE_4, LCD_CMD)
  lcd_string("",2)

  time.sleep(3) # 3 second delay

  # Turn off backlight
  GPIO.output(LED_ON, False)

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

if __name__ == '__main__':
  main()
