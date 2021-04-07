import random as rd

from utils import CsvTools

headers = ['id', 'lesson_completion', 'webinar_completion', 'test_completion', 'average_points_for_tests']
group_types = ['bad', 'good', 'excellent', 'mixed']
courses_name = ['Русский язык Гр1', 'Математика Гр1', 'Математика Гр2']


def generate_points(group_type):
    if group_type == 'bad':
        return rd.randint(0, 50)
    elif group_type == 'good':
        return rd.randint(50, 85)
    elif group_type == 'excellent':
        return rd.randint(85, 100)
    elif group_type == 'mixed':
        return rd.choice([rd.randint(0, 25), rd.randint(75, 100)])


def generate_student_id(used_ids: list, all_students_ids: list) -> int:
    available_ids = set(all_students_ids) - set(used_ids)
    return rd.choice(list(available_ids))


def main():
    students = list(range(100))
    for course in courses_name:
        already_in_group = []
        for group_type in group_types:
            print(f'COURSE: {course} ({group_type} group type)')

            writer = CsvTools.csv_writer('generated_students/' + '_'.join(course.split()) + '_' + group_type + '.csv')
            writer.writerow(headers)

            for _ in range(rd.randint(10, 25)):  # the amount of students in a group

                student_id = generate_student_id(already_in_group, students)
                already_in_group += [student_id]

                student_row = [student_id]
                print('STUDENT ID:', student_id)

                for header in headers[1:]:
                    student_row += [generate_points(group_type)]
                    print(f'{header}:', student_row[-1])

                writer.writerow(student_row)
                print()


if __name__ == '__main__':
    main()
