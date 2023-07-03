#!/usr/bin/python3
"""Module to fetch data from the extenal api"""

import requests
import creds

def get_urls():
    """get the courses urls"""
    url = "https://udemy-course-scrapper-api.p.rapidapi.com/course-names/course-instructor/course-url"

    headers = {
        "X-RapidAPI-Key": creds.api_key,
        "X-RapidAPI-Host": creds.api_host
    }

    response = requests.get(url, headers=headers)

    urls_data = response.json()
    urls = []

    for data in urls_data.values():
        for url in data.values():
            urls.append(url)

    return urls


def get_instructors():
    """get the get the courses instructors"""
    url = "https://udemy-course-scrapper-api.p.rapidapi.com/course-names/course-instructor"

    headers = {
        "X-RapidAPI-Key": creds.api_key,
        "X-RapidAPI-Host": creds.api_host
    }
    response = requests.get(url, headers=headers)
    instructors_data = response.json()
    instructors = []

    for data in instructors_data.values():
        for instructor in data.values():
            instructors.append(instructor)

    return instructors


def get_titles():
    """get the courses titles"""
    url = "https://udemy-course-scrapper-api.p.rapidapi.com/course-names"

    headers = {
        "X-RapidAPI-Key": creds.api_key,
        "X-RapidAPI-Host": creds.api_host
    }

    response = requests.get(url, headers=headers)
    titles_data = response.json()
    titles = []

    for data in titles_data.values():
        for title in data.values():
            titles.append(title)

    return titles


def assemble_data():
    """"organise all courses details"""
    titles = get_titles()
    urls = get_urls()
    instructors = get_instructors()
    index = 0
    courses = []

    while index < len(titles):
        courses.append({"title": titles[index],
                          "URL": urls[index],
                          "instructor": instructors[index]
                        })
        index += 1

    return courses

#courses_data = assemble_data()
#print(courses_data)

#fetch the datas in the cloud databse
#with engine.connect() as conn:
#    for course in courses_data:
#        title = course["title"]
#        url = course["URL"]
#        instructor = course["instructor"]
#
#        query = text("INSERT INTO courses (title, url, instructor) VALUES (:title, :url, :instructor)")
#        result = conn.execute(query, {"title": title, "url": url, "instructor": instructor})
#        print("Insert successful!")
