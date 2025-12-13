import { Component, forwardRef } from "@angular/core";
import {
  ReactiveFormsModule,
  NG_VALUE_ACCESSOR,
  NG_VALIDATORS,
  Validators,
} from "@angular/forms";
import { ParametersComponent } from "../parameters.component";
import { OneGuessParameters } from "../../../models/parameters";
import { AutoSizeInputDirective } from "ngx-autosize-input";

@Component({
  selector: "app-one-guess-parameters",
  imports: [ReactiveFormsModule, AutoSizeInputDirective],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => OneGuessParametersComponent),
      multi: true,
    },
    {
      provide: NG_VALIDATORS,
      useExisting: forwardRef(() => OneGuessParametersComponent),
      multi: true,
    },
  ],
  templateUrl: "./one-guess-parameters.component.html",
  styleUrl: "./one-guess-parameters.component.css",
})
export class OneGuessParametersComponent extends ParametersComponent {
  form = this.formBuilder.group({
    guess: [
      "",
      [Validators.required, Validators.pattern(/^[-+]?\d+(\.\d+)?$/)],
    ],
  });

  override writeValue(value: any): void {
    if (value) {
      if (value.guess) {
        this.form.controls.guess.setValue(value.guess, {
          emitEvent: false,
        });
      }
    }
  }

  override get parameters(): OneGuessParameters {
    const value = this.form.value!;

    return {
      guess: value.guess!,
    };
  }
}
