import os
import shutil
import subprocess
import sys

def abrir(caminho):
    if not os.path.exists(caminho):
        print("Arquivo ou pasta não encontrados.")
        return

    try:
        if sys.platform.startswith('win'):
            os.startfile(caminho)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', caminho])
        else:
            subprocess.run(['xdg-open', caminho])
        print("Abrindo no explorador de arquivos...")
    except Exception as e:
        print("Erro ao abrir no explorador:", e)

def renomear(caminho_atual, novo_nome):
    try:
        if not os.path.exists(caminho_atual):
            print("Erro: caminho atual não encontrado.")
            return

        if any(c in novo_nome for c in r'<>:"/\|?*'):
            print("Erro: o nome contém caracteres inválidos para o Windows.")
            return

        pasta = os.path.dirname(caminho_atual)
        novo_caminho = os.path.join(pasta, novo_nome)

        if os.path.exists(novo_caminho):
            print("Erro: já existe um arquivo/pasta com esse nome no mesmo local.")
        else:
            os.rename(caminho_atual, novo_caminho)
            print(f"Renomeado com sucesso para: {novo_caminho}")
    except Exception as e:
        print("Erro ao renomear:", e)

def mover(origem, destino):
    try:
        if not os.path.exists(origem):
            print("Erro: origem não encontrada.")
            return
        if os.path.abspath(destino).startswith(os.path.abspath(origem)):
            print("Erro: não é possível mover uma pasta para dentro de si mesma.")
            return
        shutil.move(origem, destino)
        print("Movido com sucesso.")
    except Exception as e:
        print("Erro ao mover:", e)

def copiar(origem, destino):
    try:
        if not os.path.exists(origem):
            print("Erro: origem não encontrada.")
            return
        if os.path.isdir(origem):
            shutil.copytree(origem, destino)
        else:
            shutil.copy2(origem, destino)
        print("Copiado com sucesso.")
    except FileExistsError:
        print("Erro: destino já existe.")
    except Exception as e:
        print("Erro ao copiar:", e)

def excluir(caminho):
    try:
        if not os.path.exists(caminho):
            print("Erro: caminho não encontrado.")
            return
        if os.path.isdir(caminho):
            shutil.rmtree(caminho)
        else:
            os.remove(caminho)
        print("Excluído com sucesso.")
    except Exception as e:
        print("Erro ao excluir:", e)

def menu():
    while True:
        print("\n--- Gerenciador de Arquivos ---")
        print("1. Abrir arquivo/pasta")
        print("2. Renomear arquivo/pasta")
        print("3. Mover arquivo/pasta")
        print("4. Copiar arquivo/pasta")
        print("5. Excluir arquivo/pasta")
        print("6. Sair")

        opcao = input("Escolha uma opção (1-6): ")

        if opcao == '1':
            caminho = input("Digite o caminho do arquivo/pasta: ").strip('"')
            abrir(caminho)
        elif opcao == '2':
            caminho = input("Digite o caminho atual do arquivo/pasta: ").strip('"')
            novo_nome = input("Digite o novo nome (somente nome, sem caminho): ").strip()
            renomear(caminho, novo_nome)

        elif opcao == '3':
            origem = input("Digite o caminho do arquivo/pasta a mover: ").strip('"')
            destino = input("Digite o caminho de destino: ").strip('"')
            mover(origem, destino)
        elif opcao == '4':
            origem = input("Digite o caminho do arquivo/pasta a copiar: ").strip('"')
            destino = input("Digite o caminho de destino: ").strip('"')
            copiar(origem, destino)
        elif opcao == '5':
            caminho = input("Digite o caminho do arquivo/pasta a excluir: ").strip('"')
            excluir(caminho)
        elif opcao == '6':
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
