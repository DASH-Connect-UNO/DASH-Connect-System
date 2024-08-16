import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'DASH_connect.settings')  # Replace 'your_project' with the correct settings module
django.setup()

from django.apps import apps

# Now import your models using apps.get_model
CustomUser = apps.get_model('accounts', 'CustomUser')
AdminProfile = apps.get_model('accounts', 'AdminProfile')
StudentProfile = apps.get_model('accounts', 'StudentProfile')
VisitReason = apps.get_model('accounts', 'VisitReason')


def delete_user_by_nuid(nuid):
    try:
        # Find the user by NUID
        user = CustomUser.objects.get(NUID=nuid)

        # Print user details for confirmation
        print(f"Found user: {user.first_name} {user.last_name} (NUID: {user.NUID})")

        # Delete associated profiles and data
        if user.user_type == 'admin':
            # Delete AdminProfile if it exists
            try:
                admin_profile = AdminProfile.objects.get(user=user)
                admin_profile.delete()
                print(f"Deleted AdminProfile for NUID: {nuid}")
            except AdminProfile.DoesNotExist:
                print(f"No AdminProfile found for NUID: {nuid}")

        elif user.user_type == 'student':
            # Delete VisitReasons related to the student
            visit_reasons = VisitReason.objects.filter(student__user=user)
            visit_reasons_count = visit_reasons.count()
            visit_reasons.delete()
            print(f"Deleted {visit_reasons_count} VisitReasons for NUID: {nuid}")

            # Delete StudentProfile if it exists
            try:
                student_profile = StudentProfile.objects.get(user=user)
                student_profile.delete()
                print(f"Deleted StudentProfile for NUID: {nuid}")
            except StudentProfile.DoesNotExist:
                print(f"No StudentProfile found for NUID: {nuid}")

        # Finally, delete the user
        user.delete()
        print(f"Deleted CustomUser with NUID: {nuid}")

    except CustomUser.DoesNotExist:
        print(f"No user found with NUID: {nuid}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python delete_user.py <NUID>")
        sys.exit(1)

    nuid = sys.argv[1]
    delete_user_by_nuid(nuid)