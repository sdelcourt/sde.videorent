# -*- coding: utf-8 -*-

TEST_USER_NAME = 'manager'
TEST_USER_PASSWORD = 'manager'

test_user = {
    'email': 'manager@viderorent.be',
    'username': TEST_USER_NAME,
    'password': TEST_USER_PASSWORD,
    'roles': ('Member', 'Reader'),
}

customers = [
    {
        'id': 'andre',
        'name': 'Sanfrapper',
        'firstname': 'André',
        'bonus_points': 0,
        'city': 'Namur'
    },
    {
        'id': 'gerard',
        'name': 'Mansoif',
        'firstname': 'Gérard',
        'bonus_points': 10,
        'city': 'Liège'
    },
]

films = [
    {
        'id': 'matrix_11',
        'title': 'MATRIX 11',
        'description': 'Neo is back once again to see if the spoon is really real!',
        'release_type': 'new'
    },
    {
        'id': 'spiderman',
        'title': 'Spiderman',
        'description': 'About how getting bitten by a spider can lead to great responsabilities',
        'release_type': 'regular'
    },
    {
        'id': 'spiderman_2',
        'title': 'Spiderman 2: homecoming',
        'description': 'About how getting bitten by a spider can lead to event greater responsabilities!',
        'release_type': 'regular'
    },
    {
        'id': 'out_of_africa',
        'title': 'Out of Africa',
        'description': 'Some epic romatic drama film.. in africa',
        'release_type': 'old'
    },
]

copies = [
    {
        'id': 'c1',
        'film_id': 'matrix_11',
        'copy_reference': 'SF0045',
        'physical_support': 'HD_DVD',
    },
    {
        'id': 'c2',
        'film_id': 'matrix_11',
        'copy_reference': 'SF0046',
        'physical_support': 'blueray',
    },
    {
        'id': 'c3',
        'film_id': 'spiderman',
        'copy_reference': 'MVL0096',
        'physical_support': 'DVD',
    },
    {
        'id': 'c4',
        'film_id': 'spiderman_2',
        'copy_reference': 'MVL0115',
        'physical_support': 'DVD',
    },
    {
        'id': 'c5',
        'film_id': 'out_of_africa',
        'copy_reference': 'CLS0989',
        'physical_support': 'DVD',
    },
    {
        'id': 'c6',
        'film_id': 'out_of_africa',
        'copy_reference': 'CLS0996',
        'physical_support': 'VHS',
    },
]

rentals = [
    {
        'id': 'rental',
        'customer_id': 'andre',
        'rented': [
            {'copy_id': 'c1', 'duration': 1, 'returned': False},
            {'copy_id': 'c3', 'duration': 5, 'returned': False},
            {'copy_id': 'c4', 'duration': 2, 'returned': False},
            {'copy_id': 'c5', 'duration': 7, 'returned': False},
        ],
    }
]
