import PyPDF2

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


class PdfSteg:

    def encrypt_file(input_file, key, hidden_file, output_file):
        with open(input_file, 'rb') as file:
            reader=PyPDF2.PdfReader(file)
            writer=PyPDF2.PdfWriter()
            writer.append_pages_from_reader(reader)

            binary_list=[]
            with open(hidden_file, 'rb') as hf:
                file_bytes=hf.read()
                for byte in file_bytes:
                    binary_list.append(format(byte, '08b'))

            message = ''.join(binary_list) 

            metadata=reader.metadata
            metadata.update({key : message})
            writer.add_metadata(metadata)
            with open(output_file, 'wb') as output:
                writer.write(output)
        print("\n -- file creation successful --") 
    

    def decrypt_file(input_file, output_file, key):
        with open(input_file, 'rb') as file:
            reader= PyPDF2.PdfReader(file)
            metadata=reader.metadata
            flag=False
            for item in metadata:
                if item == key:
                    flag=True
                    save_file(binary_str=metadata[item], output_file=output_file)
            if flag==False:
                print("No such key name exists")


    def decrypt(pdf_path):
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file) 
            metadata=reader.metadata
            for key in metadata:
                print(f"{key} : {metadata[key]}")


    def encrypt(pdf_path, key, message, output_file_path):
        with open(pdf_path, 'rb') as file:
            reader=PyPDF2.PdfReader(file)
            writer=PyPDF2.PdfWriter()
            writer.append_pages_from_reader(reader)
            metadata=reader.metadata
            metadata.update({key : message})
            writer.add_metadata(metadata)
            with open(output_file_path, 'wb') as output:
                writer.write(output)
        print("\n -- file creation successful --") 

