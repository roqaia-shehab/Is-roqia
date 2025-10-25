# test_improved.py
from data_loader import DataLoader
from csp_model import CSPTimetable

def test_with_more_courses():
    """Test with more courses and better distribution"""
    loader = DataLoader()
    loader.load_all_data('Courses.csv', 'Instructor.csv', 'Rooms.csv', 'TimeSlots.csv')
    
    # Select more courses that should work
    all_courses = loader.get_courses()
    
    # Filter courses that have qualified instructors
    schedulable_courses = []
    for course in all_courses[:15]:  # Try first 15 courses
        qualified_instructors = [
            instr for instr in loader.get_instructors() 
            if course.course_id in instr.qualified_courses
        ]
        if qualified_instructors:
            schedulable_courses.append(course)
    
    print(f"Testing with {len(schedulable_courses)} schedulable courses:")
    for course in schedulable_courses:
        qualified = [instr for instr in loader.get_instructors() if course.course_id in instr.qualified_courses]
        print(f"  - {course.course_id}: {len(qualified)} qualified instructors")
    
    solver = CSPTimetable(
        courses=schedulable_courses,
        instructors=loader.get_instructors(),
        rooms=loader.get_rooms(),
        timeslots=loader.get_timeslots()
    )
    
    print("\nAttempting to generate distributed timetable...")
    
    # Use the new distribution-aware solver
    success = solver.solve_with_distribution(timeout_seconds=30)
    
    if success:
        print("✅ Distributed timetable generated successfully!")
        
        # Show day distribution
        day_distribution = {}
        for assignment in solver.assignments.values():
            day = assignment[0].day
            day_distribution[day] = day_distribution.get(day, 0) + 1
        
        print(f"\nDay Distribution:")
        for day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']:
            count = day_distribution.get(day, 0)
            print(f"  {day}: {count} classes")
        
        solver.print_solution()
    else:
        print(f"❌ Result: Assigned {len(solver.assignments)} out of {len(solver.variables)} classes")
        if solver.assignments:
            # Show distribution of assigned classes
            day_distribution = {}
            for assignment in solver.assignments.values():
                day = assignment[0].day
                day_distribution[day] = day_distribution.get(day, 0) + 1
            
            print(f"\nDay Distribution of assigned classes:")
            for day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']:
                count = day_distribution.get(day, 0)
                print(f"  {day}: {count} classes")
            
            print("\nFirst 10 assigned classes:")
            for var, assignment in list(solver.assignments.items())[:10]:
                timeslot, room, instructor = assignment
                print(f"  {var.course_id}: {timeslot.day} {timeslot.start_time} in {room.room_id} by {instructor.name}")

def main():
    print("=== IMPROVED TIMETABLE GENERATOR ===")
    print("Testing with more courses and better day distribution...")
    test_with_more_courses()

if __name__ == "__main__":
    main()