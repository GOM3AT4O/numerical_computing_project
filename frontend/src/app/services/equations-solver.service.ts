import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { SolveEquationsRequest } from "../models/solve-equations-request";
import { SolveEquationsResponse } from "../models/solve-equations-response";
import { map, Observable, tap } from "rxjs";
import { Step } from "../models/step";

@Injectable({
  providedIn: "root",
})
export class EquationsSolverService {
  private http = inject(HttpClient);
  private readonly baseUrl = "http://localhost:5000/api";

  private mapRequest(request: SolveEquationsRequest) {
    let parameters = undefined;
    if ("parameters" in request) {
      switch (request.method) {
        case "jacobi-iteration":
        case "gauss-seidel-iteration":
          parameters = {
            initial_guess: request.parameters.initialGuess,
            number_of_iterations: request.parameters.numberOfIterations,
            absolute_relative_error: request.parameters.absoluteRelativeError,
          };
          break;
        default:
          parameters = request.parameters;
      }
    }

    return {
      A: request.equations.coefficients,
      b: request.equations.constants,
      method: request.method,
      precision: request.precision,
      parameters: parameters,
    };
  }

  private mapResponse(response: any): SolveEquationsResponse {
    return {
      solution: response.solution,
      steps: response.steps,
      executionTime: response.execution_time,
      numberOfIterations: response.number_of_iterations,
      L: response.L,
      U: response.U,
      P: response.P,
      message: response.message,
    };
  }

  solveEquations(
    request: SolveEquationsRequest,
  ): Observable<SolveEquationsResponse> {
    return this.http
      .post<{
        solution?: string[];
        steps?: Step[];
        L?: string[][];
        U?: string[][];
        P?: string[][];
        number_of_iterations?: number;
        execution_time: number;
        message: string;
      }>(`${this.baseUrl}/solve`, this.mapRequest(request))
      .pipe(tap((response) => console.log(response)))
      .pipe(map((response) => this.mapResponse(response)));
  }
}
