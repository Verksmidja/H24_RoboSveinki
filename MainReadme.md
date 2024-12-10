# RoboSveinki🎅

VESM:3 Lokaverkefni.  
<sub> Date started wed.20.Nov2024 </sub>

### Names:  


Daníel Aron Blanck Guðjónsson.  
Gabriel Óðinn Schurack.  
Sverrir Haukur Aðalsteinsson.  

---

### Summary list.📘

> Click on the Summary you want to go to.

- [Dialog date list](#dialog-date-list)
- [Item list](#item-list)
- [Price list](#price-listi)
- [Photos](#photos)
- [Codes](#codes)

---

## About the Project.

We made a robot Santa Claus that will sing and play music and ring the bell when you open the gift. it can be turned on by opening the gift or enabling it in the Red-Node dashboard and there is a time API that will turn on the Santa robot at a specific time or date. Daníel made the code for the Santa robot to move and sing and attached the hands. Gabriel made the gift that activates the Santa robot when it's opened and it will light up inside the gift box when you open it. Sverrir configured the Rasberry Pi to run the MQTT server and set up the dashboard to control the robot, and is managing the GitHub page to keep everyone on track and writing the Readme file.


---

## Dialog date list

> Click on the Date you want to go to.

- [Wed/20/Nov](#wed20nov)
- [Fri/22/Nov](#fri22nov)
- [Wed/27/Nov](#wed27nov)
- [Fri/29/Nov](#fri29nov)
- [Wed/4/Dec](#wed4dec)
- [Fri/6/Dec](#fri6dec)
- [Wed/11/Dec](#wed11dec)

---
## Dialogs📆
> This is every single day what we did and finished.


### (Wed/20/Nov).  

On the first day of the project, we decided to create a robot dressed as Santa Claus that would sing Christmas music when a specific action was performed. We considered two options for triggering the music: either placing a bell in the robot's hands or opening a gift. Ultimately, we decided to trigger the music when a gift is opened.

Work began with searching for a 3D model of a gift box to print. At the same time, the robot was inspected to understand its wiring. A GitHub repository was also set up to keep everything organized and streamline collaboration.

A sonar sensor was successfully tested to detect conditions as true or false. A suitable 3D model for the gift box was found and sent for 3D printing.    

# ____________________________________________________________________________
### (Fri/22/Nov).

On the second day, we received our 3D-printed gift box to hold our prop components. We started using the Raspberry Pi wiped the SD storage and formatted it with the correct OS for it to run we were not able to get it to connect that day to a computer sadly but we'd get a lot of work done getting the robot hands to move up and down that day.

<img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241127_155406.jpg" alt="GitHub Logo" width="300"> .... <img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241127_155359.jpg" alt="GitHub Logo" width="300">
# ____________________________________________________________________________
### (Wed/27/Nov).


On the third day, we were able to get the Raspberry Pi to connect to the computer the bug was that we were using the wrong IP to connect to it.

We soldered the LED strips and wired them to the ESP Arduino, which all was gonna go into the box. We fastened the hand to the robot.  

We got the LED strips to work and light up with a little jingle Red and Green animation when you open the box.

<img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241127_154815_1.gif" alt="GitHub Logo" width="350"> 
<img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241206_141856_2_1.gif" alt="GitHub Logo" width="200">

# ____________________________________________________________________________
### (Fri/29/Nov)

On the fourth day, we were able to find a 3D model of a handbell we could print out for our second prop that wasn't gonna do anything (maybe light up that was one of our plans if we had extra time).
We got done setting up the MQTT server and the Node-RED on the Raspberry Pi computer. and we were able to communicate with the gift from the Red node dashboard getting the True and the False values it was transmitting through the MQTT server that was running on the Raspberry Pi computer.

Also, we ultimately decided to remove the Volume db controller. And we went to the store to buy props to dress up the robot.

# ____________________________________________________________________________
### (Wed/4/Dec)

On the fifth day. We are able to send true statements from the dashboard and get true statements from the git and get them displayed on the Nodered dashboard.
With that, we were also able to fix the robot and now it Asycos the mouth with the music that's playing, and with that, the head and the arms move also when the music played.

Also, we refined the gift box and stuffed it all in there and made it all neet and tightly

Most of that day took trying to fix the robot.

# ____________________________________________________________________________
### (Fri/6/Dec)

On the Sixthed day. We got the MQTT setup on the robotics code and it started when we opened the gift we were basically finished we needed only the API and the dashboard and we needed to dress up the bot.
> Video of the robot working.
https://photos.app.goo.gl/nGRxHMFyuemYbyLf8


# ____________________________________________________________________________
### (Wed/11/Dec)

#### More added tomorrow!!!






---
## Item list

> These are all the items we added to the robot for out build.

| Date            | Item                                   | Quantity |
|------------------|----------------------------------------|----------|
| **Wed. 20. Nov** | MG996R (Servo motors)                 | 2        |
| **Fri. 22. Nov** | 3D Printed Gift Box                   | 1        |
|                  | LED (Neopixel) Strip                  | 2        |
|                  | Raspberry Pi 3                        | 1        |
|                  | Breadboard                            | 1        |
|                  | Battery Module                        | 1        |
| **Wed. 27. Nov** | HW-208 (Stepdown voltage regulator)    | 1        |
|                  | HC-SR04 (Sonar distance sensor)       | 1        |
| **Fri. 29. Nov** | Santa Claus Bread                     | 1        |
|                  | Santa Claus Hat                       | 1        |
|                  | Santa Claus Glasses                   | 1        |
| **Wed. 11. Dec** | 3D Printed Handbell                   | 1        |

---
## Photos

> These are all the photos that and gifs that where created (for now).

<img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241127_155406.jpg" alt="GitHub Logo" width="300"> .... <img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241127_155359.jpg" alt="GitHub Logo" width="300"> .... <img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241206_141856_2_1.gif" alt="GitHub Logo" width="225">

<img src="https://github.com/Gazzo00o/RoboSveinki/blob/main/FILES/20241127_154815_1.gif" alt="GitHub Logo" width="400"> 













  


