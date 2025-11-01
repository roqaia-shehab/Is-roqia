// app.js - Frontend JavaScript for CSP TimetableAI
// © 2025 Roqia. All Rights Reserved.

// Global state
let currentTimetable = null;
let allData = {
    courses: [],
    instructors: [],
    rooms: [],
    timeslots: []
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeForms();
    loadDataSummary();
    loadAllData();
});

// ============================================================================
// TAB NAVIGATION
// ============================================================================

function initializeTabs() {
    const navBtns = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            
            // Update active states
            navBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === tabName) {
                    content.classList.add('active');
                }
            });
        });
    });
}

// ============================================================================
// FORM HANDLING
// ============================================================================

function initializeForms() {
    const generationForm = document.getElementById('generation-form');
    generationForm.addEventListener('submit', handleGenerate);
    
    // Add search and filter listeners
    const searchInput = document.getElementById('search-timetable');
    const filterDay = document.getElementById('filter-day');
    const filterType = document.getElementById('filter-type');
    
    if (searchInput) {
        searchInput.addEventListener('input', applyFilters);
    }
    if (filterDay) {
        filterDay.addEventListener('change', applyFilters);
    }
    if (filterType) {
        filterType.addEventListener('change', applyFilters);
    }
}

async function handleGenerate(e) {
    e.preventDefault();
    
    // Show progress
    document.getElementById('generation-progress').classList.remove('hidden');
    document.getElementById('generation-results').classList.add('hidden');
    document.getElementById('progress-message').textContent = 'Scheduling ALL courses across all time slots... This may take a few minutes.';
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                timeout: 300
            })
        });
        
        const data = await response.json();
        
        // Hide progress
        document.getElementById('generation-progress').classList.add('hidden');
        
        if (data.success || data.scheduled_courses > 0) {
            currentTimetable = data;
            displayResults(data);
            showToast(data.message || 'Timetable generated successfully!', 'success');
        } else {
            showToast('Failed to generate timetable: ' + (data.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        document.getElementById('generation-progress').classList.add('hidden');
        showToast('Error: ' + error.message, 'error');
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('generation-results');
    resultsSection.classList.remove('hidden');
    
    document.getElementById('result-scheduled').textContent = data.scheduled_courses;
    document.getElementById('result-total').textContent = data.total_courses;
    
    const successRate = ((data.scheduled_courses / data.total_courses) * 100).toFixed(1);
    document.getElementById('result-success').textContent = successRate + '%';
}

// ============================================================================
// DATA LOADING
// ============================================================================

async function loadDataSummary() {
    try {
        const response = await fetch('/api/data/summary');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('courses-count').textContent = data.data.courses_count;
            document.getElementById('instructors-count').textContent = data.data.instructors_count;
            document.getElementById('rooms-count').textContent = data.data.rooms_count;
            document.getElementById('timeslots-count').textContent = data.data.timeslots_count;
        }
    } catch (error) {
        console.error('Error loading data summary:', error);
    }
}

async function loadAllData() {
    await Promise.all([
        loadCourses(),
        loadInstructors(),
        loadRooms(),
        loadTimeslots()
    ]);
}

async function loadCourses() {
    try {
        console.log('Loading courses...');
        const response = await fetch('/api/courses');
        const data = await response.json();
        
        console.log('Courses response:', data);
        
        if (data.success) {
            allData.courses = data.courses;
            displayCoursesTable(data.courses);
            console.log(`✅ Loaded ${data.courses.length} courses`);
        } else {
            console.error('Failed to load courses:', data.error);
            const tbody = document.getElementById('courses-table-body');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center error">Error loading courses</td></tr>';
            }
        }
    } catch (error) {
        console.error('Error loading courses:', error);
        const tbody = document.getElementById('courses-table-body');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center error">Failed to load courses</td></tr>';
        }
    }
}

async function loadInstructors() {
    try {
        console.log('Loading instructors...');
        const response = await fetch('/api/instructors');
        const data = await response.json();
        
        console.log('Instructors response:', data);
        
        if (data.success) {
            allData.instructors = data.instructors;
            displayInstructorsTable(data.instructors);
            console.log(`✅ Loaded ${data.instructors.length} instructors`);
        } else {
            console.error('Failed to load instructors:', data.error);
            const tbody = document.getElementById('instructors-table-body');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center error">Error loading instructors</td></tr>';
            }
        }
    } catch (error) {
        console.error('Error loading instructors:', error);
        const tbody = document.getElementById('instructors-table-body');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center error">Failed to load instructors</td></tr>';
        }
    }
}

