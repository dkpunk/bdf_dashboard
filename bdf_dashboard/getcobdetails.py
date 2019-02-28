import sys

cob_name=sys.argv[1]

file_list={"USAA" : "mail_usaa.html","USAA_BANK" : "mail_usaa.html","USAA_CARD" : "mail_usaa.html","PNC_BDF":"mail_pnc.html","PNC_SMB" : "mail_pnc_smb.html","CITI_BANK":"mail_citi.html","CITI_CARD":"mail_citi.html","CITI_LOAN":"mail_citi.html","RBC":"mail_rbc.html","ENVESTNET":"mail_envestnet.html","MS":"mail_ms.html","RHB":"mail_rhb.html"}
html_file=file_list[cob_name]
temp=cob_name.split("_")
if(temp[0]=='CITI'):
  cob_name='CITI'
elif(temp[0]=='USAA'):
  cob_name='USAA'
elif(temp[0]=='PNC' and temp[1]=='SMB'):
  cob_name='PNC_SMB'
filename="/var/www/html/SO/SO/ToolOpsDashBoard/RETINS/MQ_scripts/UN_DASHBOARD/BDF/"+cob_name+"/"+html_file
with open(filename,"r") as f:
	lines=f.readlines()
	for element in lines[5:]:
		print element

