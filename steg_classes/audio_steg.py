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


def read_group2binSTR(group_list, character_length):
    binary_string=''
    for index in range(character_length):
        binary=convert_int2bin(group_list[index])
        binary_string+=binary[-1]

    binary=convert_int2bin(group_list[-1])    
    continue_bit=binary[-1]
    return binary_string, continue_bit



def save_file(binary_str, output_file):
    try:
        if len(binary_str) % 8 != 0:
            raise ValueError("Binary string length must be 8")
        
        byte_chunks=[]
        for i in range(0, len(binary_str), 8):
            byte_chunks.append(binary_str[i:i+8])

        byte_list=[]
        for byte_chunk in byte_chunks:
            byte_value=int(byte_chunk,2)
            byte_list.append(byte_value)
        
        byte_list=bytes(byte_list)
        with open(output_file, 'wb') as file:
            file.write(byte_list)

    except Exception as e:
        print(f"An error occured : {e}")



class audioSteg:

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

    def encrypt_file(input_file, hidden_file, output_file):
        sample_rate, data = wavfile.read(input_file)

        if data.dtype != np.int16:
            raise ValueError("Expected 16 bit PCM WAV file")
        
        copy_of_data = np.copy(data)
        if data.ndim>1:
            copy_of_data=copy_of_data.flatten()
        binary_list=[]

        with open(hidden_file, 'rb') as hf:
            file_bytes=hf.read()
            for byte in file_bytes:
                binary_list.append(format(byte, '08b'))

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


    def decrypt_file(input_file, output_file):
        sample_rate, data = wavfile.read(input_file)
        data=data.flatten()
        GRP_SIZE=9
        CHR_SIZE=8
        message=''

        for index in range(0,len(data),GRP_SIZE):
            binary_string, continue_bit =read_group2binSTR(group_list=data[index:index+GRP_SIZE], character_length=CHR_SIZE)
            message+=binary_string
            if continue_bit=='1':
                break

        save_file(binary_str=message, output_file=output_file)
