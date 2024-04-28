from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# Класс, обрабатывающий HTTP-запросы
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # Метод, вызываемый при получении GET-запроса
    def do_GET(self):
        try:
            # Получаем путь к запрашиваемому ресурсу
            path = self.path

            # Если путь оканчивается на '/', добавляем к нему 'index.html'
            if path.endswith('/'):
                path += 'index.html'

            # Получаем абсолютный путь к файлу в рабочей директории сервера
            file_path = os.path.abspath(os.getcwd() + path)

            # Проверяем, существует ли файл
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Открываем файл и считываем его содержимое
                with open(file_path, 'rb') as file:
                    content = file.read()

                # Отправляем успешный HTTP-ответ с содержимым файла
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content)
            else:
                # Если файл не найден, отправляем HTTP-ответ с ошибкой 404
                self.send_error(404, 'File Not Found: {}'.format(self.path))
        except Exception as e:
            # В случае возникновения ошибки, отправляем HTTP-ответ с ошибкой 500
            self.send_error(500, 'Internal Server Error: {}'.format(str(e)))

# Функция для запуска сервера
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=80):
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print('Starting server on port {}...'.format(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        # При нажатии Ctrl+C останавливаем сервер
        print('Server stopped.')
        httpd.server_close()

# Запускаем сервер
if __name__ == '__main__':
    run()
