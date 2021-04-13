import subprocess
import os
import json

from Aux_Libs import Alib
from Aux_Libs.constructors import LISTA_TREE_VIEW,FAZER_TABLE,TESTE_HTML

ROOT_DIR = os.path.split(os.path.abspath(__file__))[0]
Alib.VARIABLES_INIT()
DB_CLIENT = Alib.CONNECT_DB()

#COMENTARIO ARTHUR

def fazer_str_porcentagem(superior,inferior):
    try:
        return f"""{Alib.format_numero(superior)}/{Alib.format_numero(inferior)} = {Alib.format_numero(superior*100/inferior)}%"""
    except:
        return 'ERRO %'
def fazer_tree(lista:list,lista_pai:LISTA_TREE_VIEW,db,collection_aux):
    total = 0
    for item in lista:
        if item['percentContaining'] == 100:
            total = item['totalOccurrences']
        if not "." in item['_id']['key']:
            nova_lista = lista_pai.add_lista()
            aux_occoridos = Alib.format_numero(item['totalOccurrences'])
            nova_lista.add_texto(f"""<strong>{item['_id']['key']}</strong> <br>QTD:{aux_occoridos}<br>{Alib.format_numero(item["percentContaining"])}%""")
            for tipo in item['value']['types']:
                tipo_list = nova_lista.add_lista()
                aux_txt = f"""class <strong>{tipo}</strong> <br>{fazer_str_porcentagem(item['value']['types'][tipo],item['totalOccurrences'])}"""
                tipo_list.add_texto(aux_txt)
                if tipo == 'Object' or tipo == 'Array':
                    fazer_tree_extra(lista,tipo_list,item['totalOccurrences'],item['_id']['key'],tipo,db,collection_aux)
                else:
                    fazer_list_aggregate(item['_id']['key'],nova_lista,db,collection_aux,item['totalOccurrences'])
    lista_pai.add_texto(f"""<br>QTD: {Alib.format_numero(total)}""")
def fazer_tree_extra(lista:list,lista_pai:LISTA_TREE_VIEW,universo_total,key:str,tipo_extra:str,db,collection_aux):
    lista_feitos = []
    lista_feitos_2 = []
    aux_empty_array = False
    if tipo_extra == 'Array':
        aux_empty_array = True
    for item in lista:
        condicao = False
        if tipo_extra == 'Object':
            if item['_id']['key'].startswith(key + ".") and not item['_id']['key'].startswith(key + ".XX."):
                condicao = True
        elif tipo_extra == 'Array':
            if item['_id']['key'].startswith(key + ".XX."):
                condicao = True
                aux_empty_array = False
        if condicao and comparacao_feitos(item['_id']['key'],lista_feitos):
            nova_lista = lista_pai.add_lista()
            aux_occoridos = Alib.format_numero(item['totalOccurrences'])
            nova_lista.add_texto(f"""<strong>{item['_id']['key']}</strong> <br>QTD:{aux_occoridos}<br>{Alib.format_numero(item['totalOccurrences']*100/universo_total)}%""")
            for tipo in item['value']['types']:
                tipo_list = nova_lista.add_lista()
                aux_txt = f"""class <strong>{tipo}</strong> <br>{fazer_str_porcentagem(item['value']['types'][tipo],item['totalOccurrences'])}"""
                tipo_list.add_texto(aux_txt)
                if tipo == 'Object' or tipo == 'Array':
                    fazer_tree_extra(lista,tipo_list,item['totalOccurrences'],item['_id']['key'],tipo,db,collection_aux)
                    lista_feitos.append(item['_id']['key'] + ".")
                else:
                    if not item['_id']['key'] in lista_feitos_2:
                        lista_feitos_2.append(item['_id']['key'])
                        fazer_list_aggregate(item['_id']['key'],nova_lista,db,collection_aux,item['totalOccurrences'])
    if aux_empty_array:
        lista_pai.add_texto("<br>ARRAY(s) VAZIO")

