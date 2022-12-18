class Station:
    def __init__(self, usaf, wban, name, cntry, lat, long) -> None:
        self.usaf = usaf.zfill(6)
        self.wban = wban.zfill(5)
        self.name = name
        self.country = cntry
        
        try:
            self.latitude = float(lat)
        except ValueError:
            self.latitude = None
            
        try:
            self.longitude = float(long)
        except ValueError:
            self.longitude = None
