
import datetime
import subprocess

date = datetime.datetime.now().strftime("%Y-%m-%d")

nexus_url = "example.com"
appversion = '1'
#print(date)
comp_open = open("components")
#print(comp_open.read())




comp_read = comp_open.read().splitlines()
print(comp_read)

for i in comp_read :
    try:
        subprocess.run(f"echo '{i}' ; sed -i 's|image: .*|image: '{nexus_url}/{i}-{date}:v{appversion}'|g' k8s/'{i}'/deployment.yaml", shell=True)
    except:
        print('Manifests are not added properly')
    
