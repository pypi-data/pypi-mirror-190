class Course:
    def __init__(self, crn: str, code: str, title: str, teaching_method: str,
                 instructor: str, building: str, day: str, time: str, room: str,
                 capacity: str, enrolled: str, reservation: str, restriction: str,
                 prereq: str, classrest: str):
        self.crn = crn
        self.code = code
        self.title = title
        self.teaching_method = teaching_method
        self.instructor = instructor
        self.building = building.strip()
        self.day = day.strip().split(" ")
        self.time = time.strip().split(" ")
        self.room = room.strip()
        self.capacity = capacity
        self.enrolled = enrolled
        self.reservation = reservation
        self.restriction = restriction.split(", ")
        self.prereq = prereq
        self.classrest = classrest

    def __repr__(self) -> str:
        return f"Course(crn={self.crn}, code={self.code})"


