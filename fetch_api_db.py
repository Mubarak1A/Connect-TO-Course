#!/usr/bin/python3
"""Module to fetch data from the external API and populate the database"""

import os
import requests

API_KEY = os.environ.get('API_KEY', '')
API_HOST = os.environ.get('API_HOST', 'udemy-course-scrapper-api.p.rapidapi.com')

def get_urls():
    """Get the courses URLs"""
    url = f"https://{API_HOST}/course-names/course-instructor/course-url"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    response = requests.get(url, headers=headers)
    urls_data = response.json()
    urls = []
    for data in urls_data.values():
        for url in data.values():
            urls.append(url)
    return urls


def get_instructors():
    """Get the courses instructors"""
    url = f"https://{API_HOST}/course-names/course-instructor"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    response = requests.get(url, headers=headers)
    instructors_data = response.json()
    instructors = []
    for data in instructors_data.values():
        for instructor in data.values():
            instructors.append(instructor)
    return instructors


def get_titles():
    """Get the courses titles"""
    url = f"https://{API_HOST}/course-names"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    response = requests.get(url, headers=headers)
    titles_data = response.json()
    titles = []
    for data in titles_data.values():
        for title in data.values():
            titles.append(title)
    return titles


def assemble_data():
    """Organise all course details"""
    titles = get_titles()
    urls = get_urls()
    instructors = get_instructors()
    courses = []
    for index in range(len(titles)):
        courses.append({
            "title": titles[index],
            "URL": urls[index],
            "instructor": instructors[index]
        })
    return courses
