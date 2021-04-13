import subprocess

configuracoes = {
    "PORT":'27080',
    "URL":'localhost',
    "PASSWORD":'',
    "LOGIN":'',
    "path_variety":'C:\\...\\variety.js',
    "path_mongo_exe":'C:\\...\\mongo.exe'
}

aux = ''
for item in configuracoes:
    aux += f"""{item}={configuracoes[item]}\n"""

file = open('config.txt','w')
file.write(aux)
file.close()

aux = subprocess.Popen('py -m pip install pymongo',shell=True)


aux.wait()

#Comentario Davi

