from enum import Enum

class Enumerations(Enum):
    class _Type(Enum):
        condo = "Condo Apartment"
        coop= "Co-op / Co-Ownership Apartment"
        condo_townhouse = "Condo Townhouse"
        townhouse = "Townhouse"
        detached = "Detached"
        semi_detached = "Semi-Detached"

    class _Style(Enum):
        apartment= "Apartment"
        studio ="Bachelor/Studio"
        two_storey = "2-Storey"
        three_storey = "3-Storey"
        stacked = "Stacked Townhouse"
        loft = "Loft"
        bungalow = "Bungalow"
    
    class _Dens(Enum):
        zero = 0
        one = 1
        two =2
        three = 3
        four = 4

    class _ParkingTotal(Enum):
        zero = 0
        one = 1
        two =2
        three = 3
        four = 4
        five = 5
        six = 6 
        seven = 7
        eight = 8
        
    class _Bathrooms(Enum):
        one = 1
        two =2
        three = 3
        four = 4
        five = 5
        six = 6 
        seven = 7
        eight = 8

    class _Bedrooms(Enum):
        zero = 0
        one = 1
        two =2
        three = 3
        four = 4
        five = 5
        six = 6 
        seven = 7
        eight = 8
        nine = 9
    

    Sqaurefootage =  ["0-499","500-599","600-699","700-799","800-899","900-999","1000-1199","1200-1399","1400-1599","1600-1799","1800-1999","2000-2249","2250-2499","2500-2749","2750-2999","3000-3249","3250-3499","3500-3749","3750-3999","4000-4499","4500-4999", "5000+"]

    Community = ['Agincourt North', 'Agincourt South-Malvern West', 'Alderwood', 'Annex', 'Banbury-Don Mills', 'Bathurst Manor', 'Bay Street Corridor', 'Bayview Village', 'Bayview Woods-Steeles', 'Bedford Park-Nortown', 'Beechborough-Greenbrook', 'Bendale', 'Birchcliffe-Cliffside', 'Black Creek', 'Blake-Jones', 'Briar Hill-Belgravia', 'Bridle Path-Sunnybrook-York Mills', 'Broadview North', 'Brookhaven-Amesbury', 'Cabbagetown-South St. James Town', 'Caledonia-Fairbank', 'Casa Loma', 'Centennial Scarborough', 'Church-Yonge Corridor', 'Clairlea-Birchmount', 'Clanton Park', 'Cliffcrest', 'Corso Italia-Davenport', 'Crescent Town', 'Danforth', 'Danforth Village-East York', 'Don Valley Village', 'Dorset Park', 'Dovercourt-Wallace Emerson-Junction', 'Downsview-Roding-CFB', 'Dufferin Grove', 'East End-Danforth', 'East York', 'Edenbridge-Humber Valley', 'Eglinton East', 'Elms-Old Rexdale', 'Englemount-Lawrence', 'Eringate-Centennial-West Deane', 'Etobicoke West Mall', 'Flemingdon Park', 'Forest Hill North', 'Forest Hill South', 'Glenfield-Jane Heights', 'Greenwood-Coxwell', 'Guildwood', 'Henry Farm', 'High Park North', 'High Park-Swansea', 'Highland Creek', 'Hillcrest Village', 'Humber Heights', 'Humber Summit', 'Humberlea-Pelmo Park W4', 'Humberlea-Pelmo Park W5', 'Humbermede', 'Humewood-Cedarvale', 'Ionview', 'Islington-City Centre West', 'Junction Area', 'Keelesdale-Eglinton West', 'Kennedy Park', 'Kensington-Chinatown', 'Kingsview Village-The Westway', 'Kingsway South', "L'Amoreaux", 'Lambton Baby Point', 'Lansing-Westgate', 'Lawrence Park North', 'Lawrence Park South', 'Leaside', 'Little Portugal', 'Long Branch', 'Malvern', 'Maple Leaf', 'Markland Wood', 'Milliken', 'Mimico', 'Morningside', 'Moss Park', 'Mount Dennis', 'Mount Olive-Silverstone-Jamestown', 'Mount Pleasant East', 'Mount Pleasant West', 'New Toronto', 'Newtonbrook East', 'Newtonbrook West', 'Niagara', 'North Riverdale', 'North St. James Town', "O'Connor-Parkview", 'Oakridge', 'Oakwood-Vaughan', 'Palmerston-Little Italy', 'Parkwoods-Donalda', 'Playter Estates-Danforth', 'Pleasant View', 'Princess-Rosethorn', 'Regent Park', 'Rexdale-Kipling', 'Rockcliffe-Smythe', 'Roncesvalles', 'Rosedale-Moore Park', 'Rouge E10', 'Rouge E11', 'Runnymede-Bloor West Village', 'Rustic', 'Scarborough Village', 'South Parkdale', 'South Riverdale', 'St. Andrew-Windfields', 'Steeles', 'Stonegate-Queensway', "Tam O'Shanter-Sullivan", 'The Beaches', 'Thistletown-Beaumonde Heights', 'Thorncliffe Park', 'Trinity-Bellwoods', 'University', 'Victoria Village', 'Waterfront Communities C1', 'Waterfront Communities C8', 'West Hill', 'West Humber-Clairville', 'Westminster-Branson', 'Weston', 'Weston-Pellam Park', 'Wexford-Maryvale', 'Willowdale East', 'Willowdale West', 'Willowridge-Martingrove-Richview', 'Woburn', 'Woodbine Corridor', 'Woodbine-Lumsden', 'Wychwood', 'Yonge-Eglinton', 'Yonge-St. Clair', 'York University Heights', 'Yorkdale-Glen Park"']

    Municipality_District = ['C01', 'C02', 'C03', 'C04', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'W01', 'W02', 'W03', 'W04', 'W05', 'W06', 'W07', 'W08', 'W09', 'W10']
    
    Type = [ t.value  for t in  _Type ]
    
    Style = [ t.value for t in  _Style ]
   
    Dens = [ t.value for t in  _Dens ]
   
    ParkingTotal = [ t.value for t in  _ParkingTotal ]
    
    Bedrooms = [ t.value for t in  _Bedrooms ]
   
    Bathrooms = [ t.value for t in  _Bathrooms ]
   