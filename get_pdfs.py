import sqlite3
import os
import shutil

db_path = r"G:\My Drive\UCL\AI Lab\obsidian practice\zotero_copy.sqlite"
zotero_storage = r"G:\My Drive\UCL\Zotero\storage"
target_dir = r"G:\My Drive\UCL\AI Lab\obsidian practice\raw\sources"

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT collectionID FROM collections WHERE collectionName LIKE '%Kim%';")
col_id = c.fetchone()[0]

c.execute("SELECT itemID FROM collectionItems WHERE collectionID = ?", (col_id,))
items = [row[0] for row in c.fetchall()]

for item_id in items:
    c.execute("SELECT a.path, i.key FROM itemAttachments a JOIN items i ON a.itemID = i.itemID WHERE a.parentItemID = ? AND a.contentType = 'application/pdf'", (item_id,))
    attachments = c.fetchall()
    for att in attachments:
        path_val = att[0]
        key = att[1]
        if path_val and path_val.startswith('storage:'):
            filename = path_val.replace('storage:', '')
            full_path = os.path.join(zotero_storage, key, filename)
            if os.path.exists(full_path):
                target = os.path.join(target_dir, filename)
                shutil.copy(full_path, target)
