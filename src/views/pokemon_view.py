from flask import request, json, Response, Blueprint, g
from ..models.pokemon import PokemonModel, PokemonSchema
import pokebase as pb

pokemon_api = Blueprint('pokemon', __name__)
pokemon_schema = PokemonSchema()

@pokemon_api.route('/all', methods=['GET'])
def get_all():
    '''
    Get all pokemon
    '''
    pokemons = PokemonModel.get_all_pokemon()
    ser_pokemon = pokemon_schema.dump(pokemons, many=True).data
    return custom_response(ser_pokemon, 200)

@pokemon_api.route('/<int:number>', methods=['GET'])
def get_pokemon(number):
    new_pokemon = pb.pokemon(number)
    new_pokemon_species = pb.pokemon_species(number)
    pokemon_fte = new_pokemon_species.flavor_text_entries
    for fte in pokemon_fte:
            if fte.language.name =="en" and fte.version.name == "alpha-sapphire" or fte.language.name == "en" and fte.version.name == "ultra-sun":
                    new_pokemon_description = fte.flavor_text
    new_pokemon_name = new_pokemon.name
    new_pokemon_number = new_pokemon.id
    
    new_pokemon_image = new_pokemon.sprites.front_default


    return f'{new_pokemon_name},\n{new_pokemon_description},\n{new_pokemon_image},\n{new_pokemon_number}'

@pokemon_api.route('/create', methods=['POST'])
def create_pokemon():
   
    req_data = request.get_json()
    data, error = pokemon_schema.load(req_data)
    print('Printing data')
    print(data, error)
    if error:
        return custom_response(error, 400)

    pokemon = PokemonModel(data)
    print(pokemon)
    pokemon.save()

    ser_data = pokemon_schema.dump(pokemon).data
    return custom_response(ser_data, 201)

@pokemon_api.route('/<string:name>', methods=['GET'])
def pokemon_info(name):
    new_pokemon = pb.pokemon(name)
    new_pokemon_species = pb.pokemon_species(name)
    pokemon_fte = new_pokemon_species.flavor_text_entries
    for fte in pokemon_fte:
            if fte.language.name =="en" and fte.version.name == "alpha-sapphire" or fte.language.name == "en" and fte.version.name == "ultra-sun":
                    new_pokemon_description = fte.flavor_text
    new_pokemon_name = new_pokemon.name
    new_pokemon_number = new_pokemon.id
    
    new_pokemon_image = new_pokemon.sprites.front_default


    return f'{new_pokemon_name},\n{new_pokemon_description},\n{new_pokemon_image},\n{new_pokemon_number}'


def custom_response(res, status_code):
    '''
    Creates a custom json response
    for proper status messages
    '''

    return Response(
        mimetype='application/json',
        response=json.dumps(res),
        status=status_code
    )

