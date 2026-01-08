import socket
import threading


def tunnel_thread(source, dest):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            dest.sendall(data)
    except:
        pass
    finally:
        try:
            dest.shutdown(socket.SHUT_WR)
        except:
            pass


def handle_https_tunnel(client_socket, host, port, logger):
    server_socket = None
    try:
        logger.log_info(f"CONNECT request received for {host}:{port}")

        # Connect to destination server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(10)
        server_socket.connect((host, port))

        # Notify client that tunnel is established
        client_socket.sendall(
            b"HTTP/1.1 200 Connection Established\r\n\r\n"
        )

        logger.log_info(f"HTTPS Tunnel Established: {host}:{port}")

        # Bidirectional forwarding (no inspection)
        t1 = threading.Thread(
            target=tunnel_thread,
            args=(client_socket, server_socket),
            daemon=True
        )
        t2 = threading.Thread(
            target=tunnel_thread,
            args=(server_socket, client_socket),
            daemon=True
        )

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    except Exception as e:
        logger.log_error(f"HTTPS Tunnel Error: {e}")

    finally:
        # Cleanup sockets
        try:
            client_socket.close()
        except:
            pass
        try:
            if server_socket:
                server_socket.close()
        except:
            pass
