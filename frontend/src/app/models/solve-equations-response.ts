export type SolveEquationsResponse = {
  solution?: number[];
  executionTime: number;
  numberOfIterations?: number;
  L?: number[][];
  U?: number[][];
};
