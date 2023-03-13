from typing import List
from tqdm import tqdm
from Bio import Entrez

class Crawler():


    def __init__(self, 
                 init_names: List[str], 
                 email: str,
                 max_authors: int = 100,
                ) -> None:
        self.db = "pubmed"
        self.names = init_names
        self.max_authors = max_authors
        Entrez.email = email


    def get_authors_pmids(self, name: str) -> List[str]:
        handle = Entrez.esearch(db="pubmed", term=name, retmax=10000)
        record = Entrez.read(handle)
        ids = record["IdList"]
        return ids


    def get_abstracts(self, ids: List[str], max_n: int = 10) -> List[str]:
        abstracts = []
        # for n in tqdm(range(max_n)):
            # id = ids[n]
        for i in tqdm(ids):
            handle = Entrez.efetch(db=self.db, 
                                      id=i, 
                                      retmode="text", 
                                      rettype="abstract")
            abstracts += [handle.read()]
        return abstracts
    
    def get_paper_authors(self, id: str,) -> List[str]:
        authors = []
        handle = Entrez.esummary(db=self.db, id=id, retmode="xml")
        records = Entrez.parse(handle)
        for record in records:
            # each record is a Python dictionary or list.
            authors +=  record['AuthorList']
        return authors

    def get_coauthors(self, name: str) -> List[str]:
        pmids = self.get_authors_pmids(name)
        coauthors = {}
        for id in tqdm(pmids):
            authors = self.get_paper_authors(id)
            for author in authors:
                if author != name:
                    if author in coauthors:
                        coauthors[author] += 1
                    else:
                        coauthors[author] = 1
        return coauthors