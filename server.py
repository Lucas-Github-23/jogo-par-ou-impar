"""
Servidor local simples para servir o index.html e permitir a leitura do estatisticas.json via HTTP.
Utiliza apenas bibliotecas padrão do Python (sem dependências externas).
"""

import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRETORIO = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRETORIO, **kwargs)


def iniciar_servidor():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 55)
        print("      SERVIDOR LOCAL DE ESTATÍSTICAS INICIADO")
        print("=" * 55)
        print(f"• URL do Painel: \033[1;36m{url}\033[0m")
        print("• Lendo: index.html e estatisticas.json")
        print("• Pressione \033[1;33mCtrl + C\033[0m para encerrar o servidor.")
        print("=" * 55 + "\n")

        # Abre o navegador automaticamente
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Servidor encerrado com sucesso.\n")


if __name__ == "__main__":
    iniciar_servidor()
