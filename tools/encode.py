# This should open a bitmap, compress into RLE pixel format and save the new bytes to a file
# RLE pixel is a bitmap, but the image table has each pixel(3 bytes) RLE compressed
# the size header stays the same (for decoding use)
# in the future a modified header with a different 2 byte code at 00 to identify it could be
# used to create a basic animated bitmap format based on the RLE compressed bitmap. it would use
# 1 header with the number of frames will be stored, the frames will be seperated with 0x00 0x00 (an error in the RLE encoding)
# to mark the frame end
