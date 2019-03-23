from rasa_core.slots import Slot

supported_cities = [
    "Ahmedabad", "Bangalore", "Chennai", "Delhi", "Hyderabad", "Kanpur", "Kolkata", "Mumbai", "Nagpur", "Pune",
    "Agra", "Ajmer", "Aligarh", "Amravati", "Amritsar", "Asansol", "Aurangabad", "Bareilly", "Belgaum",
    "Bhavnagar", "Bhiwandi", "Bhopal", "Bhubaneswar", "Bikaner", "Bokaro Steel City", "Chandigarh", "Coimbatore", "Cuttack",
     "Dehradun", "Dhanbad", "Durg-Bhilai Nagar", "Durgapur", "Erode", "Faridabad",
    "Firozabad", "Ghaziabad", "Gorakhpur", "Gulbarga", "Guntur", "Gurgaon", "Guwahati",
    "Gwalior", "Hubli-Dharwad", "Indore", "Jabalpur", "Jaipur", "Jalandhar", "Jammu", "Jamnagar",
    "Jamshedpur", "Jhansi", "Jodhpur", "Kannur", "Kakinada", "Kochi", "Kottayam",
    "Kolhapur", "Kollam", "Kota", "Kozhikode", "Kurnool", "Lucknow", "Ludhiana", "Madurai",
    "Malappuram", "Mathura", "Goa", "Mangalore", "Meerut", "Moradabad", "Mysore", "Nanded",
    "Nashik", "Nellore", "Noida", "Palakkad", "Patna", "Pondicherry", "Prayagraj", "Raipur",
    "Rajkot", "Rajahmundry", "Ranchi", "Rourkela", "Salem", "Sangli", "Siliguri", "Solapur",
    "Srinagar", "Sultanpur", "Surat", "Thiruvananthapuram", "Thrissur", "Tiruchirappalli",
    "Tirunelveli", "Tiruppur", "Tiruvannamalai", "Ujjain", "Bijapur", "Vadodara", "Varanasi",
    "Vasai-Virar City", "Vijayawada", "Visakhapatnam", "Vellore", "Warangal", ]

class LocationSlot(Slot):

    def feature_dimensionality(self):
        return 1

    def as_feature(self):
        r = [0.0] * self.feature_dimensionality()
        if len(list(filter(lambda x: x.lower() == self.value.lower(),supported_cities))) > 0:
            r[0] = 1
        else:
            r[0] = 0
        return r


