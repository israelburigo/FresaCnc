from ArquivoFrs import*

class Arquivos(object):

    def Le(self, file):
        
        extensao = file.name.split('.')[-1].upper()
        
        if extensao == 'FRS':
            return ArquivoFrs().Le(file.read())

        return None


