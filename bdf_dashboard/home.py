import requests
import json
import re
import os
import csv
from collections import Counter

cob_names=["PNC_BDF","PNC_SMB","PNC_SMB_CARD","USAA_BANK","USAA_CARD","USAA_SP11","CITI_BANK","CITI_CARD","CITI_LOAN","RBC","RHB","ENVESTNET","MS"]
bdf_home_files={"PNC_BDF":"PNC_PFM.output","PNC_SMB":"PNC_SMB.output","PNC_SMB_CARD":"PNC_SMB_CARD.output","USAA_SP11":"USAA_SP11.output","CITI_BANK":"CITI_BANK.output","CITI_CARD":"CITI_CARD.output","CITI_LOAN":"CITI_LOAN.output","RBC":"RBC.output","RHB":"RHB.output","ENVESTNET":"Envestnet.output","MS":"MS.output","USAA_BANK":"USAA_BANK.output","USAA_CARD":"USAA_CARD.output"}
mq_path="/var/www/html/SO/SO/ToolOpsDashBoard/RETINS/MQ_scripts/UN_DASHBOARD/BDF/"
def getdetails(cob_name):
	'''totalfiles="NA"
	totalfiles_r="NA"
	files_status="NA"
	sets_processed="NA"
	db_filing_rate="NA"
	tpm="NA"
	bdf_status="NA"
	start_time="NA"
	eta="NA"
	mqdepth="NA"
	mqstats="NA"
	'''
	start_time,end_time,total_files,files_received_sftp,files_status,total_sets,sets_processed,db_filing_rate,tpm,mq_depth,bdf_status,total_db_filers,db_filer_status,eta,last_run_time=("NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA")
	#details=[cob_name,totalfiles,totalfiles_r,files_status,sets_processed,db_filing_rate,tpm,bdf_status,start_time,eta,mqdepth]
	details_new=[cob_name,start_time,end_time,total_files,files_received_sftp,files_status,total_sets,sets_processed,db_filing_rate,tpm,mq_depth,bdf_status,total_db_filers,db_filer_status,eta,last_run_time]
	bdf_file=bdf_home_files[cob_name]
	try:
	   with open("./BDF_OUTPUT/"+bdf_file) as f1:
		file_out=f1.read()
	#	print file_out
		count=0
		file_arr=file_out.split(",")
		for count in range(1,len(file_arr),1):
			#details[count]=file_arr[count]
			details_new[count]=file_arr[count]
	except IOError:
	   mqdepth="Unable to read file"
	   totalfiles,totalfiles_r,files_status,sets_processed,db_filing_rate,tpm,bdf_status,start_time,eta="Unable to read file"
	   start_time,end_time,total_files,files_received_sftp,files_status,total_sets,sets_processed,db_filing_rate,tpm,mq_depth,bdf_status,total_db_filers,db_filer_status,eta,last_run_time="Unable to read file"
	return details_new

def getmqstats(cob_name):
	mqstats=""
	dbfilerlist=""
	scount=0
	tcount=0
	temp=cob_name.split("_")
	if(temp[0]=='CITI'):
  	   cob_name='CITI'
	elif(temp[0]=='USAA'):
	   cob_name='USAA'
	elif((temp[0]=='PNC') and (temp[1]=='SMB')):
	   cob_name='PNC_SMB'
	try:
	   with open(mq_path+cob_name+"/MQdepth.txt","r") as f2:
                mqstats=f2.read()
        except IOError:
           mqstats="Unable to read file"	
	try:
           with open(mq_path+cob_name+"/DC_list.txt","r") as f3:
                dbfilerlist=f3.read()
	   with open(mq_path+cob_name+"/DC_list.txt","r") as f3:
		dbarray=f3.readlines()
		tcount=len(dbarray)
		#print dbarray
		for element in dbarray:
			el_arr=element.split(':')
			if(el_arr[2].strip()=='FILING'):
				scount=scount+1
        except IOError:
           dbfilerlist="Unable to read file"
	total_db_filers="{0}/{1}".format(str(scount),str(tcount))
	return mqstats,dbfilerlist,total_db_filers
