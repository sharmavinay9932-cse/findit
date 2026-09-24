import json
import os
import uuid
from config.config import Config

class BaseRepository:
    def __init__(self, filename):
        self.filepath = os.path.join(Config.DATA_FOLDER, filename)
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def _read_data(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _write_data(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def get_all(self):
        return self._read_data()

    def get_by_id(self, item_id):
        data = self._read_data()
        for item in data:
            if item.get('id') == item_id:
                return item
        return None

    def create(self, item):
        data = self._read_data()
        if 'id' not in item:
            item['id'] = str(uuid.uuid4())
        data.append(item)
        self._write_data(data)
        return item

    def update(self, item_id, updated_item):
        data = self._read_data()
        for i, item in enumerate(data):
            if item.get('id') == item_id:
                data[i] = {**item, **updated_item}
                data[i]['id'] = item_id # Ensure ID doesn't change
                self._write_data(data)
                return data[i]
        return None

    def delete(self, item_id):
        data = self._read_data()
        new_data = [item for item in data if item.get('id') != item_id]
        if len(data) != len(new_data):
            self._write_data(new_data)
            return True
        return False
