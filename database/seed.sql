USE findit_db;

-- Seed Categories
INSERT IGNORE INTO categories (category_name) VALUES 
('Electronics'),
('Documents'),
('Bags'),
('Books'),
('Accessories'),
('Clothing'),
('Keys'),
('ID Cards'),
('Other');

-- Seed Locations
INSERT IGNORE INTO locations (location_name, description) VALUES 
('Library 2nd Floor', 'Quiet study area on the second floor'),
('Cafe', 'Campus central cafeteria'),
('Gym', 'Main university sports center'),
('Main Hall', 'Front entrance of the university');

-- NOTE: Users should be seeded via the application to ensure password hashes are correct based on the Werkzeug configuration. 
-- However, we can create a dummy admin. Password is 'admin123' hashed with Werkzeug default.
INSERT IGNORE INTO users (name, email, password_hash, role) VALUES 
('Admin User', 'admin@findit.edu', 'scrypt:32768:8:1$C0YpY5q79v2ZJQfO$9f7e5b206c9a30b42f5c9071c8c62c2f1f0e42d76f8749a4f664a7872d8a59c3a38615b3e215d2a76f8e79c5a1a1f098c474d284f6c46a6f6c95c898c62b4742', 'admin');

-- Seed Lost Item
INSERT IGNORE INTO lost_items (user_id, category_id, location_id, item_name, brand, color, description, identifying_features, date_lost, time_lost, status) VALUES 
(1, 1, 1, 'MacBook Pro Charger', 'Apple', 'White', 'A white Apple MacBook Pro charger with a slight bend on the plug.', 'Small scratch on the side', '2026-09-20', '14:30:00', 'active');

-- Seed Found Item
INSERT IGNORE INTO found_items (user_id, category_id, location_id, item_name, brand, color, description, identifying_features, date_found, time_found, status) VALUES 
(1, 1, 1, 'White Laptop Charger', 'Apple', 'White', 'Found a white charger plugged into a wall outlet near the quiet study area.', '', '2026-09-20', '18:00:00', 'active');

-- Seed Match
INSERT IGNORE INTO matches (lost_id, found_id, match_score, status) VALUES 
(1, 1, 85.00, 'potential');
