# Knock off

#### Brief Description
This project is designed to be a door bell but for knock on the door. Knock off is a retrofit electronics setup that allow you to listen for knocks on the door and then have that information relayed to an array of lights indicating that someone is that the door.

#### Features
- Ability to detect knocks
- Ability to distinguish between different knock types
- Ability to integrate wirelessly with other devices
- Ability to indicate that a knock has occured in other rooms of the residence

#### Description of folders
- neopixels : Drivers for running neo pixels on the raspberry pi.

- photos : Contains the html tags used to display the photos taken by main_door.py .

- piezo_scripts : Scripts used for analyzing a piezos performance and for recording new knocks to a data file.

- site-packages/sklearn : A file which helps handle the dependencies for the sklearn python library.

- sklearn : A python library which is used to generate a decision tree which is used to determine which knock was sent.

- temp : Contains the actual .jpg phots that will be displayed from the raspberry pi.

#### Description of files
- knock_spacings.csv : This file contains the spacing between knocks for a "shave and a haircut" knock.
- knock_spacings_basic.csv : This file contains the spacings between knocks for a "basic" knock. Basic knocks include a double/triple/any multi knock that has relatively equal spacings between knocks.

- main_door.py : Python code that will run on the raspberry pi attached to the main door. This code contains four major componetns. The first is server code that will allow other client software to connect to and read information from the door. The second component is software to read in the data from a piezo and filter out the signals so that a knock is accurately recorded. The thrid component in main_door.py is mahcine learning code that used previous knocks to determine what kind of knock sequence was just entered and relays that data to the clients. The fourth and final part of the code is the ability to take pictures of people knocking at the door through the peephole. 

- main_receiver.py : This code is the receiver/client that is connected to the main_door.py code. The receiver code is intended to tell the user when someone is at the door when it receives a signal from the main_door.py scirpt. This is done by lighting up a set of neopixels attached the the reaspberry pi with different colors to indicate who is at the door. 

- piezoHandler.py : This code handles sampling the piezos, filtering the data with an exponentially weighted average, and then implementing a state machine to determine when a knock is available or not.

- predictKnock.py : This code reads in the spacing data from previous knock sequences and then creates a decision tree with machine learning to determine which type of knock was just inputed.  
