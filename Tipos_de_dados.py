from enum import Enum, auto
from dataclasses import dataclass

class Direcoes(Enum):
    '''Quatro pontos cardeais '''
    SUL = auto()
    NORTE = auto()
    LESTE = auto()
    OESTE = auto()


def direcao_oposta(direcao: Direcoes) -> Direcoes:
    '''Indica o ponto cardeal oposto a *direcao* fornecida.
    Exemplos:
    >>> direcao_oposta(Direcoes.OESTE).name
    'LESTE'
    >>> direcao_oposta(Direcoes.LESTE).name
    'OESTE'
    >>> direcao_oposta(Direcoes.SUL).name
    'NORTE'
    >>> direcao_oposta(Direcoes.NORTE).name
    'SUL'
    '''

    if direcao == Direcoes.SUL:
        oposta = Direcoes.NORTE

    elif direcao == Direcoes.NORTE:
        oposta = Direcoes.SUL

    elif direcao == Direcoes.LESTE:
        oposta = Direcoes.OESTE

    else:
        oposta = Direcoes.LESTE

    return oposta


def ortogonal_horario(direcao: Direcoes) -> Direcoes:
    '''Indica o ponto cardeal a 90° no sentido horário da *direcao* fornecida.
    Exemplos:
    >>> ortogonal_horario(Direcoes.OESTE).name
    'NORTE'
    >>> ortogonal_horario(Direcoes.LESTE).name
    'SUL'
    >>> ortogonal_horario(Direcoes.SUL).name
    'OESTE'
    >>> ortogonal_horario(Direcoes.NORTE).name
    'LESTE'
    '''

    if direcao == Direcoes.OESTE:
        ortog = Direcoes.NORTE

    elif direcao == Direcoes.LESTE:
        ortog = Direcoes.SUL

    elif direcao == Direcoes.SUL:
        ortog = Direcoes.OESTE

    else:
        ortog = Direcoes.LESTE
    
    return ortog


def ortogonal_anti_horario(direcao: Direcoes) -> Direcoes:
    '''Indica o ponto cardeal a 90° no sentido anti-horário
    da *direcao* fornecida.
    Exemplos:
    >>> ortogonal_anti_horario(Direcoes.OESTE).name
    'SUL'
    >>> ortogonal_anti_horario(Direcoes.LESTE).name
    'NORTE'
    >>> ortogonal_anti_horario(Direcoes.SUL).name
    'LESTE'
    >>> ortogonal_anti_horario(Direcoes.NORTE).name
    'OESTE'
    '''

    return ortogonal_horario(ortogonal_horario(ortogonal_horario(direcao)))


def direciona(dir_atual: Direcoes, dir_desejada) -> str:
    '''Indica quantos graus no sentido horário são necessários para
    virar da *dir_atual* para a *dir_desejada*.
    Caso *dir_atual* = *dir_desejada*, será retornado 0°.
    Exemplos:
    >>> direciona(Direcoes.OESTE, Direcoes.SUL)
    '270°'
    >>> direciona(Direcoes.NORTE, Direcoes.NORTE)
    '0°'
    >>> direciona(Direcoes.LESTE, Direcoes.OESTE)
    '180°'
    '''

    if dir_atual == dir_desejada:
        graus = '0°'

    else:
        if ortogonal_horario(dir_atual) == dir_desejada:
            graus = '90°'

        else:
            if ortogonal_horario(ortogonal_horario(dir_atual)) == dir_desejada:
                graus = '180°'

            else:
                graus = '270°'
        
    return graus


class Status_Quo(Enum):
    '''Representa a situação atual de um elevador.'''
    SUBINDO = auto()
    PARADO = auto()
    DESCENDO = auto()

def desce_ou_sobe(andar_atual: int, andar_solicitado: int) -> Status_Quo:
    '''Determina o Status_Quo do elevador imediatamente após ele ser solicitado
    a ir ao *andar_solicitado*.
    Conseidera-se que o elevador está parado no *andar_atual*.
    Exemplos:
    >>> desce_ou_sobe(0,1).name
    'SUBINDO'
    >>> desce_ou_sobe(0,-1).name
    'DESCENDO'
    >>> desce_ou_sobe(10,10).name
    'PARADO'
    '''

    if andar_atual == andar_solicitado:
        situacao = Status_Quo.PARADO

    elif andar_atual < andar_solicitado:
        situacao = Status_Quo.SUBINDO

    else:
        situacao = Status_Quo.DESCENDO

    return situacao


