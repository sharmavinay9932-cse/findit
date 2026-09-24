from repositories.item_repository import ItemRepository
from services.image_service import ImageService
from datetime import datetime

class ItemService:
    def __init__(self):
        self.lost_repo = ItemRepository('lost')
        self.found_repo = ItemRepository('found')

    def _get_repo(self, type):
        return self.lost_repo if type == 'lost' else self.found_repo

    def report_item(self, type, data, file=None):
        repo = self._get_repo(type)
        
        image_filename = None
        if file:
            image_filename = ImageService.save_image(file, type)
            
        item = {
            'user_id': data.get('user_id'),
            'name': data.get('name'),
            'category': data.get('category'),
            'brand': data.get('brand', ''),
            'color': data.get('color', ''),
            'location': data.get('location'),
            'date': data.get('date'),
            'time': data.get('time', ''),
            'description': data.get('description', ''),
            'unique_features': data.get('unique_features', ''),
            'image': image_filename,
            'status': 'reported', # reported, returned, claimed
            'created_at': datetime.now().isoformat(),
            'type': type
        }
        return repo.create(item)

    def get_all_items(self):
        lost = self.lost_repo.get_all()
        for i in lost: i['type'] = 'lost'
        found = self.found_repo.get_all()
        for i in found: i['type'] = 'found'
        return lost + found

    def get_item(self, item_id, type=None):
        if type:
            return self._get_repo(type).get_by_id(item_id)
        # Try both
        item = self.lost_repo.get_by_id(item_id)
        if item:
            item['type'] = 'lost'
            return item
        item = self.found_repo.get_by_id(item_id)
        if item:
            item['type'] = 'found'
        return item
    
    def get_items_by_user(self, user_id):
        lost = self.lost_repo.get_by_user_id(user_id)
        for i in lost: i['type'] = 'lost'
        found = self.found_repo.get_by_user_id(user_id)
        for i in found: i['type'] = 'found'
        return {'lost': lost, 'found': found}

    def update_item_status(self, item_id, type, status):
        repo = self._get_repo(type)
        return repo.update(item_id, {'status': status})
