import json

import data

def goals_to_json():
    with open('data/goals.json', 'w') as file:
        tes.dump(data.goals, file, indent=4)
def teachers_to_json():
    with open('data/teachers.json', 'w') as file:
        tes.dump(data.teachers, file, indent=4)


if __name__ == '__main__':
    goals_to_json()
    teachers_to_json()