async function loadRooms() {
    try {
        console.log('Loading rooms...');
        const response = await fetch('/api/rooms');
        const data = await response.json();
        
        console.log('Rooms response:', data);
        
        if (data.success) {
            allData.rooms = data.rooms;
            displayRoomsTable(data.rooms);
            console.log(`✅ Loaded ${data.rooms.length} rooms`);
        } else {
            console.error('Failed to load rooms:', data.error);
            const tbody = document.getElementById('rooms-table-body');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center error">Error loading rooms</td></tr>';
            }
        }
    } catch (error) {
        console.error('Error loading rooms:', error);
        const tbody = document.getElementById('rooms-table-body');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center error">Failed to load rooms</td></tr>';
        }
    }
}

async function loadTimeslots() {
    try {
        console.log('Loading timeslots...');
        const response = await fetch('/api/timeslots');
        const data = await response.json();
        
        console.log('Timeslots response:', data);
        
        if (data.success) {
            allData.timeslots = data.timeslots;
            displayTimeslotsTable(data.timeslots);
            console.log(`✅ Loaded ${data.timeslots.length} timeslots`);
        } else {
            console.error('Failed to load timeslots:', data.error);
            const tbody = document.getElementById('timeslots-table-body');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center error">Error loading timeslots</td></tr>';
            }
        }
    } catch (error) {
        console.error('Error loading timeslots:', error);
        const tbody = document.getElementById('timeslots-table-body');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center error">Failed to load timeslots</td></tr>';
        }
    }
}

// ============================================================================
// TABLE DISPLAY
// ============================================================================

function displayCoursesTable(courses) {
    const tbody = document.getElementById('courses-table-body');
    if (!tbody) {
        return;
    }
    
    if (courses.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">No courses found</td></tr>';
        return;
    }
    
    tbody.innerHTML = courses.map(course => `
        <tr>
            <td>${course.course_id}</td>
            <td>${course.name}</td>
            <td>${course.credits}</td>
        </tr>
    `).join('');
}

function displayInstructorsTable(instructors) {
    const tbody = document.getElementById('instructors-table-body');
    if (!tbody) {
        return;
    }
    
    if (instructors.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No instructors found</td></tr>';
        return;
    }
    
    tbody.innerHTML = instructors.map(instructor => `
        <tr>
            <td>${instructor.instructor_id}</td>
            <td>${instructor.name}</td>
            <td>${instructor.role}</td>
            <td>${instructor.unavailable_day}</td>
            <td>${instructor.qualified_courses.slice(0, 5).join(', ')}${instructor.qualified_courses.length > 5 ? '...' : ''}</td>
        </tr>
    `).join('');
}

function displayRoomsTable(rooms) {
    const tbody = document.getElementById('rooms-table-body');
    if (!tbody) {
        return;
    }
    
    if (rooms.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">No rooms found</td></tr>';
        return;
    }
    
    tbody.innerHTML = rooms.map(room => `
        <tr>
            <td>${room.room_id}</td>
            <td>${room.type}</td>
            <td>${room.capacity}</td>
        </tr>
    `).join('');
}

function displayTimeslotsTable(timeslots) {
    const tbody = document.getElementById('timeslots-table-body');
    if (!tbody) {
        return;
    }
    
    if (timeslots.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">No timeslots found</td></tr>';
        return;
    }
    
    tbody.innerHTML = timeslots.map(slot => `
        <tr>
            <td>${slot.day}</td>
            <td>${slot.start_time}</td>
            <td>${slot.end_time}</td>
        </tr>
    `).join('');
}

// ============================================================================
// TIMETABLE DISPLAY
// ============================================================================

function viewTimetable() {
    // Switch to timetable tab
    document.querySelector('[data-tab="timetable"]').click();
    
    if (!currentTimetable || !currentTimetable.schedule) {
        return;
    }
    
    displayTimetableByDay(currentTimetable.schedule);
}

