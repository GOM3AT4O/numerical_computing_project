import { Step } from "./step";

export type SolveEquationsResponse = {
  solution?: string[];
  steps?: Step[];
  executionTime: number;
  numberOfIterations?: number;
  L?: string[][];
  U?: string[][];
  message?: string;
};
