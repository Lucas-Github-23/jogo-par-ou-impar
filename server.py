"""
Servidor Web Nativo para o Jogo de Par ou Ímpar & Laboratório Probabilístico.
Utiliza apenas a biblioteca padrão do Python (http.server e urllib).
"""

import http.server
import socketserver
import os
import json
import urllib.parse
import webbrowser
from core.probabilidade import calcular_probabilidade_exata, simular_monte_carlo

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "web")


class ParOuImparHandler(http.server.SimpleHTTPRequestHandler):
    """Manipulador HTTP com suporte a API REST JSON e arquivos estáticos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Rota de API: Cálculo Probabilístico Exato
        if path == "/api/calculate":
            try:
                min1 = int(query.get("min1", [0])[0])
                max1 = int(query.get("max1", [5])[0])
                min2 = int(query.get("min2", [0])[0])
                max2 = int(query.get("max2", [5])[0])

                res = calcular_probabilidade_exata(min1, max1, min2, max2)
                data = {
                    "min1": res.min1,
                    "max1": res.max1,
                    "min2": res.min2,
                    "max2": res.max2,
                    "total_combinacoes": res.total_combinacoes,
                    "combinacoes_par": res.combinacoes_par,
                    "combinacoes_impar": res.combinacoes_impar,
                    "pct_par": res.pct_par,
                    "pct_impar": res.pct_impar,
                    "vantagem": res.vantagem,
                    "diferenca_pct": res.diferenca_pct,
                    "explicacao_didatica": res.explicacao_didatica,
                    "distribuicao_somas": res.distribuicao_somas,
                    "matriz": res.matriz
                }
                self._send_json(data)
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        # Rota de API: Simulação Monte Carlo
        elif path == "/api/simulate":
            try:
                min1 = int(query.get("min1", [0])[0])
                max1 = int(query.get("max1", [5])[0])
                min2 = int(query.get("min2", [0])[0])
                max2 = int(query.get("max2", [5])[0])
                rounds = int(query.get("rounds", [50000])[0])

                res_sim = simular_monte_carlo(min1, max1, min2, max2, num_rodadas=rounds)
                self._send_json(res_sim)
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        # Rota raiz entrega index.html
        if path == "/" or path == "":
            self.path = "/index.html"

        # Arquivos estáticos
        return super().do_GET()

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        """Silencia logs padrão para manter a tela limpa."""
        return


def iniciar_servidor(porta: int = PORT, abrir_navegador: bool = True):
    """Inicia o servidor web na porta especificada."""
    tentativas = 5
    servidor = None
    porta_atual = porta

    for _ in range(tentativas):
        try:
            servidor = socketserver.TCPServer(("", porta_atual), ParOuImparHandler)
            break
        except OSError:
            porta_atual += 1

    if not servidor:
        print(f"Não foi possível abrir o servidor nas portas {porta} a {porta_atual}.")
        return

    url = f"http://localhost:{porta_atual}"
    print(f"\n✨ Servidor Web rodando com sucesso!")
    print(f"🌐 Acesse no seu navegador: \033[1;36m{url}\033[0m")
    print(f"Pressione \033[1;33mCtrl + C\033[0m no terminal para encerrar o servidor a qualquer momento.\n")

    if abrir_navegador:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor web finalizado com sucesso.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    iniciar_servidor()
