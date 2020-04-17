import array
import collections
import itertools

FREE = -1
DUMMY = -2


class Dict(collections.MutableMapping):
    'Space efficient dictionary with fast iteration and cheap resizes'

    @staticmethod
    def _gen_probes(hashvalue, mask):
        'Same sequence of probes used in the current dictionary design'
        PERTURB_SHIFT = 5
        if hashvalue < 0:
            hashvalue = -hashvalue
        i = hashvalue & mask      # 相当于对 indices 的长度取模

        yield i

        perturb = hashvalue
        while True:
            i = (5 * i + perturb + 1) & 0xFFFFFFFFFFFFFFFF    # 与上 64 位
            yield i & mask
            perturb >>= PERTURB_SHIFT

    def _lookup(self, key, hashvalue):
        'Same lookup logic as currently used in real dicts'
        assert self.filled < len(self.indices)  # At least one open slot
        freeslot = None

        for i in self._gen_probes(hashvalue, len(self.indices) - 1):
            index = self.indices[i]
            if index == FREE:
                return (FREE, i) if freeslot is None else (DUMMY, freeslot)
            elif index == DUMMY:
                if freeslot is None:
                    freeslot = i
            elif (self.keylist[index] is key or self.hashlist[index] == hashvalue and self.keylist[index] == key):  # 这里对 key compare 做了优化
                return (index, i)

    @staticmethod
    def _make_index(n):
        'New sequence of indices using the smallest possible datatype'
        if n <= 2 ** 7: return array.array('b', [FREE]) * n  # signed char
        if n <= 2 ** 15: return array.array('h', [FREE]) * n  # signed short
        if n <= 2 ** 31: return array.array('l', [FREE]) * n  # signed long
        return [FREE] * n

    def _resize(self, n):
        '''
        Reindex the existing hash/key/value entries
        Entries do not get moved, they only get new indices
        No calls are made to hash() or __eq__().
        :return:
        '''
        n = 2 ** n.bit_length()
        self.indices = self._make_index(n)
        for index, hashvalue in enumerate(self.hashlist):
            for i in Dict._gen_probes(hashvalue, n - 1):
                if self.indices[i] == FREE:
                    break
            self.indices[i] = index
        self.filled = self.used

    def clear(self):
        self.indices = self._make_index(8)
        self.used = 0       # DUMMY + ACTIVE = indices length - FREE
        self.filled = 0     # ACTIVE

        self.hashlist = []
        self.keylist = []
        self.valuelist = []


    def __getitem__(self, key):
        hashvalue = hash(key)
        index, i = self._lookup(key, hashvalue)
        if index < 0:
            raise KeyError(key)
        return self.valuelist[index]

    def __setitem__(self, key, value):
        hashvalue = hash(key)
        index, i = self._lookup(key, hashvalue)
        if index < 0:
            self.indices[i] = self.used
            self.hashlist.append(hashvalue)
            self.keylist.append(key)
            self.valuelist.append(value)
            self.used += 1
            if index == FREE:
                self.filled += 1
                if self.filled * 3 > len(self.indices) * 2:
                    self._resize(4 * len(self))

        else:
            self.valuelist[index] = value

    def __delitem__(self, key):
        hashvalue = hash(key)
        index, i = self._lookup(key, hashvalue)
        if index < 0:
            raise KeyError(key)

        self.indices[i] = DUMMY
        self.used -= 1
        # if needed swap with the lastmost entry to avoid leaving a "hole"
        if index != self.used:
            lasthash = self.hashlist[-1]
            lastkey = self.keylist[-1]
            lastvalue = self.valuelist[-1]
            lastindex, j = self._lookup(lastkey, lasthash)
            assert lastindex >= 0 and i != j
            self.indices[j] = index
            self.hashlist[index] = lasthash
            self.keylist[index] = lastkey
            self.valuelist[index] = lastvalue
        self.hashlist.pop()
        self.keylist.pop()
        self.valuelist.pop()

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'keylist'):
            self.clear()
        self.update(*args, **kwargs)

    def __len__(self):
        return self.used

    def __iter__(self):
        return iter(self.keylist)

    def iterkeys(self):
        return iter(self.keylist)

    def keys(self):
        return list(self.keylist)

    def itervalues(self):
        return iter(self.valuelist)

    def values(self):
        return list(self.valuelist)

    def iteritems(self):
        return itertools.izip(self.keylist, self.valuelist)

    def items(self):
        return zip(self.keylist, self.valuelist)

    def __contains__(self, key):
        index, i = self._lookup(key, hash(key))
        return index >= 0

    def get(self, key, default=None):
        index, i = self._lookup(key, hash(key))
        return self.valuelist[index] if index >= 0 else default

    def popitem(self):
        if not self.keylist:
            raise KeyError('popitem(): dictionary is empty')
        key = self.keylist[-1]
        value = self.valuelist[-1]
        del self[key]
        return key, value

    def __repr__(self):
        return 'Dict(%r)' % self.items()

    def show_structure(self):
        'Diagnostic method. not part of the api'

        print('=' * 50)
        print(self)
        print('Indices:', self.indices)

        for i, row in enumerate(zip(self.hashlist, self.keylist, self.valuelist)):
            print(i, row)

        print('-' * 50)

if __name__ == '__main__':
    # 增
    # 重点关注 __setitem__
    # 增的时候可能发生 collide 的情况
    d = Dict([('key0', 'value0'), ('key1', 'value1'), ('key2', 'value2'), ('key3', 'value3')])
    d.update({'key4': 'value4', 'key5': 'value5', 'key6': 'value6'})


    # 删
    # 重点关注 __delitem__
    del d['key3']
    del d['key4']

    # 改
    d['key5'] = 'value55555555555'

    # 查

    d.show_structure()
