import PyPDF2

pdf_path = "./reference/file1.pdf"

with open(pdf_path, 'rb') as file:

    reader=PyPDF2.PdfReader(file)
    writer=PyPDF2.PdfWriter()

    writer.append_pages_from_reader(reader)

    key = '/key'
    message = 'message'

    metadata=reader.metadata
    metadata.update({key : message})
    writer.add_metadata(metadata)

    with open('newfile.pdf', 'wb') as output:
        writer.write(output)

print("success") 