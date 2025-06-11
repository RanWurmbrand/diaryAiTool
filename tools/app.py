import openpyxl
from openpyxl import Workbook
from xlTool import XlsxTool


path = "/home/rwurmbra/Desktop/projects/diaryAiTool/backend/tmp.xlsx"
header_txt = "Intern Instructions: The work diary is meant to help you track your progress over the summer, reflect on your accomplishments, and support conversations with your manager, team buddy, or mentor. It will also serve as a \nhelpful reference when you complete a competency document later in your internship. Please remove examples below and fill in your own entries weekly, this should take no more than 15 minutes each week."
file = "tmp.xlsx"
xtl = XlsxTool(file)
# xtl.create_file(file)
xtl.add_text("wassup",1,2)

xtl.add_write_bold_text("wassupddd",4,2)


# xtl.add_colored_text("wassupddd",6,2,"blue")
#xtl.add_two_colored_text_sections(18,4,"blue","hey","green","bye")
# xtl.add_three_colored_text_sections(15,5,"red","blue","green","red","yellow","blue")
xtl.add_hyper_link_text(7,3,"google.com","test")
opt = ["A","B","C"]
xtl.add_options_cell(12,12,opt)