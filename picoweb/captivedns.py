import usocket as _socket
from uasyncio.core import IORead

class CaptiveDnsServer():
    def __init__(self, host, domains):
        self.host = host
        self.domains = domains
        self.port = 53
    
    def start(self):
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
        s.setblocking(False)
        ai = _socket.getaddrinfo(self.host, self.port)
        addr = ai[0][4]
        s.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
        s.bind(addr)
        while True:
            yield IORead(s)
            data, addr = s.recvfrom(2048)
            response = self.process_request(data)
            if response is not None:
                s.sendto(response, addr)
    
    def device_ip(self):
      try:
          import network
          return network.WLAN(network.AP_IF).ifconfig()[0]
      except ImportError:
          # This happens when not run on device, so dummy value is returned
          # Otherwise the import above will cause ImportError and app will stop
          return '127.0.0.1'
    
    def process_request(self, data):
        # Assuming query type is A, and only one question is in it,
        # so no checks for that

        transaction_id = data[:2]

        # Extracting domain name from request
        question_section_start_index = 12
        sub_domains = []
        i = question_section_start_index
        sub_domain_len = data[i]
        while sub_domain_len > 0:
            sub_domain = data[i + 1: i + sub_domain_len + 1].decode('utf-8')
            sub_domains.append(sub_domain)
            i += sub_domain_len + 1
            sub_domain_len = data[i]
        i += sub_domain_len + 1

        domain = '.'.join(sub_domains)
        
        question = data[question_section_start_index:i+4] # domain + type (2 bytes) + class (2 bytes)
        
        answer_count = 0
        if domain in self.domains:
            answer_count = 1

        response = b''
        response += transaction_id
        response += b'\x81\x80'                     # Flags: Standard query response, No Error
        response += b'\x00\x01'                     # 1 Question
        response += b'\x00' + bytes([answer_count]) # Number of Answer
        response += b'\x00\x00'                     # 0 Authorities
        response += b'\x00\x00'                     # 0 Additional
        response += question

        if answer_count == 0:
            return response

        #Answer
        response+= b'\xc0' + bytes([question_section_start_index])    # Pointer to domain from question
        response += b'\x00\x01' # Response type: A
        response += b'\x00\x01' # Class: IN
        response += b'\x00\x00\x00\x01' # TTL: 1
        response += b'\x00\x04' # Data Length: 4
        response += bytes([int(b) for b in self.device_ip().split('.')])   # IP

        return response