function displayTimetableByDay(schedule) {
    const content = document.getElementById('timetable-content');
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'];
    
    // Define proper time order
    const timeOrder = {
        '9:00 AM': 1,
        '10:45 AM': 2,
        '12:30 PM': 3,
        '2:15 PM': 4
    };
    
    if (schedule.length === 0) {
        content.innerHTML = '<div class="empty-state"><i class="fas fa-calendar-times"></i><p>No classes scheduled</p></div>';
        return;
    }
    
    // Group by day and time
    const grouped = {};
    schedule.forEach(entry => {
        if (!grouped[entry.day]) {
            grouped[entry.day] = {};
        }
        const timeKey = `${entry.start_time} - ${entry.end_time}`;
        if (!grouped[entry.day][timeKey]) {
            grouped[entry.day][timeKey] = [];
        }
        grouped[entry.day][timeKey].push(entry);
    });
    
    // Generate HTML with improved layout
    let html = `
        <div class="timetable-actions">
            <button class="btn btn-primary" onclick="downloadPDF()">
                <i class="fas fa-file-pdf"></i> Download as PDF
            </button>
            <button class="btn btn-secondary" onclick="printTimetable()">
                <i class="fas fa-print"></i> Print
            </button>
        </div>
        <div class="timetable-grid-improved">
    `;
    
    days.forEach(day => {
        if (grouped[day]) {
            const dayClasses = Object.values(grouped[day]).flat();
            html += `
                <div class="day-section-improved">
                    <div class="day-header-improved">
                        <div class="day-title">
                            <i class="fas fa-calendar-day"></i>
                            <span>${day}</span>
                        </div>
                        <div class="day-stats">
                            <span class="badge">${dayClasses.length} Classes</span>
                        </div>
                    </div>
                    <div class="day-content">
            `;
            
            // Sort times using custom order (9:00 AM, 10:45 AM, 12:30 PM, 2:15 PM)
            const times = Object.keys(grouped[day]).sort((a, b) => {
                const startA = a.split(' - ')[0];
                const startB = b.split(' - ')[0];
                return (timeOrder[startA] || 999) - (timeOrder[startB] || 999);
            });
            
            times.forEach(time => {
                html += `
                    <div class="timeslot-section">
                        <div class="timeslot-header-improved">
                            <i class="fas fa-clock"></i>
                            <span class="time-text">${time}</span>
                            <span class="class-count">(${grouped[day][time].length})</span>
                        </div>
                        <div class="classes-grid">
                `;
                
                grouped[day][time].forEach((entry, index) => {
                    // Determine display type based on section_id (for split Lecture+Lab courses)
                    let displayType = entry.course_type;
                    let classType = 'lecture';
                    
                    if (entry.section_id === 'LAB') {
                        displayType = 'Lab Session';
                        classType = 'lab';
                    } else if (entry.section_id === 'LECTURE') {
                        displayType = 'Lecture Session';
                        classType = 'lecture';
                    } else if (entry.course_type.includes('Lab')) {
                        classType = 'lab';
                    }
                    
                    const entryId = `${entry.course_id}-${entry.section_id || 'S1'}-${entry.day}-${entry.start_time.replace(/[: ]/g, '')}`;
                    html += `
                        <div class="class-card ${classType}" data-entry-id="${entryId}">
                            <div class="class-card-header">
                                <div class="course-info">
                                    <span class="course-code-large">${entry.course_id}</span>
                                    <span class="course-type-badge ${classType}">${displayType}</span>
                                </div>
                                <button class="btn-edit-class-small" onclick="editClass('${entryId}')" title="Edit this class">
                                    <i class="fas fa-edit"></i>
                                </button>
                            </div>
                            <div class="course-name-improved">${entry.course_name}</div>
                            <div class="class-details-improved">
                                <div class="detail-row">
                                    <i class="fas fa-door-open"></i>
                                    <span class="detail-label">Room:</span>
                                    <span class="detail-value">${entry.room_id} (${entry.room_type})</span>
                                </div>
                                <div class="detail-row">
                                    <i class="fas fa-chalkboard-teacher"></i>
                                    <span class="detail-label">Instructor:</span>
                                    <span class="detail-value">${entry.instructor_name}</span>
                                </div>
                            </div>
                        </div>
                    `;
                });
                
                html += `
                        </div>
                    </div>
                `;
            });
            
            html += `
                    </div>
                </div>
            `;
        }
    });
    
    html += '</div>';
    content.innerHTML = html;
}

// ============================================================================
// EXPORT FUNCTIONS
// ============================================================================

