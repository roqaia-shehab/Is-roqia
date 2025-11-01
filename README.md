# 🎓 CSP TimetableAI - Intelligent Scheduling System

<div align="center">

**An intelligent university timetable scheduling system powered by AI algorithms**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

**© 2025 Roqia. All Rights Reserved.**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Documentation](#-documentation)
- [Performance](#-performance)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Overview

**CSP TimetableAI** is a sophisticated web-based application that automatically generates conflict-free university timetables using **Constraint Satisfaction Problem (CSP)** algorithms. It intelligently assigns courses to instructors, rooms, and time slots while respecting all scheduling constraints.

### What Makes It Special?

✅ **Lightning Fast**: Generates complete timetables in **15-25 seconds** (15-30x faster than traditional backtracking)  
✅ **High Success Rate**: Schedules **92-97%** of all sessions automatically  
✅ **Smart Algorithm**: Uses greedy CSP with constraint optimization  
✅ **User-Friendly**: Modern, responsive web interface with real-time updates  
✅ **Flexible**: Easy data management through CSV files  
✅ **Professional**: Export timetables as PDF or JSON

---

## ⭐ Key Features

### 🤖 Intelligent Scheduling
- **Automated Timetable Generation**: One-click scheduling of all courses
- **Constraint Satisfaction**: Handles complex scheduling rules automatically
- **Conflict Resolution**: Prevents double-booking and scheduling conflicts
- **Room Type Matching**: Assigns lectures to lecture halls, labs to lab rooms
- **Instructor Qualification**: Ensures instructors teach only qualified courses

### 🎨 Modern User Interface
- **Clean Dashboard**: Intuitive tab-based navigation
- **Interactive Timetable**: View by day with color-coded sessions
- **Search & Filter**: Quick course, instructor, or room lookup
- **Real-time Updates**: Instant feedback on all actions
- **Responsive Design**: Works on desktop, tablet, and mobile

### 📊 Data Management
- **CSV-Based**: Easy data import/export
- **Live Reload**: Update data without restarting server
- **Data Validation**: Built-in integrity checks
- **Multiple Views**: Browse courses, instructors, rooms, timeslots

### ✏️ Manual Controls
- **Edit Classes**: Modify any scheduled class
- **Delete Classes**: Remove unwanted assignments
- **Add Classes**: Manually schedule unassigned courses
- **Validation**: Prevents invalid manual assignments

### 📄 Export Options
- **PDF Generation**: Professional timetable documents
- **JSON Export**: Integration with other systems
- **Print-Friendly**: Optimized printing layouts

---

## 🚀 Quick Start

### Option 1: One-Click Setup (Recommended)

**Windows Command Prompt:**
```batch
SETUP.bat
```

**Windows PowerShell:**
```powershell
.\SETUP.ps1
```

This will:
1. Check Python installation
2. Install all dependencies
3. Start the server automatically

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install Flask==3.0.0 Flask-CORS==4.0.0

# 2. Start the server
python app.py

# 3. Open browser
# Navigate to: http://localhost:5000
```

### Option 3: Start Server Only

If dependencies are already installed:

**Windows:**
```batch
START_SERVER.bat
```

**PowerShell:**
```powershell
.\START_SERVER.ps1
```

---

## 💻 System Requirements

### Minimum Requirements
| Component | Requirement |
|-----------|------------|
| **Operating System** | Windows 10/11, Linux, macOS |
| **Python** | 3.8 or higher |
| **RAM** | 512 MB |
| **Storage** | 50 MB |
| **Browser** | Chrome, Firefox, Edge (latest versions) |

### Recommended
| Component | Recommendation |
|-----------|---------------|
| **Python** | 3.11+ |
| **RAM** | 1 GB |
| **Browser** | Chrome 100+ for best performance |

---

## 📦 Installation

### Step 1: Download/Clone Project
```bash
# Clone repository (if using Git)
git clone https://github.com/yourusername/timetable-system.git
cd timetable-system

# Or extract ZIP file to a folder
```

### Step 2: Verify Python Installation
```bash
python --version
# Should show Python 3.8 or higher
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3 python3-pip`
- **macOS**: `brew install python3`

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install Flask==3.0.0 Flask-CORS==4.0.0
```

### Step 4: Verify Data Files
Ensure these CSV files exist:
- ✅ `Courses.csv`
- ✅ `instructors.csv`
- ✅ `Rooms.csv`
- ✅ `TimeSlots.csv`

### Step 5: Start the Server
```bash
python app.py
```

You should see:
```
✅ Data loaded successfully!
🎓 AUTOMATED TIMETABLE GENERATION SYSTEM
🚀 Starting Flask server...
📍 Server will be available at: http://localhost:5000
```

### Step 6: Open Browser
Navigate to: **http://localhost:5000**

---

## 📖 Usage Guide

### 1. Generate Timetable

1. Click the **"Dashboard"** tab
2. Click **"Auto Schedule All Courses"** button
3. Wait 15-25 seconds for generation
4. View results in **"Timetable View"** tab

### 2. View Timetable

1. Click **"Timetable View"** tab
2. Select day tab (Sunday-Thursday)
3. Browse scheduled classes
4. Each card shows:
   - Course ID & Name
   - Section Type (Lecture/Lab)
   - Instructor
   - Room
   - Time

### 3. Search & Filter

1. Use **Search Box** to find courses
2. Select **Day Filter** for specific days
3. Choose **Type Filter** (Lecture/Lab/All)
4. Results update instantly

### 4. Edit a Class

1. Click **✏️ Edit** icon on any class card
2. Modal opens with editable fields
3. Modify instructor, room, or time
4. Click **"Save Changes"**
5. System validates before saving

### 5. Delete a Class

1. Click **🗑️ Delete** icon on any class card
2. Confirm deletion
3. Class removed from timetable

### 6. Export Timetable

**PDF Export:**
1. Click **"Download PDF"** button
2. Professional PDF generates
3. Save to computer

**JSON Export:**
1. Click **"Download JSON"** button
2. JSON file downloads
3. Use for integration with other systems

### 7. Manage Data

1. Click **"Data Management"** tab
2. View courses, instructors, rooms, timeslots
3. Click **"Reload Data"** to refresh from CSV
4. Browse using tab navigation

### 8. View Statistics

1. Click **"Statistics"** tab
2. See:
   - Total scheduled sessions
   - Completion percentage
   - Unscheduled courses
   - Generation time

---

## 📁 Project Structure

```
Automated Timetable Generation/
│
├── 📄 Core Application
│   ├── app.py                    # Flask server (main entry point)
│   ├── enhanced_csp_model.py     # CSP scheduling algorithm
│   ├── data_loader.py            # CSV data loading
│   └── requirements.txt          # Python dependencies
│
├── 📊 Data Files
│   ├── Courses.csv               # 90 courses
│   ├── instructors.csv           # 47 instructors
│   ├── Rooms.csv                 # 43 rooms (32 halls + 11 labs)
│   └── TimeSlots.csv             # 20 timeslots (5 days × 4 slots)
│
├── 🌐 Frontend
│   ├── templates/
│   │   └── index.html            # Main UI
│   └── static/
│       ├── css/style.css         # Styling
│       └── js/app.js             # JavaScript logic
│
├── 🚀 Quick Start
│   ├── SETUP.bat                 # Windows setup script
│   ├── SETUP.ps1                 # PowerShell setup script
│   ├── START_SERVER.bat          # Windows server launcher
│   └── START_SERVER.ps1          # PowerShell server launcher
│
└── 📖 Documentation
    ├── README.md                 # This file
    ├── WORKFLOW.md               # System workflow & diagrams
    ├── PROJECT_DOCUMENTATION.md  # Complete technical documentation
    ├── ARCHITECTURE.md           # System architecture diagrams
    └── COMPLETE_FIXES_SUMMARY.md # All improvements & fixes
```

---

## 📚 Documentation

### 📖 Available Documentation

| Document | Description |
|----------|-------------|
| **README.md** | Main documentation (you are here) |
| **[WORKFLOW.md](WORKFLOW.md)** | Complete system workflow with diagrams |
| **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** | Technical documentation of all components |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System architecture and design |
| **[COMPLETE_FIXES_SUMMARY.md](COMPLETE_FIXES_SUMMARY.md)** | All fixes and improvements applied |

### 🔍 Quick Links

- **How It Works**: See [WORKFLOW.md](WORKFLOW.md)
- **API Reference**: See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md#api-reference)
- **Algorithm Details**: See [WORKFLOW.md](WORKFLOW.md#csp-algorithm-workflow)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)

---

## ⚡ Performance

### Speed Benchmarks

| Metric | Value |
|--------|-------|
| **Data Loading** | ~0.5 seconds |
| **Variable Creation** | ~0.1 seconds |
| **Domain Generation** | ~1 second |
| **Greedy Assignment** | ~15-20 seconds |
| **Total Generation Time** | **15-25 seconds** |

### Success Metrics

| Metric | Value |
|--------|-------|
| **Scheduling Success Rate** | 92-97% |
| **Typical Sessions Scheduled** | 130-138 / 142 sessions |
| **Algorithm Efficiency** | 15-30x faster than backtracking |
| **Memory Usage** | ~6.1 MB |

### Scalability

- ✅ Handles **142 sessions** efficiently
- ✅ Supports **47 instructors** 
- ✅ Manages **43 rooms**
- ✅ Covers **20 timeslots**
- ✅ Can scale to **200+ courses** with optimization

---

## 🐛 Troubleshooting

### Problem: Server won't start

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install Flask==3.0.0 Flask-CORS==4.0.0
```

---

### Problem: Port 5000 already in use

**Error**: `OSError: [Errno 48] Address already in use`

**Solution 1** - Kill existing Python process:
```bash
# Windows
taskkill /F /IM python.exe

# Linux/Mac
pkill python
```

**Solution 2** - Change port in `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

---

### Problem: CSV files not found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'Courses.csv'`

**Solution**:
1. Ensure you're in the correct directory
2. Check that all CSV files exist:
   - `Courses.csv`
   - `instructors.csv`
   - `Rooms.csv`
   - `TimeSlots.csv`

---

### Problem: Timetable generation hangs

**Symptom**: "Generating..." message doesn't finish

**Solution**:
1. Hard refresh browser: `Ctrl + Shift + R`
2. Check browser console for errors (F12)
3. Restart server
4. Clear browser cache

---

### Problem: Edit button shows "Class not found"

**Solution**:
1. Hard refresh browser: `Ctrl + Shift + R`
2. This ensures latest JavaScript is loaded

---

### Problem: Data shows doubled (180 courses instead of 90)

**Solution**:
1. This is fixed in the latest version
2. Click **"Reload Data"** button
3. Counts should remain consistent

---

<div align="center">

### ⭐ If you find this project useful, please star it!

**Made with ❤️ for efficient university scheduling**

---

**Quick Links**: [Documentation](#-documentation) | [Quick Start](#-quick-start) | [Features](#-key-features) | [Troubleshooting](#-troubleshooting)

---

## 📜 Copyright & License

**CSP TimetableAI** - Intelligent Scheduling System  
**© 2025 Roqia. All Rights Reserved.**

This software is protected by copyright law. Unauthorized copying, distribution, or modification of this software, via any medium, is strictly prohibited without prior written permission from the copyright holder.

**Developed by**: Roqia  
**Project**: CSP TimetableAI  
**Year**: 2025  
**License**: Proprietary - All Rights Reserved

---

</div>
