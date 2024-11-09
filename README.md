# USA Largest City Finder from Lat Lon by Population using OpenStreetMap Nominatim and Overpass-api.de
 Free/NoAPIKey - Python Largest City Finder for USA Counties & towns by comparing population datas from nominatim openstreetmap  & overpass.de APIs with QT Desktop App version included

Just look up params;

useGUI = False
lat = 45.0358911
lon = -109.5215668

if yo uset useGUI to true, QT App will show and asks you to enter the lat/lon to the input fields as seen on screenshots

# How it Works?
1) Gets Country, State, County and Bounding Box datas by lat/lon using this URL: https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}&zoom=10&addressdetails=1
2) Gets all cities between the bounding box lat/lon by using URL: http://overpass-api.de/api/interpreter
3) Compares all cities by 'population' tag in the datas
4) Extract the largest city data and print/set to the QT label

 ![Console](https://github.com/user-attachments/assets/ebc926c6-8cae-48b9-b662-c29eb4167e94)
![QT App](https://github.com/user-attachments/assets/98232d4c-01db-4065-aabe-5d889edb525c)
