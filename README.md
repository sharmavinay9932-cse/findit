# 🔎 FindIt — Intelligent Campus Lost & Found System

> A smart web-based Lost & Found platform designed to help students and campus members report, search, and recover lost belongings efficiently.

🌐 **Live Demo:** https://findit-1-o2g7.onrender.com

---

## 📌 Overview

**FindIt** is an intelligent campus Lost & Found management system built to simplify the process of reporting and recovering lost items.

Instead of relying on WhatsApp groups, notice boards, or informal announcements, FindIt provides a centralized platform where users can:

- Report lost items
- Report found items
- Upload item photographs
- Search and browse reported items
- View item details
- Identify potential matches
- Submit claims
- Manage their account

The system uses **Flask for the backend** and **MySQL for persistent data storage**, with a responsive HTML/CSS/JavaScript frontend.

---

## ✨ Features

### 👤 User Management

- User registration
- User login
- Password hashing
- Session-based authentication
- User profile
- Role-based access

### 📦 Lost & Found Management

- Report a lost item
- Report a found item
- Item categories
- Location information
- Item descriptions
- Date information
- Brand/color details
- Item photographs

### 🔎 Search & Discovery

- Browse lost items
- Browse found items
- Search reported items
- Filter items by category
- Filter items by location
- View detailed item information

### 🤖 Intelligent Matching

FindIt is designed with an intelligent matching layer that can compare:

- Item category
- Description
- Brand
- Color
- Location
- Date
- Other item attributes

The current matching system uses a Python-based scoring approach and can be extended with NLP and computer vision models.

### 🛡️ Security

- Password hashing using Werkzeug
- Parameterized SQL queries
- Environment-based database credentials
- Password hashes are never returned to the frontend
- Input validation
- Session-based authentication

---

## 🏗️ System Architecture

```text
