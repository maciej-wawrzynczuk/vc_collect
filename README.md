# What's that?
It's quick and dirty script which collects VM's data from a vcenter. It uses PropertyCollector
so it's faster than typical PowerCLI script. I you have more than 1000 machines - you'll the
difference. Example usage:

    vc_collect --address localhost --user user --password password name guest.ipAddress

It will gather all VMs' names and IPs, then output them to JSON.

## Install
It requires Python 3. I highly recommend using virtualenv:

    virtualenv -p python3 my_env
	. my_env/bin/activate

Then just install it with pip.

    pip install git+git://github.com/maciej-wawrzynczuk/vc_collect.git

## Usage

    usage: vc_collect [-h] --address ADDRESS --user USER --password PASSWORD
		      [properties [properties ...]]

    Collect data from vcenter

    positional arguments:
      properties           list of properties to collect

    optional arguments:
      -h, --help           show this help message and exit
      --address ADDRESS    Vcenter adderess
      --user USER          Vcenter user
      --password PASSWORD  Vcenter password
