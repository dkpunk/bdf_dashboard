<?php
$cob_name=$_GET['cob_name'];
$output=shell_exec("python ./getcobdetails.py $cob_name");
echo "$output";
?>
