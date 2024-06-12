import openpyxl as xl
import lxml.html as lh
from function import *
import pandas as pd

# READING OUR DATABASE
data=xl.load_workbook('peptrial.xlsx')
sheet=data['Sheet1']
len_max = sheet.max_row

# ACCESSING TO THE PROPERTIES
matrix=access(sheet,len_max)

# CREATING A DATA FRAME WITH THE PROPERTIES
df=pd.DataFrame(matrix)
df.to_excel(excel_writer="C:/Users/rodri/Desktop/peptidedatabase/properties.xlsx")