def fazer_list_aggregate(key:str,lista_pai:LISTA_TREE_VIEW,db,collection_aux,total):
    key = key.replace('.XX.',".$.")
    id_auxiliar =  key.replace(".$.",'.')
    lista_aux = lista_pai.add_lista()
    lista_aux.add_texto('COMMON ITENS')
    itens_list = lista_aux.add_lista()
    aggregate_array_end = []
    key_split = key.split('.$.')[:-1]
    soma_key = ''
    for unwind in key_split:
        soma_key += unwind
        aux = {'$unwind': {'path': '$' + soma_key}}
        aggregate_array_end.append(aux)
        soma_key += '.'
    aggregate_array_end.append({'$group': {
                    '_id': '$' + id_auxiliar,
                    'SOMA': {'$sum': 1}}})
    aggregate_array_end.append({'$sort': {'SOMA': -1}})
    aggregate_array_end.append({'$limit': 30})

    table_aux = FAZER_TABLE()
    table_aux.tabela_completa(class_table='')
    line_aux = table_aux.add_line_head()
    line_aux.aling_center()
    line_aux.celulas_head()
    line_aux.adicionar_celula('ITEM')
    line_aux.adicionar_celula('CONT')
    line_aux.adicionar_celula('%')
    for item in DB_CLIENT[db][collection_aux].aggregate(aggregate_array_end):
        line_aux = table_aux.add_line_body()
        line_aux.aling_center()
        line_aux.adicionar_celula(format_item(item["_id"]))
        line_aux.adicionar_celula(str(item["SOMA"]))
        line_aux.adicionar_celula(Alib.format_numero(item["SOMA"]*100/total))
    itens_list.add_texto(table_aux.end())

def comparacao_feitos(key,lista_feitos):
    for item in lista_feitos:
        if item in key:
            return False
    return True
def format_item(txt:str):
    txt = str(txt).replace('<','').replace('>','').replace("'",'')
    if len(txt) > 100:
        txt = 'LONG STRING'
    elif len(txt) == 0:
        txt = "NO DATA"
    elif txt == 'None':
        txt = "NO DATA"
    return txt
def get_json(database:str,collection:str,DB_url:str,DB_port:str):
    path_variety = Alib.get_var('path_variety')
    path_mongo_exe = Alib.get_var('path_mongo_exe')
    mongo_db_url = Alib.get_var('mongo_db_url')
    arg = f""" "{path_mongo_exe}" "{mongo_db_url}/{database}?authSource=admin&readPreference=primary&ssl=false" --eval "var collection = '{collection}', outputFormat='json'" "{path_variety}" """
    aux = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    p_aux = aux.stdout.readlines()[22:]
    lines_aux = ''
    for line in p_aux:
        lines_aux += line.decode('latin-1')
    if lines_aux == '':
        return []
    json_aux = json.loads(lines_aux)
    index_exclude = []
    item_exclude_end = {
        'SALDO_ORCAMENTO_': {
                "_id" : {
                        "key" : "SALDO_ORCAMENTO"
                },
                "value" : {
                        "types" : {}
                },
                "totalOccurrences" : 0,
                "percentContaining" : 0
        }
    }
    cont = - 1
    for item in json_aux:
        cont += 1
        for item_2 in item_exclude_end:
            if item_2 in item['_id']['key']:
                index_exclude.append(cont)
                for tipo in item['value']['types']:
                    if not tipo in item_exclude_end[item_2]['value']['types']:
                        item_exclude_end[item_2]['value']['types'][tipo] = 0
                    item_exclude_end[item_2]['value']['types'][tipo] += item['value']['types'][tipo]
                item_exclude_end[item_2]['totalOccurrences'] += item['totalOccurrences']
                item_exclude_end[item_2]['percentContaining'] += item['percentContaining']
    if len(index_exclude) > 0:
        index_exclude.sort(reverse=True)
        for item in index_exclude:
            del json_aux[item]
        for item in item_exclude_end:
            if item_exclude_end[item]['totalOccurrences'] > 0:
                json_aux.append(item_exclude_end[item])
    return json_aux

def database_map_to_HTML(DB_CLIENT):
    aux = DB_CLIENT.list_database_names()
    for item in ['admin','local','config']:
        aux.remove(item)
    lista_tree = LISTA_TREE_VIEW()
    lista_tree.add_texto(f"""<strong>TOTAL DATABASE</strong>""")
    for db in aux:
        print("-"*100)
        print('DB:',db,'\n')
        aux_db = lista_tree.add_lista()
        aux_db.add_texto(f"""<strong>{db}</strong>""")
        aux_2 = DB_CLIENT[db].list_collections()
        for collection_aux in aux_2:
            collection_aux = collection_aux['name']
            aux_collection = aux_db.add_lista()
            aux_collection.add_texto(f"""<strong>{collection_aux}</strong>""")
            aux_json = get_json(db,collection_aux,DB_CLIENT.address[0],str(DB_CLIENT.address[1]))
            if len(aux_json) == 0:
                print('COLLECTION:',collection_aux,"[EMPTY]")
            else:
                fazer_tree(aux_json,aux_collection,db,collection_aux)
                print('COLLECTION:',collection_aux," [OK]")


    aux = TESTE_HTML(ROOT_DIR)
    aux.add_texto(Alib.format_txt(lista_tree.end().replace(".XX.",".$.")))
    del lista_tree
    aux.end('DB_VIEW_HTML')

database_map_to_HTML(DB_CLIENT)
