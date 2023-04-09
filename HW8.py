# Your name: Meghan Levitt
# Your student id: 27761268
# Your email: mghnlvtt@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    data = {}
    conn = sqlite3.connect("{}".format(db))
    cur = conn.cursor()
    for restaurantdata in cur.execute('SELECT * FROM restaurants').fetchall():
        name = restaurantdata[1]
        category = cur.execute('SELECT Categories.category FROM Categories JOIN Restaurants WHERE Categories.id = {}'.format(restaurantdata[2])).fetchone()[0]
        building = cur.execute('SELECT Buildings.building FROM Buildings JOIN Restaurants WHERE Buildings.id = {}'.format(restaurantdata[3])).fetchone()[0]
        rating = restaurantdata[4]
        data[name] = {'category':category,'building':building,'rating':rating}
    return data
    pass

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect("{}".format(db))
    cur = conn.cursor() 
    data = dict(cur.execute('SELECT Categories.category, COUNT(Restaurants.category_id) FROM Categories JOIN Restaurants WHERE Categories.id = Restaurants.category_id GROUP BY category ORDER BY COUNT(Restaurants.category_id) ASC').fetchall())
    categories = list(data.keys())
    totals = list(data.values())
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.title("Types of Restaurants on South University Ave")
    plt.barh(range(len(data)), totals, tick_label = categories)
    plt.show()
    return data
    pass

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    lst = []
    conn = sqlite3.connect("{}".format(db))
    cur = conn.cursor()
    restinbuilding = cur.execute('SELECT Restaurants.name FROM Restaurants JOIN Buildings WHERE Buildings.id = Restaurants.building_id AND Buildings.building = {} ORDER BY Restaurants.rating DESC'.format(building_num)).fetchall()
    for restaurant in restinbuilding:
        lst.append(restaurant[0])
    return lst
    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect("{}".format(db))
    cur = conn.cursor()
    categories = cur.execute('SELECT Categories.category, ROUND(AVG(Restaurants.rating),1) FROM Categories JOIN Restaurants WHERE Categories.id = Restaurants.category_id GROUP BY category ORDER BY ROUND(AVG(Restaurants.rating),1) DESC').fetchall()
    buildings = cur.execute('SELECT Buildings.building, ROUND(AVG(Restaurants.rating),1) FROM Buildings JOIN Restaurants WHERE Buildings.id = Restaurants.building_id GROUP BY building ORDER BY ROUND(AVG(Restaurants.rating),1) DESC').fetchall()
    highest = [categories[0],buildings[0]]
    plt.figure(figsize=(8,8))
    category = plt.subplot(211)
    building = plt.subplot(212)
    category.set(xlabel = 'Rating',ylabel = "Categories",title ="Average Restaurant Ratings by Category")
    building.set(xlabel = 'Rating',ylabel = "Buildings",title = "Average Restaurant Ratings by Building")
    cy = [x[0] for x in sorted(categories,key=lambda x: x[1])]
    cx = [x[1] for x in sorted(categories,key=lambda x: x[1])]
    by = [str(x[0]) for x in sorted(buildings,key=lambda x: x[1])]
    bx = [x[1] for x in sorted(buildings,key=lambda x: x[1])]
    category.set_xlim(0,5)
    building.set_xlim(0,5)
    category.barh(cy,cx)
    building.barh(by,bx)
    plt.show()
    return highest
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'South_U_Restaurants.db')
        self.cur = self.conn.cursor()
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
