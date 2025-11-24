export type SolveEquationsResponse = {
  solution?: string[];
  executionTime: number;
  numberOfIterations?: number;
  L?: string[][];
  U?: string[][];
  message?: string;
};
