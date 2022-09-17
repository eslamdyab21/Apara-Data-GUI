import subprocess


        

def UrlToCheck(url):
    proc = subprocess.Popen('dirhunt ' + url + ' --to-file report.json --delay 0.005', stdout=subprocess.PIPE, shell=True)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        else: 
            yield line
            
        