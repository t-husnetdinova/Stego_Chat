""" Trystan Kaes
    July 25 2020
    Steganography Module for Chat Client """
from PIL import Image

def convert_to_binary(message):
    """ This function converts a message from ascii to binary. """
    binary = list()
    for i in message:
        binary.append(format(ord(i), '08b'))
    return binary

def encode_helper(picture, message):
    """ Encode helper encodes the message into pixels and returns the modified pixels """
    binary_message = convert_to_binary(message)

    raw = iter(picture)
    length = len(binary_message)

    for i in range(length):

        # Create a list of the next 9 pixels
        pixel = list(raw.__next__()[:3] + raw.__next__()[:3] + raw.__next__()[:3])

        for j in range(0, 8):
            #encode message
            if binary_message[i][j] == '0' and pixel[j]%2 != 0:
                if pixel[j]%2 != 0:
                    pixel[j] -= 1
            elif binary_message[i][j] == '1' and pixel[j]%2 == 0:
                pixel[j] -= 1

            #end message
            if i == length - 1:
                if pixel[-1]%2 == 0:
                    pixel[-1] -= 1
            else:
                if pixel[-1] % 2 != 0:
                    pixel[-1] -= 1

        # Bundle it back up
        pixel = tuple(pixel)
        # Return the values
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]


def encode(image_name, message):
    """ Encode a message into the picture and return the encoded image. """
    picture = Image.open(image_name, 'r')
    width = picture.size[0]

    # Indexes
    x_axis, y_axis = 0, 0

    for pixel in encode_helper(picture.getdata(), message):

        # inject encoded pixels
        picture.putpixel((x_axis, y_axis), pixel)

        #traverse the pictures pixels
        if x_axis == width - 1:
            x_axis = 0
            y_axis += 1
        else:
            x_axis += 1

    picture.save("totally_not_secret_" + image_name)
    return "totally_not_secret_" + image_name

def decode(image):
    """ Extract a message from an image and return it. """
    raw = iter(image.getdata())

    message = ''
    while True:
        # Create a list of the next 9 values
        pixel = raw.__next__()[:3] + raw.__next__()[:3] + raw.__next__()[:3]

        binary_snippet = ''

        for i in pixel[:8]:
            if i%2 == 0:
                binary_snippet += '0'
            else:
                binary_snippet += '1'

        message += chr(int(binary_snippet, 2))

        if pixel[-1]%2 != 0:
            return message
    return "Decode Failed"

def encode_choice():
    """ Handle encode choice """
    image = input("Enter a picture to hide a message in:")
    message = input("Enter a message to hide:")
    encode(image, message)
    print("Message Encoded")

def decode_choice():
    """ Handle a decode choice """
    image = input("Enter a picture that definitly doesn't have secrets:")
    image_frame = Image.open(image)
    totally_not_secret_message = decode(image_frame)
    print(f"Looks like that photo said \"{totally_not_secret_message}\"")

def main():
    """ Main function for testing the module. """
    while True:
        choice = input("Would you like to encode or decode an image? [e/d]")
        if choice.lower() == "e":
            encode_choice()
        else:
            decode_choice()

if __name__ == '__main__':
    main()