function exportCSV() {
    window.location.href = '/api/timetable/export/csv';
    showToast('Downloading CSV...', 'success');
}

function exportJSON() {
    window.location.href = '/api/timetable/export/json';
    showToast('Downloading JSON...', 'success');
}

// ============================================================================
// DATA MANAGEMENT
// ============================================================================

async function reloadData() {
    try {
        const response = await fetch('/api/reload', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Data reloaded successfully!', 'success');
            await loadDataSummary();
            await loadAllData();
        } else {
            showToast('Failed to reload data', 'error');
        }
    } catch (error) {
        showToast('Error: ' + error.message, 'error');
    }
}

// ============================================================================
// NOTIFICATIONS
// ============================================================================

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function formatTime(timeStr) {
    // Format time string for better display
    return timeStr;
}

function getCourseColor(courseType) {
    if (courseType.includes('Lab')) {
        return '#60a5fa';
    }
    return '#4ade80';
}

// ============================================================================
// SEARCH AND FILTER FUNCTIONS
// ============================================================================

function applyFilters() {
    if (!currentTimetable || !currentTimetable.schedule) {
        return;
    }
    
    const searchTerm = document.getElementById('search-timetable').value.toLowerCase();
    const filterDay = document.getElementById('filter-day').value;
    const filterType = document.getElementById('filter-type').value;
    
    // Filter schedule based on criteria
    let filteredSchedule = currentTimetable.schedule.filter(entry => {
        // Day filter
        if (filterDay !== 'all' && entry.day !== filterDay) {
            return false;
        }
        
        // Type filter
        if (filterType !== 'all') {
            const isLab = entry.course_type.toLowerCase().includes('lab');
            if (filterType === 'lab' && !isLab) return false;
            if (filterType === 'lecture' && isLab) return false;
        }
        
        // Search filter
        if (searchTerm) {
            const searchable = (
                entry.course_id.toLowerCase() +
                entry.course_name.toLowerCase() +
                entry.instructor_name.toLowerCase() +
                entry.room_id.toLowerCase()
            );
            if (!searchable.includes(searchTerm)) {
                return false;
            }
        }
        
        return true;
    });
    
    // Display filtered results
    displayTimetableByDay(filteredSchedule);
    
    // Show filter summary
    const summary = `Showing ${filteredSchedule.length} of ${currentTimetable.schedule.length} classes`;
    showFilterSummary(summary);
}

function showFilterSummary(text) {
    // Add or update filter summary element
    let summary = document.querySelector('.filter-summary');
    if (!summary) {
        summary = document.createElement('div');
        summary.className = 'filter-summary';
        const content = document.getElementById('timetable-content');
        content.insertBefore(summary, content.firstChild);
    }
    summary.textContent = text;
    summary.style.padding = '1rem';
    summary.style.background = 'var(--bg-secondary)';
    summary.style.borderRadius = '0.5rem';
    summary.style.marginBottom = '1rem';
    summary.style.textAlign = 'center';
    summary.style.color = 'var(--text-secondary)';
}

// ============================================================================
// DYNAMIC EDITING FUNCTIONS
// ============================================================================

let currentEditingEntry = null;

function editClass(entryId) {
    if (!currentTimetable || !currentTimetable.schedule) {
        showToast('No timetable loaded', 'error');
        return;
    }
    
    // Find the entry - NEW FORMAT includes section_id
    const entry = currentTimetable.schedule.find(e => {
        const id = `${e.course_id}-${e.section_id || 'S1'}-${e.day}-${e.start_time.replace(/[: ]/g, '')}`;
        return id === entryId;
    });
    
    if (!entry) {
        showToast('Class not found', 'error');
        console.error('Could not find entry with ID:', entryId);
        console.log('Available entries:', currentTimetable.schedule.map(e => 
            `${e.course_id}-${e.section_id || 'S1'}-${e.day}-${e.start_time.replace(/[: ]/g, '')}`
        ));
        return;
    }
    
    currentEditingEntry = entry;
    currentEditingEntry.entryId = entryId;
    
    // Populate modal
    document.getElementById('edit-course').value = `${entry.course_id} - ${entry.course_name}`;
    document.getElementById('edit-day').value = entry.day;
    document.getElementById('edit-timeslot').value = `${entry.start_time} - ${entry.end_time}`;
    
    // Populate rooms dropdown
    const roomSelect = document.getElementById('edit-room');
    roomSelect.innerHTML = allData.rooms.map(room => 
        `<option value="${room.room_id}" ${room.room_id === entry.room_id ? 'selected' : ''}>
            ${room.room_id} (${room.type}, Capacity: ${room.capacity})
        </option>`
    ).join('');
    
    // Populate instructors dropdown (only qualified ones)
    const instructorSelect = document.getElementById('edit-instructor');
    const qualifiedInstructors = allData.instructors.filter(inst => 
        inst.qualified_courses.includes(entry.course_id)
    );
    
    if (qualifiedInstructors.length === 0) {
        instructorSelect.innerHTML = `<option value="${entry.instructor_id}">${entry.instructor_name} (Current)</option>`;
    } else {
        instructorSelect.innerHTML = qualifiedInstructors.map(inst =>
            `<option value="${inst.instructor_id}" ${inst.instructor_id === entry.instructor_id ? 'selected' : ''}>
                ${inst.name} (${inst.role})
            </option>`
        ).join('');
    }
    
    // Show modal
    document.getElementById('editClassModal').style.display = 'flex';
}

