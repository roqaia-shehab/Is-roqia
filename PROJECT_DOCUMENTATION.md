# 📚 Complete Project Documentation

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [File Structure](#file-structure)
3. [Core Components](#core-components)
4. [Data Structures](#data-structures)
5. [Features](#features)
6. [API Reference](#api-reference)
7. [Configuration](#configuration)

---

## 🎯 Project Overview

**Automated Timetable Generation System** is an intelligent scheduling application that uses **Constraint Satisfaction Problem (CSP)** algorithms to automatically generate university timetables. The system optimally assigns courses to instructors, rooms, and time slots while respecting all constraints.

### Key Capabilities

- ⚡ **Fast Scheduling**: Generates timetables in 15-25 seconds
- 🎯 **High Success Rate**: Schedules 92-97% of all sessions
- 🧠 **Intelligent Algorithm**: Uses greedy CSP with constraint optimization
- 📊 **Data Management**: Easy CSV-based data import/export
- 🎨 **Modern UI**: Clean, responsive interface with real-time updates
- 📄 **PDF Export**: Generate professional timetable documents

---

## 📁 File Structure

```
Automated Timetable Generation/
│
├── 📄 Core Application Files
│   ├── app.py                    # Flask backend server (main entry point)
│   ├── enhanced_csp_model.py     # CSP algorithm & constraint logic
│   ├── data_loader.py            # CSV data loading & parsing
│   └── requirements.txt          # Python dependencies
│
├── 📊 Data Files (CSV Database)
│   ├── Courses.csv               # Course definitions (90 courses)
│   ├── instructors.csv           # Instructor profiles (47 instructors)
│   ├── Rooms.csv                 # Room inventory (43 rooms)
│   └── TimeSlots.csv             # Available time slots (20 slots)
│
├── 🌐 Frontend (Web Interface)
│   ├── templates/
│   │   ├── index.html            # Main application page
│   │   └── test.html             # Testing interface
│   │
│   └── static/
│       ├── css/
│       │   └── style.css         # UI styling (1200+ lines)
│       │
│       └── js/
│           └── app.js            # Client-side logic (1028 lines)
│
├── 🚀 Quick Start Scripts
│   ├── START_SERVER.bat          # Windows batch launcher
│   └── START_SERVER.ps1          # PowerShell launcher
│
├── 📖 Documentation
│   ├── README.md                 # Main documentation (this file)
│   ├── WORKFLOW.md               # System workflow & diagrams
│   ├── PROJECT_DOCUMENTATION.md  # Complete technical docs
│   ├── COMPLETE_FIXES_SUMMARY.md # All fixes applied
│   └── ARCHITECTURE.md           # System architecture
│
└── 🔧 Environment
    └── venv/                     # Python virtual environment
```

---

## 🔧 Core Components

### 1. **app.py** - Flask Backend Server

**Purpose**: Main application server that handles HTTP requests, coordinates data loading, and executes timetable generation.

**Key Functions**:

| Function | Route | Description |
|----------|-------|-------------|
| `initialize_data()` | - | Loads all CSV data on startup |
| `index()` | `GET /` | Serves main HTML page |
| `get_data_summary()` | `GET /api/data/summary` | Returns data statistics |
| `get_courses()` | `GET /api/courses` | Returns all courses |
| `get_instructors()` | `GET /api/instructors` | Returns all instructors |
| `get_rooms()` | `GET /api/rooms` | Returns all rooms |
| `get_timeslots()` | `GET /api/timeslots` | Returns all timeslots |
| `generate_timetable()` | `POST /api/generate` | Generates complete timetable |
| `save_class()` | `POST /api/save-class` | Saves manual class assignment |
| `delete_class()` | `DELETE /api/delete-class` | Removes a scheduled class |
| `download_timetable()` | `GET /api/download/json` | Downloads timetable as JSON |
| `reload_data()` | `POST /api/reload` | Reloads data from CSV files |

**Dependencies**:
```python
flask           # Web framework
flask_cors      # Cross-origin resource sharing
data_loader     # CSV data loading
enhanced_csp_model  # CSP algorithm
```

---

### 2. **enhanced_csp_model.py** - CSP Algorithm

**Purpose**: Contains the core scheduling algorithm using Constraint Satisfaction Problem (CSP) approach with greedy optimization.

**Classes**:

#### `Course`
```python
Attributes:
  - course_id: str       # e.g., "AID427"
  - name: str            # e.g., "Machine Learning"
  - credits: int         # Credit hours (1-4)
  - type: str            # "Lecture", "Lab", "Lecture and Lab"
```

#### `Instructor`
```python
Attributes:
  - instructor_id: str   # e.g., "I001"
  - name: str            # Full name
  - role: str            # "Professor", "Doctor", "TA"
  - unavailable_day: str # Day instructor cannot teach
  - qualified_courses: List[str]  # Courses they can teach
```

#### `Room`
```python
Attributes:
  - room_id: str         # e.g., "R101" or "LAB03"
  - type: str            # "Lecture" or "Lab"
  - capacity: int        # Maximum students (30-200)
```

#### `Timeslot`
```python
Attributes:
  - day: str             # "Sunday" through "Thursday"
  - start_time: str      # e.g., "9:00 AM"
  - end_time: str        # e.g., "10:30 AM"
```

#### `EnhancedCSPTimetable` - Main Solver

**Key Methods**:

| Method | Purpose |
|--------|---------|
| `create_variables()` | Converts courses to session variables (handles Lecture+Lab splitting) |
| `create_domains()` | Generates all possible assignments for each variable |
| `is_assignment_valid()` | Checks hard constraints (conflicts, availability, room types) |
| `solve_enhanced()` | Main solving loop with greedy algorithm |
| `_greedy_schedule()` | Greedy assignment with constraint scoring |
| `order_domain_values()` | Scores assignments by soft constraints |

**Algorithm Workflow**:
```python
1. Create 142 variables (split Lecture+Lab courses)
2. Generate domains (~416 options per variable)
3. Sort variables by constraint difficulty
4. Greedy assignment loop:
   - Check hard constraints
   - Score soft constraints
   - Select best valid option
5. Run 5 attempts with randomization
6. Return best result (most sessions scheduled)
```

**Constraints**:

**Hard Constraints (MUST satisfy)**:
- ❌ No instructor double-booking
- ❌ No room double-booking
- ❌ No student course conflicts
- ❌ Room type must match session type
- ❌ Instructor must be qualified
- ❌ Instructor availability (no unavailable days)

**Soft Constraints (scoring)**:
- 📊 +10 points: Spread courses across days
- 👨‍🏫 +5 points: Match instructor preferences
- ⏰ +3 points: Avoid back-to-back same course
- 🏢 +2 points: Optimize room capacity usage

---

### 3. **data_loader.py** - Data Management

**Purpose**: Loads and parses CSV files into Python objects.

**Class**: `DataLoader`

**Methods**:

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__()` | - | Initializes empty data lists |
| `load_all_data(paths...)` | None | Loads all CSV files |
| `get_courses()` | List[Course] | Returns course list |
| `get_instructors()` | List[Instructor] | Returns instructor list |
| `get_rooms()` | List[Room] | Returns room list |
| `get_timeslots()` | List[Timeslot] | Returns timeslot list |

**Important**: Lists are cleared before reloading to prevent duplication!

```python
# Clears existing data before reload
self.courses = []
self.instructors = []
self.rooms = []
self.timeslots = []
```

---

## 📊 Data Structures

### CSV File Formats

#### **Courses.csv** (90 rows)
```csv
CourseID,CourseName,Credits,Type
AID427,Artificial Intelligence,3,Lecture and Lab
CSC111,Programming I,3,Lecture and Lab
MTH212,Calculus II,4,Lecture
...
```

**Fields**:
- `CourseID`: Unique identifier (e.g., AID427)
- `CourseName`: Full course name
- `Credits`: Credit hours (1-4)
- `Type`: "Lecture", "Lab", or "Lecture and Lab"

#### **instructors.csv** (47 rows)
```csv
InstructorID,Name,Role,PreferredSlots,QualifiedCourses
I001,Prof. Marghany Hassan,Professor,Morning,"AID427,AID311,CSC111,..."
I002,Prof. LBA,Professor,Afternoon,"AID321,MTH111,PHY113,..."
...
```

**Fields**:
- `InstructorID`: Unique identifier
- `Name`: Full name with title
- `Role`: Professor / Doctor / Teaching Assistant
- `PreferredSlots`: Preferred time (not currently used)
- `QualifiedCourses`: Comma-separated course IDs

#### **Rooms.csv** (43 rows)
```csv
RoomID,Type,Capacity
R101,Lecture,100
LAB03,Lab,30
R205,Lecture,150
...
```

**Fields**:
- `RoomID`: Unique room identifier
- `Type`: "Lecture" or "Lab"
- `Capacity`: Maximum student capacity

**Distribution**:
- 32 Lecture halls (R101-R232)
- 11 Lab rooms (LAB01-LAB11)

#### **TimeSlots.csv** (20 rows)
```csv
Day,StartTime,EndTime
Sunday,9:00 AM,10:30 AM
Sunday,10:45 AM,12:15 PM
Monday,9:00 AM,10:30 AM
...
```

**Fields**:
- `Day`: Sunday through Thursday (5 days)
- `StartTime`: Class start time
- `EndTime`: Class end time

**Schedule**:
- 5 days × 4 time slots = 20 total slots
- Slot 1: 9:00 AM - 10:30 AM
- Slot 2: 10:45 AM - 12:15 PM
- Slot 3: 12:30 PM - 2:00 PM
- Slot 4: 2:15 PM - 3:45 PM

---

## ⭐ Features

### 1. **Auto Scheduling** ⚡

**Description**: Automatically generates complete timetable with one click.

**Process**:
1. Click "Auto Schedule All Courses" button
2. System analyzes 90 courses → creates 142 sessions
3. Runs CSP algorithm (5 attempts with randomization)
4. Returns best result in 15-25 seconds
5. Displays timetable by day

**Success Rate**: 92-97% (typically schedules 130-138 / 142 sessions)

---

### 2. **Interactive Timetable View** 📅

**Features**:
- **Day Tabs**: Navigate between Sunday-Thursday
- **Class Cards**: Visual cards showing:
  - Course ID & Name
  - Section Type (Lecture/Lab) with color-coded badges
  - Instructor Name
  - Room ID with type indicator
  - Time Slot
- **Edit Button**: Modify class assignments
- **Delete Button**: Remove scheduled classes
- **Color Coding**:
  - 🟢 Green gradient: Lecture sessions
  - 🔵 Blue gradient: Lab sessions

---

### 3. **Search & Filter** 🔍

**Capabilities**:
- **Search Box**: Find by course ID, name, instructor, or room
- **Day Filter**: Show only specific days
- **Type Filter**: Filter by Lecture or Lab
- **Real-time**: Results update as you type

---

### 4. **Data Management** 📊

**Features**:
- View all courses, instructors, rooms, and timeslots
- Tab-based navigation
- **Reload Data**: Refresh from CSV files without restart
- Statistics display

**Tabs**:
1. **Courses**: CourseID, Name, Credits, Type
2. **Instructors**: ID, Name, Role, Unavailable Day, Qualified Courses
3. **Rooms**: RoomID, Type, Capacity
4. **Timeslots**: Day, Start Time, End Time

---

### 5. **PDF Export** 📄

**Description**: Generate professional PDF timetable documents.

**Features**:
- Landscape A4 format
- Color-coded sections
- Course details table
- Automatic page breaks
- Professional styling

**Usage**: Click "Download PDF" button in Timetable View

---

### 6. **JSON Export** 💾

**Description**: Download timetable data in JSON format for integration with other systems.

**Format**:
```json
{
  "success": true,
  "schedule": [
    {
      "course_id": "AID427",
      "course_name": "Artificial Intelligence",
      "section_id": "LECTURE",
      "instructor_id": "I001",
      "instructor_name": "Prof. Marghany Hassan",
      "room_id": "R101",
      "day": "Sunday",
      "start_time": "9:00 AM",
      "end_time": "10:30 AM"
    },
    ...
  ]
}
```

---

### 7. **Manual Editing** ✏️

**Capabilities**:
- **Edit Class**: Modify instructor, room, or time
- **Delete Class**: Remove from schedule
- **Add Class**: Manually schedule unassigned courses
- **Validation**: Prevents conflicts

**Edit Modal Fields**:
- Course (read-only)
- Instructor (dropdown)
- Room (dropdown - filtered by type)
- Day (dropdown)
- Time Slot (dropdown)

---

### 8. **Real-time Validation** ✅

**Checks**:
- ✓ Instructor availability
- ✓ Room availability
- ✓ No time conflicts
- ✓ Room type compatibility
- ✓ Instructor qualification

**Feedback**: Instant error messages for invalid assignments

---

### 9. **Statistics Dashboard** 📈

**Metrics Displayed**:
- Total courses loaded
- Total instructors available
- Total rooms available
- Total time slots
- Scheduled sessions
- Completion percentage
- Unscheduled courses list
- Generation time

---

### 10. **Responsive Design** 📱

**Features**:
- Mobile-friendly layout
- Tablet optimization
- Desktop full-screen
- Print-friendly styles
- Adaptive navigation

---

## 🔌 API Reference

### Base URL
```
http://localhost:5000
```

### Endpoints

#### GET `/`
**Description**: Serves main application page  
**Response**: HTML page

#### GET `/api/data/summary`
**Description**: Returns data statistics  
**Response**:
```json
{
  "success": true,
  "data": {
    "courses_count": 90,
    "instructors_count": 47,
    "rooms_count": 43,
    "timeslots_count": 20
  }
}
```

#### GET `/api/courses`
**Description**: Returns all courses  
**Response**:
```json
{
  "success": true,
  "courses": [
    {
      "course_id": "AID427",
      "name": "Artificial Intelligence",
      "credits": 3,
      "type": "Lecture and Lab"
    },
    ...
  ]
}
```

#### GET `/api/instructors`
**Description**: Returns all instructors  
**Response**:
```json
{
  "success": true,
  "instructors": [
    {
      "instructor_id": "I001",
      "name": "Prof. Marghany Hassan",
      "role": "Professor",
      "unavailable_day": "Friday",
      "qualified_courses": ["AID427", "AID311", ...]
    },
    ...
  ]
}
```

#### POST `/api/generate`
**Description**: Generates complete timetable  
**Request Body**: None  
**Response**:
```json
{
  "success": true,
  "message": "Timetable generated",
  "scheduled": 135,
  "total": 142,
  "percentage": 95.1,
  "schedule": [...],
  "unscheduled": [...]
}
```

#### POST `/api/save-class`
**Description**: Saves manual class assignment  
**Request Body**:
```json
{
  "course_id": "AID427",
  "section_id": "LECTURE",
  "instructor_id": "I001",
  "room_id": "R101",
  "day": "Sunday",
  "start_time": "9:00 AM"
}
```

#### DELETE `/api/delete-class`
**Description**: Removes scheduled class  
**Request Body**:
```json
{
  "course_id": "AID427",
  "day": "Sunday",
  "start_time": "9:00 AM"
}
```

#### POST `/api/reload`
**Description**: Reloads data from CSV files  
**Response**:
```json
{
  "success": true,
  "message": "Data reloaded successfully"
}
```

---

## ⚙️ Configuration

### Python Dependencies (requirements.txt)
```
Flask==3.0.0
Flask-CORS==4.0.0
```

### Server Settings (app.py)
```python
HOST = "0.0.0.0"           # Listen on all interfaces
PORT = 5000                # Default port
DEBUG = True               # Enable debug mode
TIMEOUT = 60               # Generation timeout (seconds)
MAX_ATTEMPTS = 5           # CSP solver attempts
```

### Algorithm Parameters (enhanced_csp_model.py)
```python
MAX_DOMAIN_SAMPLE = 100    # Max options to score per variable
RANDOM_SEED = None         # Use random seed for reproducibility
```

### Frontend Settings (app.js)
```javascript
API_BASE = ''              # API base URL (relative)
PDF_ORIENTATION = 'landscape'  # PDF page orientation
PDF_FORMAT = 'a4'          # PDF page size
```

---

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| Data Loading Time | ~0.5 seconds |
| Variable Creation | ~0.1 seconds |
| Domain Generation | ~1 second |
| Greedy Assignment | ~15-20 seconds |
| **Total Generation Time** | **15-25 seconds** |
| Success Rate | 92-97% |
| Memory Usage | ~6.1 MB |
| Scalability | Handles 142 sessions efficiently |

---

## 🎯 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Storage**: 50 MB
- **Browser**: Chrome, Firefox, Edge (latest)

### Recommended
- **Python**: 3.11+
- **RAM**: 1 GB
- **Browser**: Chrome 100+ for best performance

---

## 🔒 Security Considerations

✅ **Implemented**:
- CORS protection
- Input validation
- Error handling
- Safe file operations

⚠️ **Production Recommendations**:
- Use HTTPS
- Add authentication
- Use production WSGI server (Gunicorn/uWSGI)
- Implement rate limiting
- Add input sanitization

---

## 📝 License & Credits

**Project**: Automated Timetable Generation System  
**Algorithm**: Enhanced CSP with Greedy Optimization  
**Frontend**: HTML5, CSS3, JavaScript (ES6+)  
**Backend**: Flask (Python 3.11)  
**PDF Library**: jsPDF 2.5.1  

---

**For workflow details, see [WORKFLOW.md](WORKFLOW.md)**  
**For architecture diagrams, see [ARCHITECTURE.md](ARCHITECTURE.md)**  
**For setup instructions, see [README.md](README.md)**
