export type RowOperationStep =
  | {
      step_type: "row-operation";
      operation_type: "swap";
      old_matrix: string[][];
      new_matrix: string[][];
      target_row: number;
      source_row: number;
    }
  | {
      step_type: "row-operation";
      operation_type: "scale";
      old_matrix: string[][];
      new_matrix: string[][];
      target_row: number;
      factor: string;
    }
  | {
      step_type: "row-operation";
      operation_type: "add";
      old_matrix: string[][];
      new_matrix: string[][];
      target_row: number;
      source_row: number;
      factor: string;
    };

export type SubstitutionStep = {
  step_type: "substitution";
  substitution_type: "forward" | "back";
  matrix: string[][];
  result: string[];
};

export type IterationStep = {
  step_type: "iteration";
  iteration_type: "jacobi" | "gauss-seidel";
  matrix: string[][];
  old_solution: string[];
  new_solution: string[];
  absolute_relative_error: string;
};

export type ShowMatricesStep = {
  step_type: "show-matrices";
  matrices: { [key: string]: string[][] };
};

export type Step =
  | RowOperationStep
  | SubstitutionStep
  | IterationStep
  | ShowMatricesStep;
