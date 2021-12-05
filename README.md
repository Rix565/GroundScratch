# GroundScratch
Fork of Polaris in a more federated way
## It is a fork of something else?
Yes. It's a fork of <a href="https://github.com/JTechnologies/Polaris/">Polaris</a>.
We started with that original source code, but what we built from that is completely made by us (with the help of some tutorials).
## How to run?
#### Development environnement
##### PS : Don't use that mode for production use! Because if you're using a WSGI server, it will break it & it's unsecure for production environnement.
##### Requirements
<ul>
  <li>Python 3.8+</li>
  <li>MySQL/MariaDB</li>
</ul>
Clone the repository with this command:

`git clone https://github.com/Rix565/GroundScratch/`

Go to the newly created GroundScratch folder and modify the settings.py file.
### YOU MUST SET THE TESTING VALUE TO TRUE IF ITS SET TO FALSE!!!! Or else you gonna enter the production environnement.

Run this command to install all the dependencies:

`pip install flask flask-login flask-cors flask-migrate pymysql`

Run this command to configure your database for a GroundScratch installation:

`flask db upgrade`

Finally, run this command (the 8080 port (or the port you set) must be open):

`python app.py`

And here you go! Nothing to do else.

Just go to http://localhost:8080 (or the port/domain you've set) and it should work!
#### Production environnement

##### Requirements
<ul>
  <li>A shell access if you're using an hoster</li>
  <li>Python 3.8+</li>
  <li>MySQL/MariaDB</li>
</ul>
  

Upload the repository zip file (Code->Download Zip) and extract it on a folder.

Go to the newly created GroundScratch folder and modify the settings.py file.

### YOU MUST SET THE TESTING VALUE TO FALSE IF ITS SET TO TRUE!!!! Or else you gonna enter the development environnement.

Run this command to install all the dependencies:

`pip install flask flask-login flask-cors flask-migrate pymysql`

Run this command to configure your database for a GroundScratch installation:

`flask db upgrade`

Configure your WSGI server for the GroundScratch installation.

Finally, run the WSGI server.

And here you go! Nothing to do else.
Just go to your domain URL and it should work!
