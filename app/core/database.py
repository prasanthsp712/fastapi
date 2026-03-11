from typing import List, Optional
import json
from pathlib import Path
from app.models.item import Item

class Database:
    def __init__(self, data_file: Optional[str] = None):
        self.items: List[Item] = []
        if data_file and Path(data_file).exists():
            self.load_from_file(data_file)
    
    def load_from_file(self, filepath: str) -> None:
        with open(filepath, 'r') as f:
            data = json.load(f)
            for item_data in data.get('items', []):
                self.items.append(Item(**item_data))
    
    def get_all_items(self) -> List[Item]:
        return self.items
    
    def get_item(self, item_id: int) -> Optional[Item]:
        if 0 <= item_id < len(self.items):
            return self.items[item_id]
        return None
    
    def add_item(self, item: Item) -> Item:
        item.id = len(self.items)
        self.items.append(item)
        return item

db = Database()
