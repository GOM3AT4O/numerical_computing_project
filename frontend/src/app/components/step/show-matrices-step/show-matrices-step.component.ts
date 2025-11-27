import { Component, input } from "@angular/core";
import { ShowMatricesStep } from "../../../models/step";
import { KeyValuePipe } from "@angular/common";

@Component({
  selector: "app-show-matrices-step",
  imports: [KeyValuePipe],
  templateUrl: "./show-matrices-step.component.html",
  styleUrl: "./show-matrices-step.component.css",
})
export class ShowMatricesStepComponent {
  step = input.required<ShowMatricesStep>();
}
