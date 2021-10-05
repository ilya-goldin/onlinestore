from products.models import Product, Review, Collection, Order
from faker import Faker
from django.contrib.auth.models import User
import random

fake = Faker()
Faker.seed(0)
users = User.objects.all()

for _ in range(50):
    x = Product.objects.create(
        name=fake.word(),
        description=fake.text(),
        price=fake.pyint(min_value=0, max_value=700000),
    )

for _ in range(20):
    x = Review.objects.create(
        user=random.choice(users),
        product=random.choice(Product.objects.all()),
        review_text=fake.text(),
        score=fake.pyint(min_value=1, max_value=5),
    )

for _ in range(5):
    x = Collection.objects.create(
        title=fake.words(nb=3),
        note=fake.text(),
    )
    x.save()
    x.items.set(random.choices(Product.objects.all().values_list('id', flat=True), k=5))

for _ in range(10):
    x = Order.objects.create(
        user=random.choice(users),
        status=random.choice(['NEW', 'IN_PROGRESS', 'DONE']),
    )
    x.save()
