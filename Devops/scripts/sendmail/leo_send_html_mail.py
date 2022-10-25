# =====================================
# ==== The python SonarQube script  ===
# ====== Code analisys Report =========
# ==== Build by Sergey Yvstigneev =====
# =====================================
import fnmatch
import sys
from email import encoders
from email.mime.base import MIMEBase

import cell as cell
import row as row
import xlrd
import smtplib
import glob
import os
from pathlib import Path
import shutil
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

## Go to find last create achive project folder
directory = 'F:\\jenkins\\workspace\\archive\\Leo'
dir = max(glob.glob(os.path.join(directory, '*/')), key=os.path.getmtime)
## Go to find all existing xlsx files and remove them
path = dir + "\\CodeAnalysisReports"
filenames = glob.glob(path + "/*.xlsx")
for i in filenames:
    os.remove(i)

files = []
document_dir = Path(dir + '\\CodeAnalysisReports')
cnt = 0
files = []
## Go to find all existing xlsx files
for xlsx_file in document_dir.glob('**/*.xlsx'):
    # xlsx_file is a Path object
    # if you use old libraries, you have to use str(xlsx_file) to convert the Path to a str
    report = os.path.basename(xlsx_file)
    shutil.copy2(xlsx_file, dir + '\\CodeAnalysisReports')
    # print(report)
    # print(xlsx_file)
    files.append(xlsx_file)
mess = ''

dir_path = dir + 'CodeAnalysisReports'
## Go to in defind only xlsx
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
# print(files)
count_netcore = 0
count_netcore_All = 0
count_netcore_Unconfirmed = 0
count_netcore_Issues = 0

count_Cpp = 0
count_Cpp_All = 0
count_Cpp_Unconfirmed = 0
count_Cpp_Issues = 0

## Go to find and count errors in Unified-Cs code
keyword = 'Leo-Cs-RF_Host'
for filename in os.listdir(dir_path):
    if fnmatch.fnmatch(filename, '*.xlsx'):
        if keyword in filename:
            filename_report = dir_path + "\\" + filename
            openFile = xlrd.open_workbook(filename_report)
            sheet_report = openFile.sheet_by_name('Security Hotspots')
            for k in range(sheet_report.nrows - 1):
                exelmessage = sheet_report.cell_value(k + 1, 1)
                exelseverity = sheet_report.cell_value(k + 1, 4)
                exellanguage = sheet_report.cell_value(k + 1, 5)
                exelfile = sheet_report.cell_value(k + 1, 6)

                subject = f'SonarQube Code analysis Language: {exellanguage}.</li>'

                message = f'<li>Error-{count_netcore}: {exelmessage} => ' \
                          f'File for repair: {exelfile}.</li>' \
                          f'<div style="color:red"> Severity: {exelseverity}. </div> \n' \
                          f'\n'
                status = sheet_report.cell_value(k + 1, 8)
                if status != "CLOSED":
                    # print("Unified-Cs status ==> ", status)
                    count_netcore = count_netcore + 1

            sheet_report = openFile.sheet_by_name('All')
            for k in range(sheet_report.nrows - 1):
                status = sheet_report.cell_value(k + 1, 20)
                if status != "CLOSED":
                    # print("Unified-Cs status ==> ", status)
                    count_netcore_All = count_netcore_All + 1

            sheet_report = openFile.sheet_by_name('Unconfirmed')
            for k in range(sheet_report.nrows - 1):
                status = sheet_report.cell_value(k + 1, 8)
                if status != "CLOSED" and status != "WONTFIX":
                    # print("Unified-Cs status ==> ", status)
                    count_netcore_Unconfirmed = count_netcore_Unconfirmed + 1

            sheet_report = openFile.sheet_by_name('Issues')
            for k in range(sheet_report.nrows - 1):
                status = sheet_report.cell_value(k + 1, 8)
                if status != "CLOSED":
                    # print("Unified-Cs status ==> ", status)
                    count_netcore_Issues = count_netcore_Issues + 1
