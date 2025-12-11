export type FindRootResponse = {
  root?: string;
  absoluteRelativeError?: string;
  numberOfCorrectSignificantFigures?: number;
  numberOfIterations?: number;
  executionTime?: number;
  message: string;
};
