import csv
from datetime import date

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

class TravelSystem:
    def __init__(self):
        self.trips = []
        self.load_trips()

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

def main():
    travel_system = TravelSystem()
    print("Welcome to the Travel Management System!")

    while True:
        print("\nMenu:")
        print("1. Check out upcoming trips")
        print("2. Request to book a trip")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

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
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
