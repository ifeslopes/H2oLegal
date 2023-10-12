from model.perfil import Perfil
from conexion.oracle_queries import OracleQueries


class Controller_Perfil:
    def __init__(self):
        pass

    def inserir_perfil(self) -> Perfil:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''

        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo porcentagem
        nome = str(input("Perfil (Novo): "))

        if self.verifica_existencia_perfil_nome(oracle, nome):
            # Solicita ao usuario o novo nome
            porcentagem = input("Porcetagem (Novo): ")
            # Insere e persiste o novo perfil
            oracle.write(
                f"insert into perfils values (PERFILS_CODIGO_SEQ.NEXTVAL,'{nome}','{porcentagem}')")
            # Recupera os dados do novo perfil criado transformando em um DataFrame
            df_perfil = oracle.sqlToDataFrame(
                f"select descricao_perfil, porcentagem_perfil from perfils where descricao_perfil = '{nome}'")
            # Cria um novo objeto perfil
            novo_perfil = Perfil(
                df_perfil.porcentagem_perfil.values[0], df_perfil.descricao_perfil.values[0])
            # Exibe os atributos do novo perfil
            print(novo_perfil.to_string())
            # Retorna o objeto novo_perfil para utilização posterior, caso necessário
            continue_resgristrando = input(
                "Deseja continuar regristrando? s /SIM - n /NÃo: ")
            if continue_resgristrando == "s":
                self.inserir_perfil()

            return novo_perfil
        else:
            print(f"O Perfil {nome} já está cadastrado.")
            return None

    def atualizar_perfil(self) -> Perfil:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do perfil a ser alterado
        nome = str(
            input("Nome do perfil que deseja alterar o nome: "))

        # Verifica se o perfil existe na base de dados
        if not self.verifica_existencia_perfil_nome(oracle, nome):
            novo_nome = str(
                input("Nome do Novo perfil que deseja alterar o nome: "))
            porcentagem = float(input("Porcetagem (Atuallizar): "))
            # Atualiza o nome do perfil existente
            oracle.write(
                f"update perfils set descricao_perfil = '{novo_nome}',porcentagem_perfil = {porcentagem} where descricao_perfil = '{nome}'")
            # Recupera os dados do novo perfil criado transformando em um DataFrame
            df_perfil = oracle.sqlToDataFrame(
                f"select descricao_perfil, porcentagem_perfil from perfils where descricao_perfil = '{novo_nome}'")
            # Cria um novo objeto perfil
            perfil_atualizado = Perfil(
                df_perfil.porcentagem_perfil.values[0], df_perfil.descricao_perfil.values[0])
            # Exibe os atributos do novo perfil
            print(perfil_atualizado.to_string())
            # Retorna o objeto perfil_atualizado para utilização posterior, caso necessário

            continue_resgristrando = input(
                "Deseja continuar atualizando regristrando? s /SIM - n /NÃO: ")
            if continue_resgristrando == "s":
                self.atualizar_perfil()

            return perfil_atualizado
        else:
            print(f"O nome do perfil {novo_nome} não existe.")
            return None

    def excluir_perfil(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o porcentagem do perfil a ser alterado
        codigo = str(input(" codgio do perfil que irá excluir: "))

        # Verifica se o perfil existe na base de dados
        if not self.verifica_existencia_perfil(oracle, codigo):
            # Recupera os dados do novo perfil criado transformando em um DataFrame
            df_perfil = oracle.sqlToDataFrame(
                f"select descricao_perfil, porcentagem_perfil from perfils where codigo_perfil = {codigo}")
            nome = input(
                f"você deseja excluir o perfil? {df_perfil.descricao_perfil.values[0]}:  S - Sim / N - não ")
            if nome == "s":

                if self.verifica_existencia_relacionamendo_com_perfil(oracle, codigo):
                    # Revome o perfil da tabela
                    oracle.write(
                        f"delete from perfils where codigo_perfil  = '{codigo}'")
                    # Cria um novo objeto perfil para informar que foi removido
                    perfil_excluido = Perfil(
                        df_perfil.porcentagem_perfil.values[0], df_perfil.descricao_perfil.values[0])
                    # Exibe os atributos do perfil excluído
                    print("perfil Removido com Sucesso!")
                    print(perfil_excluido.to_string())

                    continue_resgristrando = input(
                        "Deseja continuar removendo ? s /SIM - n /NÃO: ")
                    if continue_resgristrando == "s":
                        self.excluir_perfil()
                else:
                    print(
                        "Não pede ser apagado porque esta relaciondo com outra tabela")

        else:
            print(f"O Perfil {codigo} não existe.")

    def verifica_existencia_perfil(self, oracle: OracleQueries, codigo: str = None) -> bool:
        # Recupera os dados do novo perfil criado transformando em um DataFrame
        df_perfil = oracle.sqlToDataFrame(
            f"select descricao_perfil, porcentagem_perfil from perfils where codigo_perfil = '{codigo}' or descricao_perfil ='{codigo}'")
        return df_perfil.empty

    def verifica_existencia_relacionamendo_com_perfil(self, oracle: OracleQueries, codigo: int = None) -> bool:
        # Recupera os dados do novo perfil criado transformando em um DataFrame
        df_perfil = oracle.sqlToDataFrame(
            f"SELECT nome, email FROM usuario WHERE codigo_perfil = {codigo}")
        return df_perfil.empty
    
    def verifica_existencia_perfil_nome(self, oracle: OracleQueries, codigo: str = None) -> bool:
        # Recupera os dados do novo perfil criado transformando em um DataFrame
        df_perfil = oracle.sqlToDataFrame(
            f"select descricao_perfil, porcentagem_perfil from perfils where descricao_perfil ='{codigo}'")
        return df_perfil.empty
