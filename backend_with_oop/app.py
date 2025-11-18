from flask import Flask, request, jsonify
from flask_cors import CORS
from exceptions import ValidationError
from validator import LinearSystemValidator
from solver_factory import SolverFactory

app = Flask(__name__)
CORS(app)

@app.route('/api/solve', methods=['POST'])
def solve_system():
    """Main endpoint to solve linear system"""
    try:
        data = request.get_json()
        
        # Debug logging
        print("\n" + "="*50)
        print("Received request:")
        print(f"Data: {data}")
        
        # Extract data
        A = data.get('A')
        b = data.get('b')
        method = data.get('method')
        precision = data.get('precision')
        params = data.get('parameters', {})
        
        print(f"A: {A}")
        print(f"b: {b}")
        print(f"method: {method}")
        print(f"precision: {precision}")
        print(f"params: {params}")
        print("="*50 + "\n")
        
        # Validate required fields
        if not all([A, b, method]):
            return jsonify({
                'error': 'Missing required fields: A, b, and method are required'
            }), 400
        
        # Validate system
        A_matrix, b_vector = LinearSystemValidator.validate_system(A, b)
        precision_value = LinearSystemValidator.validate_precision(precision)
        
        # Create and run solver
        solver = SolverFactory.create_solver(method, A_matrix, b_vector, precision_value, params)
        result = solver.solve()
        
        return jsonify(result.to_dict()), 200
        
    except ValidationError as e:
        print(f"\n Validation Error: {str(e)}\n")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"\n Exception occurred: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        print("\n")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/api/methods', methods=['GET'])
def get_methods():
    """Get list of available methods and their parameters"""
    methods = {
        'gauss_elimination': {
            'name': 'Gauss Elimination',
            'parameters': []
        },
        'gauss_jordan': {
            'name': 'Gauss-Jordan',
            'parameters': []
        },
        'lu_decomposition': {
            'name': 'LU Decomposition',
            'parameters': [
                {
                    'name': 'form',
                    'type': 'select',
                    'options': ['doolittle', 'crout', 'cholesky'],
                    'default': 'doolittle',
                    'required': True
                }
            ]
        },
        'jacobi': {
            'name': 'Jacobi Iteration',
            'parameters': [
                {
                    'name': 'initial_guess',
                    'type': 'array',
                    'required': False,
                    'description': 'Initial guess for solution (defaults to zeros)'
                },
                {
                    'name': 'max_iterations',
                    'type': 'integer',
                    'default': 100,
                    'required': False
                },
                {
                    'name': 'tolerance',
                    'type': 'float',
                    'default': 1e-6,
                    'required': False
                }
            ]
        },
        'gauss_seidel': {
            'name': 'Gauss-Seidel',
            'parameters': [
                {
                    'name': 'initial_guess',
                    'type': 'array',
                    'required': False,
                    'description': 'Initial guess for solution (defaults to zeros)'
                },
                {
                    'name': 'max_iterations',
                    'type': 'integer',
                    'default': 100,
                    'required': False
                },
                {
                    'name': 'tolerance',
                    'type': 'float',
                    'default': 1e-6,
                    'required': False
                }
            ]
        }
    }
    return jsonify(methods), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Linear Equations Solver API'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)