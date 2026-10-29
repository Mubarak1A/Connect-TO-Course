#!/usr/bin/python3
""""Module that contain all functionalities"""

import random

def generate_courses(courses_list):
    """Generate up to 10 random unique courses"""
    if not courses_list:
        return []
    
    count = min(10, len(courses_list))
    return random.sample(courses_list, count)


def search_courses(courses_list, search_str):
    """Search for courses related to the search string and return a list of matches."""
    matched_courses = []
    for course in courses_list:
        course_title = course.title.lower()
        if search_str.lower() in course_title:
            matched_courses.append(course)

    # Convert to JSON-serializable format
    courses_data = [
        {'id': course.id, 'title': course.title, 'url': course.url, 'instructor': course.instructor}
        for course in matched_courses
    ]
    return courses_data


def save_course(course):
    """Add a course to list of saved courses"""
    save_courses = []
    save_courses.append(course)
    return save_courses


def filter_search(courses_list, course_category=None, src=None, plan=None):
    """Filter the course search, return list of courses under args"""
    courses = []
    if course_category is not None:
        for course in course_category:
            if course['source'] == src and course['plan'] == plan:
                courses.append(course)
    else:
        for course in courses_list:
            if course['source'] == src and course['plan'] == plan:
                courses.append(course)
    return courses
