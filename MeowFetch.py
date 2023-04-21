import sys
from psutil import cpu_count, cpu_freq, virtual_memory, boot_time, disk_partitions, disk_usage
from colorama import init as coloramaInit, Fore
from termcolor import colored, COLORS
from math import floor, log, pow
from datetime import timedelta
from sys import platform, argv
from getpass import getuser
from platform import uname
from GPUtil import getGPUs
from time import time
class AmeyFetch:
	def __init__(self):
		if platform == "win32":
			coloramaInit(convert=True)
		else:
			coloramaInit(convert=False)
		self.host_name = uname().node
		self.user_name = getuser()
		self.OS = f"{uname().system} {uname().release}"
		self.OS_version = uname().version
		self.cpu_name = uname().processor
		self.cpu_count = cpu_count(logical=False)
		self.cpu_thread = cpu_count(logical=True)
		self.cpu_freq_max = cpu_freq().max
		try:
			self.gpu_name = getGPUs()[0].name
			self.gpu_mem = f"{getGPUs()[0].memoryUsed} MiB / {getGPUs()[0].memoryTotal} MiB"
		except:
			self.gpu_name = "N/A"
			self.gpu_mem = "N/A"
		self.ram_usage = f"{self.memCon(virtual_memory().used)} / {self.memCon(virtual_memory().total)}"
		self.uptime = timedelta(seconds=(time()-boot_time()))
		self.disk_name = disk_partitions()[0].device.replace("\\", "")
		self.disk_usage = f"{self.memCon(disk_usage(disk_partitions()[0].mountpoint).used)} / {self.memCon(disk_usage(disk_partitions()[0].mountpoint).total)}"
		self.ameyFetchLogo = []
		self.totalInfo = []
		self.ascii_logo_image = "logo.txt"
		self.ascii_logo_color = "white"
	def memCon(self, size_bytes):
		if size_bytes == 0:
			return "0B"
		size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
		i = int(floor(log(size_bytes, 1024)))
		p = pow(1024, i)
		s = round(size_bytes / p, 2)
		return "%s %s" % (s, size_name[i])
	def getLogo(self, systemArgs=[]):
		if len(self.ameyFetchLogo)==0:
			for sysArgs in systemArgs:
				if sysArgs.startswith("--ascii_logo:"):
					self.ascii_logo_image = sysArgs.replace("--ascii_logo:", "")
				if sysArgs.startswith("--ascii_color:"):
					logo_color_temp = sysArgs.replace("--ascii_color:", "").lower()
					if self.ascii_logo_color in list(COLORS.keys()):
						self.ascii_logo_color = logo_color_temp
			with open(self.ascii_logo_image, "r") as logoFile:
				for line in logoFile:
					line = line.rstrip("\n")
					if line.endswith("."):
						line = line.rstrip(".")
						self.ameyFetchLogo.append(f"{colored(text=line, color=self.ascii_logo_color)}")
		return self.ameyFetchLogo

if __name__ == "__main__": 
	ameyFetch = AmeyFetch()
	userNameWithHostName = f"{Fore.YELLOW}{ameyFetch.user_name}{Fore.RESET}@{Fore.YELLOW}{ameyFetch.host_name}{Fore.RESET}"
	finalPrintDesign = "-"*len(userNameWithHostName)
	ameyFetch.totalInfo.append(userNameWithHostName)
	ameyFetch.totalInfo.append(finalPrintDesign)
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}OS:{Fore.RESET} {ameyFetch.OS}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}HOST:{Fore.RESET} {ameyFetch.host_name}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}KERNEL:{Fore.RESET} {ameyFetch.OS_version}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}UPTIME:{Fore.RESET} {ameyFetch.uptime}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}CPU:{Fore.RESET} {ameyFetch.cpu_name}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}CPU CORES:{Fore.RESET} {ameyFetch.cpu_count}/{ameyFetch.cpu_thread}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}CPU FREQ:{Fore.RESET} {ameyFetch.cpu_freq_max}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}GPU:{Fore.RESET} {ameyFetch.gpu_name}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}GPU MEM:{Fore.RESET} {ameyFetch.gpu_mem}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}SYSTEM MEM:{Fore.RESET} {ameyFetch.ram_usage}")
	ameyFetch.totalInfo.append(f"{Fore.YELLOW}DISK ({ameyFetch.disk_name}):{Fore.RESET} {ameyFetch.disk_usage}")
	ameyFetchGetLogo = ameyFetch.getLogo(systemArgs=argv)
	try:
		ascii_prefix = " "*(len(ameyFetchGetLogo[0])-9)
	except:
		ascii_prefix = ""
	if (len(ameyFetch.totalInfo)>len(ameyFetchGetLogo)):
		for i in range(len(ameyFetch.totalInfo)):
			try:
				print(f"{ameyFetchGetLogo[i]}{ameyFetch.totalInfo[i]}")
			except:
				print(f"{ascii_prefix}{ameyFetch.totalInfo[i]}")
	else:
		for i in range(len(ameyFetchGetLogo)):
			try:
				print(f"{ameyFetchGetLogo[i]}{ameyFetch.totalInfo[i]}")
			except:
				print(f"{ameyFetchGetLogo[i]}")
