import { Component, input } from "@angular/core";
import { CroutDecompositionStep } from "../../../models/step";

@Component({
  selector: "app-crout-decomposition-step",
  imports: [],
  templateUrl: "./crout-decomposition-step.component.html",
  styleUrl: "./crout-decomposition-step.component.css",
})
export class CroutDecompositionStepComponent {
  step = input.required<CroutDecompositionStep>();
}
