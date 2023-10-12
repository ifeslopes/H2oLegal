from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_usuarios = config.QUERY_COUNT.format(tabela="usuario")
        self.qry_total_perfils = config.QUERY_COUNT.format(tabela="perfils")
        self.qry_total_agenda = config.QUERY_COUNT.format(tabela="agenda")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = "DIEGO MOREIRA, JACÓ LEOPOLDINO"
        self.created_by1 = "KAMILA GALANDE,LEONARDO LOPES"
        self.created_by2 = "MARCIEL COUTINHO,VICTOR FERREIRA"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    
    def get_total_usuarios(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_usuarios)["total_usuario"].values[0]
    
    def get_total_perfils(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_perfils)["total_perfils"].values[0]
    
    def get_total_agenda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_agenda)["total_agenda"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE CONSUMO DE ÁGUA                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - USUARIOS:         {str(self.get_total_usuarios()).rjust(5)}
        #      2 - PERFILS:          {str(self.get_total_perfils()).rjust(5)}
        #      3 - AGENDA:           {str(self.get_total_agenda()).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #              {self.created_by1}
        #              {self.created_by2}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """