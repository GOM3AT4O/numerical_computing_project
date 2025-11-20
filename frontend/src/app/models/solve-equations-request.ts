export type Equations = {
  coefficients: number[][];
  constants: number[];
};

export type LUParameters = {
  format: "doolittle" | "crout" | "cholesky";
};

export type IterationParameters =
  | {
      initialGuess: number[];
      stoppingCondition: "number-of-iterations";
      numberOfIterations: number;
    }
  | {
      initialGuess: number[];
      stoppingCondition: "absolute-relative-error";
      absoluteRelativeError: number;
    };

export type SolveEquationsRequest =
  | {
      equations: Equations;
      method: "gauss-elimination";
      precision?: number;
    }
  | {
      equations: Equations;
      method: "gauss-jordan-elimination";
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
