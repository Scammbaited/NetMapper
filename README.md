# NetMapper: Network Mapping Tool

NetMapper is a Python-based tool that provides detailed network mapping by identifying active IPs, open ports, hostnames, SMB shares, and website titles across your local or specified network.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Versions](#versions)
    - [auto_ip](#auto_ip)
    - [custom_ip](#custom_ip)
3. [Installation](#installation)
4. [Usage](#usage)

## Prerequisites

Before using NetMapper, please ensure that you have the following prerequisites installed:

- Download and install Npcap from [npcap.com](https://npcap.com/#download). Npcap is necessary for the network scanning functionality of NetMapper.
- Install the necessary Python libraries listed in the `requirements.txt` file. You can do this by running \`pip install -r requirements.txt\` in your terminal. Make sure you run this command in the directory containing the `requirements.txt` file.

> **Note**: If you encounter any issues installing `netifaces`, please refer to this [StackOverflow thread](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst) for a solution.

## Versions

NetMapper is available in two versions:

### auto_ip

The auto_ip version automatically maps the network of the machine it's running on.

### custom_ip

The custom_ip version maps the network specified by the user in an input file.

Both versions discover active IP addresses, open ports, the hostname of the device at each IP, any available SMB shares, and website titles (if HTTP/HTTPS services are running).

## Installation

Clone the repository to your local machine and navigate into the project directory. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

For the auto_ip version, simply run the script `Auto_NetMapper.py` in the `auto_ip` folder:

```bash
python Auto_NetMapper.py
```

For the custom_ip version, first update the `ip.txt` file in the `custom_ip` folder with the IP range you want to scan. Then run the `custom_NetMapper.py` script:

```bash
python custom_NetMapper.py
```

Both versions will create a HTML file, `network_map.html`, in their respective directories which displays the mapping results in an easy-to-read format.
