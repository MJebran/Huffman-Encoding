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
        if len(freq_dict) == 1:
            self.tree = self.Node(0, list(freq_dict.keys())[0])
            return

        heap = [self.Node(freq, symbol) for symbol, freq in freq_dict.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = self.Node(left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, merged)

        self.tree = heap[0]

    def _get_code(self, symbol, node, path=""):
        if node.symbol == symbol:
            return path
        if node.left:
            left_path = self._get_code(symbol, node.left, path + "0")
            if left_path:
                return left_path
        if node.right:
            right_path = self._get_code(symbol, node.right, path + "1")
            if right_path:
                return right_path
        return None

    def encode(self, text):
        if self.tree.left is None and self.tree.right is None:
            return "0" * len(text)

        return "".join(self._get_code(symbol, self.tree) for symbol in text)

    def decode(self, encoded):
        if self.tree.left is None and self.tree.right is None:
            return self.tree.symbol * len(encoded)

        result = []
        node = self.tree

        for bit in encoded:
            if bit == "0":
                node = node.left
            else:
                node = node.right

            if node.symbol is not None:
                result.append(node.symbol)
                node = self.tree

        return "".join(result)
