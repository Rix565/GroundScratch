# GroundScratch
A new community for Scratch
## It is a fork of something else?
Yes. It's a fork of <a href="https://github.com/JTechnologies/Polaris/">Polaris</a>.
We started with that original source code, but what we built from that is completely made by us (with the help of some tutorials).
## How to run?
### Development environnement
#### PS : Don't use that mode for production use! Because if you're using a WSGI server, it will break it & it's unsecure for production environnement.
Clone the repository with this command:

`git clone https://github.com/Rix565/GroundScratch/`

Go to the newly created GroundScratch folder and modify the settings.py file.
### YOU MUST SET THE TESTING VALUE TO TRUE IF ITS SET TO FALSE!!!! Or else you gonna enter the production environnement.

Run this command to install all the dependencies:

`pip install flask flask-login flask-cors`

Finally, run this command (the 8080 port (or the port you set) must be open):

`python main.py`

And here you go! Nothing to do else. Yes! You listened right! No DB configuration stuff, the db is handled by a sqllite file.

Just go to http://localhost:8080 and it should work!
#### Production environnement
Upload the repository zip file (Code->Download Zip) and extract it on a folder.

Go to the newly created GroundScratch folder and modify the settings.py file.

### YOU MUST SET THE TESTING VALUE TO FALSE IF ITS SET TO TRUE!!!! Or else you gonna enter the development environnement.

If you're self-hosting the site:

Run this command to install all the dependencies:

`pip install flask flask-login flask-cors`

If you're using a python website hoster:

Use your hoster dependencies manager to install the packages: flask, flask-login, flask-cors

Configure your WSGI server for the GroundScratch installation.

Finally, run the WSGI server.

And here you go! Nothing to do else. Yes! You listened right! No DB configuration stuff, the db is handled by a sqllite file.

Just go to your domain URL and it should work!
