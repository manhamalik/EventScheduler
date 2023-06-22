from flask import Flask, render_template, request

app = Flask(__name__)

class Event:
    def __init__(self, date, time, location, description):
        self.date = date
        self.time = time
        self.location = location
        self.description = description

class Node:
    def __init__(self, event):
        self.event = event
        self.left = None
        self.right = None

class EventScheduler:
    def __init__(self):
        self.root = None

    def add_event(self, event):
        if self.root is None:
            self.root = Node(event)
        else:
            self._add_event_recursive(self.root, event)

    def _add_event_recursive(self, node, event):
        if event.date < node.event.date:
            if node.left is None:
                node.left = Node(event)
            else:
                self._add_event_recursive(node.left, event)
        else:
            if node.right is None:
                node.right = Node(event)
            else:
                self._add_event_recursive(node.right, event)

    def get_sorted_events(self):
        events = []
        self._inorder_traversal(self.root, events)
        return events

    def _inorder_traversal(self, node, events):
        if node is not None:
            self._inorder_traversal(node.left, events)
            events.append(node.event)
            self._inorder_traversal(node.right, events)

event_scheduler = EventScheduler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_event', methods=['POST'])
def add_event():
    date = request.form.get('date')
    time = request.form.get('time')
    location = request.form.get('location')
    description = request.form.get('description')

    event = Event(date, time, location, description)
    event_scheduler.add_event(event)

    events = event_scheduler.get_sorted_events()
    return render_template('index.html', events=events, message='Event added successfully')


@app.route('/view_events')
def view_events():
    events = event_scheduler.get_sorted_events()
    return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
