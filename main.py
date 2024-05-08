import csv
from datetime import date
from getpass import getpass

class Trip:
    def __init__(self, trip_id, trip_name, destination, start_date, end_date, cost, trip_coordinator_id):
        self.trip_id = trip_id
        self.trip_name = trip_name
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.cost = float(cost)
        self.trip_coordinator_id = int(trip_coordinator_id)

class Booking:
    def __init__(self, booking_id, trip_id, trip_name, traveller_id, status='pending', payment_status='not_paid'):
        self.booking_id = booking_id
        self.trip_id = trip_id
        self.trip_name = trip_name
        self.traveller_id = int(traveller_id)
        self.status = status
        self.payment_status = payment_status
        self.total_amount = 0.0  # Initialize total_amount to 0 initially

class TripLeg:
    def __init__(self, leg_id, trip_id, leg_name, start_date, end_date, destination):
        self.leg_id = leg_id
        self.trip_id = trip_id
        self.leg_name = leg_name
        self.start_date = start_date
        self.end_date = end_date
        self.destination = destination

class User:
    def __init__(self, user_id, username, password, role, email, phone_number, staff_id=None):
        self.user_id = int(user_id)
        self.username = username
        self.password = password
        self.role = role
        self.email = email
        self.phone_number = phone_number
        self.staff_id = int(staff_id) if staff_id else None

class TravelSystem:
    def __init__(self):
        self.trips = []
        self.trip_legs = []
        self.users = []
        self.load_trips()
        self.load_users()

    def load_trips(self):
        try:
            with open('trips.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trip = Trip(**row)
                    self.trips.append(trip)
        except FileNotFoundError:
            print("Error: trips.csv file not found.")
        except csv.Error as e:
            print(f"CSV Error: Failed to load trips data - {e}")

    def load_users(self):
        try:
            with open('users.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Extract required fields from CSV
                    user_id = row['user_id']
                    username = row['username']
                    password = row['password']
                    role = row['role']
                    email = row['email']
                    phone_number = row['phone_number']
                    staff_id = row.get('staff_id')  # Optional field

                    # Create User instance and add to users list
                    user = User(user_id, username, password, role, email, phone_number, staff_id)
                    self.users.append(user)
        except FileNotFoundError:
            print("Error: users.csv file not found.")
        except csv.Error as e:
            print(f"CSV Error: Failed to load users data - {e}")

    def get_upcoming_trips(self):
        today_date = date.today()
        upcoming_trips = [(trip.trip_id, trip.trip_name, trip.destination, trip.start_date, trip.end_date)
                          for trip in self.trips if trip.start_date >= str(today_date)]
        return upcoming_trips

    def request_to_book_trip(self, traveller_id, trip_id):
        trip = next((trip for trip in self.trips if trip.trip_id == trip_id), None)
        if trip:
            booking_id = f'B{len(self.trips) + 1}'
            booking = Booking(booking_id, trip.trip_id, trip.trip_name, traveller_id)
            self.save_booking(booking)
            return booking
        else:
            print("Error: Trip ID not found.")
            return None

    def save_booking(self, booking):
        try:
            with open('bookings.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([booking.booking_id, booking.trip_id, booking.trip_name, booking.traveller_id,
                                 booking.status, booking.payment_status, booking.total_amount])
            print("Booking saved successfully!")
        except IOError as e:
            print(f"Error: Failed to save booking - {e}")

    def login(self, username, password):
        user = next((user for user in self.users if user.username == username and user.password == password), None)
        return user

    def create_trip(self):
        print("Enter trip details:")
        trip_id = input("Trip ID: ")
        trip_name = input("Trip Name: ")
        destination = input("Destination: ")
        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")
        cost = input("Cost: ")
        trip_coordinator_id = input("Trip Coordinator ID: ")

        new_trip = Trip(trip_id, trip_name, destination, start_date, end_date, cost, trip_coordinator_id)
        self.trips.append(new_trip)
        self.save_trips()

        print(f"Trip '{trip_name}' created successfully!")

    def save_trips(self):
        try:
            with open('trips.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['trip_id', 'trip_name', 'destination', 'start_date', 'end_date', 'cost', 'trip_coordinator_id'])
                for trip in self.trips:
                    writer.writerow([trip.trip_id, trip.trip_name, trip.destination, trip.start_date,
                                     trip.end_date, trip.cost, trip.trip_coordinator_id])
        except IOError as e:
            print(f"Error: Failed to save trips - {e}")

    def create_trip_leg(self):
        print("Enter trip leg details:")
        leg_id = input("Leg ID: ")
        trip_id = input("Trip ID: ")
        leg_name = input("Leg Name: ")
        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")
        destination = input("Destination: ")

        new_trip_leg = TripLeg(leg_id, trip_id, leg_name, start_date, end_date, destination)
        self.trip_legs.append(new_trip_leg)
        self.save_trip_legs()

        print(f"Trip Leg '{leg_name}' created successfully!")

    def save_trip_legs(self):
        try:
            with open('trip_legs.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['leg_id', 'trip_id', 'leg_name', 'start_date', 'end_date', 'destination'])
                for trip_leg in self.trip_legs:
                    writer.writerow([trip_leg.leg_id, trip_leg.trip_id, trip_leg.leg_name, trip_leg.start_date,
                                     trip_leg.end_date, trip_leg.destination])
        except IOError as e:
            print(f"Error: Failed to save trip legs - {e}")

def main():
    travel_system = TravelSystem()
    print("Welcome to the Travel Management System!")

    while True:
        print("\nMenu:")
        print("1. Check out upcoming trips")
        print("2. Request to book a trip")
        print("3. Staff login here")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            upcoming_trips = travel_system.get_upcoming_trips()
            if upcoming_trips:
                print("\nUpcoming Trips:")
                print("Trip ID | Trip Name | Destination | Start Date | End Date")
                for trip in upcoming_trips:
                    print(f"{trip[0]} | {trip[1]} | {trip[2]} | {trip[3]} | {trip[4]}")
            else:
                print("No upcoming trips.")

        elif choice == '2':
            traveller_id = input("Enter your traveller ID: ")
            trip_id = input("Enter the trip ID you want to book: ")
            booking = travel_system.request_to_book_trip(traveller_id, trip_id)
            if booking:
                print(f"Booking successful! Your booking ID is: {booking.booking_id}")

        elif choice == '3':
            username = input("Enter your username: ")
            password = getpass("Enter your password: ")
            user = travel_system.login(username, password)
            if user:
                print(f"Welcome, {user.username}! You have successfully logged in as {user.role}.")
                if user.role == 'trip_manager':
                    while True:
                        print("\nTrip Manager Actions:")
                        print("1. Manage passengers on trips")
                        print("2. Update trip legs")
                        print("3. Request payment for trip")
                        print("4. Generate receipts")
                        print("5. Create a new trip")
                        print("6. Create trip legs")
                        print("7. Exit")

                        manager_choice = input("Enter your choice (1/2/3/4/5/6/7): ")

                        if manager_choice == '5':
                            travel_system.create_trip()
                        elif manager_choice == '6':
                            travel_system.create_trip_leg()
                        elif manager_choice == '7':
                            break
                        else:
                            print("Invalid choice. Please try again.")

            else:
                print("Invalid username or password. Please try again.")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

