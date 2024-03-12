import requests
import sqlite3

class SimplifiedEvent:
    def __init__(self, name, category, date, time, city, state, country, venue_name, image_url):
        self.name = name
        self.category = category
        self.date = date
        self.time = time
        self.city = city
        self.state = state
        self.country = country
        self.venue_name = venue_name
        self.image_url = image_url

class TicketmasterService:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_events(self, classification_name, page=1, page_size=20):
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey={self.api_key}&size={page_size}&pages={page}&classificationName={classification_name}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get("_embedded", {}).get("events", [])
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def simplify_event_data(self, event, classification_name) -> SimplifiedEvent:
        return SimplifiedEvent(
            name=event["name"],
            category=classification_name,
            date=event["dates"]["start"]["localDate"],
            time=event["dates"]["start"]["localTime"],
            city=event["_embedded"]["venues"][0]["city"]["name"],
            state=event["_embedded"]["venues"][0]["state"]["name"],
            country=event["_embedded"]["venues"][0]["country"]["name"],
            venue_name=event["_embedded"]["venues"][0]["name"],
            image_url=event["images"][0]["url"] if event.get("images") else None,
        )

    def insert_into_db(self, event: SimplifiedEvent = None):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO events (name, category, date, time, city, state, country, venue_name, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.name,
                    event.category,
                    event.date,
                    event.time,
                    event.city,
                    event.state,
                    event.country,
                    event.venue_name,
                    event.image_url,
                ),
            )
            conn.commit()
            print(f"SUCCESS: {event.name} inserted into database")
        except sqlite3.Error as e:
            print(f"Failed to insert event into database: {e}")
        finally:
            conn.close()

def main():
    api_key = "a7ZZ3PEKgvGkg54s5nr6j6qKg9QdVcvW"
    service = TicketmasterService(api_key)
    categories = ["Sports", "Fashion", "Music"]
    
    for category in categories:
    
        simplified_data = service.fetch_events(category)
        for event in simplified_data:
            simplified_event = service.simplify_event_data(event, category)
            print(simplified_event.name)
            print(simplified_event.category)
            print(simplified_event.date)
            print(simplified_event.time)
            print(f"{simplified_event.city}, {simplified_event.state}")
            print(simplified_event.country)
            print(simplified_event.venue_name)
            print(simplified_event.image_url)
            print()
            service.insert_into_db(simplified_event)

if __name__ == "__main__":
    main()



# def _old_simplify_event_data(event):

#     simplified_event_dict = {
#         "name": event["name"],
#         "url": event["url"],
#         "date": event["dates"]["start"]["localDate"],
#         "time": event["dates"]["start"]["localTime"],
#         "venue": {
#             "name": event["_embedded"]["venues"][0]["name"],
#             "city": event["_embedded"]["venues"][0]["city"]["name"],
#             "state": event["_embedded"]["venues"][0]["state"]["name"],
#             "country": event["_embedded"]["venues"][0]["country"]["name"],
#         },
#         "image_url": event["images"][0]["url"] if event["images"] else None,
#     }
#     return simplified_event_dict

# def _insert_sql_formatted(self):
#     sql = f"""
#         INSERT INTO events (name, date, time, city, country, venue_name)
#         VALUES ('{self.name}', '{self.date}', '{self.time}', '{self.city}', '{self.country}', '{self.venue_name}')
#     """
#     return sql