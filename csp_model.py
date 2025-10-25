# csp_model.py
import time

class Course:
    def __init__(self, course_id, name, credits, type):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.type = type

    def __repr__(self):
        return f"Course({self.course_id}: {self.name})"

class Instructor:
    def __init__(self, instructor_id, name, role, preferred_slots, qualified_courses):
        self.instructor_id = instructor_id
        self.name = name
        self.role = role
        self.unavailable_day = preferred_slots
        if isinstance(qualified_courses, str):
            self.qualified_courses = [c.strip() for c in qualified_courses.split(",")] if qualified_courses else []
        else:
            self.qualified_courses = qualified_courses or []

    def __repr__(self):
        return f"Instructor({self.instructor_id}: {self.name})"

class Room:
    def __init__(self, room_id, type, capacity):
        self.room_id = room_id
        self.type = type
        self.capacity = capacity

    def __repr__(self):
        return f"Room({self.room_id}: {self.type})"

class Timeslot:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.id = f"{day}_{start_time}"

    def __repr__(self):
        return f"Timeslot({self.id})"

class ClassVariable:
    """Represents a class that needs to be scheduled"""
    def __init__(self, course_id, section_id="S1"):
        self.course_id = course_id
        self.section_id = section_id
        self.assignment = None
    
    def __repr__(self):
        return f"Class({self.course_id}-{self.section_id})"

