import { Component, input } from "@angular/core";
import { IterationStep } from "../../../models/step";

@Component({
  selector: "app-iteration-step",
  imports: [],
  templateUrl: "./iteration-step.component.html",
  styleUrl: "./iteration-step.component.css",
})
export class IterationStepComponent {
  step = input.required<IterationStep>();

  isNotZero = (x: string) => x !== "0";
  isNotZeroOrIndex = (i: number) => (x: string, j: number) =>
    x !== "0" && i !== j;
  negate = (x: string) => {
    return x.startsWith("-") ? x.substring(1) : "-" + x;
  };
  shouldUseNew = (i: number, j: number) => {
    return this.step().iteration_type === "gauss-seidel" ? j < i : false;
  };
  coefficientSign = (x: string) => {
    return x.startsWith("-") ? "-" : "+";
  };
  formatCoefficient = (x: string) => {
    x = x.startsWith("-") ? x.substring(1) : x;
    return x === "1" ? "" : x;
  };
  formatFirstCoefficient = (x: string) => {
    if (x === "1") {
      return "";
    } else if (x === "-1") {
      return "-";
    }
    return x;
  };
}
