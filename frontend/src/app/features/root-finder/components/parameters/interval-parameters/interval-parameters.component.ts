import { Component, forwardRef } from "@angular/core";
import {
  ReactiveFormsModule,
  NG_VALUE_ACCESSOR,
  NG_VALIDATORS,
  Validators,
} from "@angular/forms";
import { ParametersComponent } from "../parameters.component";
import { IntervalParameters } from "../../../models/parameters";
import { AutoSizeInputDirective } from "ngx-autosize-input";

@Component({
  selector: "app-interval-parameters",
  imports: [ReactiveFormsModule, AutoSizeInputDirective],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => IntervalParametersComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => IntervalParametersComponent),
      multi: true,
    },
  ],
  templateUrl: "./interval-parameters.component.html",
  styleUrl: "./interval-parameters.component.css",
})
export class IntervalParametersComponent extends ParametersComponent {
  form = this.formBuilder.group({
    lowerBound: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
    upperBound: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
  });

  override writeValue(value: any): void {
    if (value) {
      if (value.lowerBound) {
        this.form.controls.lowerBound.setValue(value.lowerBound, {
          emitEvent: false,
        });
      }

      if (value.upperBound) {
        this.form.controls.upperBound.setValue(value.upperBound, {
          emitEvent: false,
        });
      }
    }
  }

  override get parameters(): IntervalParameters {
    const value = this.form.value!;

    return {
      lowerBound: value.lowerBound!,
      upperBound: value.upperBound!,
    };
  }
}
