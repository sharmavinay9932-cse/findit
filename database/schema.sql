CREATE DATABASE IF NOT EXISTS findit_db;
USE findit_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS lost_items (
    lost_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    location_id INT NOT NULL,
    item_name VARCHAR(150) NOT NULL,
    brand VARCHAR(100),
    color VARCHAR(50),
    description TEXT,
    identifying_features TEXT,
    date_lost DATE NOT NULL,
    time_lost TIME,
    status ENUM('active', 'matched', 'claimed', 'returned', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS found_items (
    found_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    location_id INT NOT NULL,
    item_name VARCHAR(150) NOT NULL,
    brand VARCHAR(100),
    color VARCHAR(50),
    description TEXT,
    identifying_features TEXT,
    date_found DATE NOT NULL,
    time_found TIME,
    status ENUM('active', 'matched', 'claimed', 'returned', 'closed') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS item_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    lost_id INT,
    found_id INT,
    image_path VARCHAR(500) NOT NULL,
    original_filename VARCHAR(255),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (lost_id IS NOT NULL AND found_id IS NULL)
        OR
        (lost_id IS NULL AND found_id IS NOT NULL)
    ),
    FOREIGN KEY (lost_id) REFERENCES lost_items(lost_id) ON DELETE CASCADE,
    FOREIGN KEY (found_id) REFERENCES found_items(found_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    lost_id INT NOT NULL,
    found_id INT NOT NULL,
    match_score DECIMAL(5,2) NOT NULL,
    status ENUM('potential', 'accepted', 'rejected') DEFAULT 'potential',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (lost_id, found_id),
    FOREIGN KEY (lost_id) REFERENCES lost_items(lost_id) ON DELETE CASCADE,
    FOREIGN KEY (found_id) REFERENCES found_items(found_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    claimant_id INT NOT NULL,
    verification_answer TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP NULL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (claimant_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS returns (
    return_id INT AUTO_INCREMENT PRIMARY KEY,
    claim_id INT NOT NULL UNIQUE,
    returned_by INT NOT NULL,
    received_by INT NOT NULL,
    return_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    confirmation TEXT,
    FOREIGN KEY (claim_id) REFERENCES claims(claim_id),
    FOREIGN KEY (returned_by) REFERENCES users(user_id),
    FOREIGN KEY (received_by) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create Indexes
CREATE INDEX idx_lost_category ON lost_items(category_id);
CREATE INDEX idx_found_category ON found_items(category_id);
CREATE INDEX idx_lost_location ON lost_items(location_id);
CREATE INDEX idx_found_location ON found_items(location_id);
CREATE INDEX idx_lost_status ON lost_items(status);
CREATE INDEX idx_found_status ON found_items(status);
CREATE INDEX idx_matches_score ON matches(match_score);
