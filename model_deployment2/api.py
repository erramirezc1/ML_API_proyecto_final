from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from m03_model_deployment import predict_probabilidad

app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='API - prediccion de popularidad de genero de peliculas',
    description='API para predecir la popularidad de géneros de películas a partir de su sinopsis.')

ns = api.namespace('predict', 
     description='Popularidad')

# Definición argumentos o parámetros de la API
parser = ns.parser()
parser.add_argument(
    'plot',
    type=str,
    required=True,
    help='Sinopsis de la película',
    location='args'
) 

resource_fields = api.model('Resource', {
    'result': fields.String,
})

# Definición de la clase para disponibilización
@ns.route('/')
class ProbabilidadPeliculaApi(Resource):

    @ns.doc(parser=parser)
    @ns.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        plot = args['plot']
        
        resultado = predict_probabilidad(plot)
        return {
            "result": str(resultado)
        }, 200
        
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)