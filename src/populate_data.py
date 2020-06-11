import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'APR.settings')

import django
django.setup()

from accounts.models import User, Student
from lessons.models import Class
from faker import Faker

fakegen = Faker()
import random

def student(N):
    lis = ['M', "F"]    
    for _ in range(N):
        email=fakegen.email()
        user= User.objects.create_user(
            email=email, 
            password=email, 
            first_name=fakegen.first_name(),
            last_name=fakegen.last_name(),
            user_type='Student')
        user.save()

        stu = Student.objects.create(            
            user=user,
            gender=random.choice(lis),
            dob=fakegen.date_of_birth(),
            PAddress=fakegen.address(),
            PCity=fakegen.city(),
            PState=fakegen.state(),
            PDistrict=fakegen.city(),
            PPincode=random.randint(100000, 999999),
            CAddress=fakegen.address(),
            CCity=fakegen.city(),
            CState=fakegen.state(),
            CDistrict=fakegen.city(),
            CPincode=random.randint(100000, 999999),
            Contact=random.randint(1000000000, 99999999999),
            Class=Class.objects.get(id=1))
        stu.save()

if __name__ == "__main__":
    print('Populating data....')
    student(10)
    print('Done')