<div align="center">
    <img src="https://frappecloud.com/files/pos-restaurant.webp" height="128">
    <h2>POS Restaurant</h2>
    <p><strong>Restaurant Management System for ERPNext</strong></p>
    <p>Version 1.8.6</p>
</div>

---

## ✨ What's New in v1.8.6

- **Frappe Helper Integrated** - No longer requires separate installation
- **Table Reservations** - Reserve and lock tables for specific customers
- **Menu Management** - Create menus; POS items are pulled from your configured menu
- **Branch Delivery** - Assign delivery orders to specific branches
- **Veg/Non-Veg Filter** - Quick dietary filtering for items
- **Recipe (BOM) Support** - Define ingredients per dish for inventory control and costing
- **Mobile Tabs View** - Tab navigation (Options, Orders, Items, Cart) for table management

---

## 🍳 Production Center System

The core of POS Restaurant is the **Production Center** (Kitchen Display System). Each production center reads orders in real-time based on order status.

### Flexible Restrictions

Administrators can configure each Production Center with three restriction levels:

| Restriction | Example |
|-------------|---------|
| **By Parent Room** | Kitchen PC in Room 1 only sees orders from Room 1 |
| **By Room List** | Bar PC sees orders from Terrace + Lounge rooms |
| **By Table List** | VIP Kitchen sees only orders from tables 1, 2, 3 |

### Product Group Filtering

Production Centers can also filter by item groups:

- **Bar PC** → Only cold drinks
- **Coffee Station** → Only hot beverages  
- **Main Kitchen** → Only food items

This allows multiple production centers to read from the same rooms but handle different product types.

---

## 🚀 Key Features

- **Room & Table Management** - Dynamic restaurant areas with drag-and-drop
- **Real-time Updates** - Instant sync across all stations
- **Role-based Permissions** - Custom access per POS profile and room
- **Order Process Tracking** - Status-based workflow (Pending → Preparing → Ready)
- **Dark Theme Compatible**

---

## 📋 Requirements

- [ERPNext](https://github.com/frappe/erpnext) V13, V14, or V15

---

## 🔧 Installation

```bash
bench get-app https://github.com/biztechnologyet/Biz-Restaurant.git
bench --site your-site.local install-app restaurant_management
bench migrate
```

---

## 📄 License

GNU General Public License (v3) - see [license.txt](license.txt)

---