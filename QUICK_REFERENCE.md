# 🚀 QUICK REFERENCE GUIDE

**One-page reference for the Automated Timetable Generation System**

---

## ⚡ Quick Start (30 Seconds)

```bash
# Windows Command Prompt
SETUP.bat

# Windows PowerShell
.\SETUP.ps1

# Opens: http://localhost:5000
```

---

## 📊 System at a Glance

| Metric | Value |
|--------|-------|
| **Generation Speed** | 15-25 seconds |
| **Success Rate** | 92-97% (130-138/142 sessions) |
| **Courses** | 90 courses → 142 sessions |
| **Instructors** | 47 instructors |
| **Rooms** | 43 rooms (32 halls + 11 labs) |
| **Timeslots** | 20 slots (5 days × 4 slots) |

---

## 📁 Essential Files

```
Core Application:
  └─ app.py                    # Main server
  └─ enhanced_csp_model.py     # Algorithm
  └─ data_loader.py            # Data loading

Data Files:
  └─ Courses.csv               # Course list
  └─ instructors.csv           # Instructor profiles
  └─ Rooms.csv                 # Room inventory
  └─ TimeSlots.csv             # Time slots

Setup:
  └─ SETUP.bat / SETUP.ps1     # First-time setup
  └─ START_SERVER.bat/.ps1     # Quick start

Documentation:
  └─ README.md                 # Main guide
  └─ WORKFLOW.md               # How it works
  └─ ARCHITECTURE.md           # System design
  └─ PROJECT_DOCUMENTATION.md  # Technical details
```

---

## 🎯 Common Tasks

### Generate Timetable
1. Click "Dashboard" tab
2. Click "Auto Schedule All Courses"
3. Wait 15-25 seconds
4. View in "Timetable View" tab

### Edit a Class
1. Click ✏️ icon on class card
2. Modify instructor/room/time
3. Click "Save Changes"

### Export Timetable
- **PDF**: Click "Download PDF"
- **JSON**: Click "Download JSON"

### Reload Data
1. Edit CSV files
2. Click "Data Management" tab
3. Click "Reload Data"

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Module not found"** | Run `pip install Flask Flask-CORS` |
| **"Port in use"** | Run `taskkill /F /IM python.exe` (Windows) |
| **"Class not found"** | Hard refresh: `Ctrl + Shift + R` |
| **Data doubled** | Click "Reload Data" button |
| **Generation hangs** | Hard refresh browser, restart server |

---

## 🔧 Configuration Quick Reference

### Change Port
Edit `app.py`, line ~377:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Change 5000 to 5001
```

### Adjust Generation Timeout
Edit `app.py`, line ~170:
```python
TIMEOUT = 60  # Change to desired seconds
```

### Modify Algorithm Attempts
Edit `enhanced_csp_model.py`, line ~460:
```python
max_attempts = 5  # Change number of attempts
```

---

## 📖 Documentation Quick Links

- **Getting Started** → `README.md`
- **How It Works** → `WORKFLOW.md`
- **Technical Details** → `PROJECT_DOCUMENTATION.md`
- **System Design** → `ARCHITECTURE.md`
- **All Fixes** → `COMPLETE_FIXES_SUMMARY.md`

---

## 🎨 CSV Data Format Reference

### Courses.csv
```csv
CourseID,CourseName,Credits,Type
AID427,Artificial Intelligence,3,Lecture and Lab
```

### instructors.csv
```csv
InstructorID,Name,Role,PreferredSlots,QualifiedCourses
I001,Prof. Smith,Professor,Morning,"AID427,CSC111"
```

### Rooms.csv
```csv
RoomID,Type,Capacity
R101,Lecture,100
LAB03,Lab,30
```

### TimeSlots.csv
```csv
Day,StartTime,EndTime
Sunday,9:00 AM,10:30 AM
```

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| **Hard Refresh** | `Ctrl + Shift + R` |
| **Open DevTools** | `F12` |
| **Find on Page** | `Ctrl + F` |

---

## 🔗 API Quick Reference

```javascript
GET  /                      → Main page
GET  /api/data/summary      → Statistics
GET  /api/courses           → All courses
GET  /api/instructors       → All instructors
GET  /api/rooms             → All rooms
GET  /api/timeslots         → All timeslots
POST /api/generate          → Generate timetable
POST /api/save-class        → Save class
DELETE /api/delete-class    → Delete class
POST /api/reload            → Reload data
```

---

## 📊 Performance Benchmarks

```
Data Loading:       ~0.5s
Variable Creation:  ~0.1s
Domain Generation:  ~1.0s
Greedy Assignment:  ~15-20s
─────────────────────────
Total Time:         15-25s
```

---

## 🎯 System Constraints

**Hard Constraints** (MUST satisfy):
- ✓ No instructor double-booking
- ✓ No room double-booking
- ✓ Room type matches session type
- ✓ Instructor is qualified
- ✓ Instructor is available

**Soft Constraints** (scoring):
- +10: Spread courses across days
- +5: Match instructor preferences
- +3: Avoid back-to-back sessions
- +2: Optimize room capacity

---

## 🚀 Deployment Checklist

### Development (Current)
- [x] Flask dev server
- [x] Debug mode ON
- [x] Port 5000
- [x] Local access only

### Production (Recommended)
- [ ] Use Gunicorn/uWSGI
- [ ] Debug mode OFF
- [ ] Use Nginx reverse proxy
- [ ] Enable HTTPS
- [ ] Set up authentication
- [ ] Configure firewall

---

## 📞 Quick Support

**Check documentation first:**
1. README.md → General guide
2. WORKFLOW.md → System workflow
3. Troubleshooting section

**Still stuck?**
- Check browser console (F12)
- Review server logs
- Verify CSV file format
- Try hard refresh (Ctrl+Shift+R)

---

## 🏆 Key Features at a Glance

✅ One-click timetable generation  
✅ 15-30x faster than backtracking  
✅ 92-97% scheduling success  
✅ Real-time validation  
✅ PDF & JSON export  
✅ Interactive editing  
✅ Search & filter  
✅ Data reload without restart  
✅ Modern responsive UI  
✅ Complete documentation  

---

**Print this page for quick reference! 📄**
