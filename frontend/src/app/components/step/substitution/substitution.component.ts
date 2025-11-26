import { Component, computed, input } from "@angular/core";
import { Substitution } from "../../../models/step";
import { RangePipe } from "../../../pipes/range.pipe";

@Component({
  selector: "app-substitution",
  imports: [RangePipe],
  templateUrl: "./substitution.component.html",
  styleUrl: "./substitution.component.css",
})
export class SubstitutionComponent {
  step = input.required<Substitution>();

  variable = computed<string>(() =>
    this.step().substitution_type == "back" ? "x" : "y",
  );
  orderSubstitutions = (x: number[]) =>
    this.step().substitution_type == "back" ? x.reverse() : x;
  isNotZero = (x: string) => x !== "0";
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
