#!/usr/bin/python3
"""The console"""
import cmd
import fetch_api_db
import functionalties
#from datetime import datetime
#import shlex  # for splitting the line along spaces except in double quotes

courses_list = fetch_api_db.assemble_data()
titles = fetch_api_db.get_titles()

courses_dict = {course['title']: course for course in courses_list}
saved_courses = []

class ConnectToCourse(cmd.Cmd):
    """ ConnectToCourse console """
    prompt = '(cTc) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def do_quit(self, arg):
        """Quit command to exit the program """
        return True

    def do_show(self, arg):
        """ print 10 random courses """
        courses = functionalties.generate_courses(courses_list)
        for course in courses:
            print(course)

    def do_search(self, arg):
        """ print all courses realated to search arg """
        search_titles = functionalties.search_courses(titles, arg)
        courses = [courses_dict[title] for title in search_titles if title in courses_dict.keys()]

        for course in courses:
            print(course)

    def do_save(self, arg):
        """ return all the save(Bookmark) courses """
        if arg in courses_dict.keys():
            courses = [course for course in
                                 functionalties.save_course(courses_dict[arg])]
            for course in courses:
                saved_courses.append(course)
        print("Course added to Bookmark Successfully")


    def do_print_saves(self, arg):
        """ print saved courses """
        print(saved_courses)


if __name__ == '__main__':
    ConnectToCourse().cmdloop()
