import {
  EliminationParameters,
  IterationParameters,
  LUParameters,
} from "./parameters";

export type Equations = {
  coefficients: string[][];
  constants: string[];
};

export type SolveEquationsRequest =
  | {
      equations: Equations;
      method: "gauss-elimination";
      parameters: EliminationParameters;
      precision?: number;
    }
  | {
      equations: Equations;
      method: "gauss-jordan-elimination";
      parameters: EliminationParameters;
      precision?: number;
    }
  | {
      equations: Equations;
      method: "lu-decomposition";
      parameters: LUParameters;
      precision?: number;
    }
  | {
      equations: Equations;
      method: "jacobi-iteration";
      parameters: IterationParameters;
      precision?: number;
    }
  | {
      equations: Equations;
      method: "gauss-seidel-iteration";
      parameters: IterationParameters;
      precision?: number;
    };
