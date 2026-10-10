"""Abre a configuração preservada de seis salas, sem alterar o menu do jogo."""
from visual import VisualApp


def main():
    app = VisualApp()
    app.session.start_campaign(configuration='prototype')
    app.build_game()
    app.run()


if __name__ == '__main__':
    main()
