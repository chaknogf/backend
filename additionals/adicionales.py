from fastapi import APIRouter

#Region: ApiRouter
router = APIRouter()



#Region: Discionarios

nacionalidad = {
    1: "Guatemalteca",
    2: "Beliceña",
    3: "Salvadoreña",
    4: "Hondureña",
    5: "Nicaragüense",
    6: "Costarricense",
    7: "Panameña",
    8: "Mexicana",
    9: "Otro_pais"
}

idiomas = {
    1: 'Achi',
    2: 'Akateka',
    3: 'Awakateka',
    4: 'Chorti',
    5: 'Chalchiteka',
    6: 'Chuj',
    7: 'Itza',
    8: 'Ixil',
    9: 'Jakalteka',
    10: 'Kaqchikel',
    11: 'Kiche',
    12: 'Mam',
    13: 'Mopan',
    14: 'Poqomam',
    15: 'Pocomchi',
    16: 'Qanjobal',
    17: 'Qeqchi',
    18: 'Sakapulteka',
    19: 'Sipakapensa',
    20: 'Tektiteka',
    21: 'Tzutujil',
    22: 'Uspanteka',
    23: 'No_indica',
    24: 'Español',
    25: 'Inglés',
    26: 'Francés',
    27: 'Portugues',
    28: 'Japones',
    29: 'Mandarin',
    30: 'Koreano',
    31: 'Italiano'
    
}

educ = {
    1: 'No_aplica',
    2: 'Pre_Primaria',
    3: 'Primaria',
    4: 'Básicos',
    5: 'Diversificado',
    6: 'Universidad',
    7: 'Ninguno',
    8: 'Otro',
    9: 'No_indica'
}

afinidad = {
    1: "madre/padre",
    2: "hermano/hermana",
    3: "hijo/hija",
    4: "tio/tia",
    5: "abuelo/abuela",
    6: "primo/prima",
    7: "sobrino/sobrina",
    8: "suegro/suegra",
    9: "yerno/nuera",
    10: "tutor",
    11: "amistad/conocido",
    12: "otro"
}

Ecivil = {
    1: "Casado",
    2: "Unido",
    3: "Soltero"
}

discapacidad = {
    0: "No_aplica",
    1: "Fisica",
    2: "Mental",
    3: "Visual",
    4: "Auditiva",
    5: "Otra" }

orientacion_sexual = {
    0: "No_aplica",
    1: "Heterosexual",
    2: "Bisexual",
    3: "Homosexual",
    4: "Trans",
    5: "Otro"
}

people = {
    1: "Ladino",
    2: "Maya",
    3: "Garífuna",
    4: "Xinca",
    5: "Otro",
    6: "No indica"
}
#Region: Funciones
def Desc_nacionalidad(codigo: int):
    if codigo in nacionalidad:
        return { nacionalidad[codigo] }


def Desc_idiomas(codigo: int):
    if codigo in idiomas:
        return {idiomas[codigo]}

def Desc_educacion(codigo: int):
    if codigo in educ:
        return { educ[codigo]}

def Desc_parentesco(codigo: int):
    if codigo in afinidad:
        return {afinidad[codigo] }

def Desc_Civil(codigo: int):
    if codigo in Ecivil:
        return { Ecivil[codigo]}
    
def Desc_discapacidad(codigo: int):
    if codigo in discapacidad:
        return { discapacidad[codigo]}
    
def Desc_orientacionSexual(codigo: int):
    if codigo in orientacion_sexual:
        return { orientacion_sexual[codigo]}
    
def Desc_people(codigo: int):
    if codigo in people:
        return { people[codigo]}








