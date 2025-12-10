from flask import Flask, request, jsonify
from flask_cors import CORS
from solvers.Fixed_Point_solver import FixedPointSolver
from exceptions import ValidationError
from validator import FunctionValidator, LinearSystemValidator
from solver_factory import SolverFactory
from decimal import Decimal, getcontext
import signal
import os

app = Flask(__name__)
CORS(app)


@app.route("/api/solve", methods=["POST"])
def solve_system():
    """Main endpoint to solve linear system or nonlinear equation"""
    try:
        data = request.get_json()

        # Debug logging
        print("\n" + "=" * 50)
        print("Received request:")
        print(f"Data: {data}")

        # Extract data
        method = data.get("method")
        precision = data.get("precision")
        parameters = data.get("parameters", {})

        print(f"method: {method}")
        print(f"precision: {precision}")
        print(f"params: {parameters}")

        # set precision and rounding method for Decimal operations
        getcontext().prec = precision if precision is not None else 6
        getcontext().rounding = "ROUND_HALF_UP"

        # Validate required fields
        if not method:
            return jsonify({"error": "Missing required field: method"}), 400

        # Handle bisection method differently (nonlinear equation)
        if method == "bisection" or method == "false-position" or method == "secant":
            print(f"Processing {method} method")
            
            # Validate precision
            precision_value = LinearSystemValidator.validate_precision(precision)
            
            # Create and run solver
            solver = SolverFactory.create_solver(
                method, None, None, precision_value, parameters
            )
            
            result = solver.solve()
            print("=" * 50 + "\n")
            return jsonify(result.to_dict()), 200
        
        # Handle linear system methods
        else:
            A = data.get("A")
            b = data.get("b")
            
            print(f"A: {A}")
            print(f"b: {b}")

            if not all([A, b]):
                return jsonify(
                    {"error": "Missing required fields: A and b are required for linear system methods"}
                ), 400

            A = [[+Decimal(x) for x in y] for y in A]
            b = [+Decimal(x) for x in b]

            # Validate system
            A_matrix, b_vector = LinearSystemValidator.validate_system(A, b)
            precision_value = LinearSystemValidator.validate_precision(precision)

            # Create and run solver
            solver = SolverFactory.create_solver(
                method, A_matrix, b_vector, precision_value, parameters
            )

            result = solver.solve()
            print("=" * 50 + "\n")
            return jsonify(result.to_dict()), 200

    except ValidationError as e:
        print(f"\n Validation Error: {str(e)}\n")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"\n Exception occurred: {str(e)}")
        import traceback

        print("Full traceback:")
        traceback.print_exc()
        print("\n")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/methods", methods=["GET"])
def get_methods():
    """Get list of available methods and their parameters"""
    methods = {
        "gauss-elimination": {
            "name": "Gauss Elimination",
            "type": "linear",
            "parameters": [
                {
                    "name": "scaling",
                    "type": "boolean",
                    "default": False,
                    "required": False,
                }
            ],
        },
        "gauss-jordan-elimination": {
            "name": "Gauss-Jordan Elimination",
            "type": "linear",
            "parameters": [
                {
                    "name": "scaling",
                    "type": "boolean",
                    "default": False,
                    "required": False,
                }
            ],
        },
        "lu-decomposition": {
            "name": "LU Decomposition",
            "type": "linear",
            "parameters": [
                {
                    "name": "format",
                    "type": "select",
                    "options": ["doolittle", "crout", "cholesky"],
                    "default": "doolittle",
                    "required": True,
                }
            ],
        },
        "jacobi-iteration": {
            "name": "Jacobi Iteration",
            "type": "linear",
            "parameters": [
                {
                    "name": "initial_guess",
                    "type": "array",
                    "required": False,
                    "description": "Initial guess for solution (defaults to zeros)",
                },
                {
                    "name": "number_of_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": True,
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": True,
                },
            ],
        },
        "gauss-seidel-iteration": {
            "name": "Gauss-Seidel Iteration",
            "type": "linear",
            "parameters": [
                {
                    "name": "initial_guess",
                    "type": "array",
                    "required": False,
                    "description": "Initial guess for solution (defaults to zeros)",
                },
                {
                    "name": "number_of_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": True,
                },
                {
                    "name": "absolute_relative_error",
                    "type": "float",
                    "default": 1e-6,
                    "required": True,
                },
            ],
        },
        "bisection": {
            "name": "Bisection Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'x**2 - 2' or 'x**3 - x - 1')",
                },
                {
                    "name": "xl",
                    "type": "float",
                    "required": True,
                    "description": "Lower bound of interval",
                },
                {
                    "name": "xu",
                    "type": "float",
                    "required": True,
                    "description": "Upper bound of interval",
                },
                {
                    "name": "epsilon",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
            ],
        },
        "false-position": {
            "name": "False Position Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'x**2 - 2' or 'x**3 - x - 1')",
                },
                {
                    "name": "xl",
                    "type": "float",
                    "required": True,
                    "description": "Lower bound of interval",
                },
                {
                    "name": "xu",
                    "type": "float",
                    "required": True,
                    "description": "Upper bound of interval",
                },
                {
                    "name": "epsilon",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
            ],
        },
        "secant": {
            "name": "Secant Method",
            "type": "nonlinear",
            "parameters": [
                {
                    "name": "function",
                    "type": "string",
                    "required": True,
                    "description": "Function expression (e.g., 'x**2 - 2')",
                },
                {
                    "name": "x0",
                    "type": "float",
                    "required": True,
                    "description": "First initial guess (x_i-1)",
                },
                {
                    "name": "x1",
                    "type": "float",
                    "required": True,
                    "description": "Second initial guess (x_i)",
                },
                {
                    "name": "epsilon",
                    "type": "float",
                    "default": 1e-6,
                    "required": False,
                    "description": "Convergence tolerance",
                },
                {
                    "name": "max_iterations",
                    "type": "integer",
                    "default": 100,
                    "required": False,
                    "description": "Maximum number of iterations",
                },
            ],
        },
    }
    return jsonify(methods), 200

# Fixed Point Solver Endpoint just for testing i will put it in the factory later with another end point to the whole open methods
@app.route("/fixed-point", methods=["POST"])
def fixed_point_solver():
    """Endpoint to solve nonlinear equation using Fixed Point method"""
    try:
        data = request.get_json()

        # Extract data
        function_str = data.get("function")
        guess = data.get("guess")
        precision = data.get("precision")
        epsilon = data.get("epsilon", 0.000001)
        max_iterations = data.get("max_iterations", 50)

        # Validate required fields
        if not all([function_str, guess is not None]):
            return jsonify(
                {"error": "Missing required fields: function and guess are required"}
            ), 400

        # Validate precision
        precision_value = LinearSystemValidator.validate_precision(precision)

        function_str = FunctionValidator.validate_and_parse(function_str)

        # Create and run solver
        result = FixedPointSolver(
            func=function_str,                   
            guess=Decimal(str(guess)),   
            precision=precision_value,
            epsilon=Decimal(str(epsilon)),
            max_iterations=max_iterations,
        ).solve()

        return jsonify(result), 200

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Numerical Methods Solver API"}), 200


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Gracefully stop the Flask server."""
    os.kill(os.getpid(), signal.SIGTERM)
    return jsonify({"status": "shutting down"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)