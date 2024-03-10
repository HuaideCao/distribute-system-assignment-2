import xmlrpc.client

# Connecting to an XML-RPC server
server_url = "http://localhost:8000/"
proxy = xmlrpc.client.ServerProxy(server_url)

def add_note():
    topic = input("Enter the topic: ")
    text = input("Enter the text of the note: ")
    timestamp = input("Enter the timestamp (YYYY-MM-DD HH:MM:SS): ")
    result = proxy.add_or_update_note(topic, text, timestamp)
    if result:
        print("Note added/updated successfully.")
    else:
        print("Failed to add/update the note.")

def get_notes():
    topic = input("Enter the topic to get notes for: ")
    notes = proxy.get_notes_by_topic(topic)
    if notes:
        print("\nNotes for topic '{}':".format(topic))
        for note in notes:
            print(note)
    else:
        print("No notes found for this topic.")

def search_wiki():
    topic = input("Enter the topic to search on Wikipedia: ")
    link = proxy.search_wikipedia(topic)
    print("Wikipedia link: ", link)

def main():
    while True:
        print("\nAvailable actions:")
        print("1. Add or update a note")
        print("2. Get notes by topic")
        print("3. Search Wikipedia")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_note()
        elif choice == "2":
            get_notes()
        elif choice == "3":
            search_wiki()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
