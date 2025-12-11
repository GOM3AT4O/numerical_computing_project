import {
  IntervalParameters,
  OneGuessParameters,
  TwoGuessesParameters,
} from "./parameters";

export type FindRootRequest = {
  function: string;
  precision?: number;
  numberOfIterations?: number;
  absoluteRelativeError?: string;
} & (
  | {
      method: "bisection" | "false-position";
      parameters: IntervalParameters;
    }
  | {
      method: "fixed-point" | "newton-raphson" | "modified-newton-raphson";
      parameters: OneGuessParameters;
    }
  | {
      method: "secant";
      parameters: TwoGuessesParameters;
    }
);
