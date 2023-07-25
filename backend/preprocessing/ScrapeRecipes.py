from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
import time

def recipe_images():
    # Function to scrape image url of the recipes.
    service = Service(
        executable_path='C:/Users/sureshv/Downloads/chromedriver_win32')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(
            'https://www.myplate.gov/myplate-kitchen/recipes?items_per_page=100&sort_bef_combine=title_ASC')
    time.sleep(3)

    image_results = driver.find_elements(By.XPATH, "//img[contains(@class,'image-style-medium')]")
    food_results = driver.find_elements(By.XPATH, ".//span[@class = 'field field--name-title field--type-string field--label-hidden']")

    image_source = []
    food_titles = []

    for image in image_results:
        image_source.append(image.get_attribute('src'))
    for name in food_results:
        food_titles.append(name.text)   

    try:
        pages = driver.find_element(
            By.CLASS_NAME, 'pager').find_elements(By.TAG_NAME, 'li')
        for page in range(1, len(pages)+1):
            print(f'In page: {page}')
            try:
                driver.find_element(
                    By.XPATH, '//*[@id="block-myplate-content"]/div/div/nav/ul/li[' + str(page) + ']/a').click()
                time.sleep(5)
            except NoSuchElementException:
                print('No more pages to load!')
                continue

    except NoSuchElementException:
            print('No next page exists.')


