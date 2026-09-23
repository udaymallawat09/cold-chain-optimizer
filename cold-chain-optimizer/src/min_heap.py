class MinHeap:
    def __init__(self):
        # The heap will store tuples in the format: (accumulated_degradation, node_id)
        self.heap = []
        
    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)
        
    def pop(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
            
        root = self.heap[0]
        # Move the last item to the root and sift down to maintain heap property
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def is_empty(self):
        return len(self.heap) == 0

    def _sift_up(self, index):
        parent = (index - 1) // 2
        # Compare kinetic costs (index 0 of the tuple); swap if child is smaller than parent
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def _sift_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        # Check if left child exists and has a smaller degradation cost
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
            
        # Check if right child exists and has a smaller degradation cost
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        # If the smallest is not the current index, swap and continue sifting down
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._sift_down(smallest)