## Go to find and count errors in Unified-Cpp code
keyword = 'Leo-Cs-RF_MCU'
for filename in os.listdir(dir_path):
    if fnmatch.fnmatch(filename, '*.xlsx'):
        if keyword in filename:
            filename_report = dir_path + "\\" + filename
            openFile = xlrd.open_workbook(filename_report)
            sheet_report = openFile.sheet_by_name('Security Hotspots')
            count_netcore = 0
            for k in range(sheet_report.nrows - 1):
                status = sheet_report.cell_value(k + 1, 8)
                if status != "CLOSED":
                    # print("Unified-Cpp status ==> ", status)
                    count_Cpp = count_Cpp + 1

            sheet_report = openFile.sheet_by_name('All')
            for k in range(sheet_report.nrows - 1):
                status = sheet_report.cell_value(k + 1, 20)
                if status != "CLOSED":
                    # print("Unified-Cpp status ==> ", status)
                    count_Cpp_All = count_Cpp_All + 1

            sheet_report = openFile.sheet_by_name('Unconfirmed')
            for k in range(sheet_report.nrows - 1):
                status = sheet_report.cell_value(k + 1, 8)
                if status != "CLOSED" and status != "WONTFIX":
                    # print("Unified-Cpp status ==> ", status)
                    count_Cpp_Unconfirmed = count_Cpp_Unconfirmed + 1

            sheet_report = openFile.sheet_by_name('Issues')
            for k in range(sheet_report.nrows - 1):
                status = sheet_report.cell_value(k + 1, 8)
                if status != "CLOSED":
                    # print("Unified-Cpp status ==> ", status)
                    count_Cpp_Issues = count_Cpp_Issues + 1

leo_color = "red"
"color:black; background-color:red;"
# leo_row_style = "bgcolor:#728FCE; color:red"
leo_row_style = "background-color:red;"
leo_status_title = "Leo project build failed"

####################################################################
ca_row_style_red = "background-color:red;"
ca_row_style_black = "background-color:#728FCE;"
####################################################################
if count_netcore == 0:
    Cs_HotSpot = ca_row_style_black
else:
    Cs_HotSpot = ca_row_style_red

if count_netcore_All == 0:
    Cs_All = ca_row_style_black
else:
    Cs_All = ca_row_style_red

if count_netcore_Unconfirmed == 0:
    Cs_Unconfirmed = ca_row_style_black
else:
    Cs_Unconfirmed = ca_row_style_red

if count_netcore_Issues == 0:
    Cs_Issues = ca_row_style_black
else:
    Cs_Issues = ca_row_style_red
####################################################################

if count_Cpp == 0:
    Cpp_HotSpot = ca_row_style_black
else:
    Cpp_HotSpot = ca_row_style_red

if count_Cpp_All == 0:
    Cpp_All = ca_row_style_black
else:
    Cpp_All = ca_row_style_red

if count_Cpp_Unconfirmed == 0:
    Cpp_Unconfirmed = ca_row_style_black
else:
    Cpp_Unconfirmed = ca_row_style_red

if count_Cpp_Issues == 0:
    Cpp_Issues = ca_row_style_black
else:
    Cpp_Issues = ca_row_style_red

####################################################################

# HTML Message Part
f = codecs.open("F:\\jenkins\\workspace\\LeoPrj\\scripts\\sendmail\\leo_included.html", 'r')

# leo_status_title = "Leo project build finished successfully"
html = f.read().format(count_netcore=count_netcore, count_netcore_All=count_netcore_All,
                       count_netcore_Unconfirmed=count_netcore_Unconfirmed, count_netcore_Issues=count_netcore_Issues,
                       count_Cpp=count_Cpp, count_Cpp_All=count_Cpp_All, count_Cpp_Unconfirmed=count_Cpp_Unconfirmed,
                       count_Cpp_Issues=count_Cpp_Issues,
                       leo_color=leo_color, leo_status_title=leo_status_title,
                       Cs_HotSpot=Cs_HotSpot, Cs_All=Cs_All, Cs_Unconfirmed=Cs_Unconfirmed, Cs_Issues=Cs_Issues,
                       Cpp_HotSpot=Cpp_HotSpot, Cpp_All=Cpp_All, Cpp_Unconfirmed=Cpp_Unconfirmed, Cpp_Issues=Cpp_Issues,
                       )

# Create MIMEMultipart object
msg = MIMEMultipart("alternative")
msg["Subject"] = "SonarQube Code Analisys Leo Project Reports."
msg["From"] = "sergey.yvstigneev@lumenis.com"
msg["To"] = "sergey.yvstigneev@lumenis.com"
#msg["To"] = "sergey.yvstigneev@lumenis.com,ilan.haimovich@lumenis.com,katy.gb@lumenis.com"
#msg["Cc"] = "david.morag@lumenis.com,ilan.haimovich@lumenis.com"
part = MIMEText(html, "html")
msg.attach(part)

# Add Attachment
with open(filename_report, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)

for f in files:  # add files to the message
    file_path = os.path.join(dir_path, f)
    attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
    attachment.add_header('Content-Disposition', 'attachment', filename=f)
    msg.attach(attachment)

## SMTP server configuration
server = smtplib.SMTP('10.10.0.140', 25)
mail_list = ['sergey.yvstigneev@lumenis.com', 'sergey.yvstigneev@lumenis.com']
amount = []
name = ['Sergey']

server.sendmail(msg["From"], msg["To"].split(","), msg.as_string())
