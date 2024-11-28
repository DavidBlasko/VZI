# deque is better form of list for pop/append at both ends with time complexity O(1)
from collections import deque

class Node:
    def __init__(self, vertice_data):
        self.vertice_data = vertice_data # number in dedicated vertice, often named KEY
        self.left = None # left child
        self.right = None # right child
        self.height = 1


# self balancing BST algorithm published in 1962 by Adelson-Veselsky and Landis
class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node): # support func, just to get height
        return False if not node else (node.height)
    
    def get_balance_factor(self, node): # func to get balance factor, in this case must be {-1, 0, 1}, so two next to each other vertices have no more than one level in difference
        return False if not node else (self.get_height(node.left) - self.get_height(node.right))
    
    def get_min_node(self, node): # to search smaller number than current node
        return node if not node or node.left else self.get_min_node(node.left)
    
    def search(self, vertice_data): # searching with time complexity O(log(n))
        x = self.root
        while x is not None and vertice_data != x.vertice_data:
            if vertice_data < x.vertice_data:
                x = x.left
            else:
                x = x.right
        return x.vertice_data if x else 'Number not found'
    
    def left_rotate(self, node): # rotating tree vertices left with time complexity O(1)
        #    A                  B
        #   / \                / \
        #  X   B     ---->    A   Z
        #     / \            / \
        #    Y   Z          X   Y
        B = node.right
        Y = B.left

        B.left = node
        node.right = Y

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        B.height = 1 + max(self.get_height(B.left), self.get_height(B.right))

        return B

    def right_rotate(self, node): # same as left_rotate but mirrored
        #     B                 A
        #    / \               / \
        #   A   Z     <----   X   B
        #  / \                   / \
        # X   Y                 Y   Z
        A = node.left
        Y = A.right

        A.right = node
        node.left = Y

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        A.height = 1 + max(self.get_height(A.left), self.get_height(A.right))

        return A

    def insert_vertice(self, root, vertice_data): # func for inserting vertice with time complexity O(log(n))
        if not root:
            return Node(vertice_data)
        elif vertice_data < root.vertice_data:
            root.left = self.insert_vertice(root.left, vertice_data)
        else:
            root.right = self.insert_vertice(root.right, vertice_data)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # updating the balance factor and rebalancing the tree if needed
        balance_factor = self.get_balance_factor(root)

        if balance_factor > 1 and vertice_data < root.left.vertice_data:
            return self.right_rotate(root)
        elif balance_factor < -1 and vertice_data > root.right.vertice_data:
            return self.left_rotate(root)
        elif balance_factor > 1 and vertice_data > root.left.vertice_data:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        elif balance_factor < -1 and vertice_data < root.left.vertice_data:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    def delete_vertice(self, root, vertice_data): # func for deleting vertice in tree with time complexity O(log(n))
        if not root:
            return root
        elif vertice_data < root.vertice_data:
            root.left = self.delete_vertice(root.left, vertice_data)
        elif vertice_data > root.vertice_data:
            root.right = self.delete_vertice(root.right, vertice_data)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp
            # finding in-order successor
            temp = self.get_min_node(root.right)
            root.vertice_data = temp.vertice_data
            root.right = self.delete_vertice(root.right, temp.vertice_data)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # updating the balance factor and balance the tree
        balance_factor = self.get_balance_factor(root)

        if balance_factor > 1 and self.get_balance_factor(root.left) >= 0:
            return self.right_rotate(root)
        elif balance_factor < -1 and self.get_balance_factor(root.right) <= 0:
            return self.left_rotate(root)
        elif balance_factor > 1 and self.get_balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        elif balance_factor < -1 and self.get_balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    def print_tree_graph(self): # print func to visualize tree in console by levels
        if not self.root:
            print("Fail, tree is empty.")
            return
        
        # use a queue to traverse the tree level by level
        queue = deque([(self.root, 0)])  # (node, level)
        current_level = 0
        level_output = []

        while queue:
            node, level = queue.popleft()

            if level > current_level:
                # print the nodes of the previous level
                print(f"Level {current_level}:", " ".join(level_output))
                level_output = []
                current_level = level

            # add current node data or "N" for None to the level output
            level_output.append(str(node.vertice_data) if node else "N")

            # add children to the queue
            if node:
                queue.append((node.left, level + 1))
                queue.append((node.right, level + 1))

        # print the last level
        if level_output:
            print(f"Level {current_level}:", " ".join(level_output))


if __name__ == "__main__":
    avl = AVLTree()   
    vertice_data_arr = [50, 25, 75, 15, 35, 60, 120, 10, 68, 90, 125, 83, 100]
    
    for data in vertice_data_arr:
        avl.root = avl.insert_vertice(avl.root, data)
    
    # AVL printed out
    avl.print_tree_graph()
    result = avl.search(125)
    print(f'Search for 125: {result}')

    # AVL test for deleting vertice
    avl.delete_vertice(avl.root, 125)
    print('\nVertice with data 125 deleted.')
    avl.print_tree_graph()
    result = avl.search(125)
    print(f'Search for 125: {result}')

    # AVL test for inserting vertice
    avl.insert_vertice(avl.root, 123)
    print('\nVertice with data 123 inserted.')
    avl.print_tree_graph()
    result = avl.search(123)
    print(f'Search for 123: {result}')