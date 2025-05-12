import PyPDF2

class PdfSteg:
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

