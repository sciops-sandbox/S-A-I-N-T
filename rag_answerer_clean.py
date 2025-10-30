from typing import List, Optional
from dataclasses import dataclass
@dataclass
class Hit:
    title: str
    section_title: str
    text: str
    score: float
class RagAnswerer:
    def answer(self, query: str, docs: List[Hit], topk:int=5, focus_terms: Optional[List[str]]=None) -> str:
        lines = []
        focus = set(t.lower() for t in (focus_terms or []))
        for h in sorted(docs, key=lambda x: -x.score)[:topk]:
            seg = h.text
            for t in list(focus):
                seg = seg.replace(t, f[*][*]{t}[*][*])
            lines.append(seg)
        return 
.join(lines)