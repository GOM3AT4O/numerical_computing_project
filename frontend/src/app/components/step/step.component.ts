import { Component, input } from "@angular/core";
import { Step } from "../../models/step";
import { RowOperationStepComponent } from "./row-operation-step/row-operation-step.component";
import { SubstitutionStepComponent } from "./substitution-step/substitution-step.component";
import { IterationStepComponent } from "./iteration-step/iteration-step.component";
import { ShowMatricesStepComponent } from "./show-matrices-step/show-matrices-step.component";
import { CroutDecompositionStepComponent } from "./crout-decomposition-step/crout-decomposition-step.component";
import { CholeskyDecompositionStepComponent } from "./cholesky-decomposition-step/cholesky-decomposition-step.component";

@Component({
  selector: "app-step",
  imports: [
    RowOperationStepComponent,
    SubstitutionStepComponent,
    IterationStepComponent,
    ShowMatricesStepComponent,
    CroutDecompositionStepComponent,
    CholeskyDecompositionStepComponent,
  ],
  templateUrl: "./step.component.html",
  styleUrl: "./step.component.css",
})
export class StepComponent {
  step = input.required<Step>();
}
