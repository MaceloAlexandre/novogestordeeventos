from dao import *


def verificar_senha(senha1, senha2):
    if senha1 == senha2:
        return True
    else:
        return False


def verificar_user_existente(email):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM usuarios WHERE email = %s", (email,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado is not None


def verificar_email(email):
    return '@' in email and email.endswith('.com')


def verificar_login(email, senha, users):
    for usuario, detalhes in users.items():
        if usuario == email and detalhes['senha'] == senha:
            print(f'Login realizado com sucesso\n'
                  f'___________________________\n'
                  f'Seja bem-vindo {detalhes['nome']}!')
            return usuario
    print('Verifique o login')
    return False


def login_db(email, senha):
    conexao = conectardb()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT email, senha, nome, idade, profissao, estado, id_usuario FROM usuarios WHERE email = '{email}' ")
    usuario = cursor.fetchall()
    cursor.close()
    conexao.close()
    if usuario:
        print(usuario)
        if usuario[0][1] == senha:
            print('Login validado com sucesso!')
            return usuario
        else:
            print('Senha inválida')
            return False
    else:
        print('Usuario não encontrado, verifique seu login')


def verify_creator(usuario, resultados):
    if usuario[0][0] == resultados[0][0]:
        return True
    else:
        return False

