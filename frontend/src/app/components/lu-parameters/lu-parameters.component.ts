import { Component, forwardRef } from "@angular/core";
import {
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { ParametersComponent } from "../parameters/parameters.component";
import { LUParameters } from "../../models/solve-equations-request";

@Component({
  selector: "app-lu-parameters",
  imports: [ReactiveFormsModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => LUParametersComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => LUParametersComponent),
      multi: true,
    },
  ],
  templateUrl: "./lu-parameters.component.html",
  styleUrl: "./lu-parameters.component.css",
})
export class LUParametersComponent extends ParametersComponent {
  formats = [
    { label: "Doolittle Form", value: "doolittle" },
    { label: "Crout Form", value: "crout" },
    { label: "Cholesky Form", value: "cholesky" },
  ] as const;

  form = this.formBuilder.group({
    format: [
      this.formats[0].value as (typeof this.formats)[number]["value"],
      Validators.required,
    ],
  });

  writeValue(value: any): void {
    if (value) {
      if (value.format) {
        this.form.controls.format.setValue(value.format, { emitEvent: false });
      }
    }
  }

  override get parameters(): LUParameters {
    const value = this.form.value!;

    return {
      format: value.format!,
    };
  }
}
