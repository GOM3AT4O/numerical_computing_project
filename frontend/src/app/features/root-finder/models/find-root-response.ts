export type FindRootResponse = {
  executionTime: number;
  message?: string;
  numberOfIterations: number;
} & (
  | {
      solution: string;
      absoluteRelativeError: string;
      numberOfCorrectSignificantFigures: number;
    }
  | {
      solution?: undefined;
      absoluteRelativeError?: undefined;
      numberOfCorrectSignificantFigures?: undefined;
    }
);
