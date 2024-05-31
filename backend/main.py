import mysql.connector
from mysql.connector import Error
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
import traceback
from datetime import date

class TodoHandler(BaseHTTPRequestHandler):
    def _set_response(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_response()

    def default(self, o):
        if isinstance(o, (date)):
            return o.isoformat()
        raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

    def do_GET(self):
        print("Handling GET request")
        try:
            connection = mysql.connector.connect(
                host='db',  # Utiliser le nom du service Docker
                user='root',
                password='root',
                database='todo_db'
            )
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM todos")
            rows = cursor.fetchall()
            cursor.close()
            connection.close()

            self._set_response()
            self.wfile.write(json.dumps(rows, default=self.default).encode('utf-8'))
        except Error as e:
            print(f"Error handling GET request: {e}")
            traceback.print_exc()
            self._set_response(500)
            self.wfile.write(json.dumps({'message': 'Internal Server Error'}).encode('utf-8'))

    def do_POST(self):
        print("Handling POST request")
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            todo = json.loads(post_data.decode('utf-8'))
            print(f"Received data: {todo}")

            connection = mysql.connector.connect(
                host='db',  # Utiliser le nom du service Docker
                user='root',
                password='root',
                database='todo_db'
            )
            cursor = connection.cursor()
            cursor.execute("INSERT INTO todos (content, due_date) VALUES (%s, %s)", (todo['content'], todo.get('due_date')))
            connection.commit()
            cursor.close()
            connection.close()

            self._set_response()
            self.wfile.write(json.dumps({'message': 'Todo added'}).encode('utf-8'))
        except Error as e:
            print(f"Error handling POST request: {e}")
            traceback.print_exc()
            self._set_response(500)
            self.wfile.write(json.dumps({'message': 'Internal Server Error'}).encode('utf-8'))

    def do_PUT(self):
        print("Handling PUT request")
        try:
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            todo = json.loads(put_data.decode('utf-8'))
            print(f"Received data: {todo}")

            connection = mysql.connector.connect(
                host='db',  # Utiliser le nom du service Docker
                user='root',
                password='root',
                database='todo_db'
            )
            cursor = connection.cursor()
            if 'content' in todo and 'due_date' in todo:
                cursor.execute("UPDATE todos SET content=%s, due_date=%s, completed=%s WHERE id=%s", 
                               (todo['content'], todo['due_date'], todo['completed'], todo['id']))
            else:
                cursor.execute("UPDATE todos SET completed=%s WHERE id=%s", 
                               (todo['completed'], todo['id']))

            connection.commit()
            cursor.close()
            connection.close()

            self._set_response()
            self.wfile.write(json.dumps({'message': 'Todo updated'}).encode('utf-8'))
        except Error as e:
            print(f"Error handling PUT request: {e}")
            traceback.print_exc()
            self._set_response(500)
            self.wfile.write(json.dumps({'message': 'Internal Server Error'}).encode('utf-8'))

    def do_DELETE(self):
        print("Handling DELETE request")
        try:
            parsed_path = urlparse(self.path)
            todo_id = parse_qs(parsed_path.query).get('id', None)
            print(f"Received ID: {todo_id}")

            if todo_id:
                connection = mysql.connector.connect(
                    host='db',  # Utiliser le nom du service Docker
                    user='root',
                    password='root',
                    database='todo_db'
                )
                cursor = connection.cursor()
                cursor.execute("DELETE FROM todos WHERE id=%s", (todo_id[0],))
                connection.commit()
                cursor.close()
                connection.close()

                self._set_response()
                self.wfile.write(json.dumps({'message': 'Todo deleted'}).encode('utf-8'))
            else:
                print("Invalid todo ID")
                self._set_response(400)
                self.wfile.write(json.dumps({'message': 'Invalid todo ID'}).encode('utf-8'))
        except Error as e:
            print(f"Error handling DELETE request: {e}")
            traceback.print_exc()
            self._set_response(500)
            self.wfile.write(json.dumps({'message': 'Internal Server Error'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=TodoHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
