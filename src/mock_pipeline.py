import json
from pathlib import Path

#defining the data path
DATA_FILE = Path(__file__).parent.parent / "data" / "sample_papers.json"


def load_sample_papers(): #function that all end-points call
    """Read the mock papers from the local JSON file and return them as a list."""
    #read-only 
    with open(DATA_FILE, "r") as f:
        #reading and transforming as python lists and dicts
        papers = json.load(f)
    return papers


if __name__ == "__main__":
    papers = load_sample_papers()
    print(f"Loaded {len(papers)} papers")
    for paper in papers:
        print("-", paper["title"])