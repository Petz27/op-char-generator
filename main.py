import csv

import dataGenerator
import pdfHandler as handler
import constants as c


def generateHTML(pirate):
    text = f'''
    <html>
        <body>
            <h1>{pirate["Name"]}</h1>
            <h2>{pirate["Race"]} {pirate["Class"]}</h2>
            <h2>Level: {pirate["Level"]} / HP: {pirate["HP"]} / DR: {pirate["DR"]}</h2>
            <h3>{pirate["Attributes"].to_html()}</h3>
            <h3>{pirate["Primaries"].to_html()}</h3>

        </body>
    </html>
    '''
    # write to file
    with open('sheet.html', 'w') as file:
        writer = csv.writer(file)
        file.write(text)


if __name__ == "__main__":
    print(c.debug_flag_info, "Hello! This is One Piece D20 character generator")
    # print(c.debug_flag_info, "If you want to randomize any input, enter 'r'")

    blooded = 1
    randomize = 1
    data = dataGenerator.generate_pirate(blooded, randomize)

    template_pdf = 'resources/template.pdf'
    output_pdf = f'resources/pirates/{data["Name"]}.pdf'

    # handler.empty_pdf_fields(template_pdf, output_pdf)

    second_page = False
    handler.fill_pdf_form(template_pdf, output_pdf, data, second_page)
    print(c.debug_flag_info, "Finished generating Pirate. Have fun!")


