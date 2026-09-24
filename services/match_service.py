from repositories.item_repository import ItemRepository
from repositories.match_repository import MatchRepository

class MatchService:
    def __init__(self):
        self.lost_repo = ItemRepository('lost')
        self.found_repo = ItemRepository('found')
        self.match_repo = MatchRepository()

    def calculate_similarity(self, lost_item, found_item):
        score = 0
        
        # Category: 20%
        if lost_item.get('category') == found_item.get('category'):
            score += 20
            
        # Item name: 20% (basic subset check)
        lost_name = str(lost_item.get('name', '')).lower()
        found_name = str(found_item.get('name', '')).lower()
        if lost_name in found_name or found_name in lost_name:
            score += 20
            
        # Brand: 15%
        if lost_item.get('brand') and lost_item.get('brand').lower() == found_item.get('brand', '').lower():
            score += 15
            
        # Color: 10%
        if lost_item.get('color') and lost_item.get('color').lower() == found_item.get('color', '').lower():
            score += 10
            
        # Location: 15%
        if lost_item.get('location') and lost_item.get('location').lower() == found_item.get('location', '').lower():
            score += 15
            
        # Date: 10%
        if lost_item.get('date') == found_item.get('date'):
            score += 10
            
        # Description: 10%
        lost_desc_words = set(str(lost_item.get('description', '')).lower().split())
        found_desc_words = set(str(found_item.get('description', '')).lower().split())
        if lost_desc_words and found_desc_words and len(lost_desc_words.intersection(found_desc_words)) > 0:
            score += 10
            
        return score

    def find_potential_matches(self, lost_item_id):
        lost_item = self.lost_repo.get_by_id(lost_item_id)
        if not lost_item:
            return []
            
        # 1. Query active found items
        found_items = self.found_repo.get_all()
        
        # 2. Calculate and upsert
        for found_item in found_items:
            # Don't match if it's already claimed/returned/closed
            if found_item.get('status') in ['returned', 'claimed', 'closed']:
                continue
                
            score = self.calculate_similarity(lost_item, found_item)
            if score >= 40: # Only store matches with at least some similarity
                self.match_repo.upsert_match(lost_item_id, found_item.get('id'), score)
                
        # 3. Retrieve and return formatted matches from the database
        return self.match_repo.get_by_lost_item_id(lost_item_id)
