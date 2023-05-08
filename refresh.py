import requests

# Made by Enomiis on Github

# simple refresh func imported from an earlier project

class Refresh_Token():
    
    def refresh(self):   
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
            
            data={"grant_type": "refresh_token","refresh_token": 'your_refresh_token'},
            
            headers={"Authorization": "Basic " + "your_base64_encoded_client"}
            )
        
        response_json = response.json()
        
        return response_json["access_token"]
