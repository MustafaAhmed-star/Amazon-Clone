import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


import random
from faker import Faker
from products.models import Product,Brand

fake = Faker()


def seed_brand(n):
    
    images = ['01.jpg','02.jpg','03.jpg','04.jpg','05.jpg','06.jpg','07.jpg','08.jpg','09.jpg','10.jpg']
    for _ in range(n):
        Brand.objects.create(
            name = fake.name(),
            image = f"brand/{images[random.randint(0,9)-1]}",
            
        )
    print(f"{n} brands added sucssesfuly")

def seed_products(n):
    
    flag_types = ['New','Sale','Feature']
    brands = Brand.objects.all()
    images = ['01.jpg','02.jpg','03.jpg','04.jpg','05.jpg','06.jpg','07.jpg','08.jpg','09.jpg','10.jpg']    
    for _ in range(n):
        Product.objects.create(
            name = fake.name(),
            flag = flag_types[random.randint(0,2)],
            price = round(random.uniform(20.99,99.99),2),
            image = f"product/{images[random.randint(0,9)-1]}",
            sku = random.randint(100,1000000),
            subtitle = fake.text(max_nb_chars= 350),
            description = fake.text(max_nb_chars= 4000),
            brand = brands[random.randint(0,len(brands)-1)],
        ) 
    print(f"{n} products added sucssesfuly num of products in database are {Product.objects.all().count()}" )    



def seed_reviews(n):
    pass


seed_brand(200)
seed_products(500)