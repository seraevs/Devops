# =====================================
# ==== The python SonarQube script  ===
# ====== Code analisys Report =========
# ==== Build by Sergey Yvstigneev =====
# =====================================
import fnmatch
import sys
from email import encoders
from email.mime.base import MIMEBase
import smtplib
import glob
import os
from pathlib import Path
import shutil
import codecs
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import xlrd
########################################################################################################
ca_row_style_red = "background-color:red;"
ca_row_style_black = "background-color:#728FCE;"
########################################################################################################
## Stages color variables
a1 = ""
a2 = ""
a3 = ""
a4 = ""
a5 = ""
a6 = ""
a7 = ""
a8 = ""
a9 = ""
a10 = ""
a11 = ""
a12 = ""
a13 = ""
a14 = ""
a15 = ""
a16 = ""
########################################################################################################
# HTML Message Part
f = codecs.open("F:\\jenkins\\workspace\\LeoPrj\\scripts\\sendmail\\leo.html", 'r')
########################################################################################################
leo_color = "red"
"color:black; background-color:red;"
# leo_row_style = "bgcolor:#728FCE; color:red"
leo_row_style = "background-color:red;"
leo_status_title = "Leo project build failed"
########################################################################################################
## Configuration and variables
Cs = "Unified-Cs"
Cpp = "Unified-Cpp"
Js_Backend = "Unified-Js-Backend"
Js_Fronted = "Unified-Js-Fronted"
########################################################################################################
leo_color = "red"
"color:black; background-color:red;"
leo_row_style = "background-color:red;"
leo_status_title = "Leo project build failed"
########################################################################################################
ca_row_style_red = "background-color:red;"
ca_row_style_black = "background-color:#728FCE;"
########################################################################################################
## Dictionaryes
## Dictionaryes for SonarQube code analisys
dictca = {
  "Security Hotspots": 8,
  "All": 20,
  "Unconfirmed": 8,
  "Issues": 8
}

## Dictionaryes for SonarQube code analisys counter C# code errors
dictcs = {
  "Security Hotspots": 0,
  "All": 0,
  "Unconfirmed": 0,
  "Issues": 0
}

## Dictionaryes for SonarQube code analisys counter Cpp code errors
dictcpp = {
  "Security Hotspots": 0,
  "All": 0,
  "Unconfirmed": 0,
  "Issues": 0
}

## Dictionaryes for SonarQube code analisys counter Js backend code errors
dictjs_backend = {
  "Security Hotspots": 0,
  "All": 0,
  "Unconfirmed": 0,
  "Issues": 0
}

## Dictionaryes for SonarQube code analisys counter Js fronted code errors
dictjs_fronted = {
  "Security Hotspots": 0,
  "All": 0,
  "Unconfirmed": 0,
  "Issues": 0
}

## Dictionary for projects
dictproject = {
  Cs: dictcs,
  Cpp: dictcpp,
  Js_Backend: dictjs_backend,
  Js_Fronted: dictjs_backend
}

dict_color_cs = {
  "Security Hotspots": ca_row_style_black,
  "All": ca_row_style_black,
  "Unconfirmed": ca_row_style_black,
  "Issues": ca_row_style_black
}

dict_color_cpp = {
  "Security Hotspots": ca_row_style_black,
  "All": ca_row_style_black,
  "Unconfirmed": ca_row_style_black,
  "Issues": ca_row_style_black
}

dict_color_fronted = {
  "Security Hotspots": ca_row_style_black,
  "All": ca_row_style_black,
  "Unconfirmed": ca_row_style_black,
  "Issues": ca_row_style_black
}

dict_color_backend = {
  "Security Hotspots": ca_row_style_black,
  "All": ca_row_style_black,
  "Unconfirmed": ca_row_style_black,
  "Issues": ca_row_style_black
}

dict_color = {
  Cs: dict_color_cs,
  Cpp: dict_color_cpp,
  Js_Backend: dict_color_fronted,
  Js_Fronted: dict_color_backend
}
########################################################################################################
## Smtp configuration
ip_smtp = '10.10.0.140'
port_smtp = 25
subject = f'SonarQube Code analysis Language: Unicocede.</li>'
message = f'<li>Error-"Messagd" \n'

directory = 'F:\\jenkins\\workspace\\archive\\Leo'
# HTML Message Part
path_to_html = "F:\\jenkins\\workspace\\LeoPrj\\scripts\\sendmail\\included.html"

status_wontfix="WONTFIX"
status_clossed="CLOSED"
########################################################################################################
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
    files.append(xlsx_file)
mess = ''

dir_path = dir + 'CodeAnalysisReports'
## Go to in defind only xlsx
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

print('============= test =================')
for i in range(1, len(sys.argv)):
    print('argument:', i, 'value:', sys.argv[i])
print('============= test =================')

########################################################################################################
def count_global(item_sheet_report_key, keyword):
    if keyword == Cs:
        dictcs[item_sheet_report_key] += 1

    if keyword == Cpp:
        dictcpp[item_sheet_report_key] += 1

    if keyword == Js_Backend:
        dictjs_backend[item_sheet_report_key] += 1

    if keyword == Js_Fronted:
        dictjs_fronted[item_sheet_report_key] += 1
