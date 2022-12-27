# lookup-editor_scripts


## Upload lookups - [upload_lookups_to_splunk.py](https://github.com/mthcht/lookup-editor_scripts/blob/main/upload_lookups_to_splunk.py)
  - Simple script using splunk application [lookup-editor](https://splunkbase.splunk.com/app/1724) endpoint to upload multiple lookups at once:
![2022-12-24 08_37_55-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209426236-8a713d04-f128-4c52-97c3-0e2b6109aeac.png)


## Update lookups - [update_lookups_from_splunk.py](https://github.com/mthcht/lookup-editor_scripts/blob/main/update_lookups_from_splunk.py)
  - script using splunk application [lookup-editor](https://splunkbase.splunk.com/app/1724) endpoint to update part of a lookup or multiple lookups:


### Example of using the -p option (can be done with multiple lookups at once)

The lookup we have on splunk search app:
![2022-12-26 23_09_01-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209585956-1eab4858-a727-488b-a065-aad4d6f6540c.png)


Execution of the script (script asked for input, we paste the content in the terminal and typed 'ok' to confirm (can be done on multiple lookups at once):
![2022-12-26 23_10_35-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209585959-931ad7e7-6096-4df9-a538-87a3036698a1.png)
![2022-12-26 23_11_05-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209585964-ea14a374-1368-4f7d-bdfd-ee7f85522788.png)


result:
![2022-12-26 23_11_27-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209585966-6d410f30-34a7-45a6-ad43-f9d7f40cbe7f.png)




---

### Example of using the -i option (can be done with multiple lookups at once)

The lookup we have on splunk search app:

![2022-12-26 22_32_47-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209585490-9fe0d7da-0261-45c3-aa71-76623fd36400.png)

Execution of the script (script asked for each input, can be done on multiple lookups at once):

![2022-12-26 22_56_19-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209585499-597ee43b-cac3-44c2-9863-e57b5c312c8f.png)

result:
![image](https://user-images.githubusercontent.com/75267080/209585461-11de78f1-fe6c-4fa2-be51-dabeac8ccedb.png)



---

### Example of merging two csv files with option -f 
*(not limited to 2 files, we can merge demo_file_to_merge to all the lookups we want on splunk):*

The lookup we have on splunk search app:

![image](https://user-images.githubusercontent.com/75267080/209583591-650e3113-deb9-489e-baf4-5b4e58b5ae25.png)

The csv file on our desktop we want to merge to the lookup test.csv:

![2022-12-26 21_48_00-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209583442-ec5dbba9-8349-41a1-9b03-9b4f9bf32bf7.png)


Execution of the script to merge both files:

![2022-12-26 21_54_20-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209583455-06c86f30-bea6-4747-9e0c-954ce5c6e353.png)


result:

![image](https://user-images.githubusercontent.com/75267080/209583519-460a3cdb-edb6-4104-8238-96460117d96f.png)

---

### Example of merging tree csv files with option -f:

The lookups we have on splunk search app:

![2022-12-26 22_18_27-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584199-c7cb46b1-f3d2-4583-b13d-46dff03de9e1.png)
![2022-12-26 22_18_36-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584203-bcba925e-aaba-4ef6-a722-3c6922ad684c.png)

The csv file on our desktop we want to merge to the lookup test.csv and test2.csv:

![2022-12-26 22_22_57-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584212-1b126602-1567-484f-bb5c-6d38c8ca9b5f.png)


Execution of the script to the files:

![2022-12-26 22_25_22-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584246-759171ee-e9e1-47f5-8be9-324b6346bac6.png)
![2022-12-26 22_25_57-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584252-168c482b-7648-4f11-9afb-e9e463c2fed1.png)
![2022-12-26 22_26_08-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584255-fbc1609e-255f-44b8-8a0e-44a08ca93ffa.png)


result:

![2022-12-26 22_27_01-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584262-72d286f9-e9a9-4e1f-9021-c1268a3f4758.png)
![2022-12-26 22_27_12-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209584265-8a140ec5-d153-4f4c-a14d-3674b4e7203b.png)


## Download lookups - [download_lookups_from_splunk.py](https://github.com/mthcht/lookup-editor_scripts/blob/main/download_lookups_from_splunk.py)
- Simple script using splunk application [lookup-editor](https://splunkbase.splunk.com/app/1724) endpoint to download lookup(s) from splunk:

no arguments (use default values declared in the script)
![2022-12-27 19_04_48-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209706146-825392de-6341-4d20-b75d-bb8a7e4c40f2.png)

with arguments:
![2022-12-27 19_10_50-Windows 10 and later x64 - VMware Workstation](https://user-images.githubusercontent.com/75267080/209706214-9166f846-b7db-484b-ab5f-38d78513d69f.png)







