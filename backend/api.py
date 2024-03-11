import requests
import sqlite3


class SimplifiedEvent:
    def __init__(self, name, date, time, city, country, venue_name):
        self.name = name
        self.date = date
        self.time = time
        self.city = city
        self.country = country
        self.venue_name = venue_name

    def _insert_sql_formatted(self):
        sql = f"""
            INSERT INTO events (name, date, time, city, country, venue_name)
            VALUES ('{self.name}', '{self.date}', '{self.time}', '{self.city}', '{self.country}', '{self.venue_name}')
        """
        return sql


#
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


def simplify_event_data(event) -> SimplifiedEvent:
    event = SimplifiedEvent(
        name=event["name"],
        date=event["dates"]["start"]["localDate"],
        time=event["dates"]["start"]["localTime"],
        city=event["_embedded"]["venues"][0]["city"]["name"],
        country=event["_embedded"]["venues"][0]["country"]["name"],
        venue_name=event["_embedded"]["venues"][0]["name"],
    )
    return event


def make_api_call(api_key):
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey={api_key}&size={10}&pages={1}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            simplified_events = [
                simplify_event_data(event) for event in data["_embedded"]["events"]
            ]
            return simplified_events
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def insert_into_db(event: SimplifiedEvent = None):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    print(f"Inserting {event.name} into table: events...")

    cursor.execute(
        """
        INSERT INTO events (name, date, time, city, country, venue_name)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            event.name,
            event.date,
            event.time,
            event.city,
            event.country,
            event.venue_name,
        ),
    )

    conn.commit()
    conn.close()
    print(f"\tSUCCESS: {event.name} now in database")


def main():
    api_key = "a7ZZ3PEKgvGkg54s5nr6j6qKg9QdVcvW"

    simplified_data = make_api_call(api_key)
    for event in simplified_data:
        insert_into_db(event)


if __name__ == "__main__":
    main()
