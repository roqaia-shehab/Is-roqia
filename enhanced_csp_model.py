# enhanced_csp_model.py - Enhanced CSP Timetable Generator
import time
import random
from collections import defaultdict

class Course:
    def __init__(self, course_id, name, credits, type):
        self.course_id = course_id
        self.name = name
        self.credits = credits
        self.type = type

    def __repr__(self):
        return f"Course({self.course_id}: {self.name})"
    
    def to_dict(self):
        return {
            'course_id': self.course_id,
            'name': self.name,
            'credits': self.credits,
            'type': self.type
        }

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
    
    def to_dict(self):
        return {
            'instructor_id': self.instructor_id,
            'name': self.name,
            'role': self.role,
            'unavailable_day': self.unavailable_day,
            'qualified_courses': self.qualified_courses
        }

class Room:
    def __init__(self, room_id, type, capacity):
        self.room_id = room_id
        self.type = type
        self.capacity = capacity

    def __repr__(self):
        return f"Room({self.room_id}: {self.type})"
    
    def to_dict(self):
        return {
            'room_id': self.room_id,
            'type': self.type,
            'capacity': self.capacity
        }

class Timeslot:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.id = f"{day}_{start_time}"

    def __repr__(self):
        return f"Timeslot({self.id})"
    
    def to_dict(self):
        return {
            'day': self.day,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'id': self.id
        }

class ClassVariable:
    """Represents a class that needs to be scheduled"""
    def __init__(self, course_id, section_id="S1"):
        self.course_id = course_id
        self.section_id = section_id
        self.assignment = None
    
    def __repr__(self):
        return f"Class({self.course_id}-{self.section_id})"
    
    def __hash__(self):
        return hash((self.course_id, self.section_id))
    
    def __eq__(self, other):
        return self.course_id == other.course_id and self.section_id == other.section_id

