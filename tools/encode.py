# This should open a bitmap, compress into RLE pixel format and save the new bytes to a file
# RLE pixel is a bitmap, but the image table has each pixel(3 bytes) RLE compressed
# the size header stays the same (for decoding use)
# in the future a modified header with a different 2 byte code at 00 to identify it could be
# used to create a basic animated bitmap format based on the RLE compressed bitmap. it would use
# 1 header with the number of frames will be stored, the frames will be seperated with 0x00 0x00 (an error in the RLE encoding)
# to mark the frame end

import struct

def open_file(filename):
    f = open(filename, 'br')
    data = bytearray(f.read())
    #print(data.hex())
    return data

def save_file(filename, data):
    f = open(filename,'bw')
    f.write(data)

def compress(data):
    len_start = len(data)
    pixels = []
    current_colour = bytearray([0,0,0])
    position = 0

    for byte in data:
        if position == 0:
            current_colour[0] = byte
            position += 1
        elif position == 1:
            current_colour[1] = byte
            position += 1
        elif position == 2:
            current_colour[2] = byte
            pixels.append(bytearray(current_colour.copy()))
            position = 0


    current_pixel = None
    count = 0
    compressed_data = bytearray()
    for pixel in pixels:
        if current_pixel == None:
            current_pixel = pixel
        if current_pixel != pixel or count >= 254:
            if count > 1:
                #print("compressed", count)
                compressed_data.append(0x00)
                compressed_data.extend(count.to_bytes(1,byteorder='little',signed=False))
            compressed_data.append(current_pixel[0])
            compressed_data.append(current_pixel[1])
            compressed_data.append(current_pixel[2])
            current_pixel = pixel
            count = 0
        count += 1
    len_end = len(compressed_data)
    print("Original data size:{}, Compressed Data: {}, Space Saved: {}, New image data is {:.2f}% of original".format(len_start, len_end, len_start-len_end, (len_end/len_start)*100))
    #print(compressed_data.hex())
    return compressed_data

def decode_bitmap(data):
    size = struct.unpack_from('I',data,0x02)[0]
    print(size)
    dataStart = struct.unpack_from('I',data,0x0A)[0]
    print(dataStart)
    header = bytearray(data[:dataStart])
    image_data = bytearray(data[dataStart:])
    return(header,image_data)

filename = r"C:\Users\simon\Desktop\s2.bmp"
bitmap = bytearray(open_file(filename))
bitmap = decode_bitmap(bitmap)
#print("header")
#print(bitmap[0].hex())
#print("data")
#print(bitmap[1].hex())
compressed_data = compress(bitmap[1])
bitmap = bitmap[0] + compressed_data
save_file(filename+"c", bitmap)
