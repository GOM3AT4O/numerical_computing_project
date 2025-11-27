import { Component, input } from "@angular/core";
import { ShowMatrices } from "../../../models/step";
import { KeyValuePipe } from "@angular/common";

@Component({
  selector: "app-show-matrices",
  imports: [KeyValuePipe],
  templateUrl: "./show-matrices.component.html",
  styleUrl: "./show-matrices.component.css",
})
export class ShowMatricesComponent {
  step = input.required<ShowMatrices>();
}