class EnhancedCSPTimetable:
    """Enhanced CSP solver with improved constraints and heuristics"""
    
    def __init__(self, courses, instructors, rooms, timeslots):
        self.courses = courses
        self.instructors = instructors
        self.rooms = rooms
        self.timeslots = timeslots
        
        self.variables = []
        self.assignments = {}
        self.domains = {}
        
        # Statistics for soft constraints
        self.soft_constraint_violations = 0
        self.instructor_workload = defaultdict(int)
        
    def create_variables(self):
        """Create variables for all courses that need to be scheduled
        
        IMPORTANT: Courses with type 'Lecture and Lab' need TWO separate sessions:
        - One lecture session (in a lecture hall)
        - One lab session (in a lab room)
        """
        print("Creating variables (classes to schedule)...")
        
        self.variables = []
        for course in self.courses:
            if "and" in course.type.lower():
                # Course needs BOTH lecture and lab sessions
                lecture_var = ClassVariable(course.course_id, section_id="LECTURE")
                lab_var = ClassVariable(course.course_id, section_id="LAB")
                self.variables.append(lecture_var)
                self.variables.append(lab_var)
                print(f"  {course.course_id}: Created 2 sessions (Lecture + Lab)")
            else:
                # Regular course - only one session
                var = ClassVariable(course.course_id, section_id="S1")
                self.variables.append(var)
            
        print(f"Created {len(self.variables)} variables to schedule (includes split Lecture+Lab courses)")
        return self.variables
    
    def create_domains(self):
        """Create initial domains for all variables with enhanced filtering
        
        For 'Lecture and Lab' courses, respect the section type:
        - LECTURE sections must use Lecture halls
        - LAB sections must use Lab rooms
        """
        print("Creating domains for each variable...")
        
        for variable in self.variables:
            course = next((c for c in self.courses if c.course_id == variable.course_id), None)
            if not course:
                continue
                
            # Find qualified instructors
            qualified_instructors = [
                instr for instr in self.instructors 
                if variable.course_id in instr.qualified_courses
            ]
            
            # Find suitable rooms based on VARIABLE SECTION TYPE (not just course type)
            if variable.section_id == "LAB":
                # This is the LAB portion of a "Lecture and Lab" course
                suitable_rooms = [room for room in self.rooms if room.type == "Lab"]
            elif variable.section_id == "LECTURE":
                # This is the LECTURE portion of a "Lecture and Lab" course
                suitable_rooms = [room for room in self.rooms if room.type == "Lecture"]
            elif "Lab" in course.type:
                # Regular lab-only course
                suitable_rooms = [room for room in self.rooms if room.type == "Lab"]
            else:
                # Regular lecture-only course
                suitable_rooms = [room for room in self.rooms if room.type == "Lecture"]
            
            # Build domain
            domain = []
            for timeslot in self.timeslots:
                for room in suitable_rooms:
                    for instructor in qualified_instructors:
                        # Pre-filter obviously invalid assignments
                        if self._is_instructor_available(instructor, timeslot):
                            domain.append((timeslot, room, instructor))
            
            self.domains[variable] = domain
            
        # Print summary
        total_domain_size = sum(len(self.domains.get(var, [])) for var in self.variables)
        avg_domain_size = total_domain_size / len(self.variables) if self.variables else 0
        print(f"Average domain size: {avg_domain_size:.1f} assignments per variable")
            
        return self.domains
    
    def _is_instructor_available(self, instructor, timeslot):
        """Check if instructor is available at this timeslot"""
        unavailable_day = instructor.unavailable_day.replace("Not on", "").strip()
        return timeslot.day.lower() != unavailable_day.lower()
    
    def is_assignment_valid(self, variable, timeslot, room, instructor):
        """Check if an assignment violates any HARD constraints"""
        course = next((c for c in self.courses if c.course_id == variable.course_id), None)
        if not course:
            return False
        
        # HARD CONSTRAINT 1: Room type must match the SECTION type (not just course type)
        if variable.section_id == "LAB":
            # LAB section of "Lecture and Lab" course - must be in a lab
            if room.type != "Lab":
                return False
        elif variable.section_id == "LECTURE":
            # LECTURE section of "Lecture and Lab" course - must be in lecture hall
            if room.type != "Lecture":
                return False
        elif "Lab" in course.type:
            # Regular lab-only course
            if room.type != "Lab":
                return False
        else:
            # Regular lecture-only course
            if room.type != "Lecture":
                return False
        
        # HARD CONSTRAINT 2: Instructor cannot teach on their unavailable day
        if not self._is_instructor_available(instructor, timeslot):
            return False
        
        # HARD CONSTRAINT 3: Instructor must be qualified for the course
        if variable.course_id not in instructor.qualified_courses:
            return False
            
        # HARD CONSTRAINT 4: No room double-booking
        for other_var, other_assignment in self.assignments.items():
            if other_assignment[0].id == timeslot.id and other_assignment[1].room_id == room.room_id:
                return False
                
        # HARD CONSTRAINT 5: No instructor double-booking
        for other_var, other_assignment in self.assignments.items():
            if other_assignment[0].id == timeslot.id and other_assignment[2].instructor_id == instructor.instructor_id:
                return False
        
        # HARD CONSTRAINT 6: Instructor workload limit (max 4 classes per day)
        day_workload = sum(1 for other_var, other_assignment in self.assignments.items() 
                          if other_assignment[0].day == timeslot.day 
                          and other_assignment[2].instructor_id == instructor.instructor_id)
        if day_workload >= 4:
            return False
        
        # HARD CONSTRAINT 7: Lecture and Lab sections of same course must be at DIFFERENT times
        # (Students can't attend both at the same time!)
        for other_var, other_assignment in self.assignments.items():
            if (variable.course_id == other_var.course_id and 
                variable.section_id != other_var.section_id and
                other_assignment[0].id == timeslot.id):
                # Same course, different sections (LECTURE vs LAB), same timeslot = CONFLICT!
                return False
                
        return True
    
    def calculate_soft_constraint_score(self, variable, timeslot, room, instructor):
        """Calculate a score based on soft constraints (lower is better)"""
        score = 0
        
        # SOFT CONSTRAINT 1: Very light penalty for early/late slots (don't avoid them too much)
        if timeslot.start_time in ["9:00 AM"]:
            score += 0.5  # Very small penalty for early morning
        if timeslot.start_time in ["2:15 PM"]:
            score += 0.5  # Very small penalty for late afternoon
        
        # SOFT CONSTRAINT 2: Balance day distribution (but less aggressive)
        day_count = sum(1 for ass in self.assignments.values() if ass[0].day == timeslot.day)
        score += day_count * 0.5  # Reduced penalty - still balance but don't avoid days
        
        # SOFT CONSTRAINT 3: Instructor workload balance
        instructor_count = sum(1 for ass in self.assignments.values() 
                              if ass[2].instructor_id == instructor.instructor_id)
        score += instructor_count * 0.3  # Prefer instructors with fewer classes
        
        # SOFT CONSTRAINT 4: Prefer larger rooms for lecture courses
        course = next((c for c in self.courses if c.course_id == variable.course_id), None)
        if course and "Lab" not in course.type and room.capacity < 50:
            score += 1
        
        # SOFT CONSTRAINT 5: Bonus for consecutive slots (reduces gaps)
        consecutive_bonus = 0
        for other_var, other_assignment in self.assignments.items():
            if other_assignment[2].instructor_id == instructor.instructor_id:
                if other_assignment[0].day == timeslot.day:
                    # Check if it's the same timeslot or adjacent
                    if self._are_timeslots_consecutive(timeslot, other_assignment[0]):
                        consecutive_bonus -= 2  # Bonus for consecutive slots (reduces gaps)
        score += consecutive_bonus
        
        # Add randomness to explore more possibilities
        score += random.uniform(-0.5, 0.5)
        
        return score
    
    def _are_timeslots_consecutive(self, slot1, slot2):
        """Check if two timeslots are consecutive"""
        time_order = ["9:00 AM", "10:45 AM", "12:30 PM", "2:15 PM"]
        if slot1.day != slot2.day:
            return False
        try:
            idx1 = time_order.index(slot1.start_time)
            idx2 = time_order.index(slot2.start_time)
            return abs(idx1 - idx2) == 1
        except:
            return False
    
    def select_unassigned_variable(self):
        """Select next variable using MRV (Minimum Remaining Values) heuristic"""
        unassigned = [v for v in self.variables if v not in self.assignments]
        if not unassigned:
            return None
        
        # MRV: Choose variable with smallest domain
        return min(unassigned, key=lambda v: len(self.domains.get(v, [])))
    
    def order_domain_values(self, variable):
        """Order domain values using soft constraint scores - OPTIMIZED for speed"""
        domain = self.domains.get(variable, [])
        
        if not domain:
            return []
        
        # For speed: limit scoring to first 100 options (usually enough)
        if len(domain) > 100:
            # Randomly sample to ensure variety
            random.shuffle(domain)
            domain = domain[:100]
        
        # Score each assignment
        scored_assignments = []
        for assignment in domain:
            timeslot, room, instructor = assignment
            score = self.calculate_soft_constraint_score(variable, timeslot, room, instructor)
            scored_assignments.append((score, assignment))
        
        # Sort by score (lower is better)
        scored_assignments.sort(key=lambda x: x[0])
        
        # Return ordered assignments
        return [assignment for score, assignment in scored_assignments]
    
    def forward_check(self):
        """Perform forward checking to reduce domains"""
        for variable in self.variables:
            if variable not in self.assignments:
                self.domains[variable] = [
                    ass for ass in self.domains.get(variable, [])
                    if self.is_assignment_valid(variable, ass[0], ass[1], ass[2])
                ]
                if not self.domains[variable]:
                    return False
        return True
    
    def solve_enhanced(self, timeout_seconds=60):
        """Enhanced solver using FAST GREEDY algorithm with constraint satisfaction"""
        print("\n" + "="*80)
        print("🚀 FAST GREEDY CSP SOLVER - Starting...")
        print("="*80)
        
        start_time = time.time()
        
        if not self.variables:
            self.create_variables()
        if not self.domains:
            self.create_domains()
        
        self.start_time = start_time
        self.timeout_seconds = timeout_seconds
        
        print(f"\n📊 Problem Size:")
        print(f"   - Sessions to schedule: {len(self.variables)}")
        print(f"   - Instructors: {len(self.instructors)}")
        print(f"   - Rooms: {len(self.rooms)}")
        print(f"   - Timeslots: {len(self.timeslots)}")
        
        # Use FAST GREEDY algorithm instead of slow backtracking
        best_assignments = {}
        best_count = 0
        
        max_attempts = 5  # Try multiple times with different orders
        
        for attempt in range(max_attempts):
            print(f"\n🔄 Attempt {attempt + 1}/{max_attempts}")
            
            # Clear previous assignments
            self.assignments = {}
            
            # Recreate domains with randomization
            self.create_domains()
            
            # GREEDY SCHEDULING: Assign each variable to best available slot
            scheduled = self._greedy_schedule()
            
            # Keep track of best result
            if scheduled > best_count:
                best_count = scheduled
                best_assignments = dict(self.assignments)
                print(f"   ✨ New best: {best_count}/{len(self.variables)} sessions scheduled ({best_count/len(self.variables)*100:.1f}%)")
            
            # If we got 95%+ success, that's good enough
            if scheduled >= len(self.variables) * 0.95:
                print(f"   ✅ Excellent result (95%+ scheduled)!")
                break
            
            # Check elapsed time
            elapsed = time.time() - start_time
            if elapsed > 20:  # Stop after 20 seconds
                print(f"   ⏰ Time limit reached ({elapsed:.1f}s)")
                break
        
        # Use the best assignments found
        self.assignments = best_assignments
        for var, assignment in self.assignments.items():
            var.assignment = assignment
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"\n{'='*80}")
        print(f"✅ Solver finished in {elapsed:.2f} seconds")
        print(f"📊 Scheduled: {len(self.assignments)}/{len(self.variables)} sessions ({(len(self.assignments)/len(self.variables)*100):.1f}%)")
        print(f"{'='*80}")
        
        return len(self.assignments) > 0
    
    def _greedy_schedule(self):
        """Fast greedy scheduling algorithm"""
        # Sort variables by domain size (most constrained first)
        sorted_vars = sorted(self.variables, key=lambda v: len(self.domains.get(v, [])))
        
        scheduled = 0
        for i, variable in enumerate(sorted_vars):
            # Progress indicator every 20 sessions
            if i % 20 == 0 and i > 0:
                print(f"     Progress: {i}/{len(sorted_vars)} sessions processed, {scheduled} scheduled")
            
            # Get ordered domain values
            domain = self.order_domain_values(variable)
            
            # Try to assign first valid value
            for assignment in domain:
                timeslot, room, instructor = assignment
                
                if self.is_assignment_valid(variable, timeslot, room, instructor):
                    # Make assignment
                    self.assignments[variable] = assignment
                    variable.assignment = assignment
                    scheduled += 1
                    break
        
        return scheduled

    def _backtrack_enhanced(self):
        """Enhanced backtracking with better heuristics"""
        # Check timeout
        if time.time() - self.start_time > self.timeout_seconds:
            print("⏰ Timeout reached!")
            return False
        
        # Check if complete
        if len(self.assignments) == len(self.variables):
            return True
        
        # Select variable using MRV
        variable = self.select_unassigned_variable()
        if variable is None:
            return True
        
        # Progress indicator
        progress = len(self.assignments)
        if progress % 10 == 0:
            elapsed = time.time() - self.start_time
            print(f"  Progress: {progress}/{len(self.variables)} classes assigned ({elapsed:.1f}s)")
        
        # Order domain values
        ordered_domain = self.order_domain_values(variable)
        
        for assignment in ordered_domain:
            timeslot, room, instructor = assignment
            
            if self.is_assignment_valid(variable, timeslot, room, instructor):
                # Save current state
                original_domains = {v: list(self.domains.get(v, [])) for v in self.variables}
                
                # Make assignment
                self.assignments[variable] = assignment
                variable.assignment = assignment
                
                # Forward checking
                if self.forward_check():
                    if self._backtrack_enhanced():
                        return True
                
                # Backtrack
                del self.assignments[variable]
                variable.assignment = None
                self.domains = original_domains
                
        return False
    
    def get_statistics(self):
        """Get statistics about the generated timetable"""
        if not self.assignments:
            return None
        
        stats = {
            'total_classes': len(self.assignments),
            'day_distribution': defaultdict(int),
            'instructor_workload': defaultdict(int),
            'room_utilization': defaultdict(int),
            'timeslot_usage': defaultdict(int)
        }
        
        for variable, assignment in self.assignments.items():
            timeslot, room, instructor = assignment
            stats['day_distribution'][timeslot.day] += 1
            stats['instructor_workload'][instructor.name] += 1
            stats['room_utilization'][room.room_id] += 1
            stats['timeslot_usage'][timeslot.id] += 1
        
        return stats
    
    def print_solution(self):
        """Print the generated timetable in a formatted way"""
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
                
            course = next((c for c in self.courses if c.course_id == variable.course_id), None)
            schedule_by_timeslot[key].append({
                'course_id': variable.course_id,
                'course_name': course.name if course else 'Unknown',
                'room': room.room_id,
                'instructor': instructor.name,
                'type': course.type if course else 'Unknown'
            })
        
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
        for day in days:
            print(f"\n{'='*80}")
            print(f"  {day.upper()}")
            print(f"{'='*80}")
            
            day_slots = {k: v for k, v in schedule_by_timeslot.items() if k[0] == day}
            
            if not day_slots:
                print("  No classes scheduled")
                continue
                
            for timeslot_key in sorted(day_slots.keys(), key=lambda x: x[1]):
                day, start, end = timeslot_key
                classes = day_slots[timeslot_key]
                
                print(f"\n  📅 {start} - {end}")
                print(f"  {'-'*76}")
                for class_info in classes:
                    print(f"    • {class_info['course_id']:12} | {class_info['course_name'][:30]:30} | "
                          f"{class_info['room']:12} | {class_info['instructor']}")
        
        # Print statistics
        stats = self.get_statistics()
        if stats:
            print(f"\n{'='*80}")
            print("STATISTICS")
            print(f"{'='*80}")
            print(f"\nDay Distribution:")
            for day in days:
                count = stats['day_distribution'][day]
                print(f"  {day:12}: {count:3} classes {'█' * count}")
            
            print(f"\nTop 10 Most Utilized Rooms:")
            top_rooms = sorted(stats['room_utilization'].items(), key=lambda x: x[1], reverse=True)[:10]
            for room, count in top_rooms:
                print(f"  {room:15}: {count:2} classes")
            
            print(f"\nTop 10 Busiest Instructors:")
            top_instructors = sorted(stats['instructor_workload'].items(), key=lambda x: x[1], reverse=True)[:10]
            for instructor, count in top_instructors:
                print(f"  {instructor[:30]:30}: {count:2} classes")
    
    def export_to_dict(self):
        """Export timetable to dictionary format for JSON serialization"""
        result = {
            'success': len(self.assignments) == len(self.variables),
            'total_courses': len(self.variables),
            'scheduled_courses': len(self.assignments),
            'schedule': []
        }
        
        for variable, assignment in self.assignments.items():
            timeslot, room, instructor = assignment
            course = next((c for c in self.courses if c.course_id == variable.course_id), None)
            
            result['schedule'].append({
                'course_id': variable.course_id,
                'course_name': course.name if course else 'Unknown',
                'course_type': course.type if course else 'Unknown',
                'section_id': variable.section_id,
                'day': timeslot.day,
                'start_time': timeslot.start_time,
                'end_time': timeslot.end_time,
                'room_id': room.room_id,
                'room_type': room.type,
                'room_capacity': room.capacity,
                'instructor_id': instructor.instructor_id,
                'instructor_name': instructor.name,
                'instructor_role': instructor.role
            })
        
        # Add statistics
        stats = self.get_statistics()
        if stats:
            result['statistics'] = {
                'day_distribution': dict(stats['day_distribution']),
                'instructor_workload': dict(stats['instructor_workload']),
                'room_utilization': dict(stats['room_utilization'])
            }
        
        return result
