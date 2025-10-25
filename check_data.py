# check_data.py
from data_loader import DataLoader

def check_data_integrity():
    loader = DataLoader()
    loader.load_all_data('Courses.csv', 'Instructor.csv', 'Rooms.csv', 'TimeSlots.csv')
    
    print("=== DATA INTEGRITY CHECK ===")
    
    # Check if courses have qualified instructors
    courses_with_instructors = 0
    for course in loader.get_courses()[:10]:  # Check first 10
        qualified = [instr for instr in loader.get_instructors() if course.course_id in instr.qualified_courses]
        if qualified:
            courses_with_instructors += 1
            print(f"✓ {course.course_id} has {len(qualified)} qualified instructors")
        else:
            print(f"✗ {course.course_id} has NO qualified instructors!")
    
    print(f"\nSummary: {courses_with_instructors}/10 courses have qualified instructors")
    
    # Check room types
    lecture_rooms = len([r for r in loader.get_rooms() if r.type == "Lecture"])
    lab_rooms = len([r for r in loader.get_rooms() if r.type == "Lab"])
    print(f"Rooms: {lecture_rooms} lecture rooms, {lab_rooms} lab rooms")
    
    # Check instructor availability patterns
    unavailable_days = {}
    for instr in loader.get_instructors():
        day = instr.unavailable_day
        unavailable_days[day] = unavailable_days.get(day, 0) + 1
    
    print("Instructor unavailable days:")
    for day, count in unavailable_days.items():
        print(f"  {day}: {count} instructors")

if __name__ == "__main__":
    check_data_integrity()