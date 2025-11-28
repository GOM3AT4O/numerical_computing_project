import { Component, input } from "@angular/core";
import { CholeskyDecompositionStep } from "../../../models/step";

@Component({
  selector: "app-cholesky-decomposition-step",
  imports: [],
  templateUrl: "./cholesky-decomposition-step.component.html",
  styleUrl: "./cholesky-decomposition-step.component.css",
})
export class CholeskyDecompositionStepComponent {
  step = input.required<CholeskyDecompositionStep>();
}
