from Aux_Libs import Alib

class LISTA_TREE_VIEW():
    def __init__(self):
        self.texto = ''
        self.listas = []
    def add_texto(self,txt:str):
        self.texto += txt
    def add_lista(self):
        lista = LISTA_TREE_VIEW()
        self.listas.append(lista)
        return lista
    def end(self):
        aux_txt = ''
        if len(self.listas) > 0:
            for item in self.listas:
                aux_txt += item.end()
            aux_txt = f"""<ul>{aux_txt}</ul>"""
        aux_primeiro = ''
        if 'DATABASE' in self.texto:
            aux_primeiro = ' style="display:initial;"'
        txt_end = f"""<li{aux_primeiro}>
                        <div>{self.texto}</div>
                        {aux_txt}
                    </li>"""
            
        return txt_end

class FAZER_TABLE():
    def __init__(self):
        self.lines_thead = []
        self.lines_tbody = []
        self.tabela_completa_aux = False
        self.id_tbody_aux = ''
        self.styles_thead = ''
    def add_style_thead(self,txt:str):
        self.styles_thead = ' style="' + txt + '"'
    def add_line_head(self):
        linha = LINE_TABLE()
        self.lines_thead.append(linha)
        return linha
    def add_line_body(self):
        linha = LINE_TABLE()
        self.lines_tbody.append(linha)
        return linha
    def add_id_tbody(self,txt:str):
        self.id_tbody_aux = ' id="' + txt + '"'
    def tabela_completa(self, id_tabela:str ='', class_table:str ='', style_table:str =''):
        self.tabela_completa_aux = True
        if id_tabela != '':
            id_tabela = ' id="' + id_tabela + '"'
        if style_table != '':
            style_table = ' style="' + style_table + '"'
        if class_table != '':
            class_table = ' class="' + class_table + '"'
        self.class_table = class_table
        self.id_tabela = id_tabela
        self.style_table = style_table
    def end(self):
        txt = f'<thead{self.styles_thead}>'
        for item in self.lines_thead:
            txt += item.end()
        txt += '</thead>'

        txt += f'<tbody{self.id_tbody_aux}>'
        for item in self.lines_tbody:
            txt += item.end()
        txt += '</tbody>'
        if self.tabela_completa_aux:
            txt = f"""<table class="{self.class_table}"{self.id_tabela}{self.style_table}>{txt}</table>"""
        return txt

class LINE_TABLE():
    def __init__(self):
        self.celulas = []
        self.aling_center_var = False
        self.extra_styles = ''
        self.function = ''
        self.extra_classes = ''
        self.cell_type = 'td'
    def adicionar_celula(self,innerHTML):
        aux_obj = {'type': 'normal_cell','innerHTML':innerHTML}
        self.celulas.append(aux_obj)
    def adicionar_celula_especial(self,celula :str):
        aux_obj = {'type': 'cell_completa','innerHTML':celula}
        self.celulas.append(aux_obj)
    def adicionar_classes(self,class_aux:str):
        self.extra_classes += f" {class_aux}"
    def aling_center(self):
        self.aling_center_var = True
    def celulas_head(self):
        self.cell_type = 'th'
    def styles(self,txt: str):
        self.extra_styles = ' style="' + txt + '"'
    def adicionar_on_click(self, function: str):
        self.function = " onclick=" + function
    def end(self):
        if self.aling_center_var:
            texto = '<tr align="center"'
        else:
            texto = '<tr'
        if len(self.extra_classes) != 0:
            texto += f""" class="{self.extra_classes}" """
        if self.extra_styles != '':
            texto += self.extra_styles
        if self.function != '':
            texto += self.function
        texto += '>'
        for cell in self.celulas:
            if cell['type'] == 'normal_cell':
                texto += f"<{self.cell_type}>{cell['innerHTML']}</{self.cell_type}>"
            elif cell['type'] == 'cell_completa':
                texto += cell['innerHTML']
        texto += '</tr>'
        if len(self.celulas)>0 or len(self.celulas_especial)>0:
            return texto
        else:
            raise Exception(14,"HTML_CONTRUCTOR","LINE_TABLE")

class TESTE_HTML():
    def __init__(self,ROOT_DIR):
        self.dir = ROOT_DIR
        self.documento = Alib.readtxtfile_and_format(ROOT_DIR + '/base_tree_view.html')
        self.texto_body = ''
    def add_texto(self,txt:str):
        self.texto_body += txt
    def end(self,name_out ='nome_padrao'):
        path_out = f"""{self.dir}/{name_out}.html"""
        self.documento = self.documento.replace('LISTAS_SUBSTITUIR',self.texto_body)
        Alib.writefile(path_out,Alib.format_to_write(self.documento))

