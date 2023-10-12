from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
       
        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("sql/relatorio_usuario.sql") as f:
            self.query_relatorio_usuario = f.read()
       
        with open("sql/relatorio_perfil.sql") as f:
            self.query_relatorio_perfil = f.read()
            
        with open("sql/relatorio_perfil_usuario.sql") as f:
            self.query_relatorio_perfil_usuario = f.read()
            
        with open("sql/relatorio_agenda.sql") as f:
            self.query_relatorio_agenda = f.read()

    def get_relatorio_usuario(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_usuario))
        input("Pressione Enter para Sair do Relatório de Usuarios")
    
    def get_relatorio_perfil(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_perfil))
        input("Pressione Enter para Sair do Relatório de Perfils")

    def get_relatorio_perfil_usuario(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_perfil_usuario))
        input("Pressione Enter para Sair do Relatório de  quantidade de Perfils por usuarios")

    def get_relatorio_agenda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_agenda))
        input("Pressione Enter para Sair do Relatório de Perfils")
