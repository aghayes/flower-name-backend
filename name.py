import pandas as pd
import phonetics
import jellyfish
import sys
from flask import Flask, request, abort
from flask_restful import Resource, Api

app = Flask("__name__")
api = Api(app)
api.species = pd.read_csv("encoded_names.csv")
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

class dmetaphone(Resource):
	def get(self):
		name = request.args["name"]
		encoded = phonetics.dmetaphone(name)[0]
		row = api.species.loc[api.species["dmetaphone"].map(lambda x: jellyfish.jaro_distance(x, encoded)).idxmax()]
		response = {"name": row["scientificName"], "url": row["scientificNameID"]}
		return response

api.add_resource(dmetaphone, "/")

if __name__ == "__main__":
	app.run()