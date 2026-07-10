import sqlite3

db_path = r"G:\My Drive\UCL\AI Lab\obsidian practice\zotero_copy.sqlite"
out_path = r"G:\My Drive\UCL\AI Lab\obsidian practice\zotero_titles.txt"
try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT collectionID, collectionName FROM collections WHERE collectionName LIKE '%Kim%';")
    collections = c.fetchall()
    
    with open(out_path, "w", encoding="utf-8") as f:
        for col in collections:
            col_id = col[0]
            col_name = col[1]
            f.write(f"Collection: {col_name}\n")
            c.execute("""
                SELECT v.value 
                FROM collectionItems ci
                JOIN itemData id ON ci.itemID = id.itemID
                JOIN fields f ON id.fieldID = f.fieldID
                JOIN itemDataValues v ON id.valueID = v.valueID
                WHERE ci.collectionID = ? AND f.fieldName = 'title'
            """, (col_id,))
            titles = c.fetchall()
            for t in titles:
                f.write(f"- {t[0]}\n")
except Exception as e:
    print("Error:", e)
