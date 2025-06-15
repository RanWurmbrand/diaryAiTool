from xlTool import XlsxTool
from diaryTool import DiaryTool

path = "/home/rwurmbra/Desktop/projects/diaryAiTool/backend/tmp.xlsx"
header_txt = "Intern Instructions: The work diary is meant to help you track your progress over the summer, reflect on your accomplishments, and support conversations with your manager, team buddy, or mentor. It will also serve as a \nhelpful reference when you complete a competency document later in your internship. Please remove examples below and fill in your own entries weekly, this should take no more than 15 minutes each week."
file = "tmp.xlsx"
# xtl = XlsxTool(file)
# xtl.change_row_height(1,65)
# xtl.merged_cells(1,1,1,20)
# xtl.dye_mereged_cell(1,1,"yellow")
# xtl.write_text(1,1,header_txt)

dt = DiaryTool(file)
dt.create_header(header_txt)
dt.create_details_row("Ran Wurmbrand","Konveyor-AI", "Ilanit Stein")
links= {"Jira":["jira.com","google.com"],"Github":["github.com"]}

dt.create_links_table(links)
dt.create_input_data_row()
dt.add_week_line("1", "jun 8", "jun 14")

default_details = {
        "date": "jun 15",
        "effortType": "medium",
        "desc": "reateing diary tool",
        "links": "google.com",
        "placeholders": "",
        "status": "in progras",
        "impact": "make an inside tool at redhat",
        "additional_notes": "None"
    }
dt.add_diary_line(default_details)

# xtl.create_file(file)
#xtl.add_text("wassup",1,2)

#xtl.add_write_bold_text("wassupddd",4,2)


# xtl.add_colored_text("wassupddd",6,2,"blue")
#xtl.add_two_colored_text_sections(18,4,"blue","hey","green","bye")
# xtl.add_three_colored_text_sections(15,5,"red","blue","green","red","yellow","blue")
#xtl.add_hyper_link_text(7,3,"google.com","test")
#opt = ["A","B","C"]
#xtl.add_options_cell(12,12,opt)
# xtl.merged_cells(1,2,3,4)

#xtl.add_divided_merged_cells(4,4,4,1)

#xtl.change_row_size(1,15)



# xtl.add_matrix(2,2,4,4)
# xtl.make_cell_bold(8,8)
# xtl.make_mereged_cells_bold(3,3)
# xtl.add_matrix(6,6,5,5)
# titles= ["a","b","c","d","e","f"]
# xtl.add_top_titled_matrix(6,6,5,5,titles)
# xtl.add_side_titled_matrix(9,9,5,5,titles)
#xtl.dye_cell(1,1,"yellow")
# xtl.dye_mereged_cell(2,3,"blue")




dt.save_file()