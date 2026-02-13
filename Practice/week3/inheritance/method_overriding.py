class User:
    def save(self):
        print("Saving data to database")

class Admin(User):
    def save(self):
        print("Logging admin action")
        super().save()

a = Admin()
a.save()