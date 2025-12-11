export type LUParameters = {
  format: "doolittle" | "crout" | "cholesky";
};

export type IterationParameters = {
  initialGuess: string[];
  numberOfIterations: number;
  absoluteRelativeError: string;
};

export type EliminationParameters = {
  scaling: boolean;
};
