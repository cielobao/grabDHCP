# grabDHCP
Receives DHCP details, such as IP address, subnet mask, lease time, default gateway, and DNS servers.

**Requirements:**
_Python 3.x_


**Usage:**
Ensure you have Python 3.x installed on your system.
Run the script in your terminal or command prompt: python dhcp_discover_offer.py
The script will send a DHCP Discover message and wait for a DHCP Offer message.
If a DHCP Offer is received, the script will print the offer details.
If there is a timeout or an error, the script will display an appropriate message.
Press any key to exit the script.


**Code Overview:**
The code consists of the following components:
macByte(): A function that retrieves the MAC address of the current device and returns it as a byte string.
DHCPDiscover: A class that represents a DHCP Discover message, builds the message packet, and generates a random transaction ID.
DHCPOffer: A class that represents a DHCP Offer message, unpacks the received data, and prints the offer details.
The main block of the script initializes the socket, binds it to port 68, sends the DHCP Discover message, and listens for a DHCP Offer message.


**Notes:**
grabDHCP is for educational purposes and may not be suitable for production use.
It assumes a single network interface and retrieves the MAC address accordingly.
The script listens for DHCP Offer messages on port 68, which may require administrative privileges on some systems.
grabDHCP does not implement the full DHCP handshake (i.e., it does not send a DHCP Request message or handle DHCP Acknowledgment messages).
