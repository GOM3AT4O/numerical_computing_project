export type Equations = {
  coefficients: string[][];
  constants: string[];
};

export type LUParameters = {
  format: "doolittle" | "crout" | "cholesky";
};

export type IterationParameters =
  | {
      initialGuess: string[];
      stoppingCondition: "number-of-iterations";
      numberOfIterations: number;
    }
  | {
      initialGuess: string[];
      stoppingCondition: "absolute-relative-error";
      absoluteRelativeError: string;
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
