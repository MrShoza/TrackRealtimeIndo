import requests
import json


api_key = 'YOUR_TELESIGN_API_KEY'
customer_id = 'YOUR_CUSTOMER_ID'
google_maps_api_key = 'YOUR_GOOGLE_MAPS_API_KEY'

def lookup_phone_number(phone_number):
    """
    Fungsi untuk mendapatkan informasi lokasi dan operator berdasarkan nomor ponsel
    Menggunakan API Telesign
    """
    url = f'https://rest-api.telesign.com/v1/phoneid/standard/{phone_number}'
    
    headers = {
        'Authorization': f'Basic {api_key}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Nomor Ponsel: {data['phone_number']}")
        print(f"Operator: {data['carrier']['name']}")
        print(f"Lokasi Negara: {data['location']['country_code']}")
        print(f"Lokasi Kota: {data['location']['locality']}")
        print(f"Is Number Valid? {data['valid']}")
        
        country = data['location']['country_code']
        city = data['location']['locality']
        
        get_coordinates_from_google_maps(city, country)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def get_coordinates_from_google_maps(city, country):
    """
    Fungsi untuk mendapatkan koordinat (latitude, longitude) menggunakan Google Maps Geocoding API
    """
    geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city},{country}&key={google_maps_api_key}'
    
    response = requests.get(geocode_url)
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            
            generate_map(latitude, longitude)
        else:
            print("Lokasi tidak ditemukan.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def generate_map(latitude, longitude):
    """
    Fungsi untuk menghasilkan kode HTML untuk menampilkan peta dengan lokasi yang diberikan
    """
    map_html = f"""
    <html>
    <head>
        <title>Lokasi Ponsel</title>
        <script src="https://maps.googleapis.com/maps/api/js?key={google_maps_api_key}&callback=initMap" async defer></script>
        <script>
        function initMap() {{
            var location = {{lat: {latitude}, lng: {longitude}}};
            var map = new google.maps.Map(document.getElementById('map'), {{
                zoom: 14,
                center: location
            }});
            var marker = new google.maps.Marker({{
                position: location,
                map: map
            }});
        }}
        </script>
    </head>
    <body>
        <h3>Lokasi Ponsel: {latitude}, {longitude}</h3>
        <div id="map" style="height: 500px; width: 100%;"></div>
    </body>
    </html>
    """
    
    with open('location_map.html', 'w') as file:
        file.write(map_html)
    
    print("Peta berhasil dibuat! Buka 'location_map.html' untuk melihat lokasi di Google Maps.")

phone_number = input("Masukkan nomor ponsel untuk dilacak : ")

lookup_phone_number(phone_number)
