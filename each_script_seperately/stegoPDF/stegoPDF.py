import argparse
import PyPDF2


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


def main():
    parser = argparse.ArgumentParser(description="</> StegoPDF is a script for embedding messages into pdfs, by altering it's metadata.")
    parser.add_argument('-d', action='store_true', help='decrypt the file (requires -f option)')
    parser.add_argument('-e', action='store_true', help='encrypt the file (requires -f -k -m -o options)')
    parser.add_argument('-f', required=False, type=str, help='path to the input file', metavar='INPUT_FILE')
    parser.add_argument('-o', required=False, type=str, help='path to the output file', metavar='OUTPUT_FILE')
    parser.add_argument('-k', required=False, type=str, help='metadata-key name (must be preceded by /) (use "") ', metavar='KEY')
    parser.add_argument('-m', required=False, type=str, help='message you want to add (use "")', metavar='MESSAGE')
    args = parser.parse_args()

    if args.e and args.d:
        parser.error("-e and -d are non-concurrent (use -e OR -d)")

    if not (args.d or args.e):
        parser.error("either -e or -d option must be used")
    if args.d:
        if not args.f:
            parser.error("must include -f option")
        decrypt(args.f)
    elif args.e:
        if args.f and args.o and args.k and args.m:
            encrypt(args.f,args.k,args.m,args.o)
        else:
            parser.error("must include -f -k -m and -o options")


if __name__ == "__main__":
    main()

