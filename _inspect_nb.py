import json

path = r"c:\Users\Vítor\workspace\analise_estados_ricos_dados (1).ipynb"
with open(path, encoding="utf-8") as f:
    nb = json.load(f)

for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    print(f"--- cell {i} ({len(src.splitlines())} lines) exec={c.get('execution_count')} ---")
    print(src)
    for o in c.get("outputs", []):
        if o.get("output_type") == "error":
            print("ERROR:", o.get("ename"), "-", o.get("evalue"))
            for t in o.get("traceback", [])[-2:]:
                print(t[:400])
    print()
