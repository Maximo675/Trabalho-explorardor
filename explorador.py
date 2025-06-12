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

        # Ensure destination is treated as a directory if it exists
        if os.path.exists(destino) and not os.path.isdir(destino):
            print(f"Erro: O destino '{destino}' já existe e não é uma pasta.")
            return

        # If the destination path is a directory, append the basename of the source
        # This ensures the file/folder is moved *into* the destination directory
        if os.path.isdir(destino):
            final_destino = os.path.join(destino, os.path.basename(origem))
        else:
            # If destination doesn't exist, shutil.move will act as a rename or create
            # The user explicitly typed it, so we'll try to use it as-is,
            # but the prompt should make it clear whether they intend a new name or a folder.
            final_destino = destino

        # Add a check for moving a folder into itself (already there, good!)
        if os.path.abspath(final_destino).startswith(os.path.abspath(origem)):
            print("Erro: Não é possível mover uma pasta para dentro de si mesma.")
            return

        shutil.move(origem, final_destino) # Use final_destino
        print(f"'{origem}' movido com sucesso para '{final_destino}'.") # More specific success message
    except shutil.Error as se: # Catch specific shutil errors
        print(f"Erro ao mover (shutil.Error): {se}")
    except Exception as e:
        print(f"Erro ao mover: {e}")
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

from pathlib import Path

def excluir(caminho):
    try:
        path_obj = Path(caminho)

        if not path_obj.exists():
            print(f"Erro: '{caminho}' não encontrado.")
            return

        # Interactive confirmation for deletion
        confirm = input(f"Tem certeza que deseja excluir '{caminho}'? (s/n): ").lower()
        if confirm != 's':
            print("Exclusão cancelada.")
            return

        if path_obj.is_dir():
            shutil.rmtree(path_obj)
        else:
            path_obj.unlink() # For files, equivalent to os.remove

        print(f"'{caminho}' excluído com sucesso.")

    except PermissionError:
        print(f"Erro ao excluir '{caminho}': Permissão negada. Verifique suas permissões.")
    except FileNotFoundError:
        print(f"Erro ao excluir '{caminho}': O arquivo ou pasta não existe mais.")
    except Exception as e:
        print(f"Erro inesperado ao excluir '{caminho}': {e}")

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

        # ...
        elif opcao == '3':
            origem = input("Digite o caminho COMPLETO do arquivo/pasta a mover: ").strip('"')
            destino = input("Digite o caminho COMPLETO de destino (pasta onde será movido): ").strip('"')
            # Add a check to ensure 'destino' is a valid directory path if it exists
            # Or ensure 'destino' is intended to be the *new name* if moving to the same directory
            if not os.path.isabs(destino):
                print("Erro: O caminho de destino deve ser um caminho absoluto (ex: C:\\Pasta\\Subpasta).")
                continue # Go back to menu
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
