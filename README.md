The repositry files are structured as follows:
Report Folder: contains the report that explains each step implementing in the project.

Results Folder: It includes the results saved in CSV files.

Source_code folder: It consists of two folders
1-Twitter harvester folders:
•	createDB: contains source code for creating CouchDB database.
•	history: code file for retrieving historical tweets of each users and save them into the database.
•	stream: contains code file for retrieving the tweets within trending topic in Saudi Arabia and saves them into CouchDb.
•	User: code file for saving the users who tweeted within the trending topics into the database.
•	Alo there are 2 folders replies and quoted folders which contain code files for saving quoted and replied tweets of each user into the database. 

•	Process_Tweet: It contains the code used to preprocess the tweets and save the dataset as a CSV file in the dataset folder.
 
2- Topic Modelling using LDA:
•	dataset: contains the extracted tweets from the database.
•	stopwords:contains Arabic stopwords
•	Visualization:contains the HTML file for visualizing the most important words within topics.
•	Requirements:required Python  packages for running  LDA_Arabic_Topic_Modelling  code.
•	
•	.LDA_Arabic_Topic_Modelling: LDA_Arabic_Topic_Modelling (jupyter notebook) :source code for implementing LDA algorithm. 
