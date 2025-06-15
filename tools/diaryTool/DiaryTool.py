from xlTool import XlsxTool



dataInfo = ["Date", "Effort Type", "Description", "Links", "Status","Impact/OutCome","Additional Notes"]

class DiaryTool:

    def __init__(self,file_name):
        self.xlsx_writter= XlsxTool(file_name)

    
    def create_header(self,text):
        self.xlsx_writter.change_row_height(1,65)
        self.xlsx_writter.merged_cells(1,1,1,20)
        self.xlsx_writter.dye_mereged_cell(1,1,"yellow")
        self.xlsx_writter.write_text(1,1,text)

    def create_details_row(self,intern_name= "", team_name="",manager_name=""):
        xlsx_writter = self.xlsx_writter
        xlsx_writter.change_row_height(2,40)
        xlsx_writter.dye_cell(2,1,"grey")
        xlsx_writter.merged_cells(2,2,2,8)
        xlsx_writter.write_text(2,2,intern_name)
        xlsx_writter.dye_mereged_cell(2,2,"grey")
        xlsx_writter.merged_cells(2,9,2,13)
        xlsx_writter.write_text(2,9,team_name)
        xlsx_writter.dye_mereged_cell(2,13,"grey")
        xlsx_writter.merged_cells(2,14,2,20)
        xlsx_writter.dye_mereged_cell(2,14,"grey")
        xlsx_writter.write_text(2,14,manager_name)


    def create_links_table(self,links_hsh={}):
        if len(links_hsh) == 0 :
            return
        xl_writter = self. xlsx_writter
        titles = list(links_hsh)
        num_cells = 0
        for i in range(len(titles)):
            num_cells = max(num_cells, len(links_hsh[titles[i]]))
        print(num_cells)
        print(links_hsh)
        print(titles)
        xl_writter.add_side_titled_matrix(3,2,num_cells,len(titles) -1,titles)
        for i in range(len(titles)):
            tmp = 3
            for link in links_hsh[titles[i]]:
                xl_writter.add_hyper_link_text(3 + i,tmp,link)
                tmp +=1


    def create_input_data_row(self):
        xlsx_writter = self.xlsx_writter
        next_row = xlsx_writter.get_next_row() + 1
        xlsx_writter.change_row_height(next_row,25)
        xlsx_writter.merged_cells(next_row,1,next_row,2)
        xlsx_writter.dye_mereged_cell(next_row,1,"blue")
        xlsx_writter.write_text(next_row,1,dataInfo[0])
        col = 3
        
        print(next_row)
        for i in range(1,len(dataInfo)):
            xlsx_writter.merged_cells(next_row,col,next_row,col + 2)
            xlsx_writter.dye_mereged_cell(next_row,col,"blue")
            xlsx_writter.write_text(next_row,col,dataInfo[i])
            col += 3
                
    def add_week_line(self,week_num,start_date,end_date):
        xlsx_writter= self.xlsx_writter
        next_row = xlsx_writter.get_next_row()
        xlsx_writter.merged_cells(next_row,1,next_row,20)
        xlsx_writter.dye_mereged_cell(next_row,1,"grey")
        week_str = f"week {week_num} ({start_date} - {end_date})"
        xlsx_writter.write_text(next_row,1,week_str)

    def add_diary_line(self, details=None):
        if details is None:
            details = {}
        
        # Set defaults for missing keys
        default_details = {
            "date": "",
            "effortType": "",
            "desc": "",
            "links": "",
            "placeholders": "",
            "status": "",
            "impact": "",
            "additional_notes": ""
        }
        
        # Update defaults with provided details
        for key, value in default_details.items():
            if key not in details:
                details[key] = value
        
        xlsx_writter = self.xlsx_writter
        keys = list(details)
        next_row = xlsx_writter.get_next_row()
        col = 3
        xlsx_writter.merged_cells(next_row,1,next_row,2)
        xlsx_writter.write_text(next_row,1,details["date"])
        xlsx_writter.make_mereged_cells_bold(next_row,1)
        for key in keys:
            if key != "date" and key !="placeholders":    
                xlsx_writter.merged_cells(next_row,col,next_row,col+2)
                if key == "links":
                    xlsx_writter.add_hyper_link_text(next_row,col,details[key])
                else:  
                    xlsx_writter.write_text(next_row,col,details[key])
                xlsx_writter.make_mereged_cells_bold(next_row,col)
                col +=3

            

    def save_file(self):
        self.xlsx_writter.save_file() 

    