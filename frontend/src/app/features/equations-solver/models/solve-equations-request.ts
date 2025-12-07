import {
  EliminationParameters,
  IterationParameters,
  LUParameters,
} from "./parameters";

export type Equations = {
  coefficients: string[][];
  constants: string[];
};

export type SolveEquationsRequest = {
  equations: Equations;
  precision?: number;
} & (
  | {
      method: "gauss-elimination" | "gauss-jordan-elimination";
      parameters: EliminationParameters;
    }
  | {
      method: "lu-decomposition";
      parameters: LUParameters;
    }
  | {
      method: "jacobi-iteration" | "gauss-seidel-iteration";
      parameters: IterationParameters;
    }
);
