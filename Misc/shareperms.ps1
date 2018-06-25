
#########################
# NTFS Folder Permissions Analyzer 
#
# Description: This powershell script reads from a user provided list of NTFS shares and then recursively maps
# permissions for folders. Findings are saved to a csv file for easy analysis. Erros such as insufficient
# priveleges and path not found are printed to the screen as well as sent to a csv file.
#
# Original: https://blog.netwrix.com/2017/08/18/top-5-free-tools-for-ntfs-permissions-reporting/
# Exception handling, comments, and output 'beautifications' made by Nolan Kennedy (nxkennedy) (https://github.com/nxkennedy/)
#
# Usage:
# 1. Change the '$InFile', '$Errors', and '$OutFile' variables if necessary.
# 2. Run the script: powershell.exe -ExecutionPolicy Bypass -NoExit -File shareperms.ps1
# 3. ( or for easy mode just run from ISE :) )
##########################


# Our input file
$InFile = ".\cifs-final.txt"

"`n[+] Starting analyzer"
"[*] Reading list '$InFile'"
"--------------------"

# Read through our text file containing file shares and paths. Format is '\\Server\path ShareName' (eg. \\192.168.1.2\foo OurCompanyShare)
foreach($line in Get-Content $InFile) {
    # Separate the path and ShareName. This is helpful for naming our output files with the ShareName.
    $RootPath = $line.Split(" ")[0]
    $ShareName = $line.Split(" ")[1]
    "`n[+] Scanning '$RootPath'..."
    $Errors = ".\ERRORS.csv"
    $Header = "Folder Path,IdentityReference,AccessControlType,IsInherited,InheritanceFlags,PropagationFlags"

    # Test if the share path exists
    try
    {
        $Folders = dir $RootPath -recurse -ErrorAction Stop | where {$_.psiscontainer -eq $true}
    }
    # If not, write the share name to a file and continue to the next share on the list
    catch
    {
        $ErrorMessage = $_.Exception.Message
        Add-Content -Value $ErrorMessage -Path $Errors
        "[!] $ErrorMessage" 
        "[!] Error saved to '$Errors'"
        "Moving on..."
        continue
    }
    
	# Our output file 
    $OutFile = ".\$ShareName-perms.csv"
    Add-Content -Value $Header -Path $OutFile
    # Iterate through the folders on the share
    foreach ($Folder in $Folders){
       $ACLs = get-acl $Folder.fullname | ForEach-Object { $_.Access  }
       Foreach ($ACL in $ACLs){
       $OutInfo = $Folder.Fullname + "," + $ACL.IdentityReference  + "," + $ACL.AccessControlType + "," + $ACL.IsInherited + "," + $ACL.InheritanceFlags + "," + $ACL.PropagationFlags
       Add-Content -Value $OutInfo -Path $OutFile
       }}
    "[+] Done. Moving to next share."
}
"--------------------"
"[+] Share Scanning Complete"
