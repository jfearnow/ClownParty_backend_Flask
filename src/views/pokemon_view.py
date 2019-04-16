from flask import request, json, Response, Blueprint, g
from ..models.pokemon import PokemonModel, PokemonSchema

pokemon_api = Blueprint('pokemon', __name__)
pokemon_schema = PokemonSchema()

@pokemon_api.route('/pokemon', methods=['GET'])
def get_all():
    '''
    Get all pokemon
    '''
    pokemons = PokemonModel.get_all_pokemon()
    ser_pokemon = pokemon_schema.dump(pokemons, many=True).data
    return custom_response(ser_pokemon, 200)

@pokemon_api.route('/pokemon', methods=['GET'])
def get_pokemon(pokemonnumber):
    '''
    Get a single pokemon
    '''
    pokemon = PokemonModel.get_one_pokemon(pokemonnumber)
    if not pokemon:
        return custom_response({'error': 'Pokemon not found'}, 404)

    ser_pokemon = pokemon_schema.dump(pokemon).data
    return custom_response(ser_user, 200)

