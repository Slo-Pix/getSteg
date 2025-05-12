import argparse
import numpy as np
from scipy.io import wavfile


def turn_message_to_binary_string_list(message):
    binary_list=[]
    for character in message:
        binary_list.append(format(ord(character), '08b'))
    return binary_list


def convert_int2bin(value):
    if value < 0:
        value=value+(2**16)
    return format(value, '016b')


def change_lsb(binary_string, bit):
    bianry_list= list(binary_string)
    bianry_list[-1]=bit
    return ''.join(bianry_list)
    

def convert_bin2int(value):
    if value[0]=='1':
        unsigned = int(value,2)
        signed = unsigned - (2**16)
        return signed
    else:
        return int(value,2)
    

def encrypt(input_file, message, output_file):
    sample_rate, data = wavfile.read(input_file)

    if data.dtype != np.int16:
        raise ValueError("Expected 16 bit PCM WAV file")
    
    copy_of_data = np.copy(data)
    if data.ndim>1:
        copy_of_data=copy_of_data.flatten()

    binary_list = turn_message_to_binary_string_list(message=message)
    audio_index=0
    for index in range(len(binary_list)):
        for bit in binary_list[index]:
            binary = convert_int2bin(value=copy_of_data[audio_index])
            binary = change_lsb(binary_string=binary , bit=bit)
            copy_of_data[audio_index]=convert_bin2int(value=binary)
            audio_index=audio_index+1

        binary=convert_int2bin(copy_of_data[audio_index])
        if index != len(binary_list)-1:
            binary = change_lsb(binary_string=binary, bit='0')
        else:
            binary = change_lsb(binary_string=binary, bit='1')
        copy_of_data[audio_index]=convert_bin2int(binary)
        audio_index=audio_index+1
    
    copy_of_data=copy_of_data.reshape(data.shape)
    wavfile.write(output_file, sample_rate, copy_of_data)


def unsigned_bin2int(value):
    return int(value,2)


def read_group(group_list, character_length):
    binary_string=''
    for index in range(character_length):
        binary=convert_int2bin(group_list[index])
        binary_string+=binary[-1]

    binary=convert_int2bin(group_list[-1])    
    continue_bit=binary[-1]
    return chr(unsigned_bin2int(value=binary_string)), continue_bit


def decrypt(input_file):
    sample_rate, data = wavfile.read(input_file)
    data=data.flatten()
    GRP_SIZE=9
    CHR_SIZE=8
    message=''

    for index in range(0,len(data),GRP_SIZE):
        character, continue_bit =read_group(group_list=data[index:index+GRP_SIZE], character_length=CHR_SIZE)
        message+=character
        if continue_bit=='1':
            break

    print(f"\n{message}")


def main():

    parser=argparse.ArgumentParser(description="</> StegoAUD is a script that hides plaintext inside audio files using LSB steganography")

    parser.add_argument('-d', action='store_true', help='decrypt the file (requires -f option)')
    parser.add_argument('-e', action='store_true', help='encrypt the file (requires -f -m -o options)')
    parser.add_argument('-f', required=False, type=str, help='path to the input file', metavar='INPUT_FILE')
    parser.add_argument('-o', required=False, type=str, help='path to the output file', metavar='OUTPUT_FILE')
    parser.add_argument('-m', required=False, type=str, help='message you want to add (use "")', metavar='MESSAGE')
    args = parser.parse_args()

    if args.e and args.d:
        parser.error("-e and -d are non-concurrent (use -e OR -d)")
    if not (args.d or args.e):
        parser.error("either -e or -d option must be used")
    if args.d:
        if not args.f:
            parser.error("must include -f option")
        else:
            decrypt(args.f)
    elif args.e:
        if args.f and args.o and args.m:
            encrypt(input_file=args.f,message=args.m,output_file=args.o)
            print("Encrypted successfully")
        else:
            parser.error("must include -f -m and -o options")



if __name__ == "__main__":
    main()