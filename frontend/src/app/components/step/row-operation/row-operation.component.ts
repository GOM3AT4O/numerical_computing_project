import { Component, input } from "@angular/core";
import { RowOperation } from "../../../models/step";

@Component({
  selector: "app-row-operation",
  imports: [],
  templateUrl: "./row-operation.component.html",
  styleUrl: "./row-operation.component.css",
})
export class RowOperationComponent {
  step = input.required<RowOperation>();

  coefficientSign = (x: string) => {
    return x.startsWith("-") ? "-" : "+";
  };
  formatCoefficient = (x: string) => {
    x = x.startsWith("-") ? x.substring(1) : x;
    return x === "1" ? "" : x;
  };
}
