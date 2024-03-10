# Importing the necessary libraries
from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import requests
import xml.dom.minidom

def save_pretty_xml(xml_data, file_path):
    """
    Format and save XML data to a file in a pretty way.
    """
    xml_str = ET.tostring(xml_data, 'utf-8')
    pretty_xml_str = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="    ")
    with open(file_path, 'w') as xml_file:
        xml_file.write(pretty_xml_str)


# Setting the server address and port
server_address = ('localhost', 8000)

# Initialize XML database path
xml_db_path = '/Users/jackcao/Desktop/distribute/db (1).xml'

# Define functions that handle client requests
def add_or_update_note(topic, text, timestamp):
    try:
        # Loading XML files
        tree = ET.parse(xml_db_path)
        root = tree.getroot()
        
        # Find out if the same topic already exists
        topics = root.findall(f"./topic[@name='{topic}']")
        if topics:
            for topic_element in topics:
                new_note = ET.SubElement(topic_element, 'note')
                text_element = ET.SubElement(new_note, 'text')
                text_element.text = text
                timestamp_element = ET.SubElement(new_note, 'timestamp')
                timestamp_element.text = timestamp
        else:
            new_topic = ET.SubElement(root, 'topic', name=topic)
            new_note = ET.SubElement(new_topic, 'note')
            text_element = ET.SubElement(new_note, 'text')
            text_element.text = text
            timestamp_element = ET.SubElement(new_note, 'timestamp')
            timestamp_element.text = timestamp
        
        save_pretty_xml(root, xml_db_path)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False



def get_notes_by_topic(topic):
    try:
        tree = ET.parse(xml_db_path)
        root = tree.getroot()

        notes_content = []
        topics = root.findall(f"./topic[@name='{topic}']")
        for topic_element in topics:
            notes = topic_element.findall('note')
            for note in notes:
                # Check that the note element contains the text child element
                if note.find('text') is not None:
                    text_content = note.find('text').text
                else:
                    text_content = note.text  # Get the text content of the note directly
                notes_content.append(text_content)

        return notes_content
    except Exception as e:
        print(f"Error: {e}")
        return []
 
    
def add_wikipedia_link_to_note(topic, wikipedia_link):
    try:
        tree = ET.parse(xml_db_path)
        root = tree.getroot()
        
        # Find or create a topic
        topic_element = root.find(f"./topic[@name='{topic}']")
        if topic_element is None:
            topic_element = ET.SubElement(root, 'topic', name=topic)
        
        # Adding notes with Wikipedia links under topics
        new_note = ET.SubElement(topic_element, 'note', type='wikipedia')
        new_note.text = wikipedia_link
        
        # Saving XML Changes in a pretty way
        save_pretty_xml(root, xml_db_path)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

    
def search_wikipedia(topic):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "namespace": "0",
        "search": topic,
        "limit": "1",
        "format": "json"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parsing the returned data
        result = response.json()
        if result[3]:
            wikipedia_link = result[3][0]
            # Adding Wikipedia links to notes
            add_wikipedia_link_to_note(topic, wikipedia_link)
            return wikipedia_link
        else:
            return "No Wikipedia link found."
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Error querying Wikipedia."



# Registering a function makes it possible to call it remotely
server = SimpleXMLRPCServer(server_address, allow_none=True)
server.register_function(add_or_update_note, "add_or_update_note")
server.register_function(get_notes_by_topic, "get_notes_by_topic")
server.register_function(search_wikipedia, "search_wikipedia")

# Start the server
print("Server is running...")
server.serve_forever()