def verifica(estado_atual: Status_Quo, estado_desejado: Status_Quo) -> bool:
    '''Verifica se um elevador pode passar de um Status_Quo para outro.
    Considera-se que um elevador só pode começar a se mover caso esteja parado.
    Exemplos:
    >>> verifica(Status_Quo.PARADO, Status_Quo.SUBINDO)
    True
    >>> verifica(Status_Quo.PARADO, Status_Quo.DESCENDO)
    True
    >>> verifica(Status_Quo.PARADO, Status_Quo.PARADO)
    True
    >>> verifica(Status_Quo.DESCENDO, Status_Quo.SUBINDO)
    False
    >>> verifica(Status_Quo.DESCENDO, Status_Quo.DESCENDO)
    True
    >>> verifica(Status_Quo.DESCENDO, Status_Quo.PARADO)
    True
    >>> verifica(Status_Quo.SUBINDO, Status_Quo.SUBINDO)
    True
    >>> verifica(Status_Quo.SUBINDO, Status_Quo.DESCENDO)
    False
    >>> verifica(Status_Quo.SUBINDO, Status_Quo.PARADO)
    True
    '''

    if estado_atual == Status_Quo.SUBINDO:

        if estado_desejado == Status_Quo.DESCENDO:
            possivel = False

        else:
            possivel = True

    elif estado_atual == Status_Quo.DESCENDO:
        
        if estado_desejado == Status_Quo.SUBINDO:
            possivel = False

        else:
            possivel = True

    else:
        possivel = True

    return possivel


@dataclass
class Data:
    '''Representa datas no formato dd/mm/aaaa.
    Datas anteriores a Cristo são representadas com anos negativos.
    Exemplo: 18/12/400 A.C == 18/12/-400.'''
    dia: str
    mes: str
    ano: str


def converte(data: str) -> Data:
    '''Converte *data* no formato 'dd/mm/aaaa' no seu equivalente em Data.
    Exemplos:
    >>> converte('01/04/1992')
    Data(dia='01', mes='04', ano='1992')
    >>> converte('31/12/2015')
    Data(dia='31', mes='12', ano='2015')
    '''

    dia = data[:2]
    mes = data[3:5]
    ano = data[6:]

    return Data(dia,mes,ano)


def confere(data: Data) -> bool:
    '''Verifica se *data* representa o último dia de um ano.
    Exemplos:
    >>> confere(Data(dia='31', mes='12', ano='2024'))
    True
    >>> confere(Data(dia='15', mes='12', ano='0101'))
    False
    '''

    return data.dia == '31' and data.mes == '12'


def primazia(primeira: Data, segunda: Data) -> bool:
    '''Verifica se a *primeira* data precede a *segunda*.
    Caso ambas sejam iguais, retorna-se False.
    Exemplos:
    >>> primazia(Data(dia='14',mes='08',ano='0001'),Data(dia='17',mes='05',ano='0002'))
    True
    >>> primazia(Data(dia='14',mes='08',ano='0001'),Data(dia='17',mes='05',ano='-0002'))
    False
    >>> primazia(Data(dia='14',mes='10',ano='0100'),Data(dia='14',mes='10',ano='0100'))
    False
    >>> primazia(Data(dia='14',mes='09',ano='0100'),Data(dia='14',mes='10',ano='0100'))
    True
    >>> primazia(Data(dia='15',mes='10',ano='0100'),Data(dia='14',mes='10',ano='0100'))
    False
    '''

    
    if int(primeira.ano) > int(segunda.ano):
        verifica = False

    elif int(primeira.ano) < int(segunda.ano):
        verifica = True

    else:
        
        if int(primeira.mes) < int(segunda.mes):
            verifica = True

        else:
            if int(primeira.dia) < int(segunda.dia):
                verifica = True

            else:
                verifica = False

    return verifica

