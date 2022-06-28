# mattildaIO Hackaton
for the correct execution of this project you must create the settings.cfg file in the settings folder, this file must include the following data:

postgresql:

[database]
host: dbhost
user: dbuser
password: dbpassword
db: dbname
port: dbport

MongoDB:

[mongodb]
host: mongohost
user: mongouser
password: mongopassword
db: mongodbname
port: mongodbport

JWT:

[token]
secret_key: secretkey
access_token_expire: minutes to expire token
