import { Component, input } from "@angular/core";
import { RowOperationStep } from "../../../models/step";

@Component({
  selector: "app-row-operation-step",
  imports: [],
  templateUrl: "./row-operation-step.component.html",
  styleUrl: "./row-operation-step.component.css",
})
export class RowOperationStepComponent {
  step = input.required<RowOperationStep>();

  coefficientSign = (x: string) => {
    return x.startsWith("-") ? "-" : "+";
  };
  formatCoefficient = (x: string) => {
    x = x.startsWith("-") ? x.substring(1) : x;
    return x === "1" ? "" : x;
  };
}
