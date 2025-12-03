import { Component, forwardRef } from "@angular/core";
import {
  NG_VALIDATORS,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
  Validators,
} from "@angular/forms";
import { ParametersComponent } from "../../parameters/parameters.component";
import { EliminationParameters } from "../../../models/parameters";

@Component({
  selector: "app-elimination-parameters",
  imports: [ReactiveFormsModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => EliminationParametersComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => EliminationParametersComponent),
      multi: true,
    },
  ],
  templateUrl: "./elimination-parameters.component.html",
  styleUrl: "./elimination-parameters.component.css",
})
export class EliminationParametersComponent extends ParametersComponent {
  form = this.formBuilder.group({
    scaling: [false, Validators.required],
  });

  writeValue(value: any): void {
    if (value) {
      if (value.scaling) {
        this.form.controls.scaling.setValue(value.scaling, {
          emitEvent: false,
        });
      }
    }
  }

  override get parameters(): EliminationParameters {
    const value = this.form.value!;

    return {
      scaling: value.scaling!,
    };
  }
}
