
from app.flight.server import make_server

def main():
    server = make_server()
    print("Starting Arrow Flight on", server.location)
    server.serve()

if __name__ == "__main__":
    main()