def navigate():
    service = Service(
        executable_path='C:/Users/sureshv/Downloads/chromedriver_win32')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    temp_list = []
    course_types = {
        'course-116': 'Appetizers',
        'course-117': 'Beverages',
        'course-118': 'Breads',
        'course-119': 'Breakfast',
        'course-120': 'Desserts',
        'course-121': 'Main',
        'course-122': 'Salads',
        'course-126': 'Sandwiches',
        'course-123': 'Dressings',
        'course-124': 'Sides',
        'course-125': 'Snacks',
        'course-127': 'Soups'
    }

    for key in course_types:
        print(f'Course key: {key}')
        print(f'Course value: {course_types[key]}')
        course_type_value = course_types[key]
        recipe_links = []
        driver.get(
            'https://www.myplate.gov/myplate-kitchen/recipes?items_per_page=100&sort_bef_combine=title_ASC')

        # Find the 'course' element
        course_dropdown = driver.find_element(
            By.XPATH, '/html/body/div[2]/main/div/div/div/aside/div/div[2]/div/div[2]/div/div/div[1]/button')
        course_dropdown.click()

        # Select by each course - checkbox
        course_checkbox = driver.find_element(By.ID, key)
        course_checkbox.click()

        time.sleep(10)

        # Select the recipes, navigate to next page (if there exists)
        # Check if next page exists
        try:
            pages = driver.find_element(
                By.CLASS_NAME, 'pager').find_elements(By.TAG_NAME, 'li')
            for page in range(1, len(pages)+1):
                print(f'In page: {page}')
                # Wait and Navigate to next pages (if exists)
                try:
                    driver.find_element(
                        By.XPATH, '//*[@id="block-myplate-content"]/div/div/nav/ul/li[' + str(page) + ']/a').click()
                    time.sleep(5)
                except NoSuchElementException:
                    print('No more pages to load!')
                    continue

                recipe_rows = driver.find_element(
                    By.CLASS_NAME, 'view-content').find_elements(By.CLASS_NAME, 'views-row')

                for recipe in recipe_rows:
                    recipe_links.append(recipe.find_element(By.CLASS_NAME, 'mp-recipe-teaser__main').find_element(
                        By.CLASS_NAME, 'mp-recipe-teaser__title').find_element(By.TAG_NAME, 'a').get_attribute("href"))

        except NoSuchElementException:
            print('No next page exists.')
            recipe_rows = driver.find_element(
                By.CLASS_NAME, 'view-content').find_elements(By.CLASS_NAME, 'views-row')

            for recipe in recipe_rows:
                recipe_links.append(recipe.find_element(By.CLASS_NAME, 'mp-recipe-teaser__main').find_element(
                    By.CLASS_NAME, 'mp-recipe-teaser__title').find_element(By.TAG_NAME, 'a').get_attribute("href"))

        print(f'Number of recipes: {len(recipe_links)}')

        # Visit each recipe link and scrape details
        for link in recipe_links:
            driver.get(link)
            time.sleep(3)

            # Fetch name of dish and serving size
            name = driver.find_element(
                By.XPATH, '/html/body/div[2]/main/div/div/div/div[2]/section/div/article/div[2]/div[1]/h1/span').text
            print(name)
            servings = driver.find_element(
                By.XPATH, '/html/body/div[2]/main/div/div/div/div[2]/section/div/article/div[3]/div[2]/div[1]/span[3]').text

            # Fetch list of ingredients
            ingredients_list = driver.find_element(
                By.XPATH, '/html/body/div[2]/main/div/div/div/div[2]/section/div/article/div[5]/div[1]/ul').find_elements(By.TAG_NAME, 'li')
            ingredients = []
            for ig in ingredients_list:
                ingredients.append(ig.text)

            # Fetch the directions
            directions = []
            try:
                directions_list = driver.find_element(
                    By.XPATH, '/html/body/div[2]/main/div/div/div/div[2]/section/div/article/div[5]/div[2]/div/ol').find_elements(By.TAG_NAME, 'li')
                for dr in directions_list:
                    directions.append(dr.text)
            except NoSuchElementException:
                directions_list = driver.find_element(
                    By.XPATH, '/html/body/div[2]/main/div/div/div/div[2]/section/div/article/div[5]/div[2]/div').find_elements(By.TAG_NAME, 'p')
                for dr in directions_list:
                    directions.append(dr.text)

            nutrition_information = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/div/div/div[2]/section/div/div[1]/div[1]/article/form').find_element(
                By.XPATH, '/html/body/div[2]/main/div/div/div/div[2]/section/div/div[1]/div[1]/article/form/label[1]/span')
            nutrition_information.click()
            time.sleep(5)

            rows = nutrition_information.find_elements(
                By.XPATH, '//*[@id="block-myplate-content"]/section/div/div[1]/div[1]/article/form/div[2]/table/tbody/tr')
            columns = nutrition_information.find_elements(
                By.XPATH, '//*[@id="block-myplate-content"]/section/div/div[1]/div[1]/article/form/div[2]/table/tbody/tr[1]/td')

            nutrients = {}
            # Traverse through nutrition table
            for i in range(1, len(rows) + 1):
                try:
                    key = driver.find_element(
                        By.XPATH, '//*[@id="block-myplate-content"]/section/div/div[1]/div[1]/article/form/div[2]/table/tbody/tr[' + str(i) + ']/td[' + str(1) + ']').text
                    value = driver.find_element(
                        By.XPATH, '//*[@id="block-myplate-content"]/section/div/div[1]/div[1]/article/form/div[2]/table/tbody/tr[' + str(i) + ']/td[' + str(2) + ']').text
                    nutrients[key] = value
                except NoSuchElementException:
                    pass

            row = {
                'name': name,
                'servings': servings,
                'ingredients': ingredients,
                'directions': directions,
                'type': course_type_value,
                'calories': nutrients.get('Total Calories'),
                'cholesterol': nutrients.get('Cholesterol'),
                'fat': nutrients.get('Total Fat'),
                'carbohydrates': nutrients.get('Carbohydrates'),
                'fiber': nutrients.get('Dietary Fiber'),
                'sugars': nutrients.get('Total Sugars'),
                'protein': nutrients.get('Protein'),
                'calcium': nutrients.get('Calcium'),
                'iron': nutrients.get('Iron'),
                'vitamin_a': nutrients.get('Vitamin A'),
                'vitamin_c': nutrients.get('Vitamin C'),
                'vitamin_d': nutrients.get('Vitamin D'),
                'folate': nutrients.get('Folate')
            }

            # Convert each row to dataframe
            temp_list.append(row)
            df = pd.DataFrame(temp_list)

        time.sleep(3)

        # write scrapped data onto csv
        # TODO: NEEd to add '\\preprocessing
        output_file_path = os.getcwd() + '\\datasets\\Food_recommender\\'
        df.to_csv(output_file_path + course_type_value + '.csv', index=False)
        print('Written successfully to csv')
    driver.quit()


if __name__ == "__main__":
    # navigate()
    recipe_images()
