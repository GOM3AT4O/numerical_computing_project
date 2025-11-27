import { Component, input } from "@angular/core";
import { Step } from "../../models/step";
import { SubstitutionComponent } from "./substitution/substitution.component";
import { RowOperationComponent } from "./row-operation/row-operation.component";
import { IterationComponent } from "./iteration/iteration.component";
import { ShowMatricesComponent } from "./show-matrices/show-matrices.component";

@Component({
  selector: "app-step",
  imports: [
    RowOperationComponent,
    SubstitutionComponent,
    IterationComponent,
    ShowMatricesComponent,
  ],
  templateUrl: "./step.component.html",
  styleUrl: "./step.component.css",
})
export class StepComponent {
  step = input.required<Step>();
}
