export type RowOperation =
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

export type Step = RowOperation;
