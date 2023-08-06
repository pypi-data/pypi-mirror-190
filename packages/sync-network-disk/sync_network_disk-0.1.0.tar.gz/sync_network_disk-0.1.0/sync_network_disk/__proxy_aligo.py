from .__aligo import Aligo

class AligoIsNone(Exception): pass

class ProxyAligo:
    def __init__(self, ali: Aligo=None) -> None:
        self.ali = ali
    def __lshift__(self, other):
        self.ali = other
    def __getattr__(self, k: str):
        if self.ali is None:
            raise AligoIsNone()
        return getattr(self.ali, k)