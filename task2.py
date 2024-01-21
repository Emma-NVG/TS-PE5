from graphviz import Digraph
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.value = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if root.value < key:
                root.right = self.insert(root.right, key)
            else:
                root.left = self.insert(root.left, key)
        return root

    def search(self, root, key):
        if root is None:
            return False
        if root.value == key:
            return True
        elif root.value < key:
            return self.search(root.right, key)
        else:
            return self.search(root.left, key)

    def delete(self, root, key):
        if root is None:
            return root
        if key < root.value:
            root.left = self.delete(root.left, key)
        elif key > root.value:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.find_min_value_node(root.right)
            root.value = temp.value
            root.right = self.delete(root.right, temp.value)
        return root

    def find_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.inorder_traversal(root.left, result)
            result.append(root.value)
            self.inorder_traversal(root.right, result)
        return result

    def preorder_traversal(self, root, result=None):
        if result is None:
            result = []
        if root:
            result.append(root.value)
            self.preorder_traversal(root.left, result)
            self.preorder_traversal(root.right, result)
        return result

    def postorder_traversal(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.postorder_traversal(root.left, result)
            self.postorder_traversal(root.right, result)
            result.append(root.value)
        return result


def test_traverse_functions(bst):
    test_results = {}

    inorder_result = bst.inorder_traversal(bst.root)
    test_results['inorder_sorted'] = inorder_result == sorted(inorder_result)

    preorder_result = bst.preorder_traversal(bst.root)
    test_results['preorder_start_root'] = preorder_result[0] == bst.root.value

    postorder_result = bst.postorder_traversal(bst.root)
    test_results['postorder_end_root'] = postorder_result[-1] == bst.root.value

    return test_results, inorder_result, preorder_result, postorder_result


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    width = 2 ** (layer + 1)
    pos[node.value] = (x, y)
    if node.left:
        graph.add_edge(node.value, node.left.value)
        add_edges(graph, node.left, pos, x - width, y - 1, layer + 1)
    if node.right:
        graph.add_edge(node.value, node.right.value)
        add_edges(graph, node.right, pos, x + width, y - 1, layer + 1)
    return pos

def plot_bst_nx(bst):
    graph = nx.DiGraph()
    pos = {}
    if bst.root:
        pos = add_edges(graph, bst.root, pos)
    nx.draw(graph, pos=pos, with_labels=True, arrows=False)
    plt.show()


def save_bst_plot(bst, filename):
    def add_edges(graph, node, pos, x=0, y=0, layer=1):
        width = 2 ** (layer + 1)
        pos[node.value] = (x, y)
        if node.left:
            graph.add_edge(node.value, node.left.value)
            add_edges(graph, node.left, pos, x - width, y - 1, layer + 1)
        if node.right:
            graph.add_edge(node.value, node.right.value)
            add_edges(graph, node.right, pos, x + width, y - 1, layer + 1)
        return pos

    graph = nx.DiGraph()
    pos = {}
    if bst.root:
        pos = add_edges(graph, bst.root, pos)

    plt.figure(figsize=(12, 8))

    nx.draw(graph, pos=pos, with_labels=True, arrows=False, node_size=700, font_size=10)

    plt.savefig(filename, format='png', bbox_inches='tight')
    plt.close()


def save_and_plot(bst, filename):
    plt.figure(figsize=(12, 8))
    graph = nx.DiGraph()
    pos = add_edges(graph, bst.root, {})
    nx.draw(graph, pos=pos, with_labels=True, arrows=False, node_size=700, font_size=10)
    plt.savefig(filename, format='png', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    a = [49, 38, 65, 97, 60, 76, 13, 27, 5, 1]
    bst = BinarySearchTree()
    for key in a:
        bst.root = bst.insert(bst.root, key)
    print("BST created with list 'a'")
    print("In-order traversal of the initial BST:", bst.inorder_traversal(bst.root))


    b = [149, 38, 65, 197, 60, 176, 13, 217, 5, 11]
    for key in b:
        bst.insert(bst.root, key)
    print("\nBST after inserting elements from list 'b'")
    print("In-order traversal after inserts:", bst.inorder_traversal(bst.root))

    for key in b:
        if key not in a:
            bst.delete(bst.root, key)
    print("\nBST after deleting elements from list 'b' not in 'a'")
    print("In-order traversal after deletes:", bst.inorder_traversal(bst.root))

    c = [49, 38, 65, 97, 64, 76, 13, 77, 5, 1, 55, 50, 24]
    for key in c:
        if key not in a :
            bst.insert(bst.root, key)
            print(f"\nInserted {key} from list 'c'")
            print("In-order traversal after insert:", bst.inorder_traversal(bst.root))
        elif bst.search(bst.root, key):
            print(f"\nDeleted {key} from list 'c'")

    test_values = {
        'insert': [100, 50, 150],
        'search': [65, 100, 50],
        'delete': [100, 1],
        'traverse': [],
    }

    bst = BinarySearchTree()
    for key in a:
        bst.root = bst.insert(bst.root, key)


    for value in test_values['search']:
        result = bst.search(bst.root, value)
        if result is not None:
            print(f"Value {value} found in the tree.")
        else:
            print(f"Value {value} not found in the tree.")

    for value in test_values['insert']:
        bst.insert(bst.root, value)
        save_and_plot(bst, f'bst_test_insert.png')

    for value in test_values['delete']:
        bst.delete(bst.root, value)
        save_and_plot(bst, f'bst_test_delete.png')

    traverse_test_results, inorder, preorder, postorder = test_traverse_functions(bst)
    print(traverse_test_results)
    print(inorder)
    print(preorder)
    print(postorder)
