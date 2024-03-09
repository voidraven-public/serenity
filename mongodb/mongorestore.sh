wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -sc)/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt-get update
sudo apt-get install -y mongodb-database-tools

mongorestore --username xxx --password yyyy --authenticationDatabase admin --db zzz --host aaaa /tmp
Explanation of the options:

--username xxx: Replace xxx with your actual MongoDB username.
--password yyyy: Replace yyyy with your actual MongoDB password.
--authenticationDatabase admin: Specify the database where the user’s credentials are stored (usually admin).
--db zzz: Restore data to the database named zzz.
--host aaaa: Connect to the MongoDB server at the specified hostname or IP address (aaaa).
/tmp: Restore data from the local folder called /tmp.