function closeEditModal() {
    document.getElementById('editClassModal').style.display = 'none';
    currentEditingEntry = null;
}

function saveClassEdit() {
    if (!currentEditingEntry) {
        return;
    }
    
    // Get new values
    const newDay = document.getElementById('edit-day').value;
    const newTimeslot = document.getElementById('edit-timeslot').value;
    const [newStartTime, newEndTime] = newTimeslot.split(' - ');
    const newRoomId = document.getElementById('edit-room').value;
    const newInstructorId = document.getElementById('edit-instructor').value;
    
    // Find instructor and room details
    const instructor = allData.instructors.find(i => i.instructor_id === newInstructorId);
    const room = allData.rooms.find(r => r.room_id === newRoomId);
    
    if (!instructor || !room) {
        showToast('Invalid instructor or room selected', 'error');
        return;
    }
    
    // Check for conflicts
    const conflict = currentTimetable.schedule.find(e => {
        if (e === currentEditingEntry) return false;  // Skip current entry
        return (
            e.day === newDay &&
            e.start_time === newStartTime &&
            (e.room_id === newRoomId || e.instructor_id === newInstructorId)
        );
    });
    
    if (conflict) {
        showToast(`Conflict detected: ${conflict.room_id === newRoomId ? 'Room' : 'Instructor'} already assigned at this time`, 'error');
        return;
    }
    
    // Update the entry
    currentEditingEntry.day = newDay;
    currentEditingEntry.start_time = newStartTime;
    currentEditingEntry.end_time = newEndTime;
    currentEditingEntry.room_id = newRoomId;
    currentEditingEntry.instructor_id = newInstructorId;
    currentEditingEntry.instructor_name = instructor.name;
    
    // Refresh display
    displayTimetableByDay(currentTimetable.schedule);
    applyFilters();  // Reapply any active filters
    
    showToast('Class updated successfully!', 'success');
    closeEditModal();
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('editClassModal');
    if (event.target === modal) {
        closeEditModal();
    }
}

// ============================================================================
// PDF DOWNLOAD AND PRINT FUNCTIONS
// ============================================================================

function printTimetable() {
    window.print();
}

