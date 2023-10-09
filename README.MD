# Aplicativo de Consumo de Água

Este é um aplicativo simples de consumo de água, onde o usuário entra com informações pessoais, como nome, e-mail, altura, idade e peso, e o aplicativo calcula a quantidade de água que o usuário deve beber diariamente, com base no peso.

## Requisitos

- Python 3.x
- Bibliotecas Python listadas em [requirements.txt](src/requirements.txt)

## Instruções de Uso

1. Clone ou faça o download deste repositório em sua máquina.

2. Navegue até o diretório `src`:

   ```shell
   cd src
   ```

3. Instale as bibliotecas Python necessárias:

   ```shell
   pip install -r requirements.txt
   ```

4. 
Testando conexão com banco de dados:

   ```shell
   python3 test.py
   ```

   Certifique-se de que o Oracle Instant Client esteja instalado e configurado corretamente, pois o aplicativo se conecta ao banco de dados Oracle.


5. Crie as tabelas e registros fictícios executando o script `create_tables_and_records.py`:

   ```shell
   python create_tables_and_records.py
   ```

   Certifique-se de que o Oracle Instant Client esteja instalado e configurado corretamente, pois o aplicativo se conecta ao banco de dados Oracle.

6. Agora você pode executar o aplicativo principal:

   ```shell
   python principal.py
   ```

7. Siga as instruções no aplicativo para inserir suas informações pessoais.

7. O aplicativo calculará a quantidade de água que você deve beber diariamente com base no seu peso e mostrará o resultado.

## Organização do Código

- `src/conexion`: Módulo de conexão com o banco de dados Oracle.
- `src/controller`: Classes controladoras para inserção, atualização e exclusão de registros.
- `src/model`: Classes que representam as entidades do aplicativo.
- `src/reports`: Classes responsáveis por gerar relatórios.
- `src/utils`: Scripts de configuração e tela de informações iniciais.
- `src/create_tables_and_records.py`: Script para criar as tabelas e registros fictícios.
- `src/principal.py`: Aplicativo principal que interage com o usuário.

- [diagrams](diagrams): Nesse diretório está o [diagrama relacional](diagrams/diagrama.png) (lógico) do sistema.
    * O sistema possui tres entidades: USUARIO, PERFIL, AGENDA
- [sql](sql): Nesse diretório estão os scripts para criação das tabelas e inserção de dados fictícios para testes do sistema
    * Certifique-se de que o usuário do banco possui todos os privilégios antes de executar os scripts de criação, caso ocorra erro, execute o comando a seguir com o superusuário via SQL Developer: `GRANT ALL PRIVILEGES TO LABDATABASE;`
    * [create_tables_pedidos.sql](sql/create_tables_pedidos.sql): script responsável pela criação das tabelas, relacionamentos e criação de permissão no esquema LabDatabase.
    * [inserting_samples_records.sql](sql/inserting_samples_records.sql): script responsável pela inserção dos registros fictícios para testes do sistema.
## Observações

Certifique-se de que o Oracle Instant Client esteja instalado e configurado corretamente. Se você encontrar problemas relacionados à senha expirada, siga as instruções fornecidas no README para alterar a senha.

Este aplicativo é um exemplo simples e pode ser estendido para incluir recursos adicionais, como armazenamento de dados do usuário, histórico de consumo de água e muito mais.

## Bibliotecas Utilizadas

As bibliotecas Python necessárias estão listadas no arquivo [requirements.txt](src/requirements.txt). Você pode instalá-las com o comando `pip install -r requirements.txt`.

### Instalando Oracle InstantClient
- Baixe a versão do [InstantClient](https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html) de acordo com a versão do Banco de Dados
- Caso esteja utilizando uma distribuição Linux baseado em Debian, será necessário executar o comando a seguir para converter o arquivo .rpm para .deb.
  ```shell
  sudo alien --scripts oracle-instantclient18.5-basic-18.5.0.0.0-3.x86_64.rpm
  ```
- Descompacte o arquivo e será gerado um diretório em um diretório de fácil acesso.
- Mova os diretórios lib e share para dentro do diretório do InstantClient
  ```shell
  sudo mv lib /usr/local/oracle/instantclient_18_5/
  ```
  
  ```shell
  sudo mv share instantclient_18_5/
  ```
- Edite o arquivo `.bash_profile` incluindo as linhas a seguir ao final do arquivo:
  ```shell
  export ORACLE_HOME=/usr/local/oracle/instantclient_18_5/lib/oracle/18.5/client64
  export LD_LIBRARY_PATH=$ORACLE_HOME/lib
  export PATH=$PATH:$ORACLE_HOME/bin
  export PATH
  ```
  #### Em caso de problemas com a execução dos software dando a seguinte mensagem `ORA-28001: the password has expired`, execute as linhas de comando a seguir no Oracle:
- `ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;`
- `ALTER USER labdatabase IDENTIFIED BY "labDatabase2022";`
- `ALTER USER labdatabase IDENTIFIED BY  "labDatabase2022";`
## Utilizando Aplicativo