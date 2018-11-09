# MicrosoftAzure-Cloud-Project1
A cloud-based picture and associated information storage and retrieval system with a (local) web interface (UI)

Description:  
The project provides a local interface to a cloud service 
that will allow a user to upload a meta-information table “people.csv”, 
a .csv (text) table followed by several individual pictures. Then the user may  
do queries that select some (or none) pictures, specified in the people table. 

Which will look like (in the “people.csv”): 

Nora,100,550,1000010,nora.jpg,Nora is nice 
Jees,98,420,,jees.jpg,Jees is Jees 
Abhishek,98,,,abhishek.jpg,Abhishek is not Jees 

And cloud-based “service” will allow a user to: 
+ Search for Nora (Name) and show her picture on a web page. 
+ Search for (display) all pictures where the grade is less than 99. 
+ Add a picture for Dave 
+ Remove Dave 
+ Change Jees keywords to “Jees is still Jees” 
+ Change Abhishek’s grade 
 
