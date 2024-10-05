import heapq
from collections import defaultdict


class HufCodec:
    class Node:
        def __init__(self, freq, symbol=None, left=None, right=None):
            self.freq = freq
            self.symbol = symbol
            self.left = left
            self.right = right

        def __lt__(self, other):
            return self.freq < other.freq

    def __init__(self, freq_dict):
        # Special case: If there is only one symbol, assign '0' to it
        if len(freq_dict) == 1:
            self.codes = {list(freq_dict.keys())[0]: "0"}
            self.tree = self.Node(0)
            return

        # Step 1: Build the Huffman Tree
        heap = [self.Node(freq, symbol) for symbol, freq in freq_dict.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = self.Node(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)

        self.tree = heap[0]  # Root of the tree
        self.codes = {}
        self._build_codes(self.tree)

    def _build_codes(self, node, code=""):
        # Build the encoding table (recursive DFS)
        if node.symbol is not None:
            self.codes[node.symbol] = code
            return

        self._build_codes(node.left, code + "0")
        self._build_codes(node.right, code + "1")

    def encode(self, text):
        # Special case for single-character input
        if self.tree.left is None and self.tree.right is None:
            return "0" * len(text)

        # Traverse the tree dynamically to find the encoding for each symbol
        def get_code(symbol, node, path=""):
            if node.symbol == symbol:
                return path
            if node.left:
                left_path = get_code(symbol, node.left, path + "0")
                if left_path:
                    return left_path
            if node.right:
                right_path = get_code(symbol, node.right, path + "1")
                if right_path:
                    return right_path
            return None

        return "".join(get_code(symbol, self.tree) for symbol in text)

    def decode(self, encoded):
        # Handle single character special case by checking if the root is a leaf
        if self.tree.left is None and self.tree.right is None:
            return self.tree.symbol * len(encoded)

        # Decode a sequence of '0's and '1's to a string of symbols
        result = []
        node = self.tree

        for bit in encoded:
            if bit not in {"0", "1"}:
                raise ValueError(f"Invalid bit in encoded string: {bit}")

            if bit == "0":
                node = node.left
            else:
                node = node.right

            if node.symbol is not None:
                result.append(node.symbol)
                node = self.tree  # Go back to the root

        return "".join(result)

    def to_dict(self):
        return self.codes