########################################################################################################
for item in dictproject.keys():
    keyword = item
    for filename in os.listdir(dir_path):
        if fnmatch.fnmatch(filename, '*.xlsx'):
            if keyword in filename:
                filename_report = dir_path + "\\" + filename
                openFile = xlrd.open_workbook(filename_report)
                for item_sheet_report_key, item_sheet_report_value in dictca.items():
                    sheet_report = openFile.sheet_by_name(item_sheet_report_key)
                    for k in range(sheet_report.nrows - 1):
                        status = sheet_report.cell_value(k + 1, item_sheet_report_value)
                        if status != status_clossed and status != status_wontfix:
                            count_global(item_sheet_report_key, keyword)
########################################################################################################
for key_dictproject,value_dictproject in dictproject.items():
    for key_item_type_error,value_item_type_error in value_dictproject.items():
        for key_item_type_color,value_item_type_color, in dict_color.items():
            if value_dictproject[key_item_type_error] != 0 and key_dictproject == key_item_type_color:
                value_item_type_color[key_item_type_error] = ca_row_style_red
            else:
                if value_dictproject[key_item_type_error] == 0 and key_dictproject == key_item_type_color:
                    value_item_type_color[key_item_type_error] = ca_row_style_black

########################################################################################################
print(sys.argv[1])
argument = sys.argv[1]
if "Create_Version_Number" == argument:
    a1 = leo_row_style

if "Git_Clone_Leo" == argument:
    a2 = leo_row_style

if "Git_Clone_Unified" == argument:
    a3 = leo_row_style

if "Unit_Test" == argument:
    a4 = leo_row_style

if "Code_Analysis" == argument:
    a5 = leo_row_style

if "Build_Java_Backend" == argument:
    a6 = leo_row_style

if "Build_Java_Fronted" == argument:
    a7 = leo_row_style

if "Unified_Build_C#_C++" == argument:
    a8 = leo_row_style

if "Build_Embedded_NuET_RF_Bootloader" == argument:
    a9 = leo_row_style

if "Build_Embedded_NuET_RF_App" == argument:
    a10 = leo_row_style

if "Build_Embedded_LeoInterfaces_samd21" == argument:
    a11 = leo_row_style

if "Archive_Version&&Reports_CA" == argument:
    a12 = leo_row_style

if "Deployment" == argument:
    a13 = leo_row_style

if "Allure_tests" == argument:
    a14 = leo_row_style

if "Sending_Mail" == argument:
    a15 = leo_row_style

if "Finish" == argument:
    a16 = leo_row_style
########################################################################################################
# leo_status_title = "Leo project build finished successfully"
html = f.read().format(count_netcore=dictcs["Security Hotspots"], count_netcore_All=dictcs["All"],
                       count_netcore_Unconfirmed=dictcs["Unconfirmed"], count_netcore_Issues=dictcs["Issues"],
                       count_Cpp=dictcpp["Security Hotspots"], count_Cpp_All=dictcpp["All"], count_Cpp_Unconfirmed=dictcpp["Unconfirmed"],
                       count_Cpp_Issues=dictcpp["Issues"],
                       count_Fronted=dictjs_fronted["Security Hotspots"], count_Fronted_All=dictjs_fronted["All"],
                       count_Fronted_Unconfirmed=dictjs_fronted["Unconfirmed"], count_Fronted_Issues=dictjs_fronted["Issues"],
                       count_Backend=dictjs_backend["Security Hotspots"], count_Backend_All=dictjs_backend["All"],
                       count_Backend_Unconfirmed=dictjs_backend["Unconfirmed"], count_Backend_Issues=dictjs_backend["Issues"],
                       leo_color=leo_color, leo_status_title=leo_status_title,
                       Cs_HotSpot=dict_color_cs["Security Hotspots"], Cs_All=dict_color_cs["All"], Cs_Unconfirmed=dict_color_cs["Unconfirmed"], Cs_Issues=dict_color_cs["Issues"],
                       Cpp_HotSpot=dict_color_cpp["Security Hotspots"], Cpp_All=dict_color_cpp["All"], Cpp_Unconfirmed=dict_color_cpp["Unconfirmed"], Cpp_Issues=dict_color_cpp["Issues"],
                       Fronted_HotSpot=dict_color_fronted["Security Hotspots"], Fronted_All=dict_color_fronted["All"],
                       Fronted_Unconfirmed=dict_color_fronted["Unconfirmed"], Fronted_Issues=dict_color_fronted["Issues"],
                       Backend_HotSpot=dict_color_backend["Security Hotspots"], Backend_All=dict_color_backend["All"],
                       Backend_Unconfirmed=dict_color_backend["Unconfirmed"], Backend_Issues=dict_color_backend["Issues"],
                       a1=a1, a2=a2, a3=a3, a4=a4, a5=a5, a6=a6, a7=a7, a8=a8, a9=a9, a10=a10, a11=a11, a12=a12,
                       a13=a13, a14=a14, a15=a15, a16=a16)
########################################################################################################
# Create MIMEMultipart object
msg = MIMEMultipart("alternative")
msg["Subject"] = "SonarQube Code Analisys Unified Project Reports."
msg["From"] = "sergey.yvstigneev@.com"
#msg["To"] = "sergey.yvstigneev@.com"
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
########################################################################################################
## SMTP server configuration
server = smtplib.SMTP(ip_smtp, port_smtp)
mail_list = ['sergey.yvstigneev@.com', 'sergey.yvstigneev@.com']
amount = []
name = ['Sergey']
server.sendmail(msg["From"], msg["To"].split(","), msg.as_string())
########################################################################################################
