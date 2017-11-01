import sys
from PIL import Image


length_field = 32


# - - - - - - - - - - - Start of Restore Message Declaration - - - - - - - - - - - - - - - - - - - - - - - - - - -
def restore_message(bits):
    bit_list = int(bits, 2)
    return bit_list.to_bytes((bit_list.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass') or '\0'

# - - - - - - - - - - - End of Restore Message Declaration - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - Start of Create List Declaration - - - - - - - - - - - - - - - - - - -
def create_bit_list(input: str):
    bit_ist = bin(int.from_bytes(input.encode('utf-8', 'surrogatepass'), 'big'))[2:]
    return bit_ist.zfill(8 * ((len(bit_ist) + 7) // 8))
# - - - - - - - - - - - End of Create List Declaration - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - Start of Change Mode Declaration - - - - - - - - - - - - - - - - - - -
def change_mode(image: Image) -> Image:
    # Change image to RGB mode
    image.load()
    r, g, b, a = image.split()
    image = image.merge("RGB", (r, g, b))
    return image
# - - - - - - - - - - - End of Change Mode Declaration - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - Start of Alter Bit Declaration - - - - - - - - - - - - - - - - - - - -
def alter_bit(color, index, setting_bit):
    mask = 1 << index
    color &= ~mask
    return color | mask if setting_bit else color
# - - - - - - - - - - - End of Alter Bit Declaration - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - Start of Encoder Declaration - - - - - - - - - - - - - - - - - - - - -
def encode(image: Image, message: str) -> Image:
    pixel_access_list = image.load()
    width, height = image.size
    message_size = str(len(message))
    message_bit_list = create_bit_list(message_size)
    message_bit_list += create_bit_list(message)

    if length_field % len(pixel_access_list[width, height]) != 0:
        message_length_body_separator = (len(pixel_access_list[width, height]) - length_field
                                         % len(pixel_access_list[width, height])) * [0]

    if "RGBA" == image.mode:
        image = change_mode(image)

    bit_list = iter(message_bit_list)

    for y in reversed(range(height)):
        for x in reversed(range(width)):
            pixel = list(pixel_access_list[x, y])
            for index, color in enumerate(pixel):
                bit = next(bit_list, None)
                if bit is None:
                    pixel_access_list[x, y] = tuple(pixel)
                    return image
                pixel[index] = alter_bit(color, 0, bit)
            pixel_access_list[x, y] = tuple(pixel)
# - - - - - - - - - - - End of Encoder Declaration - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - Start of Decoder Declaration - - - - - - - - - - - - - - - - - - - - -
def decode(image: Image):
    message_size = 0
    pixel_access_list = image.load()
    width, height = image.size
    bit_list = ''

    for y in reversed(range(height)):
        for x in reversed(range(width)):
            pixel = list(pixel_access_list[x, y])
            for color in pixel:
                color_bitstring = format(color, '08b')
                if bit_list.__len__() == 32:
                    message_size = int(bit_list, 2)
                    message_size.to_bytes((message_size.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrorgatepass')

                if bit_list.__len__() == message_size:
                    return message_size, restore_message(bit_list)
                bit_list += color_bitstring[7]
# - - - - - - - - - - - End of Decoder Declaration - - - - - - - - - - - - - - - - - - - - - -


def main():
    if sys.argv[1] == "-e":
        with open(sys.argv[2], 'r') as textfile:
            message = textfile.read()

        original_image = Image.open(sys.argv[3])
        new_image = original_image.copy()
        new_image = encode(new_image, message)

        try:
            new_image.save(sys.argv[4])
        except AttributeError:
            print("Couldn't save image {}".format(new_image))
    elif sys.argv[1] == "-d":
        encoded_image = Image.open(sys.argv[2])  # type: Image

        size, message = decode(encoded_image)  # type: str
        print("Message size is:", size)
        print(message)


if __name__ == "__main__":
    main()


