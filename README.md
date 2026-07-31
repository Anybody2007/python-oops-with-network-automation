# Python OOPs with Network Automation

This is my personal playground for learning Python OOP — but instead of the usual `Dog` / `Animal` / `Car` examples you see in every tutorial, I'm building things around stuff I actually deal with at work: firewalls, IPs, credentials, logins.

The idea is simple — take one networking concept (say, a firewall), turn it into a class, and slowly make it smarter as I learn more OOP. Each folder is a step in that journey, messy notes and all.

## What's in here

```
python-oops-with-network-automation/
├── 01_classes/
│   ├── 01_classes_basic.py
│   ├── 02_classes_contructor.py
│   ├── 03_classes_steful.py
│   ├── inventory.csv
│   ├── images/
│   └── README.md
├── requirments.txt
└── README.md
```

## 01_classes — where it started

This folder is basically me figuring out classes for the first time, using a `Firewall` class.

**`01_classes_basic.py`** — my very first attempt. Just a class with one method, `show_info()`, and you have to feed it every single detail (hostname, IP, vendor, username, password) every time you call it. Worked fine but got annoying real quick — felt like I wasn't really gaining anything over just writing a function.

**`02_classes_contructor.py`** — this is where `__init__` clicked for me. Instead of passing hostname/IP/etc. every call, the object just... remembers them. Also threw in an `inventory_loader()` function here that reads a list of firewalls from `inventory.csv`, checks each row isn't garbage (blank hostname, bad IP, unknown vendor, etc.), and spits out a list of `Firewall` objects. Felt like a genuine "aha" moment after the first file.

**`03_classes_steful.py`** — added actual behavior: `login()`, `logout()`, `backup_config()`, `reboot()`, `change_password()`. The fun part was adding a `logged_in` flag so you can't do things like backup or reboot before logging in — small thing, but it's the first time the class actually "remembers" what state it's in, not just data.

There's a `README.md` inside `01_classes` too with a bit more detail and screenshots of the output if you want to see what it actually looks like when you run these.

`inventory.csv` is just dummy lab data:

```
hostname,vendor,management_ip,username,password
FGT-HQ-A,Fortigate,192.168.100.100,admin,admin1234
FGT-HQ-P,Fortigate,192.168.100.101,admin,admin1234
```

(obviously fake creds, don't ever commit real ones)

## Running it

Nothing fancy needed — just Python 3 and the standard library, no pip installs yet.

```bash
git clone https://github.com/Anybody2007/python-oops-with-network-automation.git
cd python-oops-with-network-automation/01_classes
python 01_classes_basic.py
python 02_classes_contructor.py
python 03_classes_steful.py
```

## What's next

Still figuring this out as I go, but on my list:

- Inheritance — probably a base `NetworkDevice` class, then `Firewall` / `Switch` / `Router` under it
- Encapsulation / properties
- Actually hooking these classes up to something real (Netmiko, NAPALM, or RESTCONF)

Will keep adding folders as I go and update this whenever something new lands.