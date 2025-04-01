class MaxHeap:
    def __init__(self):
        self.data = []
        self.size = 0

    def top(self):
        if not self.size:
            return None
        return self.data[0]

    def insert(self, e):
        self.data.append(e)
        self.size += 1
        i = self.size-1
        while i > 0:
            parent = (i+1)//2 - 1
            if self.data[i] > self.data[parent]:
                self.data[parent], self.data[i] = self.data[i], self.data[parent]
                i = parent
            else:
                break

    def remove(self):
        if not self.size:
            return None
        if self.size == 1:
            self.size -= 1
            return self.data.pop()
        
        self.data[0], self.data[self.size-1] = self.data[self.size-1], self.data[0]
        x = self.data.pop()
        self.size -= 1
        self.heapify(0)
        return x

    def heapify(self, i):
        largest = i
        while True:
            left = 2*i + 1
            right = 2*i + 2
            if left < self.size and self.data[left] > self.data[largest]:
                largest = left
            if right < self.size and self.data[right] > self.data[largest]:
                largest = right
            if largest != i:
                self.data[i], self.data[largest] = self.data[largest], self.data[i]
                i = largest
            else:
                break
