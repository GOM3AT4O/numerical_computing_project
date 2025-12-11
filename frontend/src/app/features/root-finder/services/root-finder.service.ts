import { HttpClient } from "@angular/common/http";
import { inject, Injectable } from "@angular/core";
import { Observable, catchError, map, of } from "rxjs";
import { FindRootRequest } from "../models/find-root-request";
import { FindRootResponse } from "../models/find-root-response";

@Injectable({
  providedIn: "root",
})
export class RootFinderService {
  private http = inject(HttpClient);
  private readonly baseUrl = "http://localhost:5000/api";

  // maps the FindRootRequest to the format expected by the backend API.
  private mapRequest(request: FindRootRequest) {
    let parameters: any = request.parameters;
    if ("parameters" in request) {
      switch (request.method) {
        case "bisection":
        case "false-position":
          parameters = {
            lower_bound: request.parameters.lowerBound,
            upper_bound: request.parameters.upperBound,
          };
          break;
        case "secant":
          parameters = {
            first_guess: request.parameters.firstGuess,
            second_guess: request.parameters.secondGuess,
          };
          break;
        default:
      }
    }

    return {
      function: request.function,
      method: request.method,
      absolute_relative_error: request.absoluteRelativeError,
      number_of_iterations: request.numberOfIterations,
      precision: request.precision,
      parameters: parameters,
    };
  }

  // maps the backend API response to the FindRootResponse format.
  private mapResponse(response: any): FindRootResponse {
    return {
      root: response.root,
      absoluteRelativeError: response.absolute_relative_error,
      numberOfCorrectSignificantFigures:
        response.number_of_correct_significant_figures,
      numberOfIterations: response.number_of_iterations,
      executionTime: response.execution_time,
      message: response.message,
    };
  }

  findRoot(request: FindRootRequest): Observable<FindRootResponse> {
    return this.http
      .post<{
        root?: string;
        absolute_relative_error?: string;
        number_of_correct_significant_figures?: number;
        number_of_iterations?: number;
        execution_time?: number;
        message: string;
      }>(`${this.baseUrl}/find-root`, this.mapRequest(request))
      .pipe(
        catchError((error) =>
          of({
            message: error.error.error,
          }),
        ),
        map((response) => this.mapResponse(response)),
      );
  }
}
