import paramiko
from time import sleep
from TestConfig.web_log import WebLog


class SSH(WebLog):
    def MakePublishingPoint(self):
        self.info_log("Start setting up your USP publishing point")
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("10.1.0.130", port="22", username="ubuntu", password="ubuntu")
        ssh_cmd = ssh.get_transport().open_session()
        ssh_cmd.get_pty()
        ssh_cmd.invoke_shell()
        ssh_cmd.send("sudo su" + "\n")
        ssh_cmd.send("cd /var/www/usp-evaluation/" + "\n")
        ssh_cmd.send(f"rm -rf jacob; ./makePublishingScte35.sh jacob" + "\n")
        while True:
            if ssh_cmd.recv_ready():
                output = ssh_cmd.recv(65536)
                # self.exec_log(output.decode("utf-8"))
            else:
                sleep(0.2)
                if not (ssh_cmd.recv_ready()):
                    break
        self.info_log("USP publishing point setup complete")
        ssh.close()
