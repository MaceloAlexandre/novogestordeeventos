import psycopg2


# conexãoDB


def conectardb():
    conexao = psycopg2.connect(database="gestor_de_eventos",
                               host="localhost",
                               user="postgres",
                               password="Macelo321",
                               port="5432")
    return conexao

# DAO referente ao usuario


def inserir_usuario(nome, email, senha, idade, profissao, estado, genero):
    conexao = conectardb()  # Estabelece conexão com o banco de dados.
    cursor = conexao.cursor()  # Cria um cursor para executar comandos SQL.
    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha, idade, profissao, estado, genero)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nome, email, senha, idade, profissao, estado, genero))
    conexao.commit()
    cursor.close()
    conexao.close()


def buscar_usuario(nome):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT email, nome FROM usuarios WHERE nome = '{nome}' ")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado


def buscar_usuario_id(id):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT email, nome FROM usuarios WHERE id_usuario = '{id}' ")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado


# Listar Todos os Usuários
def listar_usuarios():
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_usuario, nome, email, idade, profissao, estado FROM usuarios")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    if resultado:
        return resultado
    else:
        return "Nenhum usuário encontrado."


# Atualizar Usuário
def atualizar_usuario(id, novo_nome, novo_email, nova_senha, nova_idade, nova_profissao, novo_estado):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET nome = %s, email = %s, senha = %s, idade = %s, profissao = %s, estado = %s
        WHERE id_usuario = %s
    """, (novo_nome, novo_email, nova_senha, nova_idade, nova_profissao, novo_estado, id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return buscar_usuario_id(id)


# Deletar Usuário
def deletar_usuario(id):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()


# DAO refente aos eventos

def verificar_evento_existe(nome_evento):

    conexao = conectardb()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT 1 FROM eventos WHERE nome_evento = %s", (nome_evento,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conexao.close()


def inserir_evento(dados_evento):

    conexao = conectardb()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO eventos 
            (nome_evento, descricao, data_evento, local, valor, cancelavel, idade_minima,
             data_criacao, criador, aberto, codigo_inscricao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, dados_evento)
        conexao.commit()
        return True
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao cadastrar o evento: {e}")
        return False
    finally:
        cursor.close()
        conexao.close()
