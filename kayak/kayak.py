# origin
# destination
# adults {n}adults
# seniors {nseniors}
# youth (12-17), 17
# child (2-11), 11
# Seat Infant, 1S
# Lap Infant, 1L
# departDate
# returnDate (optional)
# carry on bags = cfc
# checked bag = bfc



# url = https://kayak.com/flights/{orign}-{destination}/{departDate}/{returnDate}/{(n)adults}/{(n)seniros}/?query params

# Query Parameters

# can't have more than 7 children
# children=11-11-17-17-1S-1L


class Kayak:

    REQUIRED = ['origin', 'destination', 'departDate']

    REQUIRED_TRAVELERS = ['adults', 'seniors']

    CHILDREN_MAP = {
        'youth': '17',
        'child': '11',
        'seat_infant': '1S',
        'lap_infant': '1L'
    }

    def __init__(self, data=None):
        self.data = data

    @property
    def base_url(self):
        return "https://kayak.com/flights"

    def _check_data(self, data):
        if not isinstance(data, dict):
            raise TypeError(f"Data must be a dictionary, not {type(data)}")
        if not all (k in data for k in self.REQUIRED):
            raise ValueError(f"Missing one of {self.REQUIRED}")
        if not any (k in data for k in self.REQUIRED_TRAVELERS):
            raise ValueError(f"Need to have at least one of {self.REQUIRED_TRAVELERS")
        if sum(v for k, v in data.items if k in self.REQUIRED_TRAVELERS) < 1:
            raise ValueError(f"Searches need at least 1 traveler")
        children = sum(v for k, v in data.items() if k in self.CHILDREN_MAP)
        if children > 7:
            raise ValueError(f"Searches cannot have more than 7 children.  You have {children}.")

    def _construct_url(self, data):
        self._check_data(data)
        url = f"{self.base_url}/{data.pop('origin')}-{data.pop('destination')}/{data.pop('depart_date')}/"
        if 'returnDate' in data.keys():
            url += f"{data['returnDate']}/"
        url += self._add_travelers(data)
        url += self._add_children(data)

    def _add_travelers(self, data):
        s = ''
        for k in self.REQUIRED_TRAVELERS:
            if k in data:
                s += f"{data[k]}{k}/"
        return s

    def _add_children(self, data):
        s = 'children'
        for k in data:
            if k in self.CHILDREN_MAP:
                s += f"-{CHILDREN_MAP[k]}" * v
        return s
