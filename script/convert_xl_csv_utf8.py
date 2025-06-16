'''
This script converts excel files into csv with utf-8 encoding
by MY Sia
June 2025
'''
import glob
from pathlib import Path
import pandas as pd

##locate excel files
proj = "C:/Users/user/Desktop/try/2_streamline_final"
files_path = Path(f"{proj}")
file_list = glob.glob(f"{files_path}/*.xlsx")

##loop excel files
for xl_file in file_list:
    kid=xl_file[len(proj)+1:len(proj)+4] ##ID of child
    xl=pd.read_excel(xl_file)
    xl.to_csv(f'{files_path}/kid.csv', index=False, encoding="utf-8-sig")
