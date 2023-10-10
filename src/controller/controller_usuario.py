from model.usuario import Usuario
from conexion.oracle_queries import OracleQueries
from reports.relatorios import Relatorio


class Controller_Usuario:
    def __init__(self):
        pass

    def inserir_usuario(self) -> Usuario:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        relatorio = Relatorio()

        # Solicita o novo email
        email = input("Email (Novo): ")

        if self.verifica_existencia_usuario(oracle, email):
            # Solicita o nome de usuário
            nome = input("Nome de Usuário (Novo): ")
            # Solicita a idade
            idade_usuario = float(input("Idade (Novo): "))
            
            # Solicita a altura
            altura_usuario = float(input("Altura (Novo): "))
            # Solicita o peso
            peso_usuario = float(input("Peso (Novo): "))
            # Listar os perfils
            relatorio.get_relatorio_perfil()

            # Solicita o código do perfil
            codigo_perfil = int(input("Código do Perfil (Novo): "))

            
            # Insere e persiste o novo usuário
            oracle.write(f"insert into usuario values (USUARIO_CODIGO_SEQ.NEXTVAL,'{nome}','{email}', {idade_usuario}, {altura_usuario}, {peso_usuario}, {codigo_perfil})")
            # Recupera os dados do novo usuário criado transformando em um DataFrame
            df_usuario = oracle.sqlToDataFrame(
                f"select email, nome, idade_usuario, altura_usuario, peso_usuario, codigo_perfil from usuario where email = '{email}'")
            # Cria um novo objeto Usuario
            novo_usuario = Usuario(
                df_usuario.email.values[0],
                df_usuario.nome.values[0],
                df_usuario.idade_usuario.values[0],
                df_usuario.altura_usuario.values[0],
                df_usuario.peso_usuario.values[0],
                df_usuario.codigo_perfil.values[0]
            )
            # Exibe os atributos do novo usuário
            print(novo_usuario.to_string())
            # Retorna o objeto novo_usuario para utilização posterior, caso necessário
            continue_resgristrando =input("Deseja continuar regristrando? s /SIM - n /NÃO: ")
            if continue_resgristrando =="s":
                self.inserir_usuario()
            return novo_usuario
        else:
            print(f"O email {email} já está cadastrado.")
            return None

    def atualizar_usuario(self) -> Usuario:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        relatorio = Relatorio()

        # Solicita o email do usuário a ser alterado
        email = input("Email do usuário que deseja alterar: ")

        # Verifica se o usuário existe na base de dados
        if not self.verifica_existencia_usuario(oracle, email):
            # Solicita o novo nome
            novo_nome = input("Nome (Novo): ")
            # Solicita a nova idade
            nova_idade_usuario = int(input("Idade (Nova): "))
            # Solicita a nova altura
            nova_altura_usuario = float(input("Altura (Nova): "))
            # Solicita o novo peso
            novo_peso_usuario = float(input("Peso (Novo): "))

            relatorio.get_relatorio_perfil()
            # Solicita o novo código do perfil
            novo_codigo_perfil = int(input("Código do Perfil (Novo): "))

            # Atualiza os dados do usuário existente
            oracle.write(
                f"update usuario set nome = '{novo_nome}', idade_usuario = {nova_idade_usuario}, altura_usuario = {nova_altura_usuario}, peso_usuario = {novo_peso_usuario}, codigo_perfil = {novo_codigo_perfil} where email = '{email}'")
            # Recupera os dados do usuário atualizado transformando em um DataFrame
            df_usuario = oracle.sqlToDataFrame(
                f"select email, nome, idade_usuario, altura_usuario, peso_usuario, codigo_perfil from usuario where email = '{email}'")
            # Cria um novo objeto usuario_atualizado
            usuario_atualizado = Usuario(
                df_usuario.email.values[0],
                df_usuario.nome.values[0],
                df_usuario.idade_usuario.values[0],
                df_usuario.altura_usuario.values[0],
                df_usuario.peso_usuario.values[0],
                df_usuario.codigo_perfil.values[0]
            )
            # Exibe os atributos do novo usuário
            print(usuario_atualizado.to_string())
            # Retorna o objeto usuario_atualizado para utilização posterior, caso necessário
            continue_resgristrando =input("Deseja continuar atualizando os regristos? s /SIM - n /NÃO: ")
            if continue_resgristrando =="s":
                self.atualizar_usuario()
            return usuario_atualizado
        else:
            print(f"O email {email} não existe.")
            return None

    def excluir_usuario(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita o email do usuário a ser excluído
        email = input("Email do Usuário que irá excluir: ")

        # Verifica se o usuário existe na base de dados
        if not self.verifica_existencia_usuario(oracle, email):
            # Remove o usuário da tabela
            oracle.write(f"delete from usuario where email = '{email}'")
            # Exibe uma mensagem informando que o usuário foi removido
            print(f"Usuário com email {email} removido com sucesso!")
            continue_resgristrando =input("Deseja continuar excluindo os regristos? s /SIM - n /NÃO: ")
            if continue_resgristrando =="s":
                self.excluir_usuario()
        else:
            print(f"O email {email} não existe.")

    def verifica_existencia_usuario(self, oracle: OracleQueries, email: str = None) -> bool:
        # Recupera os dados do usuário criado transformando em um DataFrame
        df_usuario = oracle.sqlToDataFrame(
            f"select email, nome from usuario where email = '{email}'")
        return df_usuario.empty
