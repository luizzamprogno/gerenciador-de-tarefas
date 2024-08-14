import sqlite3

def create_conection():

    return sqlite3.connect('tarefas.db')

def define_cursor(conexao):

    return conexao.cursor()

def create_table(cursor, conexao):


    cursor.execute('''

        CREATE TABLE IF NOT EXISTS Tarefas (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tarefa TEXT NOT NULL,

        status TEXT NOT NULL

        );
    ''')

    conexao.commit()

def create_data(cursor, conexao):

    tarefa = input('Digite a tarefa: ')

    status = input('Digite o status: ')

    cursor.execute('''

        INSERT INTO tarefas (tarefa, status)

        VALUES (?, ?)

    ''', (tarefa, status))


    conexao.commit()

def read_data(cursor, conexao):

    cursor.execute('''

        SELECT * FROM tarefas
    ''')


    for linha in cursor.fetchall():

        print(linha)

def update_data(cursor, conexao):

    nova_tarefa = input('Digite a nova tarefa: ')

    novo_status = input('Digite o novo status: ')


    cursor.execute('''

        UPDATE tarefas

        SET tarefa = ?, status = ?

        WHERE id = 1

    ''', (nova_tarefa, novo_status))


    conexao.commit()

def delete_data(cursor, conexao):

    deletar_id = input('Qual tarefa deseja deletar: ')


    cursor.execute('''

        DELETE FROM  tarefas

        WHERE id = ?

    ''', (deletar_id))


    conexao.commit()

def main_menu():
    while True:
        try:
            return int(input('''
            
            ***LISTA DE TAREFAS***
            
            Selecione abaixo o que deseja fazer:

            Adicionar nova tarefa - (1)
            Visualizar todas as tarefas - (2)
            Atualizar uma tarefa existente - (3)
            Apagar um tarefa - (4)
            Sair - (5)
            
            '''))
        except ValueError:
            print('Entrada inválida, por favor digite um número entre 1 e 5')

def secondary_menu():
    while True:
        try:
            return int(input('''O que deseja fazer agora?
                                Voltar ao meun principal - (1)
                                Criar outra tarefa - (2)
                                Sair - (3)
                        '''))
        except ValueError:
            print('Entrada inválida, por favor digite um número entre 1 e 5')

def handle_secondary_menu(action, cursor, conexao):
    while True:
        next_step = secondary_menu()
        if next_step == 1:
            break
        elif next_step == 2:
            action(cursor, conexao)
        elif next_step == 3:
            print('Encerrando o programa')
            conexao.close()
            return True
        else:
            print('Entrada inválida, por favor digite um número entre 1 e 5')
    return False

def user_decision(cursor, conexao):
    
    while True:
        user_choice = main_menu()

        if user_choice == 1:
            create_data(cursor, conexao)
            handle_secondary_menu(create_data, cursor, conexao)
            
        elif user_choice == 2:
            read_data(cursor, conexao)
            handle_secondary_menu(read_data, cursor, conexao)

        elif user_choice == 3:
            update_data(cursor, conexao)
            handle_secondary_menu(update_data, cursor, conexao)

        elif user_choice == 4:
            delete_data(cursor, conexao)
            handle_secondary_menu(delete_data, cursor, conexao)

        elif user_choice == 5:
            print('Encerrando o programa')

            break
        else:
            print('Entrada inválida, por favor digite um número entre 1 e 5')

def main():

    conexao = create_conection()
    cursor = define_cursor(conexao)
    create_table(cursor, conexao)
    user_decision(cursor, conexao)

    conexao.close()

if __name__ == '__main__':
    main()