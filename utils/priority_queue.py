from heapq import heappop, heappush


class priority_queue:
    def __init__(self, elements=[]):
        self._heap = []
        for element in elements:
            heappush(self._heap, element)

    def append(self, item):
        heappush(self._heap, item)

    def appendleft(self, item):
        heappush(self._heap, item)

    def pop(self):
        if not self._heap:
            raise IndexError("pop from an empty priority queue")

        return heappop(self._heap)

    def popleft(self):
        if not self._heap:
            raise IndexError("pop from an empty priority queue")

        return heappop(self._heap)

    def __len__(self):
        return len(self._heap)

    def __iter__(self):
        return iter(sorted(self._heap))

    def __repr__(self):
        return f"priority_queue({sorted(self._heap)})"
