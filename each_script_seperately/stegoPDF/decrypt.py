import PyPDF2

pdf_path = "newfile.pdf"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)

    metadata=reader.metadata
    for key in metadata:
        print(f"{key} : {metadata[key]}")
