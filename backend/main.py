from demodata_server.server import DemodataServer

if __name__ == "__main__":
    demodata_server = DemodataServer("0.0.0.0", 8080, "/demodata")
    demodata_server.demodata_input("./data/test_large.json")
    demodata_server.start_server()
