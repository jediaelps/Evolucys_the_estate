import time
from game_state import GameState
from command_parser import CommandParser


def main():
    while True:
        game = GameState()
        parser = CommandParser(game)
        print('=' * 40)
        print('EVOLUCYS: THE ESTATE')
        print('=' * 40)
        print('Digite ajuda para ver os comandos ou sair para encerrar.\n')
        print(parser.execute('olhar'))
        while not game.game_over:
            try:
                command = input('> ')
            except (EOFError, KeyboardInterrupt):
                print('\nAté a próxima.')
                return
            if command.strip().lower() in ('sair', 'quit', 'exit'):
                print('Até a próxima.')
                return
            print(parser.execute(command), flush=True)
            if parser.delayed_response is not None:
                time.sleep(.8)
                print(parser.finish_delayed_response())
            print()
        print('VOCÊ MORREU\n\n[1] Continuar (reiniciar)\n[2] Sair')
        try:
            if input('> ').strip() != '1':
                return
        except (EOFError, KeyboardInterrupt):
            return


if __name__ == '__main__':
    main()
