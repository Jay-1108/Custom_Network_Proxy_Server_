class FilterEngine:
    def __init__(self, path="config/blocked_domains.txt"):
        self.rules = set()
        try:
            with open(path, "r") as f:
                for line in f:
                    line = line.strip().lower()
                    if line:
                        self.rules.add(line)
        except:
            pass

    def is_blocked(self, host):
        host = host.lower()
        for rule in self.rules:
            if rule in host:
                return True
        return False
