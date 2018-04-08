pair = bytearray(b'\xFF\xEE')
print(pair)
x = pair
x.append(0xaa)
print("data is %s" %x)