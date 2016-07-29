EnvironmentMonitor
==================

A residential environment monitoring system that records temperature, humidity and moisture around the house.

Hardware Punch List
-------------------

<table>
  <tr>
    <td></td>
    <td></td>
  </tr>
</table>

Security & OS Setup
-------------------

Ensure you install necessary updates and install a firewall (such as UFW) before proceeding. Rather than exposing motion and other services externally, we will be proxying them through Apache. This means the only ports you should need to open are port 80 (HTTP) and port 22 (SSH), especially since motion hasn't has as extensive vetting for security. As an example, you could setup a simple firewall as:
~~~~
sudo apt-get install ufw
sudo ufw allow 80
sudo ufw allow 22
sudo ufw enable
~~~~
Bear in mind EnvironmentMonitor uses BASIC HTTP authentication and does not necessarily support SSL out of the box (although you could definitely add it), so man-in-the-middle interception of your password is super-de-duper possible.

Also - the latest version of Raspian (Jessie) doesn't bring up wireless interfaces on boot by default, even for the RPi 3. Which is odd. To fix this, make sure your wireless interfaces in `/etc/network/interfaces` are set to "auto," such as:
~~~~
auto wlan0
allow-hotplug wlan0
iface wlan0 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
~~~~

It may be a good idea to create a crontab entry to delete old captured videos, e.g. `0 1 * * * find /home/motion -ctime +14 -delete`

To enable I2C communication for temperature and humidity monitoring, follow the I2C instructions from Adafruit available at https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

Hardware Installation
---------------------

See https://hackaday.io/project/12908-environment-monitor/instructions for hardware installation

Software Installation
---------------------

These installation instructions have been tested with the latest version of Raspian (Jessie)

1. Install the base packages with `sudo apt-get install wiringpi python-dev python-smbus python-imaging apache2 libapache2-mod-proxy-html libapache2-mod-authnz-external motion nodejs-legacy libav-tools npm monit`
2. Install Bower using `sudo npm install -g bower`
3. Enable the Apache2 modules using `sudo a2enmod authnz_external proxy_http`
4. If you are using the Raspberry Pi camera, add `bcm2835-v4l2` to /etc/modules
5. Edit `/etc/default/motion` and set it to start on boot
6. Clone this repository or download https://github.com/deckerego/EnvironmentMonitor/archive/master.zip which will include the Bottle webapp and some admin configs/scripts
7. Install EnvironmentMonitor's dependencies using `sudo pip install -r app/requirements.txt`
8. Copy the files within the app/ directory into /srv/environment
9. Change into the /srv/environment/views directory and execute `bower install bootstrap`
10. Copy the service config files from config/etc into the appropriate /etc directory, altering them as needed.
11. Create a copy of app/config.sample as /srv/environment/config.py, altering config.py to fit your preferences
12. Enable the webapp with `sudo a2dissite 000-default`, followed by `sudo a2ensite environment`, then start up (or restart) Apache2
13. Ensure config/etc/init.d/environment has been copied to /etc/init.d, then install it using `sudo update-rc.d environment defaults`
14. Start the webapp using `sudo service environment start`
