from PIL import Image

def convert_messg2bin(message):
    binary_list= []
    for character in message:
        binary_list.append(format(ord(character), '08b'))
    return binary_list
 

def convert_int2bin(color_value):
    return format(color_value, '08b')


def convert_bin2int(binary_string):
    return int(binary_string, 2)


def change_lsb(color_binary, lsb):
    binary_list=list(color_binary)
    binary_list[-1]=lsb
    return ''.join(binary_list)


def change_pixel_colors_lsb(binary_message, pixel_list, continue_bit):
    binary_message_index=0
    for pixel_index in range(len(pixel_list)):
        new_colors=[]
        for color_value in pixel_list[pixel_index]:
            color_binary=convert_int2bin(color_value)
            if binary_message_index==8:
                if continue_bit=='1':
                    new_colors.append(convert_bin2int(change_lsb(color_binary,'1')))
                else:
                    new_colors.append(convert_bin2int(change_lsb(color_binary,'0')))
            else:
                new_colors.append(convert_bin2int(change_lsb(color_binary,binary_message[binary_message_index])))
            
            binary_message_index=binary_message_index+1
        pixel_list[pixel_index]=(new_colors[0], new_colors[1], new_colors[2])    
    return pixel_list


def decrypt_character_from_pixel_group(pixel_list):
    binary_string=''
    continue_flag=''
    index=0
    for pixel in pixel_list:
        for color in pixel:
            color_list = list(convert_int2bin(color))
            if index != 8:
                binary_string+=color_list[-1] 
                index=index+1
            else:
                continue_flag=color_list[-1]
    character = chr(int(binary_string, 2))
    return character, continue_flag



def perform_lsb_steg(new_img, binary_list):
    pixels = new_img.getdata()
    pixel_index=0
    group_size=3
    for index in range(len(binary_list)):
        current_pixel_list= []
        i=0
        for i in range(group_size):
            current_pixel_list.append(pixels[pixel_index+1])
        new_pixels=[]
        if index==len(binary_list)-1:
            new_pixels=change_pixel_colors_lsb(binary_message=binary_list[index], pixel_list=current_pixel_list, continue_bit='1')
        else:
            new_pixels=change_pixel_colors_lsb(binary_message=binary_list[index], pixel_list=current_pixel_list, continue_bit='0')

        pixel_index=(i+1)+pixel_index 
        yield(new_pixels)
     
class Imagesteg:

    def encrypt(input_file, message, output_file):
        binary_list=convert_messg2bin(message)
        print("\nEncrypt Successful...")    

        image=Image.open(input_file)
        if image.mode != 'RGB':
            image=image.convert('RGB')
        
        width, height=image.size
        new_img=image.copy()
        
        curr_x=0
        curr_y=0
        for pixel_list in perform_lsb_steg(new_img=new_img, binary_list=binary_list):
            for pixel in pixel_list:
                new_img.putpixel((curr_x,curr_y), pixel)
                if curr_x == width:
                    curr_x=0
                    curr_y=curr_y+1
                else:
                    curr_x=curr_x+1
        new_img.save(output_file)   


    def decrypt(input_file):
        image=Image.open(input_file)
        pixels=list(image.getdata())
        GRP_SIZE=3
        message=''
        for index in range(0,len(pixels), GRP_SIZE):
            character, continue_flag=decrypt_character_from_pixel_group(pixels[index : index+GRP_SIZE])
            message=message+character
            if continue_flag=='1':
                break
        print(f"\n{message}")
