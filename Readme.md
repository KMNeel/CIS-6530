Malware Assessment Safety Guidelines (README.md)
⚠️ WARNING: READ BEFORE PROCEEDING ⚠️ 
Handling malicious code is hazardous. Mismanagement can result in infection of your host machine, network, and data loss. You are responsible for maintaining a secure environment. 
________________________________________
1. Environment Requirements
•	Isolation: All malware analysis MUST be conducted within an isolated Virtual Machine (VM).
•	Networking: The VM network adapter must be set to Host-Only or Disconnected. Ensure no bridged networking is used.
•	Host Protection: Disable shared folders, clipboard sharing, and drag-and-drop functionality between the host and guest OS.
•	Snapshots: Take a clean snapshot immediately before introducing any malware sample.
•	Disposable VM: Use a dedicated, disposable VM (e.g., Windows 10/11 or Linux) that can be easily reverted. 
2. Sample Handling & Storage
•	Password Protection: All Samples of Malware and other payloads samples are in  a ZIP file, encrypted with the password “infected”.
•	File Naming: Do not use original file names. Rename to [sample_ID].zip to prevent accidental execution. The contents of the files 	are in two folders namely “Executable Malware” and “Other Payloads” folders.
•	Safe Transfer: Use encrypted, secure methods to move files into the VM, such as a secure, dedicated malware repository.
•	Extensions: Add exceptions to your AV for specific directories if the AV continuously deletes your samples, but never disable AV 	on your host. 
3. Execution & Analysis Protocols
•	Authorization: Ensure you have explicit permission to analyze the sample.
•	Tools: Use provided, approved, and up-to-date tools (e.g., Sysinternals, Wireshark).
•	Monitoring: Monitor system calls, network traffic, and file system modifications.
•	Revert: Revert to the clean snapshot immediately after finishing the analysis of each sample. 
4. Cleanup & Disposal
•	Secure Deletion: Delete all samples, reports, and evidence files securely.
•	Snapshot Rollback: Revert to the baseline snapshot to eliminate any persistent changes. 
5. Miscellaneous
•	Besides the two folders “Executable Malware Folder” and “Other Payloads Folder” there are two word documents which has details on the following.
   1.Mitre ID
   2.Name of ATP Group
   3.Country
   4.Source Reference
   5.MD Hash list
   6.Campaign Label
   7.Sourcing and Reproducibility information
   8.Malware  Data Gathering Methodology Note
	
Finally, the submission includes this README.md

Thank you very much for your time and efforts! It is much appreciated! 


