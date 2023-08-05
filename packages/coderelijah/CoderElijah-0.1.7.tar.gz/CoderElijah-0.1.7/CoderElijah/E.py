########
# Info #
########
# This Py file contains my extra functions that are not included in any Python Library
# Version: 13
# Last updated: 2/4/2023
# For version 14, I will make this file more efficient, logical, and add comments to everything. Look forward to version 14!


####################
# ANSI Color Codes #
####################
class ansi:
  red = "31"
  burntYellow = "33"
  yellow = "93"
  green = "32"
  blue = "34"
  purple = "35"
  white = "37"


###########################
# Create a clear function #
###########################
# Thanks to @bigminiboss on Replit.com for this clear command.
# To use, type "clear()"
clear = lambda: print("\033c", end="", flush=True)


###################
# Timeout Command #
###################
def timeout(timeDuration, function):
  from time import sleep
  x = int(timeDuration)
  while x >= 0:
    clear()
    function()
    print("\nThis message will display for " + str(x) + " seconds.")
    x = x - 1
    sleep(1)


############
# Rickroll #
############
# This can be used to do other things too.
def rickRoll(fileName, timePerLine=2, infinity="yes"):
  from time import sleep
  rick = open(fileName)
  contents = rick.readlines()

  def main():
    clear()
    x = 0
    for fun in range(0, len(contents)):
      print(contents[x].strip("\n"))
      if contents[x] != "\n":
        sleep(timePerLine)
      x = x + 1

  main()
  while any(infinity == f for f in ["yes", "y"]):
    main()


##############################
# Timed Display of Text File #
##############################
# This is a modified rickRoll()
def showTextFor(fileName, timeToShow):

  def textDisplay():
    rick = open(fileName)
    x = 0
    contents = rick.readlines()
    for fun in range(0, len(contents)):
      print(contents[x].strip("\n"))
      x = x + 1

  timeout(timeToShow, textDisplay)


###########################################
# Display Text File (for titles and such) #
###########################################
# This is a modified rickRoll()
def showTextFile(fileName, startLine="", endLine=""):
  rick = open(fileName)
  contents = rick.readlines()
  if startLine == "":
    startLine = 0
  else:
    startLine = int(startLine) - 1
  if endLine == "":
    endLine = len(contents)
  else:
    endLine = int(endLine)
  if startLine == 0 and endLine == 0:
    all_lines = 1
  else:
    all_lines = endLine - startLine

  def textDisplay():
    x = startLine
    for fun in range(all_lines):
      print(contents[x].strip("\n"))
      x = x + 1

  textDisplay()
############################
# User Input Error Catcher #
############################
# Adapted from @InvisibleOne's post here:
#https://ask.replit.com/t/how-to-validate-user-input-properly/9586/2?
def getInput(prompt, options, inputLine='=> ', error='Invalid Input', clear='no'):
# prompt: What question the user is asked.
# options: The options available to the user (must be in the form of a list)
# inputLine: The text displayed on the line that the user types in their input. If you want it to be blank, set it to '' or "".
# error: The message displayed when the user's input is invalid.
  while True: # This runs until it is ended
    print(prompt) # Display the prompt
    for option in options: # Goes through the whole list of options
      print(f"{options.index(option)} {option}") # Displays the option number and text
      
    userInput = input(inputLine) # Gets user input, dipslaying the text from "inputLine"
    
    try: # This stops the code from crashing when it gets errors
      userInput = int(userInput) # Convert user's input into a number
      
      if options[userInput]: # This returns the value of the number the user inputted as their answer. The text is not actually used and Python just uses the numbers
        return userInput
    except: # If anything went awry (such as the user putting in text)
      if clear in ('yes', 'y', 'clear', 'clear()'): # User must set it to clear manually from the function options
        clear() # Clear screen
    else:
      print() # Displays blank line
      pass # Keep going
    
    print(error) # Display error message
###############
# ASCII Movie #
###############
# This was created in order to display the Star Wars ASCII movie using Python.
# However, it can be used with any ASCII movie that meets the following parameters:
# (1) The ASCII movie must be in a text file
# (2) The first line of the text file must contain a number indicating the number of times each frame should be shown
# (3) After that, there must be a "frame" consisting of 13 lines of text, or you can specify the number of lines of text in the function
# (4) Repeat steps 2 and 3 indefinitely; the program will work just fine no matter how many frames there are. There must be at least 3 and the last frame must have 0 as the number of frames for the program to work properly.
# Syntax: from E import movie
# Syntax: movie("text file", "font color", #)
# Syntax: # represents any number you wish; it is the number of lines per frame. Default is 13. Default text color is white. There is not default text file, so you must specify that.
def movie(textFile, fontColor="white", lines=13):
  ##############
  # Font Color #
  ##############
  cb = "\033["  # Beginning of ANSI color code
  ce = "m"  # End of ANSI color code
  if fontColor == "red":
    color = cb + ansi.red + ce
  elif fontColor == "burntYellow":  # No orange, but true ANSI yellow is really weird
    color = cb + ansi.burntYellow + ce
  elif fontColor == "yellow":  # Technically bright yellow, I like it better
    color = cb + ansi.yellow + ce
  elif fontColor == "green":
    color = cb + ansi.green + ce
  elif fontColor == "blue":
    color = cb + ansi.blue + ce
  elif fontColor == "purple":  # Technically magenta
    color = cb + ansi.purple + ce
  else:  # If parameters are not met, font is white
    color = cb + ansi.white + ce
  #########
  # Delay #
  #########
  from time import sleep
  #####################
  # Movie Source File #
  #####################
  file = open(textFile)
  #############
  # Read File #
  #############
  content = file.readlines()
  #######################
  # Configure Variables #
  #######################
  lineWithInt = lines + 1  # This is the number of lines per frame, INCLUDING the data line (how many times to show each line)
  x = 1  # "x" is the line that the program is displaying
  delayNum = 0  # The first line of the text file is line 0 (it's a Python thing), and we need that line number
  delayFrame = int(
    content[delayNum].strip()
  )  # Get the contents of the above line number and remove the weird double-spacing that Python does when reading text files
  ##############
  # Show Movie #
  ##############
  for fun in range(len(content)):  # This "for" loop plays the movie
    for movie in range(
        delayFrame
    ):  # This "for" loop plays each frame as many times as the text file indicates
      clear()  # Always start each frame with a blank canvas
      y = x  # "y" is the first line of each frame
      for frame in range(lines):  # This "for" loop creates each frame
        print(color + str(content[y]).strip("\n"))  # Print first line of frame
        y = y + 1  # This causes the loop to move on to the next line of the frame
      print(
      )  # Optional blank line at the bottom of each frame so the blinking cursor doesn't detract from the experience. Comment this line to remove it.
      sleep(
        0.067
      )  # After each complete frame is displayed, there is a 0.067 second pause. Otherwise, Python would show the movie as fast as it can, which is unbearably fast. I had it at 0.1 seconds, but discovered on the website that first made the animation that it should be 15 frames per second. 1/15 seconds is 0.067. So, I updated it.
    x = x + 14  # There are a total of 14 lines per frame: 1 of data (delayFrame) and 13 lines of image
    if delayNum < len(
        content
    ) - lineWithInt:  # This "if" statement stops the program from printing lines that come after the end of the text file (which don't exist), and end the program when it is supposed to end instead
      delayNum = delayNum + lineWithInt
      delayFrame = int(content[delayNum].strip())

