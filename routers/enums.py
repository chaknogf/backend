from pydantic import BaseModel
from enum import Enum
from typing import Optional
import sys

# sys.path.append("/ruta/al/directorio")



class GeneroEnum(str, Enum):
    Masculino = 'M'
    Femenino = 'F'
    
class EstadoEnum(str, Enum):
    Vivo = 'v'
    Muerto = 'm'
    
    
class PuebloEnum(int, Enum):
    Ladino = 1
    Maya = 2
    Garífuna = 3
    Xinca = 4
    Otros = 5
    No_indica = 6
    
class IdiomaEnum(int, Enum):
    Achi = 1
    Akateka = 2
    Awakateka = 3
    Chorti = 4
    Chalchiteka = 5
    Chuj = 6
    Itza = 7 
    Ixil = 8
    Jakalteka = 9
    Kaqchikel = 10
    Kiche = 11
    Mam = 12
    Mopan = 13
    Poqomam = 14 
    Pocomchi = 15
    Qanjobal = 16
    Qeqchi = 17
    Sakapulteka = 18
    Sipakapensa = 19
    Tektiteka = 20
    Tzutujil = 21
    Uspanteka = 22 
    No_indica = 23
    Español = 24 
    Otro = 25

class DiscapacidadEnum(int, Enum):
    No_aplica = 0
    Fisica = 1
    Mental = 2
    Visual = 3
    Auditiva = 4
    Otra = 5

class OrientacionSexualEnum(int, Enum):
    No_aplica = 0
    Heterosexual = 1
    Bisexual = 2
    Homosexual = 3
    Trans = 4
    Otro = 5
    
class EstudiosEnum(int, Enum):
    No_aplica = 1
    Pre_Primaria = 2
    Primaria = 3
    Básicos = 4
    Diversificado = 5
    Universidad = 6
    Ninguno = 7
    Otro = 8
    No_indica = 9
    
class ParentescoEnum(int, Enum):
    
    Madre_Padre = 1
    hijo_a = 2
    hermano_a = 3
    abuelo_a = 4
    tio_a = 5
    primo_a = 6
    sobrino_a = 7
    yerno_nuera = 8
    esposo_a = 9
    suegro_a = 10
    tutor = 11
    amistad = 12
    novio_a = 13
    cuñado_a = 14
    nieto_a = 15
    hijastros = 16
    padrastros = 17
    otro = 18
    
    
    
class EstadoCivilEnum(int, Enum):
    casado = 1
    unido = 2
    soltero = 3
    


class nacionalidadEnum(int, Enum):
     
    Guatemalteca = 1
    Beliceña = 2
    Salvadoreña = 3
    Hondureña = 4
    Nicaragüense = 5
    Costarricense = 6
    Panameña = 7
    Mexicana = 8
    Otro_pais = 9
    No_indica = 0
    
# class especialidadEnum(int, Enum):
    

   

    
   
    