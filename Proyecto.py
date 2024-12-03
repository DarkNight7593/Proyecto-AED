import tkinter as tk
import random
import time
from tkinter import messagebox

# Clase Nodo
class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(1, 100)  # Prioridad aleatoria
        self.left = None
        self.right = None
        self.x = 0  # Coordenada x (se asignará en el dibujo)
        self.y = 0  # Coordenada y (se asignará en el dibujo)


# Clase Treap
import tkinter as tk
import random
import time
from tkinter import messagebox

# Clase Nodo
class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(1, 100)  # Prioridad aleatoria
        self.left = None
        self.right = None
        self.x = 0  # Coordenada x (se asignará en el dibujo)
        self.y = 0  # Coordenada y (se asignará en el dibujo)

# Clase Treap
class Treap:
    def rotate_right(self, y, visualizer):
        """Realiza una rotación a la derecha y actualiza el árbol."""
        x = y.left
        y.left = x.right
        x.right = y
        visualizer.show_rotation_message("Rotación a la derecha", [x, y])
        return x

    def rotate_left(self, x, visualizer):
        """Realiza una rotación a la izquierda y actualiza el árbol."""
        y = x.right
        x.right = y.left
        y.left = x
        visualizer.show_rotation_message("Rotación a la izquierda", [x, y])
        return y

    def insert(self, root, key, visualizer):
        """Inserta un nodo en el Treap y maneja rotaciones necesarias."""
        if root is None:
            return Node(key)
        if key < root.key:
            root.left = self.insert(root.left, key, visualizer)
            if root.left.priority > root.priority:
                root = self.rotate_right(root, visualizer)
        else:
            root.right = self.insert(root.right, key, visualizer)
            if root.right.priority > root.priority:
                root = self.rotate_left(root, visualizer)
        visualizer.draw_tree()
        return root

    def delete(self, root, key, visualizer):
        """Elimina un nodo del Treap y maneja las rotaciones necesarias."""
        if root is None:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key, visualizer)
        elif key > root.key:
            root.right = self.delete(root.right, key, visualizer)
        else:  # Nodo a eliminar encontrado
            if root.left is None or root.right is None:
                root = root.left if root.left else root.right
            else:
                if root.left.priority > root.right.priority:
                    root = self.rotate_right(root, visualizer)
                    root.right = self.delete(root.right, key, visualizer)
                else:
                    root = self.rotate_left(root, visualizer)
                    root.left = self.delete(root.left, key, visualizer)
        visualizer.draw_tree()
        return root

    def search(self, root, key, visualizer, path=[]):
        if root is None or root.key == key:
            visualizer.draw_tree(highlight_nodes=path, search=True)
            return root
        path.append(root)
        if key < root.key:
            return self.search(root.left, key, visualizer, path)
        return self.search(root.right, key, visualizer, path)

class TreapVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("Treap Visualizer")
        self.canvas = tk.Canvas(self.master, width=1000, height=700, bg="white")
        self.canvas.pack()

        self.treap = Treap()
        self.root = None

        self.controls = tk.Frame(self.master)
        self.controls.pack()

        self.entry = tk.Entry(self.controls)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.insert_button = tk.Button(self.controls, text="Insert", command=self.insert_key)
        self.insert_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.controls, text="Delete", command=self.delete_key)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.controls, text="Search", command=self.search_key)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.message_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.message_label.pack()

    def insert_key(self):
        try:
            key = int(self.entry.get())
            if self.root is None:
                self.root = self.treap.insert(self.root, key, self)
            else:
                self.root = self.treap.insert(self.root, key, self)
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def delete_key(self):
        try:
            key = int(self.entry.get())
            self.root = self.treap.delete(self.root, key, self)
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def search_key(self):
        try:
            key = int(self.entry.get())
            node = self.treap.search(self.root, key, self)
            if node:
                messagebox.showinfo("Search Result", f"Key {key} found with priority {node.priority}.")
            else:
                messagebox.showinfo("Search Result", f"Key {key} not found.")
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")

    def draw_tree(self, highlight_nodes=[], search=False, rotation=None, nodes_involved=None, action=None):
        self.canvas.delete("all")
        if self.root:
            self._draw_node(self.root, 500, 80, 300, 100, highlight_nodes, search, rotation, nodes_involved, action)

    def _draw_node(self, node, x, y, offset, level, highlight_nodes, search, rotation, nodes_involved, action):
        if node is None:
            return

        node_radius = 20

        # Resaltamos el nodo actual
        node_color = "lightblue"
        if node in highlight_nodes:
            node_color = "yellow"  # Resaltado de nodos recorridos
        elif search and node in highlight_nodes:
            node_color = "orange"  # Resaltado para búsqueda

        # Dibujar el nodo actual (círculo)
        self.canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill=node_color)
        self.canvas.create_text(x, y, text=f"{node.key}\nP:{node.priority}")

        # Aumentar el espacio entre niveles según el nivel actual
        next_offset = offset // 1.65 if level > 0 else offset

        # Dibujar el hijo izquierdo
        if node.left:
            left_x = x - next_offset
            left_y = y + 90
            self.canvas.create_line(x - node_radius, y, left_x + node_radius, left_y, width=2)
            self._draw_node(node.left, left_x, left_y, next_offset, level + 2, highlight_nodes, search, rotation, nodes_involved, action)

        # Dibujar el hijo derecho
        if node.right:
            right_x = x + next_offset
            right_y = y + 90
            self.canvas.create_line(x + node_radius, y, right_x - node_radius, right_y, width=2)
            self._draw_node(node.right, right_x, right_y, next_offset, level + 2, highlight_nodes, search, rotation, nodes_involved, action)


    def clear_message(self):
        self.canvas.delete("all")
        self.draw_tree()

    def show_rotation_message(self, rotation, nodes_involved):
        self.message_label.config(text=f"Rotation: {rotation} | Nodes involved: {', '.join(str(n.key) for n in nodes_involved)}")
        self.master.after(500, self.clear_message)
        self.master.after(7000, lambda: self.message_label.config(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = TreapVisualizer(root)
    root.mainloop()