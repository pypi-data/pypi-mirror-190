from dataclasses import dataclass
from typing import List, Tuple, Any, Union, Dict, Callable, Generator, Optional, Set
from prettytable import PrettyTable
import tempfile
from struct import pack, unpack
import random
import pickle
from pathlib import Path
from glob import glob
from faker import Faker
import secrets
from itertools import islice
import time
from mines_data_engineering.data_generation import city_generator
fake = Faker()

# constants
PAGE_SIZE_NUMREC = 1000 # number of records in each page

# utility functions for iterators
def take(iterable, n):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(islice(it, n))):
        yield batch

def nth(iterable, n, default=None):
    "Returns the nth item or a default value"
    return next(islice(iterable, n, None), default)

# define set of domains for our attributes
AtomicType = Union[int, str, bool]
# define conditions for filters
Condition = Callable[['Record'], bool]

"""
Simplified implementation:

@dataclass
class Record:
    fields: Tuple[AtomicType]
"""

@dataclass
class Record:
    """
    The Record type represents a tuple in a relation
    """
    fields: Tuple[AtomicType]

    def __getitem__(self, key):
        return self.fields[key]
    
    def serialize(self) -> bytes:
        """Serialize 4-byte length, then pickled tuple of fields"""
        f = pickle.dumps(self.fields)
        return pack('<I', len(f)) + f
    
    @classmethod
    def deserialize(cls, b: bytes):
        """Load a record from a pickled tuple of fields"""
        fields = pickle.loads(b)
        return cls(fields)

@dataclass
class Attribute:
    """Represents an attribute of a relational schema"""
    name: str
    dtype: type # assume to be valid types...


"""
Simplified Relation representation

@dataclass
class Relation:
    name: str
    attributes: List[Attribute]
    records: List[Record]
"""

@dataclass
class Relation:
    name: str # name of the relation
    attributes: List[Attribute] # relation schema
    _records: Generator[Record, None, None] # internal iterator for records
    
    @property
    def records(self):
        """Iterator over the relation's records"""
        for r in self._records:
            if isinstance(r, tuple):
                yield Record(fields=r)
            else:
                yield r

    @property
    def attribute_names(self) -> Set[str]:
        return {a.name for a in self.attributes}

    def index_of_attribute(self, name: str) -> int:
        """Returns the position of the given attribute in the relation
        as an index"""
        assert name in self.attribute_names
        for idx, att in enumerate(self.attributes):
            if att.name == name:
                return idx
    
    def uniquify_attributes(self, wrt: Set[str]) -> List[Attribute]:
        return [
            Attribute(a.name if a.name not in wrt else f'{self.name}.{a.name}', a.dtype)
            for a in self.attributes
        ]
    
    def copy_schema(self, name: str) -> "Relation":
        """return new empty relation w/ same schema but new name"""
        return Relation(name, self.attributes, [])

    def record_at(self, idx: int) -> Optional[Record]:
        i = nth(self._records, idx)
        if i is not None and isinstance(i, tuple):
            return Record(i)
        return i

    def size(self) -> Tuple[int, int]:
        return (len(self.attributes), len(list(self.records)))
            
    def generate_records(self, n: int, generators: List[Callable]):
        """Generate N random records for this relation"""
        for _ in range(n):
            tmp = []
            for idx, a in enumerate(self.attributes):
                if generators[idx] is not None:
                    tmp.append(generators[idx]())
                elif a.dtype == str:
                    tmp.append(fake.text(20))
                elif a.dtype == int:
                    tmp.append(random.randint(1,100000))
                elif a.dtype == bool:
                    tmp.append(random.random() < .5)
            self.insert(Record(tuple(tmp)))
    
    def insert(self, rec: Record):
        """Add a record to the relation"""
        assert isinstance(self._records, list)
        self._records.append(rec)

    def __repr__(self):
        t = PrettyTable()
        t.field_names = [a.name for a in self.attributes]
        ri = iter(self.records)
        for rec in take(ri, 10):
            t.add_row(rec.fields)
        try:
            next(ri)
            t.add_row(['...' for _ in range(len(self.attributes))])
        except StopIteration:
            pass
        return t.get_string()


######################
# Relational Operators
######################


def scan(R: Relation):
    for record in R.records:
        for attr, val in zip(R.attributes, record.fields):
            print(f"{attr.name}={val}",end='')
        print('')

def rename(R: Relation, mapping: Dict[str, str]) -> Relation:
    new_att = [
        Attribute(mapping.get(a.name, a.name), a.dtype)
        for a in R.attributes        
    ]
    return Relation(R.name, new_att, R._records)

def project(R: Relation, A: List[int]) -> Relation:
    """keep all attributes in A from R"""
    new_attributes = [R.attributes[i] for i in A]
    new_tuples = map(lambda r: [r.fields[i] for i in A], R.records)
    new_R = Relation(f"{R.name}-project", new_attributes, new_tuples)
    return new_R

def select(R: Relation, C: Condition) -> Relation:
    new_records = filter(C, R.records)
    return Relation(f"{R.name}-select", R.attributes, new_records)

def cross(R: Relation, S: Relation) -> Relation:
    # handle renaming!
    shared_names = R.attribute_names.intersection(S.attribute_names)
    new_attributes = R.uniquify_attributes(shared_names) + S.uniquify_attributes(shared_names)
    
    def _generate_tuples():
        for r_rec in R.records:
            for s_rec in S.records:
                yield Record(r_rec.fields + s_rec.fields)
            
    return Relation(f"{R.name}-join-{S.name}", new_attributes, _generate_tuples())

def join(R: Relation, S: Relation, C: Condition) -> Relation:
    tmp = cross(R, S)
    return select(tmp, C)

def natural_join(R: Relation, S: Relation) -> Relation:
    # determine shared attributes
    shared_attributes = R.attribute_names.intersection(S.attribute_names)
    # figure out their indices
    R_indices = [R.index_of_attribute(a) for a in shared_attributes]
    S_indices = [len(R.attributes) + S.index_of_attribute(a) for a in shared_attributes]
    def _condition(r: Record) -> bool:
        for (Ridx, Sidx) in zip(R_indices, S_indices):
            if r[Ridx] != r[Sidx]:
                return False
        return True

    tmp = cross(R, S)
    return select(tmp, _condition)
