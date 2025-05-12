import argparse
from steg_classes.pdf_steg import PdfSteg
from steg_classes.image_steg import Imagesteg
from steg_classes.audio_steg import audioSteg

def encrypt(type, input_file, output_file, key, message, parser):
    if type=="pdf":
        if key:
            PdfSteg.encrypt(pdf_path=input_file, key=key, message=message, output_file_path=output_file)
        else:
            parser.error("PDF requires -k option")
    elif type =="image":
        Imagesteg.encrypt(input_file=input_file, message=message, output_file=output_file)
    elif type =="audio":
        audioSteg.encrypt(input_file=input_file, message=message, output_file=output_file)
    else:
        parser.error("Accepted inputs for -t include image, pdf and audio")


def decrypt(type, input_file, parser):
    if type=="pdf":
        PdfSteg.decrypt(pdf_path=input_file)
    elif type=="image":
        Imagesteg.decrypt(input_file=input_file)
    elif type=="audio":
        audioSteg.decrypt(input_file=input_file)
    else:
        parser.error("Accepted inputs for -t include image, pdf and audio")
        

def main():

    parser=argparse.ArgumentParser(description="</> getSteg is a palindrome string ")

    parser.add_argument('-d', action='store_true', help='decrypt the file (requires -f option)')
    parser.add_argument('-e', action='store_true', help='encrypt the file (requires -f -m -o options)')
    parser.add_argument('-f', required=False, type=str, help='path to the input file', metavar='INPUT_FILE')
    parser.add_argument('-o', required=False, type=str, help='path to the output file', metavar='OUTPUT_FILE')
    parser.add_argument('-m', required=False, type=str, help='message you want to add (use "")', metavar='MESSAGE')
    parser.add_argument('-t', required=True, type=str, help='type of steg you want to perform', metavar='TYPE')
    parser.add_argument('-k', required=False, type=str, help='metadata key', metavar='KEY')
    args = parser.parse_args()

    if args.e and args.d:
        parser.error("-e and -d are non-concurrent (use -e OR -d)")

    if not (args.d or args.e):
        parser.error("either -e or -d option must be used")

    if args.d:
        if not args.f:
            parser.error("must include -f option")
        else:
            decrypt(type=args.t, input_file=args.f, parser=parser)

    elif args.e:
        if (args.f and args.o and args.m and args.k) or (args.f and args.o and args.m):
            encrypt(type=args.t, input_file=args.f,output_file=args.o,key=args.k, message=args.m, parser=parser)
        else:
            parser.error("must include -f -m -o options (for image and audio) and an additional option -k for pdf")



if __name__ == "__main__":
    main()