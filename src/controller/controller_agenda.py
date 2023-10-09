from model.usuario import Usuario
from model.agenda import Agenda
from conexion.oracle_queries import OracleQueries
from reports.relatorios import Relatorio


class Controller_Agenda:
    def __init__(self):
        pass

    def inserir_agenda(self) -> Usuario:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        relatorio = Relatorio()
        
        relatorio.get_relatorio_usuario()
        # Solicita o novo email
        codigo = input("entre com codigo do usuario: ")

        if self.verifica_usuario_completou_quantidade_agua(oracle, codigo):

            agenda = self.criar_agenda_para_usuario(oracle, codigo)

            # Insere e persiste o novo usuário
            oracle.write(
                f"insert into agenda values (AGENDA_CODIGO_SEQ.NEXTVAL,{agenda.get_quantidade_indicada()},{agenda.get_quantidade_consumida()}, {agenda.get_quantidade_consumida_total()}, {agenda.get_data_cadastro()}, {agenda.get_codigo_usuario()})")
           
            id = oracle.sqlToDataFrame(f"select max(codigo_agenda)as id from agenda").id.values[0]
           
            # Recupera os dados do novo usuário criado transformando em um DataFrame
            df_agenda = oracle.sqlToDataFrame(
                f"SELECT QTD_INDICADA, QTD_CONSUMIDA, QTD_TOTAL,DATA_CADASTRO, CODIGO_USUARIO FROM AGENDA WHERE CODIGO_AGENDA ={id}")
           
            # Cria um novo objeto Usuario
            nova_agenda = Agenda(
                df_agenda.qtd_indicada.values[0],
                df_agenda.qtd_consumida.values[0],
                df_agenda.qtd_total.values[0],
                df_agenda.data_cadastro.values[0],
                df_agenda.codigo_usuario.values[0]
            )

            # Exibe os atributos do novo usuário
            print(nova_agenda.to_string())

            #Retorna o objeto novo_usuario para utilização posterior, caso necessário
            return  nova_agenda
        else:
            print(f"O usuario não completou quantidade água indicada")
            return None

    def atualizar_usuario(self) -> Usuario:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        relatorio = Relatorio()

        # Solicita o email do usuário a ser alterado
        email = input("Email do usuário que deseja alterar: ")

        # Verifica se o usuário existe na base de dados
        if not self.verifica_usuario_completou_quantidade_agua(oracle, email):
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
            df_agenda = oracle.sqlToDataFrame(
                f"select email, nome, idade_usuario, altura_usuario, peso_usuario, codigo_perfil from usuario where email = '{email}'")
            # Cria um novo objeto usuario_atualizado
            usuario_atualizado = Usuario(
                df_agenda.email.values[0],
                df_agenda.nome.values[0],
                df_agenda.idade_usuario.values[0],
                df_agenda.altura_usuario.values[0],
                df_agenda.peso_usuario.values[0],
                df_agenda.codigo_perfil.values[0]
            )
            # Exibe os atributos do novo usuário
            print(usuario_atualizado.to_string())
            # Retorna o objeto usuario_atualizado para utilização posterior, caso necessário
            return usuario_atualizado
        else:
            print(f"O usario não existe.")
            return None

    def excluir_agenda(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita o email do usuário a ser excluído
        id = input("Entre com Id da agendamento ou do usuario que irá excluir: ")

        # Verifica se o usuário existe na base de dados
        if not self.verifica_agendamento_banco(oracle, id):
            # Remove o usuário da tabela
            oracle.write(f"delete from agenda where codigo_agenda = {id}")
            # Exibe uma mensagem informando que o usuário foi removido
            print(f"Agendamento do código {id} removido com sucesso!")
        else:
            print(f"O agendamentop do código {id} não existe.")

    def verifica_usuario_completou_quantidade_agua(self, oracle: OracleQueries, codigo: str = None) -> bool:
        # Recupera os dados do agenda criado transformando em um DataFrame
        df_agenda = oracle.sqlToDataFrame(
            f"select * from agenda WHERE (QTD_CONSUMIDA < QTD_INDICADA ) AND CODIGO_USUARIO   = '{codigo}'")
        return df_agenda.empty


    def verifica_agendamento_banco(self, oracle: OracleQueries, codigo: str = None) -> bool:
        # Recupera os dados do agenda criado transformando em um DataFrame
        df_agenda = oracle.sqlToDataFrame(
            f"select * from agenda where codigo_agenda = {codigo}")
        return df_agenda.empty

    def criar_agenda_para_usuario(self, oracle: OracleQueries, id_usuario: int = None) -> Agenda:
        # Recupera os dados do agenda criado transformando em um DataFrame
        ml_agua_kilo = float(35)
        ml_agua_dia = float(350)
        df_agenda = oracle.sqlToDataFrame(
            f" select c.CODIGO_USUARIO, c.NOME, c.EMAIL, c.IDADE_USUARIO, c.ALTURA_USUARIO, c.PESO_USUARIO,c.codigo_perfil, p.DESCRICAO_PERFIL as PERFIL, p.PORCENTAGEM_PERFIL as PORCENTAGEM from usuario c JOIN PERFILS p ON(c.CODIGO_PERFIL =p.CODIGO_PERFIL) where c.CODIGO_USUARIO =  '{id_usuario}'")
       
       

        qauntidade_agua_indicada = int(float(df_agenda.peso_usuario.values[0] * ml_agua_kilo) * float(df_agenda.porcentagem.values[0])) / 1000
       
        tempo = str(input(
            "Entre com intervalo de tempo que gostaria de receber os aviso entre com Horas e Minutos Ex:[1:30]: "))
        
        segundos = float(float(tempo.split(":")[0]) * 60*60 + float(tempo.split(":")[1]) * 60)
        qauntidade_consumida = str(
            input("Entre com quantidade de água cunsumida em Ml: "))
        agenda = Agenda(qauntidade_agua_indicada, qauntidade_consumida,
                        qauntidade_consumida, "SYSDATE", df_agenda.codigo_usuario.values[0])

        return agenda