class CSPTimetable:
    """Main CSP solver for timetable generation"""
    
    def __init__(self, courses, instructors, rooms, timeslots):
        self.courses = courses
        self.instructors = instructors
        self.rooms = rooms
        self.timeslots = timeslots
        
        self.variables = []
        self.assignments = {}
        self.domains = {}
        
    def create_variables(self):
        """Create variables for all courses that need to be scheduled"""
        print("Creating variables (classes to schedule)...")
        
        self.variables = []
        for course in self.courses:
            var = ClassVariable(course.course_id)
            self.variables.append(var)
            
        print(f"Created {len(self.variables)} variables to schedule")
        return self.variables
    
    def create_domains(self):
        """Create initial domains for all variables"""
        print("Creating domains for each variable...")
        
        for variable in self.variables:
            course = next((c for c in self.courses if c.course_id == variable.course_id), None)
            if not course:
                continue
                
            qualified_instructors = [
                instr for instr in self.instructors 
                if variable.course_id in instr.qualified_courses
            ]
            
            if "Lab" in course.type:
                suitable_rooms = [room for room in self.rooms if room.type == "Lab"]
            else:
                suitable_rooms = [room for room in self.rooms if room.type == "Lecture"]
            
            domain = []
            for timeslot in self.timeslots:
                for room in suitable_rooms:
                    for instructor in qualified_instructors:
                        domain.append((timeslot, room, instructor))
            
            self.domains[variable] = domain
            
        for variable in self.variables[:5]:
            print(f"  {variable}: {len(self.domains.get(variable, []))} possible assignments")
            
        return self.domains
    
    def is_assignment_valid(self, variable, timeslot, room, instructor):
        """Check if an assignment violates any hard constraints"""
        course = next((c for c in self.courses if c.course_id == variable.course_id), None)
        if not course:
            return False
            
        # Constraint 1: Room type must match course type
        if "Lab" in course.type and room.type != "Lab":
            return False
        elif "Lab" not in course.type and room.type != "Lecture":
            return False
        
        # Constraint 2: Instructor cannot teach on their unavailable day
        # FIX: Better day matching - extract the day from "Not on Tuesday"
        unavailable_day = instructor.unavailable_day.replace("Not on", "").strip()
        if timeslot.day.lower() == unavailable_day.lower():
            return False
            
        # Constraint 3: No room double-booking
        for other_var, other_assignment in self.assignments.items():
            if other_assignment[0] == timeslot and other_assignment[1] == room:
                return False
                
        # Constraint 4: No instructor double-booking
        for other_var, other_assignment in self.assignments.items():
            if other_assignment[0] == timeslot and other_assignment[2] == instructor:
                return False
                
        return True
    
    def solve_naive(self, timeout_seconds=30):
        """A simple backtracking solver with timeout"""
        print("\nStarting CSP solver...")
        start_time = time.time()
        
        if not self.variables:
            self.create_variables()
        if not self.domains:
            self.create_domains()
        
        self.start_time = start_time
        self.timeout_seconds = timeout_seconds
        
        result = self._backtrack_with_timeout()
        
        end_time = time.time()
        print(f"Solver finished in {end_time - start_time:.2f} seconds")
        return result

    def _backtrack_with_timeout(self):
        """Backtracking with timeout check"""
        if time.time() - self.start_time > self.timeout_seconds:
            print("⏰ Timeout reached!")
            return False
            
        if len(self.assignments) == len(self.variables):
            return True
            
        unassigned = [v for v in self.variables if v not in self.assignments]
        variable = min(unassigned, key=lambda v: len(self.domains.get(v, [])))
        
        progress = len(self.assignments)
        if progress % 5 == 0:
            print(f"  Progress: {progress}/{len(self.variables)} classes assigned")
        
        domain = self.domains.get(variable, [])
        for assignment in domain:
            timeslot, room, instructor = assignment
            
            if self.is_assignment_valid(variable, timeslot, room, instructor):
                original_domains = {v: list(self.domains.get(v, [])) for v in self.variables}
                
                self.assignments[variable] = assignment
                variable.assignment = assignment
                
                success = True
                for other_var in self.variables:
                    if other_var not in self.assignments:
                        self.domains[other_var] = [
                            ass for ass in self.domains.get(other_var, [])
                            if self.is_assignment_valid(other_var, ass[0], ass[1], ass[2])
                        ]
                        if not self.domains[other_var]:
                            success = False
                            break
                
                if success:
                    if self._backtrack_with_timeout():
                        return True
                
                del self.assignments[variable]
                variable.assignment = None
                self.domains = original_domains
                
        return False

    def solve_with_distribution(self, timeout_seconds=30):
        """Solver that tries to distribute classes across days"""
        print("\nStarting CSP solver with day distribution...")
        start_time = time.time()
        
        if not self.variables:
            self.create_variables()
        if not self.domains:
            self.create_domains()
        
        self.start_time = start_time
        self.timeout_seconds = timeout_seconds
        
        result = self._backtrack_with_distribution()
        
        end_time = time.time()
        print(f"Solver finished in {end_time - start_time:.2f} seconds")
        return result

    def _backtrack_with_distribution(self):
        """Backtracking that prefers spreading classes across days"""
        if time.time() - self.start_time > self.timeout_seconds:
            print("⏰ Timeout reached!")
            return False
            
        if len(self.assignments) == len(self.variables):
            return True
            
        unassigned = [v for v in self.variables if v not in self.assignments]
        
        # MRV: Select variable with smallest domain
        variable = min(unassigned, key=lambda v: len(self.domains.get(v, [])))
        
        progress = len(self.assignments)
        if progress % 5 == 0:
            print(f"  Progress: {progress}/{len(self.variables)} classes assigned")
        
        # Sort domain to prefer less-used days first
        domain = self.domains.get(variable, [])
        domain = self._sort_domain_by_day_distribution(domain)
        
        for assignment in domain:
            timeslot, room, instructor = assignment
            
            if self.is_assignment_valid(variable, timeslot, room, instructor):
                original_domains = {v: list(self.domains.get(v, [])) for v in self.variables}
                
                self.assignments[variable] = assignment
                variable.assignment = assignment
                
                # Forward checking
                success = True
                for other_var in self.variables:
                    if other_var not in self.assignments:
                        self.domains[other_var] = [
                            ass for ass in self.domains.get(other_var, [])
                            if self.is_assignment_valid(other_var, ass[0], ass[1], ass[2])
                        ]
                        if not self.domains[other_var]:
                            success = False
                            break
                
                if success:
                    if self._backtrack_with_distribution():
                        return True
                
                # Backtrack
                del self.assignments[variable]
                variable.assignment = None
                self.domains = original_domains
                
        return False

    def _sort_domain_by_day_distribution(self, domain):
        """Sort domain to prefer days with fewer scheduled classes"""
        # Count current assignments per day
        day_counts = {}
        for assignment in self.assignments.values():
            day = assignment[0].day
            day_counts[day] = day_counts.get(day, 0) + 1
        
        # Default all days to 0
        all_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        for day in all_days:
            if day not in day_counts:
                day_counts[day] = 0
        
        def day_priority(assignment):
            timeslot, room, instructor = assignment
            return day_counts[timeslot.day]  # Prefer days with fewer classes
        
        return sorted(domain, key=day_priority)
    
    def print_solution(self):
        """Print the generated timetable"""
        if not self.assignments:
            print("No solution found or solver hasn't run yet.")
            return
            
        print("\n" + "="*80)
        print("GENERATED TIMETABLE")
        print("="*80)
        
        schedule_by_timeslot = {}
        
        for variable, assignment in self.assignments.items():
            timeslot, room, instructor = assignment
            key = (timeslot.day, timeslot.start_time, timeslot.end_time)
            
            if key not in schedule_by_timeslot:
                schedule_by_timeslot[key] = []
                
            schedule_by_timeslot[key].append({
                'course': variable.course_id,
                'room': room.room_id,
                'instructor': instructor.name
            })
        
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        for day in days:
            print(f"\n--- {day} ---")
            day_slots = {k: v for k, v in schedule_by_timeslot.items() if k[0] == day}
            
            if not day_slots:
                print("  No classes")
                continue
                
            for timeslot_key in sorted(day_slots.keys(), key=lambda x: x[1]):
                day, start, end = timeslot_key
                classes = day_slots[timeslot_key]
                
                print(f"  {start} - {end}:")
                for class_info in classes:
                    print(f"    {class_info['course']} in {class_info['room']} by {class_info['instructor']}")