def data_valida(data: Data) -> bool:
    '''Verifica se a *data* fornecida é válida.
    Exemplos:
    >>> data_valida(Data(dia='29', mes='02', ano='0004'))
    True
    >>> data_valida(Data(dia='29', mes='02', ano='2025'))
    False
    >>> data_valida(Data(dia='31', mes='04', ano='2024'))
    False
    >>> data_valida(Data(dia='14', mes='13', ano ='5050'))
    False
    >>> data_valida(Data(dia='32', mes='12', ano='2010'))
    False
    >>> data_valida(Data(dia='29', mes='02', ano='1500'))
    False
    >>> data_valida(Data(dia='31', mes='05', ano='7089'))
    True
    >>> data_valida(Data(dia='29', mes='02', ano='0004'))
    True
    '''

    ano = int(data.ano)
    
    if int(data.mes) > 12:
        valido = False

    elif (ano%4 == 0 and ano%100 != 0) or ano%400 == 0:
        if data.mes == '01' or data.mes == '05' or data.mes == '07' or data.mes == '08' or data.mes == '10' or data.mes == '12':
            if 0 < int(data.dia) <= 31:
                valido = True
            else:
                valido = False
        elif data.mes == '03' or data.mes == '04' or data.mes == '06' or data.mes == '09' or data.mes =='11':
            if 0 < int(data.dia) <= 30:
                valido = True
            else:
                valido = False

        else:
            if 0 < int(data.dia) <= 29:
                valido = True
            else:
                valido = False
    
    else:
        if data.mes == '01' or data.mes == '05' or data.mes == '07' or data.mes == '08' or data.mes == '10' or data.mes == '12':
            if 0 < int(data.dia) <= 31:
                valido = True
            else:
                valido = False
        elif data.mes == '03' or data.mes == '04' or data.mes == '06' or data.mes == '09' or data.mes =='11':
            if 0 < int(data.dia) <= 30:
                valido = True
            else:
                valido = False

        else:
            if 0 < int(data.dia) <= 28:
                valido = True
            else:
                valido = False

    return valido


@dataclass
class Resolucao:
    '''Representa a resolução de uma tela ou imagem na forma dos seus valores
    de altura e largura em pixels.'''

    altura_pix: int
    comprimento_pix: int

def megapixels(resolucao: Resolucao) -> float:
    '''Calcula a quantidade de megapixels contidos em uma imagem dada
    a sua *resolucao*.
    Exemplos:
    >>> megapixels(Resolucao(altura_pix=10**3 ,comprimento_pix=10**3))
    1.0
    >>> megapixels(Resolucao(altura_pix=10**6 ,comprimento_pix=10**6))
    1000000.0
    >>> megapixels(Resolucao(altura_pix=10 ,comprimento_pix=100))
    0.001
    '''
    
    return (resolucao.altura_pix*resolucao.comprimento_pix)/10**6
    
class Aspecto(Enum):
    '''Representa o aspect ratio de uma tela ou imagem, em pixels.'''
    Ratio_16_9= auto()
    Ratio_4_3 = auto()
    Ratio_3_2 = auto()
    Ratio_1_1 = auto()


def aspect_ratio(resolucao: Resolucao) -> Aspecto:
    '''Indica se *resolucao* apresenta aspecto 16:9, 4:3, 3:2, 1:1, ou nenhum.
    Exemplos:
    >>> aspect_ratio(Resolucao(1920,1080)).name
    'Ratio_16_9'
    >>> aspect_ratio(Resolucao(7600,5700)).name
    'Ratio_4_3'
    >>> aspect_ratio(Resolucao(2700, 1800)).name
    'Ratio_3_2'
    >>> aspect_ratio(Resolucao(10000,10000)).name
    'Ratio_1_1'
    '''

    if resolucao.altura_pix * 9 == resolucao.comprimento_pix * 16:
        ratio = Aspecto.Ratio_16_9

    elif resolucao.altura_pix * 3 == resolucao.comprimento_pix * 4:
        ratio = Aspecto.Ratio_4_3

    elif resolucao.altura_pix * 2 == resolucao.comprimento_pix * 3:
        ratio = Aspecto.Ratio_3_2

    else:
        ratio = Aspecto.Ratio_1_1

    return ratio


def exibivel(imagem: Resolucao, tela: Resolucao) -> bool:
    '''Verifica se *imagem* cabe em *tela* sem a necessidade de rotação ou mudança de tamanho.
    Exemplos:
    >>> exibivel(Resolucao(1000, 1000), Resolucao(1000, 1000))
    True
    >>> exibivel(Resolucao(1200, 1000), Resolucao(1000, 1200))
    False
    '''

    if (imagem.altura_pix == tela.altura_pix) and (imagem.comprimento_pix == tela.comprimento_pix):
        exibe = True

    else:
        exibe = False

    return exibe
            
    







    








    




















    
    
    



















































    
    
