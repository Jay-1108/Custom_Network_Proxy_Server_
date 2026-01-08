class HTTPRequest:
    def __init__(self, method, url, version, headers, host, port, raw):
        self.method = method
        self.url = url
        self.version = version
        self.headers = headers
        self.host = host
        self.port = port
        self.raw = raw


class HTTPParser:
    def parse(self, raw_request):
        try:
            header_data = raw_request.split(b"\r\n\r\n")[0]
            headers = header_data.decode().split("\r\n")

            request_line = headers[0].split()
            method = request_line[0]
            url = request_line[1]
            version = request_line[2]

            header_dict = {}
            for h in headers[1:]:
                if ":" in h:
                    k, v = h.split(":", 1)
                    header_dict[k.strip()] = v.strip()

            # Extract host & port
            host = ""
            port = 80

            if method == "CONNECT":
                host_port = url.split(":")
                host = host_port[0]
                port = host_port[1]
            else:
                if url.startswith("http://"):
                    tmp = url[7:].split("/", 1)[0]
                    if ":" in tmp:
                        host, port = tmp.split(":")
                    else:
                        host = tmp
                else:
                    host = header_dict.get("Host", "")
                    if ":" in host:
                        host, port = host.split(":")
                    else:
                        port = 80

            return HTTPRequest(method, url, version, header_dict, host, port, raw_request)

        except:
            return None
