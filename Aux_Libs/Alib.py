import pymongo

OBJETO_GLOBAL = {}

def get_var(key):
    global OBJETO_GLOBAL
    return OBJETO_GLOBAL[key]

def VARIABLES_INIT():
    global OBJETO_GLOBAL
    for line in readlinesfile('config.txt'):
        y = line.rstrip().split('=')
        OBJETO_GLOBAL[y[0]] = y[1]

    aux_txt = ''
    if OBJETO_GLOBAL['LOGIN'] != '':
        aux_txt += f"""{OBJETO_GLOBAL['LOGIN']}:{OBJETO_GLOBAL['PASSWORD']}@"""
        
    OBJETO_GLOBAL['mongo_db_url'] = f"""mongodb://{aux_txt}{OBJETO_GLOBAL['URL']}:{OBJETO_GLOBAL['PORT']}"""
def readlinesfile(path):
    file = open(path,'r',encoding='latin-1')
    response = file.readlines()
    file.close()
    return response

def readtxtfile_and_format(path):
    dict_aux = {
        'Á': '&Aacute;',
        'á': '&aacute;',
        'Â': '&Acirc;',
        'â': '&acirc;',
        'À': '&Agrave;',
        'à': '&agrave;',
        'Ã': '&Atilde;',
        'ã': '&atilde;',
        'É': '&Eacute;',
        'é': '&eacute;',
        'Ê': '&Ecirc;',
        'ê': '&ecirc;',
        'È': '&Egrave;',
        'è': '&egrave;',
        'Í': '&Iacute;',
        'í': '&iacute;',
        'Î': '&Icirc;',
        'î': '&icirc;',
        'Ì': '&Igrave;',
        'ì': '&igrave;',
        'Ó': '&Oacute;',
        'ó': '&oacute;',
        'Ô': '&Ocirc;',
        'ô': '&ocirc;',
        'Ò': '&Ograve;',
        'ò': '&ograve;',
        'Õ': '&Otilde;',
        'õ': '&otilde;',
        'Ú': '&Uacute;',
        'ú': '&uacute;',
        'Û': '&Ucirc;',
        'û': '&ucirc;',
        'Ù': '&Ugrave;',
        'ù': '&ugrave;',
        'Ç': '&Ccedil;',
        'ç': '&ccedil;',
        'Ñ': '&Ntilde;',
        'ñ': '&ntilde;',
        '°': '&ordm;'}
    file = open(path,'r',encoding='utf-8')
    response = file.read()
    file.close()
    for item in dict_aux:
        response = response.replace(item,dict_aux[item])
    return response
def format_to_write(txt:str):
    txt = txt.replace('\u2013','-')
    txt = txt.replace('\u263a',' ')
    txt = txt.replace('\u2019',"'")
    txt = txt.replace('\u2014',"_")
    txt = txt.replace('\u201c','"')
    txt = txt.replace('\u201d','"')
    return txt

def writefile(path,txt):
    file = open(path,'w',encoding='latin-1')
    file.write(format_to_write(txt))
    file.close()

def format_numero(qtd):
    if type(qtd) == str:
        qtd = float(qtd)
    if (qtd - int(qtd) > 0):
        return '{0:.2f}'.format(qtd).replace('.',',')
    else:
        return '{0:.0f}'.format(qtd).replace('.',',')
def format_txt(texto: str):
    dict_aux = {
        'Á': '&Aacute;',
        'á': '&aacute;',
        'Â': '&Acirc;',
        'â': '&acirc;',
        'À': '&Agrave;',
        'à': '&agrave;',
        'Ã': '&Atilde;',
        'ã': '&atilde;',
        'É': '&Eacute;',
        'é': '&eacute;',
        'Ê': '&Ecirc;',
        'ê': '&ecirc;',
        'È': '&Egrave;',
        'è': '&egrave;',
        'Í': '&Iacute;',
        'í': '&iacute;',
        'Î': '&Icirc;',
        'î': '&icirc;',
        'Ì': '&Igrave;',
        'ì': '&igrave;',
        'Ó': '&Oacute;',
        'ó': '&oacute;',
        'Ô': '&Ocirc;',
        'ô': '&ocirc;',
        'Ò': '&Ograve;',
        'ò': '&ograve;',
        'Õ': '&Otilde;',
        'õ': '&otilde;',
        'Ú': '&Uacute;',
        'ú': '&uacute;',
        'Û': '&Ucirc;',
        'û': '&ucirc;',
        'Ù': '&Ugrave;',
        'ù': '&ugrave;',
        'Ç': '&Ccedil;',
        'ç': '&ccedil;',
        'Ñ': '&Ntilde;',
        'ñ': '&ntilde;',
        '°': '&ordm;'} 
    for item in dict_aux:
        texto = texto.replace(item,dict_aux[item])
    return texto

def CONNECT_DB():
    aux_password = get_var('PASSWORD')
    if not aux_password == '':
        BD_CLIENT = pymongo.MongoClient(get_var('URL'),int(get_var('PORT')), username=get_var('LOGIN'), password=aux_password)
    else:
        BD_CLIENT = pymongo.MongoClient(get_var('URL'),int(get_var('PORT')))
    return BD_CLIENT