print '''
<!DOCTYPE html>
<html>
<head>
<title>BDF Monitoring</title>
<style>
.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
.showme{ 
   display: none;
 }
 .showhim:hover .showme{
   display : block;
 }
 .showhim:hover .ok{
   display : none;
 }
table {
  border-collapse: collapse;
}
th {
background-color: #eee;
}
.tooltip {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 12px;
  font-style: normal;
  font-weight: normal;
  line-height: 1.42857143;
  text-align: left;
  text-align: start;
  text-decoration: none;
  text-shadow: none;
  text-transform: none;
  letter-spacing: normal;
  word-break: normal;
  word-spacing: normal;
  word-wrap: normal;
  white-space: normal;
  /* ... */
}
.tooltip-inner {
  max-width: 200px;
  padding: 3px 8px;
  color: #fff;
  text-align: center;
  background-color: #000;
  border-radius: 4px;
}
table, th, td {
  border: 1px solid black;
}</style>
</head><body><h3>BDF Monitoring</h3>
<table id=\"customers\" class=\"table table-bordered\" cellspacing=\"0\" style=\"width:100%\">
<thead class=\"thead-darl\"><tr><th>Cobrand group</th><th>Start Time</th><th>End Time</th><th>Total Files</th><th>Files Received</th><th>Files Status</th><th>Total Sets</th><th>Sets Processed</th><th>DB Filing Rate</th><th>TPM</th><th>MQ Depth</th><th>BDF Status</th><th>Total DB Filers</th><th>DB Filer Status</th><th>ETA</th><th>Last Run Time</th></tr></thead><tbody>'''
'''
<thead class=\"thead-darl\"><tr><th>Cobrand group</th><th>Total Files</th><th>Total_Files Received</th><th>Files STATUS</th><th>Sets processed</th><th>DB Filing Rate</th><th>TPM</th><th>BDF Status</th><th>Start Time</th><th>ETA</th><th>MQ Depth</th></tr></thead><tbody>'''
for cob_name in cob_names:
#	temp,totalfiles,totalfiles_r,files_status,sets_processed,db_filing_rate,tpm,bdf_status,start_time,eta,mqdepth=getdetails(cob_name)
	temp,start_time,end_time,total_files,files_received_sftp,files_status,total_sets,sets_processed,db_filing_rate,tpm,mq_depth,bdf_status,total_db_filers,db_filer_status,eta,last_run_time=getdetails(cob_name)
	mqstats,dbfilerlist,total_db_filers=getmqstats(cob_name)
	file_color="#ffb84d"
	bdf_color='#ffb84d'
	db_filer_color='#ffb84d'
	if(files_status=='COMPLETED'):
		file_color='#99ff99'
	if(files_status=='FAILURE'):
		file_color='#ff4d4d'
	if(files_status=='SLA BREACHED-PLEASE CHECK'):
		file_color='#ff4d4d'
	if(bdf_status=='COMPLETED'):
		bdf_color="#99ff99"
	if(bdf_status=='FAILED'):
		bdf_color='#ff4d4d'
	if(db_filer_status=='COMPLETED'):
                db_filer_color="#99ff99"
        if(db_filer_status=='FAILED'):
                db_filer_color='#ff4d4d'
	
#	print "<tr><td><a href=\"getcobdetails.php?cob_name={0}\" target=\"_blank\"><b>{0}</b></a></td><td>{1}</td><td>{2}</td><td bgcolor=\"{12}\">{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td><td>{8}</td><td>{9}</td><td><div class=\"showhim\">{10}<div class=\"showme\"><table><td>{11}</td></table></div></div></td></tr>".format(cob_name,totalfiles,totalfiles_r,files_status,sets_processed,db_filing_rate,tpm,bdf_status,start_time,eta,mqdepth,mqstats,bgcolor)
#	print "<tr><td><a href=\"getcobdetails.php?cob_name={0}\" target=\"_blank\"><b>{0}</b></a></td><td>{1}</td><td>{2}</td><td bgcolor=\"{12}\">{3}</td><td>{4}</td><td>{5}</td><td>{6}</td><td bgcolor=\"{13}\">{7}</td><td>{8}</td><td>{9}</td><td><div class=\"showhim\"><a href=\"#\" data-toggle=\"tooltip\" title=\"{11}\">{10}</a></div></td></tr>".format(cob_name,totalfiles,totalfiles_r,files_status,sets_processed,db_filing_rate,tpm,bdf_status,start_time,eta,mqdepth,mqstats,bgcolor,bdf_color)
	print "<tr><td><a href=\"getcobdetails.php?cob_name={0}\" target=\"_blank\"><b>{0}</b></a></td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td bgcolor=\"{16}\">{5}</td><td>{6}</td><td>{7}</td><td>{8}</td><td>{9}</td><td><div class=\"showhim\"><a href=\"#\" data-toggle=\"tooltip\" title=\"{19}\">{10}</a></div></td><td bgcolor=\"{17}\">{11}</td><td><div class=\"showhim\"><a href=\"#\" data-toggle=\"tooltip\" title=\"{20}\">{12}</a></div></td><td bgcolor=\"{18}\">{13}</td><td>{14}</td><td>{15}</td></tr>".format(cob_name,start_time,end_time,total_files,files_received_sftp,files_status,total_sets,sets_processed,db_filing_rate,tpm,mq_depth,bdf_status,total_db_filers,db_filer_status,eta,last_run_time,file_color,bdf_color,db_filer_color,mqstats,dbfilerlist)
print '''</tbody></table><script src="jquery-1.12.4.js"></script> 
     <script src="jquery.dataTables.min.js"></script>
     <script src="dataTables.bootstrap.min.js"></script>
      <link href="bootstrap.min.css" rel="stylesheet"> 
      <link href="dataTables.bootstrap.min.css" rel="stylesheet">
      


    <script>


$(document).ready(function() {
     $('#customers').DataTable({
"pageLength":20
});
} );


</script></body></html>'''
	
	
