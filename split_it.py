from PyPDF2 import PdfFileWriter as PfW, PdfFileReader as PfR
import csv

def split_the_pdf(pdf_file_name, csv_file_name):

    # CSV file to get the participant name
    reader_handle = open(csv_file_name, 'r')
    reader = csv.reader(reader_handle)
    header = next(reader)

    # PDF file handle stuff
    pdf_infile = open(pdf_file_name, 'rb')
    pdf_reader = PfR(pdf_infile)

    # Page numbers for getPage() begins wth 0
    page_number = 0
    for row in reader:
        output_filename = row[0] + ".pdf"
        # The actual creation of the new PDFs
        pdf_writer = PfW()
        pdf_writer.addPage(pdf_reader.getPage(page_number))
        outfile = open(output_filename, 'wb')
        pdf_writer.write(outfile)
        outfile.close()

        page_number += 1
        print("Page Number :", page_number)

    # Closing the connection to the input file
    pdf_infile.close()

if __name__ == '__main__':
    split_the_pdf('allcerts.pdf', 'details.csv')
