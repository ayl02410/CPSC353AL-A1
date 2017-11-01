# CPSC353AL-A1


CPSC 353 - Assignment 1: Image Steganography

Alex Liao: ycl@csu.fullerton.edu

Description:
This short Python program contains functionality which allows a user to embed message into an image by changing the least significant bit of the pixels of the image, and to extract the embedded message from the encoded image with the user’s message by reading the least significant bit of the pixels of the image. When the program is executed, it takes in two to four arguments depending on the user’s desired action (encoding or decoding). Instructions of how to execute the program is specified below.

Instructions:
1. Program is executed via a command shell/ terminal.

2. To run the program with encoding function, enter the command into the terminal in the following format: python3 stegprog.py -e message inputImage.jpg outputImage.png

3. To run the program with decoding function, enter the command into the terminal in the following format: python3 stegprog.py -d inputImage.png

a: stegprog.py 	
-> this program.

b: -e/ -d 	
-> specify -e for encoding, -d for decoding.

c: message	
-> the message to embed into the image, can be a string, text files, or files containing texts, such as a python script file.

d: inputImage.jpg
-> the image to use for embedding/ decoding the user’s message, can be in other formats such as .png

e: outputImage.jpg
-> the image out as a result of embedding the user’s message.
