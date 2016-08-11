import urllib
import os
import getpass
import subprocess
import tarfile

class ExtractPot:
    
    def __init__(self, program_name, locale):
        self.program_name = program_name
        self.locale = locale

        self.user = getpass.getuser()
        self.home = ""
        
        if self.user != "root":
            self.home = "/home/"+self.user
        else:
            self.home = "/root"

        self.srpm_dir = self.home+"/.autotest/srpm"
        self.srpm_path = self.srpm_dir+"/"+self.program_name+".src.rpm"
        
        if not os.path.exists(self.home+"/.autotest/pot_files"):
            os.makedirs(self.home+"/.autotest/pot_files")
    
        if not os.path.exists(self.home+"/.autotest/srpm"):
            os.makedirs(self.home+"/.autotest/srpm")


    def extractPot(self):
        top_url = "https://kojipkgs.fedoraproject.org/packages"
        pkg_path = subprocess.check_output(['rpm -qa '+self.program_name+' --queryformat %{NAME}/%{VERSION}/%{RELEASE}'], shell=True)
        pkg_name = subprocess.check_output(['rpm -qa '+self.program_name+' --queryformat %{NAME}-%{VERSION}-%{RELEASE}'], shell=True)
        tar_name = subprocess.check_output(['rpm -qa '+self.program_name+' --queryformat %{NAME}-%{VERSION}'], shell=True)
        pkg_url = top_url+"/"+pkg_path+"/src/"+pkg_name+".src.rpm"
        
        urllib.urlretrieve(pkg_url, self.srpm_path)

        os.chdir(self.srpm_dir)

        command = "rpm2cpio "+self.program_name+".src.rpm | cpio -idm"
        subprocess.call(command, shell=True)

        command = "tar -xf "+tar_name+".tar.xz"
        subprocess.call(command, shell=True)

        os.chdir(self.srpm_dir+"/"+tar_name+"/po")

        command = "intltool-update -p"
        subprocess.call(command, shell=True)

        pot_name = self.program_name+".pot"

        os.rename(pot_name, self.home+"/.autotest/pot_files/"+pot_name)

        os.chdir(os.path.abspath(os.path.dirname(__file__)))