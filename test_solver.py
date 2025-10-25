# test_solver.py (FIXED VERSION)
from data_loader import DataLoader
from csp_model import CSPTimetable

def test_small_subset():
    """Test with a small subset of courses using improved solver"""
    loader = DataLoader()
    loader.load_all_data('Courses.csv', 'Instructor.csv', 'Rooms.csv', 'TimeSlots.csv')
    
    # Take only first 10 courses for testing
    test_courses = loader.get_courses()[:10]
    print(f"Testing with {len(test_courses)} courses:")
    for course in test_courses:
        qualified = [instr for instr in loader.get_instructors() if course.course_id in instr.qualified_courses]
        status = "✓" if qualified else "✗"
        print(f"  {status} {course.course_id}: {course.name} ({len(qualified)} qualified instructors)")
    
    # Filter out courses with no qualified instructors
    schedulable_courses = [c for c in test_courses if any(instr for instr in loader.get_instructors() if c.course_id in instr.qualified_courses)]
    print(f"\nActually schedulable: {len(schedulable_courses)} courses")
    
    solver = CSPTimetable(
        courses=schedulable_courses,
        instructors=loader.get_instructors(),
        rooms=loader.get_rooms(),
        timeslots=loader.get_timeslots()
    )
    
    print("\nAttempting to generate timetable...")
    success = solver.solve_with_distribution(timeout_seconds=15)
    
    if success:
        print("✅ Timetable generated successfully!")
        
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
            print("\nPartial solution found. Showing assigned classes:")
            for var, assignment in solver.assignments.items():
                timeslot, room, instructor = assignment
                print(f"  {var.course_id}: {timeslot.day} {timeslot.start_time} in {room.room_id} by {instructor.name}")

def test_with_proven_courses():
    """Test with courses we know work well"""
    loader = DataLoader()
    loader.load_all_data('Courses.csv', 'Instructor.csv', 'Rooms.csv', 'TimeSlots.csv')
    
    # Select courses that have multiple qualified instructors (better chance of scheduling)
    all_courses = loader.get_courses()
    
    # Find courses with at least 2 qualified instructors
    courses_with_multiple_instructors = []
    for course in all_courses:
        qualified = [instr for instr in loader.get_instructors() if course.course_id in instr.qualified_courses]
        if len(qualified) >= 2:
            courses_with_multiple_instructors.append(course)
    
    # Take first 15 of these
    test_courses = courses_with_multiple_instructors[:15]
    
    print(f"Testing with {len(test_courses)} courses that have multiple qualified instructors:")
    for course in test_courses:
        qualified = [instr for instr in loader.get_instructors() if course.course_id in instr.qualified_courses]
        print(f"  ✓ {course.course_id}: {len(qualified)} qualified instructors")
    
    solver = CSPTimetable(
        courses=test_courses,
        instructors=loader.get_instructors(),
        rooms=loader.get_rooms(),
        timeslots=loader.get_timeslots()
    )
    
    print("\nAttempting to generate timetable...")
    success = solver.solve_with_distribution(timeout_seconds=30)
    
    if success:
        print("✅ Timetable generated successfully!")
        
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

def main():
    print("=== AUTOMATED TIMETABLE GENERATOR ===")
    print("1. Test with first 10 courses (filtered)")
    print("2. Test with courses that have multiple instructors (better success)")
    
    choice = input("\nChoose test (1 or 2): ").strip()
    
    if choice == "1":
        test_small_subset()
    elif choice == "2":
        test_with_proven_courses()
    else:
        print("Invalid choice. Running proven test...")
        test_with_proven_courses()

if __name__ == "__main__":
    main()