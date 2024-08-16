import os
import django
import random
from faker import Faker
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DASH_connect.settings')
django.setup()

from accounts.models import CustomUser, AdminProfile, StudentProfile, VisitReason
from DASH_pillars.models import BasicNeedSupport, Hardship, Scholarship

faker = Faker()

def create_fake_users(n):
    for _ in range(n):
        user_type = random.choice(['student', 'admin'])

        # Generate NUID - a random unique 8-character string
        nuid = ''.join(random.choices('0123456789', k=8))

        # Generate other user details
        first_name = faker.first_name()
        middle_name = faker.first_name() if random.choice([True, False]) else None
        last_name = faker.last_name()
        email = faker.email()

        # Set password based on user type
        raw_password = 'student' if user_type == 'student' else 'admin'

        # Create the CustomUser instance
        user = CustomUser.objects.create(
            NUID=nuid,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            user_type=user_type,
            date_joined=timezone.now(),
            is_active=True
        )

        # Set the password using Django's set_password method
        user.set_password(raw_password)
        user.save()

        if user_type == 'admin':
            AdminProfile.objects.create(
                user=user,
                role_within_DASH=faker.job(),
                edits_made=faker.text()
            )
        elif user_type == 'student':
            # Create the StudentProfile
            student_profile = StudentProfile.objects.create(
                user=user,
                year=random.choice(['Freshman', 'Sophomore', 'Junior', 'Senior']),
                other_year=faker.text()[:100] if random.choice([True, False]) else None,
                DASH_Member=random.choice([True, False]),
                date_added=timezone.now()
            )

            # Randomly assign hardships, basic needs supports, and scholarships
            hardships = Hardship.objects.all()
            basic_needs_supports = BasicNeedSupport.objects.all()
            scholarships = Scholarship.objects.all()

            if hardships.exists():
                selected_hardships = random.sample(list(hardships), random.randint(1, min(3, hardships.count())))
                student_profile.hardships.add(*selected_hardships)

            if basic_needs_supports.exists():
                selected_supports = random.sample(list(basic_needs_supports), random.randint(1, min(3, basic_needs_supports.count())))
                student_profile.basic_need_supports.add(*selected_supports)

            if scholarships.exists():
                selected_scholarships = random.sample(list(scholarships), random.randint(1, min(3, scholarships.count())))
                student_profile.scholarships.add(*selected_scholarships)

            # Create VisitReasons associated with this student
            for _ in range(random.randint(1, 5)):  # Create 1 to 5 visit reasons
                VisitReason.objects.create(
                    student=student_profile,
                    appointment=random.choice([True, False]),
                    printing=random.choice([True, False]),
                    study=random.choice([True, False]),
                    socialize=random.choice([True, False]),
                    event=random.choice([True, False]),
                    schedule_appointment=random.choice([True, False]),
                    hardship=random.choice([True, False]),
                    basic_needs_support=random.choice([True, False]),
                    financial_wellness=random.choice([True, False]),
                    volunteer_opportunities=random.choice([True, False]),
                    date_time=timezone.now()
                )

        print(f'Created {user_type} user: {first_name} {last_name} (NUID: {nuid}) with password {raw_password}')

if __name__ == '__main__':
    import sys
    try:
        num_users = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Please provide the number of users to generate as a command-line argument.")
        sys.exit(1)

    create_fake_users(num_users)