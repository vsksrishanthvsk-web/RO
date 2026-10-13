from decimal import Decimal
from django.core.management.base import BaseCommand
from menu.models import Category, MenuItem


class Command(BaseCommand):
    help = 'Seeds initial categories and menu items for Rasoi Restaurant'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Rasoi restaurant menu data...")

        # Categories
        categories_data = [
            {'name': 'Starters', 'slug': 'starters', 'description': 'Tandoori delicacies and crisp bites', 'display_order': 1},
            {'name': 'Mains', 'slug': 'mains', 'description': 'Rich curries and slow-cooked gravies', 'display_order': 2},
            {'name': 'Biryani & Rice', 'slug': 'rice', 'description': 'Aromatic dum-cooked basmati specials', 'display_order': 3},
            {'name': 'Breads', 'slug': 'breads', 'description': 'Freshly baked tandoori rotis and naans', 'display_order': 4},
            {'name': 'Desserts', 'slug': 'desserts', 'description': 'Traditional sweets and chilled delights', 'display_order': 5},
            {'name': 'Drinks', 'slug': 'drinks', 'description': 'Refreshing coolers and artisanal lassis', 'display_order': 6},
        ]

        cat_objs = {}
        for c in categories_data:
            obj, _ = Category.objects.update_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'description': c['description'], 'display_order': c['display_order']}
            )
            cat_objs[c['slug']] = obj

        # Menu Items
        dishes = [
            # Starters
            {
                'category': cat_objs['starters'],
                'name': 'Paneer Tikka Charcoal',
                'slug': 'paneer-tikka-charcoal',
                'description': 'Cottage cheese cubes marinated in spiced yogurt, infused with ajwain and grilled in charcoal tandoor.',
                'price': Decimal('320.00'),
                'image_url': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': True,
                'prep_time_minutes': 15,
            },
            {
                'category': cat_objs['starters'],
                'name': 'Dahi Ke Kebab',
                'slug': 'dahi-ke-kebab',
                'description': 'Silken hung yogurt patties spiced with cardamom, green chilies and fresh coriander, shallow fried to golden perfection.',
                'price': Decimal('290.00'),
                'image_url': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': False,
                'prep_time_minutes': 12,
            },
            {
                'category': cat_objs['starters'],
                'name': 'Murgh Malai Tikka',
                'slug': 'murgh-malai-tikka',
                'description': 'Tender chicken morsels soaked in cashew cream, cheese, and aromatic spices grilled to melt-in-mouth texture.',
                'price': Decimal('380.00'),
                'image_url': 'https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?auto=format&fit=crop&w=800&q=80',
                'is_veg': False,
                'is_spicy': False,
                'is_featured': True,
                'prep_time_minutes': 18,
            },
            # Mains
            {
                'category': cat_objs['mains'],
                'name': 'Old Delhi Butter Chicken',
                'slug': 'old-delhi-butter-chicken',
                'description': 'Tandoor-charred chicken simmered in rich velvety tomato makhani, scented with fenugreek and hand-churned butter.',
                'price': Decimal('440.00'),
                'image_url': 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80',
                'is_veg': False,
                'is_spicy': False,
                'is_featured': True,
                'prep_time_minutes': 20,
            },
            {
                'category': cat_objs['mains'],
                'name': 'Dal Rasoi Signature',
                'slug': 'dal-rasoi-signature',
                'description': 'Black lentils simmered overnight over slow charcoal flame with ripe tomatoes, white butter and secret Rasoi masala.',
                'price': Decimal('340.00'),
                'image_url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': True,
                'prep_time_minutes': 15,
            },
            {
                'category': cat_objs['mains'],
                'name': 'Paneer Lababdar',
                'slug': 'paneer-lababdar',
                'description': 'Soft malai paneer cubes gently cooked in luscious onion-tomato gravy with grated paneer and freshly pounded spices.',
                'price': Decimal('360.00'),
                'image_url': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': True,
                'is_featured': False,
                'prep_time_minutes': 16,
            },
            {
                'category': cat_objs['mains'],
                'name': 'Kashmiri Rogan Josh',
                'slug': 'kashmiri-rogan-josh',
                'description': 'Slow-braised tender lamb shank flavored with Kashmiri red chillies, ratan jot, dry ginger and royal whole spices.',
                'price': Decimal('520.00'),
                'image_url': 'https://images.unsplash.com/photo-1545247181-516773cae754?auto=format&fit=crop&w=800&q=80',
                'is_veg': False,
                'is_spicy': True,
                'is_featured': True,
                'prep_time_minutes': 25,
            },
            # Biryani & Rice
            {
                'category': cat_objs['rice'],
                'name': 'Awadhi Dum Murgh Biryani',
                'slug': 'awadhi-dum-murgh-biryani',
                'description': 'Fragrant aged long-grain basmati rice and marinated chicken slow dum-cooked with saffron, rose water, and kewra.',
                'price': Decimal('420.00'),
                'image_url': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80',
                'is_veg': False,
                'is_spicy': True,
                'is_featured': True,
                'prep_time_minutes': 20,
            },
            {
                'category': cat_objs['rice'],
                'name': 'Nawabi Subz Biryani',
                'slug': 'nawabi-subz-biryani',
                'description': 'Layered garden vegetables and basmati infused with saffron milk, caramelized shallots and roasted dry fruits.',
                'price': Decimal('330.00'),
                'image_url': 'https://images.unsplash.com/photo-1642821373181-696a54913e9a?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': False,
                'prep_time_minutes': 18,
            },
            # Breads
            {
                'category': cat_objs['breads'],
                'name': 'Smoked Garlic Butter Naan',
                'slug': 'smoked-garlic-butter-naan',
                'description': 'Clay oven baked fluffy refined flour bread tossed with minced burnt garlic, fresh cilantro and clarified butter.',
                'price': Decimal('85.00'),
                'image_url': 'https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': False,
                'prep_time_minutes': 8,
            },
            {
                'category': cat_objs['breads'],
                'name': 'Chur Chur Laccha Paratha',
                'slug': 'chur-chur-laccha-paratha',
                'description': 'Multi-layered flaky whole wheat bread crushed with butter, mint flakes and chaat masala.',
                'price': Decimal('95.00'),
                'image_url': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': False,
                'prep_time_minutes': 8,
            },
            # Desserts
            {
                'category': cat_objs['desserts'],
                'name': 'Royal Saffron Gulab Jamun',
                'slug': 'royal-saffron-gulab-jamun',
                'description': 'Warm golden khoya dumplings soaked in green cardamom and saffron sugar syrup, topped with slivered pistachios.',
                'price': Decimal('160.00'),
                'image_url': 'https://images.unsplash.com/photo-1541832676-9b763b0239ab?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': True,
                'prep_time_minutes': 5,
            },
            {
                'category': cat_objs['desserts'],
                'name': 'Kesar Pista Rasmalai',
                'slug': 'kesar-pista-rasmalai',
                'description': 'Delicate cottage cheese patties poached in sweetened thick saffron milk scented with cardamom and rose.',
                'price': Decimal('190.00'),
                'image_url': 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': False,
                'prep_time_minutes': 5,
            },
            # Drinks
            {
                'category': cat_objs['drinks'],
                'name': 'Alphonso Mango Lassi',
                'slug': 'alphonso-mango-lassi',
                'description': 'Traditional churned sweet yogurt blended with authentic Ratnagiri Alphonso mango pulp and saffron.',
                'price': Decimal('150.00'),
                'image_url': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': True,
                'prep_time_minutes': 5,
            },
            {
                'category': cat_objs['drinks'],
                'name': 'Kullad Masala Chai',
                'slug': 'kullad-masala-chai',
                'description': 'Slow-brewed Assam CTC black tea with fresh ginger, crushed cardamom and cloves served in earthen clay cup.',
                'price': Decimal('90.00'),
                'image_url': 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=800&q=80',
                'is_veg': True,
                'is_spicy': False,
                'is_featured': False,
                'prep_time_minutes': 6,
            },
        ]

        for d in dishes:
            MenuItem.objects.update_or_create(
                slug=d['slug'],
                defaults=d
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(categories_data)} categories and {len(dishes)} menu items!"))
