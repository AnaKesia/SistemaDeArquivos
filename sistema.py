import os

class INode:
    def __init__(self, name, is_directory=False):
        self.name = name
        self.is_directory = is_directory
        self.size = 0
        self.data_blocks = []
        self.children = {}  # Para diretórios, mapeia nomes de arquivos/diretórios para i-nodes

class FileSystem:
    def __init__(self):
        self.root = INode("/", is_directory=True)
        self.current_dir = self.root
        self.inodes = {}  # Mapeia caminhos para i-nodes

    def create(self, path, is_directory=False):
        components = path.strip("/").split("/")
        name = components[-1]
        dir_inode = self._traverse(components[:-1])

        if name in dir_inode.children:
            print(f"Erro: '{name}' já existe.")
            return

        inode = INode(name, is_directory)
        dir_inode.children[name] = inode
        full_path = os.path.join(*components)
        self.inodes[full_path] = inode
        print(f"{'Diretório' if is_directory else 'Arquivo'} '{name}' criado.")

    def _traverse(self, components):
        inode = self.root
        for comp in components:
            if comp not in inode.children or not inode.children[comp].is_directory:
                raise ValueError(f"Erro: diretório '{comp}' não encontrado.")
            inode = inode.children[comp]
        return inode

    def list_dir(self, path):
        inode = self._traverse(path.strip("/").split("/"))
        if not inode.is_directory:
            print(f"Erro: '{path}' não é um diretório.")
            return
        print(f"Conteúdo de '{inode.name}':", list(inode.children.keys()))

    def change_dir(self, path):
        if path == "..":
            # Navega para o diretório pai
            if self.current_dir == self.root:
                print("Já está no diretório raiz.")
                return
            self.current_dir = self._traverse(os.path.dirname(self.current_dir.name).split("/"))
        elif path == ".":
            print(f"Você já está no diretório '{self.current_dir.name}'.")
        else:
            self.current_dir = self._traverse(path.strip("/").split("/"))
        print(f"Diretório atual: {self.current_dir.name}")

    def move(self, src, dest):
        components_src = src.strip("/").split("/")
        name = components_src[-1]
        dir_inode_src = self._traverse(components_src[:-1])

        if name not in dir_inode_src.children:
            print(f"Erro: '{name}' não encontrado.")
            return

        inode = dir_inode_src.children.pop(name)
        dir_inode_dest = self._traverse(dest.strip("/").split("/"))
        dir_inode_dest.children[name] = inode
        print(f"'{name}' movido de '{src}' para '{dest}'.")

    def write(self, path, data):
        components = path.strip("/").split("/")
        name = components[-1]
        dir_inode = self._traverse(components[:-1])

        if name not in dir_inode.children:
            print(f"Erro: '{name}' não encontrado.")
            return

        inode = dir_inode.children[name]
        if inode.is_directory:
            print(f"Erro: '{name}' é um diretório.")
            return

        inode.data_blocks.append(data)
        inode.size += len(data)
        print(f"Escrito '{data}' em '{name}'.")

    def read(self, path):
        components = path.strip("/").split("/")
        name = components[-1]
        dir_inode = self._traverse(components[:-1])

        if name not in dir_inode.children:
            print(f"Erro: '{name}' não encontrado.")
            return

        inode = dir_inode.children[name]
        if inode.is_directory:
            print(f"Erro: '{name}' é um diretório.")
            return

        print(f"Dados em '{name}':", "".join(inode.data_blocks))

    def delete(self, path):
        components = path.strip("/").split("/")
        name = components[-1]
        dir_inode = self._traverse(components[:-1])

        if name not in dir_inode.children:
            print(f"Erro: '{name}' não encontrado.")
            return

        inode = dir_inode.children.pop(name)
        if inode.is_directory and inode.children:
            print(f"Erro: '{name}' não está vazio.")
            dir_inode.children[name] = inode
            return

        print(f"'{name}' deletado.")

# Exemplo de uso:
fs = FileSystem()
fs.create("/dir1", is_directory=True)
fs.create("/dir1/arquivo1.txt")
fs.list_dir("/dir1")
fs.write("/dir1/arquivo1.txt", "Hello, World!")
fs.read("/dir1/arquivo1.txt")
fs.create("/dir2", is_directory=True)
fs.move("/dir1/arquivo1.txt", "/dir2")
fs.delete("/dir1")
fs.list_dir("/dir2")
fs.create("/dir2/dir3", is_directory=True)
fs.change_dir("/dir2/dir3")
fs.list_dir("/dir2/dir3")
fs.change_dir("/dir2")
fs.list_dir("/dir2")
