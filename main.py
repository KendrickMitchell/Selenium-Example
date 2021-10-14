# Forum post extractor.
# The purpose of this script is to extract posts from a GITP forum thread and store them in a file.
# Forum threads are a sequence of posts. Posts are objects with a poster name, time of posting and revisions,
# and text which may enclose hidden text inside "spoiler" sub forms. Threads are organized in segments of 30 posts each.

# Steps.
# 1 Go to specified thread url.
# 2 For all thread segments
# 3  For all posts in a segment
# 4   Harvest the username, time, and text from the post. Then save the trio in a file in csv format.
# 5 Close the internet browser window controlled by the webdriver in this script.
#
import time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    Edge(executable_path="MicrosoftWebDriver.exe")
    # MS Edge web Browser and executable in project on local machine must be version 93
    driver = Edge()

    URL = input("Welcome to GITP thread harvester put in the URL of the thread you want to harvest")
    # print(URL)  # Add in later
    driver.get("URL")
    time.sleep(2)

    thread_title = driver.find_element_by_class_name("threadtitle")
    print(thread_title.text)

    Thread_progress = driver.find_element(By.ID, "postpagestats_above")
    print(Thread_progress.text)  # To see if we are at the last page in the thread.

    f = open("Thread.txt", "w", encoding="utf-8")
    f.write(thread_title.text)

    not_at_end_of_thread = True
    pages_passed = 0
    while not_at_end_of_thread:

        # now to click all the spoilers buttons if there are any.

        # now to gather all names, dates, and post contents.
        # Dates and contents are separate. But are they in parralel lists?
        dates = driver.find_elements_by_class_name("date")
        names = driver.find_elements_by_class_name("username_container")
        text_blocks = driver.find_elements_by_class_name("postbody")
        spoiler_buttons = driver.find_elements_by_class_name("spoiler-button")

        for spoiler_button in spoiler_buttons:
            spoiler_button.click()
            time.sleep(.1)

        if len(names) != len(dates) != len(text_blocks):
            print("Error. name count !=  date count != text blocks")
            break

        for index in range(0, len(dates)):  # Print out pairs of names and dates associated with individual posts
            print(index, dates[index].text, names[index].text)  # text_blocks[index].text)
            f.write(str(index + pages_passed*30) + dates[index].text + "," + names[index].text + text_blocks[index].text + "\n")

        Thread_progress = driver.find_element(By.ID, "postpagestats_above")
        print(Thread_progress.text)  # To see if we are at the last page in the thread.

        if Thread_progress.text.split()[3] == Thread_progress.text.split()[5]:  # Results x-29 to x of Posts_in_thread
            not_at_end_of_thread = False
        else:
            next_buttons = driver.find_elements_by_class_name("prev_next")  # Click on the > button to go to the next page.
            # Apparently the < prev page and > next page buttons use the same class names. But description text differs.
            # The < and > buttons occur on pages that are not the first or last in the thread.
            if len(next_buttons == 2):
                next_buttons[1].click()

            if len(next_buttons == 1):
                next_buttons[0].click()

            time.sleep(1)
    f.close()
    print("We traversed the thread!")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Harvesting text boxes immediately will only yield the text not in spoiler boxes, no images and likely no URLs.