async function downloadPDF() {
    if (!currentTimetable || !currentTimetable.schedule) {
        showToast('No timetable to download', 'error');
        return;
    }
    
    showToast('Generating PDF... Please wait', 'info');
    
    // Import jsPDF
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('l', 'mm', 'a4'); // Landscape A4
    
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'];
    const times = ['9:00 AM - 10:30 AM', '10:45 AM - 12:15 PM', '12:30 PM - 2:00 PM', '2:15 PM - 3:45 PM'];
    
    // Group schedule by day and time
    const grouped = {};
    currentTimetable.schedule.forEach(entry => {
        if (!grouped[entry.day]) {
            grouped[entry.day] = {};
        }
        const timeKey = `${entry.start_time} - ${entry.end_time}`;
        if (!grouped[entry.day][timeKey]) {
            grouped[entry.day][timeKey] = [];
        }
        grouped[entry.day][timeKey].push(entry);
    });
    
    // Title
    doc.setFontSize(20);
    doc.setTextColor(40, 40, 40);
    doc.text('CSP TIMETABLEAI - INTELLIGENT SCHEDULING', 148, 15, { align: 'center' });
    
    doc.setFontSize(12);
    doc.setTextColor(100, 100, 100);
    const date = new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    doc.text(`Generated on: ${date}`, 148, 22, { align: 'center' });
    
    // Summary stats
    doc.setFontSize(10);
    doc.setTextColor(60, 60, 60);
    const stats = `Total Classes: ${currentTimetable.schedule.length} | Success Rate: ${currentTimetable.success_rate}%`;
    doc.text(stats, 148, 28, { align: 'center' });
    
    let yPos = 35;
    
    // Draw timetable grid
    days.forEach((day, dayIndex) => {
        if (yPos > 180) {
            doc.addPage();
            yPos = 20;
        }
        
        // Day header
        doc.setFillColor(52, 152, 219);
        doc.rect(10, yPos, 277, 8, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.text(day, 15, yPos + 5.5);
        
        const dayClasses = grouped[day] || {};
        const classCount = Object.values(dayClasses).flat().length;
        doc.text(`(${classCount} classes)`, 270, yPos + 5.5);
        
        yPos += 10;
        
        // Time slots
        times.forEach((time, timeIndex) => {
            const classes = dayClasses[time] || [];
            
            if (classes.length > 0) {
                // Time slot header
                doc.setFillColor(236, 240, 241);
                doc.rect(10, yPos, 277, 6, 'F');
                doc.setTextColor(60, 60, 60);
                doc.setFontSize(9);
                doc.setFont(undefined, 'bold');
                doc.text(time, 15, yPos + 4);
                doc.text(`(${classes.length})`, 270, yPos + 4);
                
                yPos += 8;
                
                // Classes
                classes.forEach((entry, idx) => {
                    if (yPos > 185) {
                        doc.addPage();
                        yPos = 20;
                    }
                    
                    const isLab = entry.course_type.includes('Lab');
                    const bgColor = isLab ? [255, 243, 224] : [232, 245, 233];
                    doc.setFillColor(bgColor[0], bgColor[1], bgColor[2]);
                    doc.rect(15, yPos, 267, 10, 'F');
                    doc.rect(15, yPos, 267, 10, 'S');
                    
                    doc.setFont(undefined, 'bold');
                    doc.setTextColor(40, 40, 40);
                    doc.setFontSize(9);
                    doc.text(entry.course_id, 18, yPos + 4);
                    
                    doc.setFont(undefined, 'normal');
                    doc.setTextColor(60, 60, 60);
                    doc.setFontSize(8);
                    const courseName = entry.course_name.length > 40 ? 
                        entry.course_name.substring(0, 37) + '...' : 
                        entry.course_name;
                    doc.text(courseName, 18, yPos + 7.5);
                    
                    // Room and instructor
                    doc.setFontSize(7);
                    doc.setTextColor(80, 80, 80);
                    doc.text(`Room: ${entry.room_id}`, 160, yPos + 4);
                    const instName = entry.instructor_name.length > 25 ? 
                        entry.instructor_name.substring(0, 22) + '...' : 
                        entry.instructor_name;
                    doc.text(`Instructor: ${instName}`, 160, yPos + 7.5);
                    
                    // Type badge
                    const badgeColor = isLab ? [255, 152, 0] : [76, 175, 80];
                    doc.setFillColor(badgeColor[0], badgeColor[1], badgeColor[2]);
                    doc.roundedRect(250, yPos + 2, 28, 6, 2, 2, 'F');
                    doc.setTextColor(255, 255, 255);
                    doc.setFont(undefined, 'bold');
                    doc.setFontSize(7);
                    doc.text(isLab ? 'LAB' : 'LECTURE', 264, yPos + 5.5, { align: 'center' });
                    
                    yPos += 11;
                });
                
                yPos += 2;
            }
        });
        
        yPos += 3;
    });
    
    // Footer on last page
    const pageCount = doc.internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(`Page ${i} of ${pageCount}`, 148, 200, { align: 'center' });
        doc.setFontSize(7);
        doc.text('Generated by CSP TimetableAI - Intelligent Scheduling System', 148, 204, { align: 'center' });
        doc.setFontSize(6);
        doc.text('© 2025 Roqia. All Rights Reserved.', 148, 207, { align: 'center' });
    }
    
    // Save the PDF
    doc.save('CSP-TimetableAI-Schedule.pdf');
    showToast('PDF downloaded successfully!', 'success');
}
