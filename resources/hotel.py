from flask_restful import Resource , reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return { 'Hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')
    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404
    
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' already exists.".format(hotel_id)},200

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()
    

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()  #pegandos      
        
        hotelfound = HotelModel.find_hotel(hotel_id)
        if hotelfound:
            hotelfound.update_hotel(**dados)
            hotelfound.save_hotel()
            return hotelfound.json(),200

        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(),201

    def delete(self,hotel_id):
        hotelfound = HotelModel.find_hotel(hotel_id)
        if hotelfound:
            hotelfound.delete_hotel()
            return {'message':'Hotel Deleted.'},200
        return {'message':'Hotel not found'},404

