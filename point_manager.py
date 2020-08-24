
class PointManager():
    
    def __init__(self):
        self.p1p = 0
        self.p2p = 0
        self.p1g = 0
        self.p2g = 0

    def is_game_end(self):
        if self.p1p >= 11 or self.p2p >= 11:
            if abs(self.p1p - self.p2p) >= 2:
                return True
    
    def add_point(self, p):
        if self.is_game_end():
            if self.p1p > self.p2p:
                self.p1g += 1
            else:
                self.p2g += 1
            self.p1p, self.p2p = 0, 0
        if p == 1:
            self.p1p += 1
        else:
            self.p2p += 1

    def get_score(self):
        return {"p1p":self.p1p, "p2p":self.p2p,
            "p1g":self.p1g, "p2g":self.p2g}
