# Stumpy Macro

A macro for Bee Swarm Simulator, written in Python.

## Features
* GUI for easy setup
* Pine tree / Stump / Pineapple / Rose gathering
* E_lol pattern
* Mondo buff (not loot)
* Wealth clock
* Disconnect check / auto reconnect
* Webhook integration

## How to install
### Step 1: Install Python (3.11.1)
Visit https://www.python.org/downloads/release/python-3111/  
Scroll down to the downloads, and download the **installer** for your respective operating system.  
Run the installer.
### Step 2: Download the macro
In this repository, scroll up and click the green "Code" button.    
Click "Download ZIP".  
Go to where you downloaded the macro and extract the zip file.  
### Step 3: Install dependencies
Open a new Terminal and navigate to the folder where you extracted the macro.  
Do this by running the following command, replacing <path-to-macro> with the path to the extracted folder:
```shell
cd <path-to-macro>
```
Then, run the following command:
```shell
python3 -m pip install -r requirements.txt
```
### Step 4: Run the macro
Run the following command:
```shell
python3 main.py
```
During this process, you may be prompted to enable certain system settings. Please go ahead and enable them, as the macro needs these permissions to function.

## How to use
### Step 1: Setup
When you run the macro, you will be greeted with a window.  
In this window, you will be able to configure the macro.  
By default, the macro will be configured to gather in pine tree with the e_lol pattern.  
### Step 2: Run
Open Bee Swarm Simulator and go to any hive. Claim the hive.  
Run the macro by pressing "f1".  
Stop the macro by pressing "f3".