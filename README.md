# Camera With Face Detection
This is a simple camera app that allows to take snapshots.<br>
Works on both Raspberry Pi Camera and normal Webcams.<br> 
Made with Python (Tkinter and OpenCV)

## How to run ##
First, installed the dependencies using the following command<br>
```sh
pip install requirements.txt 
```
Then you can execute the program by using the following command<br>
```sh
python photo_booth.py --output <OUTPUT-PATH>
```
You can use the ```-p``` or ```--picamera``` argument to specify that a Raspberry Pi camera is being used.
