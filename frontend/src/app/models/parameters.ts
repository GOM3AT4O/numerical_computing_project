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

export type EliminationParameters = {
  scaling: boolean;
};
