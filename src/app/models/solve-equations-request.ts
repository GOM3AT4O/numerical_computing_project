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
      stoppingCondition: "relative-error";
      relativeError: number;
    };

export type SolveEquationsRequest =
  | {
      equationCount: number;
      equations: Equations;
      method: "gauss-elimination";
      precision?: number;
    }
  | {
      equationCount: number;
      equations: Equations;
      method: "gauss-jordan-elimination";
      precision?: number;
    }
  | {
      equationCount: number;
      equations: Equations;
      method: "lu-decomposition";
      parameters: LUParameters;
      precision?: number;
    }
  | {
      equationCount: number;
      equations: Equations;
      method: "jacobi-iteration";
      parameters: IterationParameters;
      precision?: number;
    }
  | {
      equationCount: number;
      method: "gauss-seidel-iteration";
      parameters: IterationParameters;
      precision?: number;
    };
