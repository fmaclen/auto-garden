import socket
from requests import get

def parse_request(request):
    headers = {}
    lines = request.split('\r\n')
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
    return headers

def main():
    addr = socket.getaddrinfo('0.0.0.0', 9999)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024).decode('utf-8')
        
        headers = parse_request(request)
        
        if 'OPTIONS' in request:
            # Handling preflight request
            response_headers = [
                "HTTP/1.1 204 No Content",
                "Access-Control-Allow-Origin: *",
                "Access-Control-Allow-Methods: POST, OPTIONS",
                "Access-Control-Allow-Headers: Authorization, Content-Type, Pot-Id",
                "Access-Control-Max-Age: 3600"  # Cache preflight response for 1 hour
            ]
            response = "\r\n".join(response_headers) + "\r\n\r\n"
            cl.send(response.encode('utf-8'))
            
        elif 'POST' in request:
            if 'Authorization' in headers and 'Pot-Id' in headers and is_valid_jwt(headers['Authorization']):
                response_headers = [
                    f"HTTP/1.1 200 OK",
                    "Content-Type: application/json",
                    "Access-Control-Allow-Origin: *"  # Required for CORS
                ]
                response = "\r\n".join(response_headers)
                
                cl.send(response.encode('utf-8'))
            else:
                cl.send('HTTP/1.1 400 Bad Request\r\n\r\n'.encode('utf-8'))
        else:
            cl.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode('utf-8'))
        
        cl.close()


def is_valid_jwt(jwt: str) -> bool:
    headers = {
        "Content-Type": "application/json",
        "Authorization": jwt # e.g. `Bearer aaaa.bbbb.cccc`
    }

    url = "http://127.0.0.1:8090/api/settings"
    response = get(url, headers=headers)

    return response.status_code == 200


if __name__ == "__main__":
    main()
