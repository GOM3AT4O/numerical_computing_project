import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { SolveEquationsRequest } from "../models/solve-equations-request";
import { SolveEquationsResponse } from "../models/solve-equations-response";
import { map, Observable, tap } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class EquationsSolverService {
  private http = inject(HttpClient);
  private readonly baseUrl = "http://localhost:5000/api";

  private readonly mapMethod = {
    "gauss-elimination": "gauss-elimination",
    "gauss-jordan-elimination": "gauss-jordan",
    "lu-decomposition": "lu-decomposition",
    "jacobi-iteration": "jacobi",
    "gauss-seidel-iteration": "gauss-seidel",
  } as const;

  private mapRequest(request: SolveEquationsRequest) {
    let parameters = undefined;
    if ("parameters" in request) {
      switch (request.method) {
        case "lu-decomposition":
          parameters = {
            form: request.parameters.format,
          };
          break;
        case "jacobi-iteration":
        case "gauss-seidel-iteration":
          switch (request.parameters.stoppingCondition) {
            case "number-of-iterations":
              parameters = {
                initial_guess: request.parameters.initialGuess,
                max_iterations: request.parameters.numberOfIterations,
              };
              break;
            case "absolute-relative-error":
              parameters = {
                initial_guess: request.parameters.initialGuess,
                tolerance: request.parameters.absoluteRelativeError,
              };
              break;
          }
          break;
      }
    }

    return {
      A: request.equations.coefficients,
      b: request.equations.constants,
      method: this.mapMethod[request.method],
      precision: request.precision,
      parameters: parameters,
    };
  }

  private mapResponse(response: any): SolveEquationsResponse {
    return {
      solution: response.has_solution ? response.solution : null,
      executionTime: response.execution_time,
      numberOfIterations: response.iterations,
      L: response.L,
      U: response.U,
      message: response.message,
    };
  }

  solveEquations(
    request: SolveEquationsRequest,
  ): Observable<SolveEquationsResponse> {
    return this.http
      .post<{
        has_solution: boolean;
        solution: number[];
        L?: number[][];
        U?: number[][];
        iterations?: number;
        execution_time: number;
        message: string;
      }>(`${this.baseUrl}/solve`, this.mapRequest(request))
      .pipe(tap((response) => console.log(response)))
      .pipe(map((response) => this.mapResponse(response)));
  }
}
