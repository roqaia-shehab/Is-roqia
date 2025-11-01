# data_loader.py (using built-in csv module - NO PANDAS)
import csv
from enhanced_csp_model import Course, Instructor, Room, Timeslot

class DataLoader:
    def __init__(self):
        self.courses = []
        self.instructors = []
        self.rooms = []
        self.timeslots = []

    def load_all_data(self, courses_path, instructors_path, rooms_path, timeslots_path):
        """Loads all data from the provided CSV file paths using built-in csv module."""
        try:
            # Clear existing data before reloading
            self.courses = []
            self.instructors = []
            self.rooms = []
            self.timeslots = []
            
            # Load Courses
            with open(courses_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.courses.append(Course(
                        row['CourseID'], 
                        row['CourseName'], 
                        row['Credits'], 
                        row['Type']
                    ))
            
            # Load Instructors
            with open(instructors_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.instructors.append(Instructor(
                        row['InstructorID'],
                        row['Name'],
                        row['Role'],
                        row['PreferredSlots'],
                        row['QualifiedCourses']
                    ))
            
            # Load Rooms
            with open(rooms_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.rooms.append(Room(
                        row['RoomID'],
                        row['Type'],
                        int(row['Capacity'])
                    ))
            
            # Load Timeslots
            with open(timeslots_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.timeslots.append(Timeslot(
                        row['Day'],
                        row['StartTime'],
                        row['EndTime']
                    ))
            
            print("All data loaded successfully using CSV module!")
            print(f"Loaded {len(self.courses)} courses, {len(self.instructors)} instructors, {len(self.rooms)} rooms, {len(self.timeslots)} timeslots")
            
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def get_courses(self):
        return self.courses

    def get_instructors(self):
        return self.instructors

    def get_rooms(self):
        return self.rooms

    def get_timeslots(self):
        return self.timeslots

# Test the data loader
if __name__ == "__main__":
    loader = DataLoader()
    loader.load_all_data('Courses.csv', 'instructors.csv', 'Rooms.csv', 'TimeSlots.csv')
    
    # Print a sample of loaded data
    print("\nSample Course:", loader.courses[0] if loader.courses else "No courses")
    print("Sample Instructor:", loader.instructors[0] if loader.instructors else "No instructors")
    print("Sample Room:", loader.rooms[0] if loader.rooms else "No rooms")
    print("Sample Timeslot:", loader.timeslots[0] if loader.timeslots else "No timeslots")
    
    # Show some qualified courses for the first instructor
    if loader.instructors:
        print(f"\nFirst instructor can teach: {loader.instructors[0].qualified_courses}")
